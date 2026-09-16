"""Ingesta de Cisco Validated Designs (CVDs) al corpus de conocimiento.

Convierte el catálogo `cvd_sources.yaml` en documentos del corpus
(`corpus/cvd-<arch>-<slug>.md`) que el `KnowledgeBase` usa para fundamentar
(grounding) los hallazgos de cada especialista. Así los agentes "aprenden"
automáticamente de los CVDs: en cada corrida citan el CVD oficial de su
arquitectura.

cisco.com bloquea el scraping automático (403/WAF), por eso el catálogo guarda
título + URL + resumen técnico. Para TEXTO COMPLETO, descarga el CVD (PDF/HTML)
a `cvd_downloads/` y referencia `local_file` en la entrada; aquí se parsea y
enriquece el documento (PDF con pypdf; HTML con el parser estándar).
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

import yaml

KNOWLEDGE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = KNOWLEDGE_DIR / "cvd_sources.yaml"
CORPUS_DIR = KNOWLEDGE_DIR / "corpus"
DOWNLOADS_DIR = KNOWLEDGE_DIR / "cvd_downloads"

ARCHITECTURES = {
    "secure_networking",
    "security",
    "it_ot",
    "observability_soc",
    "datacenter_ai",
    "collaboration",
}


def _slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:60]


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip = 0
        self.chunks: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            t = data.strip()
            if t:
                self.chunks.append(t)


def _extract_local(path: Path, max_chars: int = 6000) -> str:
    """Extrae texto de un CVD local (PDF o HTML). Devuelve '' si no puede."""
    if not path.exists():
        return ""
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(path))
            text = "\n".join((page.extract_text() or "") for page in reader.pages)
            return text[:max_chars].strip()
        except Exception:
            return ""
    if path.suffix.lower() in (".html", ".htm"):
        try:
            parser = _TextExtractor()
            parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
            return " ".join(parser.chunks)[:max_chars].strip()
        except Exception:
            return ""
    return ""


def _doc_markdown(arch: str, entry: dict, retrieved: str) -> tuple[str, str]:
    title = entry["title"]
    slug = _slugify(title)
    doc_id = f"cvd-{arch}-{slug}"
    tags = sorted({arch, "cvd", *re.findall(r"[a-z0-9]+", title.lower())})

    body = entry.get("summary", "").strip()

    # Enriquecimiento opcional con texto completo local.
    local_ref = entry.get("local_file")
    candidates = []
    if local_ref:
        candidates.append(DOWNLOADS_DIR / local_ref)
    candidates.append(DOWNLOADS_DIR / f"{slug}.pdf")
    candidates.append(DOWNLOADS_DIR / f"{slug}.html")
    for cand in candidates:
        extracted = _extract_local(cand)
        if extracted:
            body += "\n\n## Extracto del documento\n" + extracted
            break

    frontmatter = {
        "id": doc_id,
        "title": title,
        "architecture": arch,
        "source": entry["url"],
        "source_date": retrieved,
        "version": entry.get("version"),
        "status": entry.get("status", "verificada"),
        "tags": tags,
    }
    fm = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    return doc_id, f"---\n{fm}\n---\n{body}\n"


def ingest(
    catalog_path: Path | str | None = None,
    architecture: str | None = None,
) -> list[str]:
    """Genera/actualiza los documentos del corpus a partir del catálogo.

    Devuelve la lista de ids de documentos escritos.
    """
    path = Path(catalog_path) if catalog_path else CATALOG_PATH
    catalog = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    retrieved = str(catalog.get("retrieved", ""))
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    for arch in ARCHITECTURES:
        if architecture and arch != architecture:
            continue
        section = catalog.get(arch) or {}
        for entry in section.get("cvds", []):
            doc_id, md = _doc_markdown(arch, entry, retrieved)
            (CORPUS_DIR / f"{doc_id}.md").write_text(md, encoding="utf-8")
            written.append(doc_id)
    return written


if __name__ == "__main__":
    ids = ingest()
    print(f"Ingestados {len(ids)} documentos CVD al corpus:")
    for i in ids:
        print("  -", i)
