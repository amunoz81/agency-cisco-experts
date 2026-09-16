"""App FastAPI: formulario de oportunidad + generación de propuesta por los agentes."""

from __future__ import annotations

import asyncio
import re
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from ..config import get_settings
from ..graph import build_graph
from ..metrics import run_report
from .parsing import parse_install_base
from .verticals import vertical_label, verticals_list

WEB_DIR = Path(__file__).resolve().parent
STATIC_DIR = WEB_DIR / "static"
OUTPUT_DIR = Path("output/web")

app = FastAPI(title="Cisco Experts Agency", docs_url="/api/docs")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (text or "cliente").lower()).strip("_") or "cliente"


def _split(text: str | None) -> list[str]:
    if not text:
        return []
    parts = re.split(r"[\n;,]+", text)
    return [p.strip() for p in parts if p.strip()]


@app.get("/")
def index() -> FileResponse:
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/api/config")
def config(lang: str = "en") -> JSONResponse:
    s = get_settings()
    return JSONResponse(
        {
            "verticals": verticals_list(lang),
            "offline_default": s.effective_offline(),
            "provider": s.llm_provider,
            "fiscal_year": s.fiscal_year,
        }
    )


def _run_pipeline(raw: dict, offline: bool) -> dict:
    import time

    settings = get_settings()
    if offline:
        settings = settings.model_copy(update={"offline": True})
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    graph = build_graph(settings, out_dir=str(OUTPUT_DIR))
    t0 = time.perf_counter()
    final = graph.invoke({"raw_input": raw, "offline": offline})
    report = run_report(final, duration_s=time.perf_counter() - t0)
    proposal = final.get("proposal", {})
    html_path = proposal.get("html")
    pdf_path = proposal.get("pdf")
    return {
        "ok": True,
        "html_file": Path(html_path).name if html_path else None,
        "pdf_file": Path(pdf_path).name if pdf_path else None,
        "pdf_error": proposal.get("pdf_error"),
        "metrics": report,
        "specialists": report.get("specialists", []),
    }


@app.post("/api/proposal")
async def create_proposal(
    customer: str = Form(...),
    vertical: str = Form(""),
    situation: str = Form(""),
    problem: str = Form(""),
    current_products: str = Form(""),
    n_sites: str = Form(""),
    n_datacenters: str = Form(""),
    remote_users: str = Form(""),
    cloud_providers: str = Form(""),
    lang: str = Form("en"),
    offline: str = Form("false"),
    install_base: UploadFile | None = File(None),
) -> JSONResponse:
    products = _split(current_products)
    clouds = _split(cloud_providers)
    parsed = {"items": [], "text": "", "note": ""}
    if install_base is not None and install_base.filename:
        content = await install_base.read()
        parsed = parse_install_base(install_base.filename, content)

    objectives = []
    if problem:
        objectives.append(problem)
    inventory = products + parsed["items"]

    def _int(v: str) -> int:
        try:
            return max(int(float(v)), 0)
        except (ValueError, TypeError):
            return 0

    raw = {
        "customer": customer.strip(),
        "industry": vertical_label(vertical, lang) or vertical,
        "situation": situation.strip() or None,
        "problem": problem.strip() or None,
        "objectives": objectives,
        "current_products": products,
        "inventory": inventory,
        "n_sites": _int(n_sites),
        "n_datacenters": _int(n_datacenters),
        "remote_users": _int(remote_users),
        "cloud_providers": clouds,
        "workloads": [],
        "pending_data": (
            [parsed["note"]] if parsed.get("note") else []
        ),
    }

    is_offline = str(offline).lower() in ("1", "true", "yes", "on")
    try:
        result = await asyncio.to_thread(_run_pipeline, raw, is_offline)
    except Exception as exc:  # pragma: no cover - errores de runtime del LLM
        return JSONResponse({"ok": False, "error": str(exc)}, status_code=500)

    result["install_base_note"] = parsed.get("note") or ""
    result["install_base_lines"] = len(parsed.get("items", []))
    return JSONResponse(result)


@app.get("/files/{name}")
def download(name: str) -> FileResponse:
    # Solo sirve archivos del directorio de salida (evita path traversal).
    safe = Path(name).name
    path = OUTPUT_DIR / safe
    if not path.exists():
        return JSONResponse({"error": "no encontrado"}, status_code=404)
    return FileResponse(str(path))
