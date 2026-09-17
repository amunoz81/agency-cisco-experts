"""Skill: Propuesta ejecutiva (generación del documento).

Renderiza la plantilla Jinja2 a HTML (siempre) e intenta exportar a PDF con
WeasyPrint si está instalado. Entrega STAR, blueprint, casos de uso, hoja de
ruta, métricas y anexos técnicos.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .. import __version__
from ..schemas import (
    Bom,
    CritiqueResult,
    ExecutiveSynthesis,
    FinancialCase,
    Opportunity,
    ReviewResult,
    ScopeClassification,
    SpecialistFinding,
)
from .assets import PALETTE

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

ARCH_LABELS = {
    "secure_networking": "Secure Networking",
    "security": "Security",
    "it_ot": "IT/OT (Cyber Vision)",
    "observability_soc": "Observabilidad y SOC",
    "datacenter_ai": "Data Center y AI",
    "collaboration": "Collaboration (Webex)",
}


def _build_star(opportunity: Opportunity) -> dict:
    objectives = "; ".join(opportunity.objectives) or "objetivos por confirmar"
    return {
        "situation": (
            f"{opportunity.customer}"
            + (f" ({opportunity.industry})" if opportunity.industry else "")
            + f" opera {len(opportunity.sites)} sede(s) y requiere modernizar su "
            "arquitectura de red y seguridad de extremo a extremo."
        ),
        "task": f"Objetivos declarados: {objectives}.",
        "action": (
            "La Agencia de Expertos Cisco integró Secure Networking, Security y las "
            "arquitecturas complementarias necesarias en un diseño único con "
            "identidad, segmentación y observabilidad coherentes."
        ),
        "result": (
            "Arquitectura Zero Trust de extremo a extremo, BOM consolidado y caso "
            "financiero con escenarios, lista para validación técnica y ejecutiva."
        ),
    }


def _build_kpis(bom: Bom, findings: list[SpecialistFinding]) -> list[dict]:
    hw = sum(1 for line in bom.lines if not line.is_license)
    lic = sum(1 for line in bom.lines if line.is_license)
    return [
        {"value": len(findings), "label": "Arquitecturas en la solución"},
        {"value": len(bom.lines), "label": "Líneas de BOM"},
        {"value": hw, "label": "Componentes de HW"},
        {"value": lic, "label": "Suscripciones/licencias"},
    ]


def _default_use_cases(findings: list[SpecialistFinding]) -> list[str]:
    present = {f.architecture.value for f in findings}
    cases = [
        "Acceso seguro basado en identidad (Zero Trust) para usuarios y dispositivos.",
        "Segmentación macro y micro para contener movimiento lateral.",
    ]
    if "it_ot" in present:
        cases.append("Visibilidad de activos OT y control de comunicaciones industriales.")
    if "observability_soc" in present:
        cases.append("Correlación cross-domain y respuesta automatizada en el SOC.")
    if "datacenter_ai" in present:
        cases.append("Plataforma de datacenter e IA con seguridad integrada.")
    if "collaboration" in present:
        cases.append("Colaboración híbrida segura (Webex) con voz, video y salas.")
    return cases


def _default_roadmap() -> list[dict]:
    return [
        {"phase": "Fase 0 – Descubrimiento",
         "focus": "Inventario, requisitos y línea base", "duration": "2–4 semanas"},
        {"phase": "Fase 1 – Base segura",
         "focus": "Red, identidad (ISE/DUO) y segmentación", "duration": "6–10 semanas"},
        {"phase": "Fase 2 – Protección",
         "focus": "Firewall, micro-segmentación, NDR/EDR", "duration": "6–10 semanas"},
        {"phase": "Fase 3 – Observabilidad",
         "focus": "Splunk/ThousandEyes y casos de uso SOC", "duration": "4–8 semanas"},
        {"phase": "Fase 4 – Optimización",
         "focus": "Automatización (AgenticOps) y mejora continua", "duration": "Continuo"},
    ]


def build_proposal(
    *,
    opportunity: Opportunity,
    scope_plan: dict[str, ScopeClassification],
    findings: list[SpecialistFinding],
    integration: dict,
    bom: Bom,
    financial_case: FinancialCase,
    review: ReviewResult,
    verification: dict,
    fiscal_year: str,
    out_dir: str | Path,
    basename: str | None = None,
    synthesis: ExecutiveSynthesis | None = None,
    critique: CritiqueResult | None = None,
) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    slug = (basename or opportunity.customer).lower().replace(" ", "_")

    # Diagrama de arquitectura de red (PNG incrustado + .drawio editable).
    diagram_data_uri = ""
    diagram_png = None
    diagram_drawio = None
    try:
        import base64

        from .diagram import build_topology, render_png, write_drawio

        tiers = build_topology(opportunity, findings)
        diagram_png = render_png(tiers, out_dir, slug, opportunity.customer)
        diagram_drawio = write_drawio(tiers, out_dir, slug, opportunity.customer)
        b64 = base64.b64encode(Path(diagram_png).read_bytes()).decode()
        diagram_data_uri = "data:image/png;base64," + b64
    except Exception:  # pragma: no cover - diagrama es best-effort
        pass

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("proposal.html.j2")

    scope_serialized = {
        k: (v.value if isinstance(v, ScopeClassification) else v)
        for k, v in scope_plan.items()
    }
    financial_scenarios = {s.name: s for s in financial_case.scenarios}

    if synthesis is not None:
        star = {
            "situation": synthesis.situation,
            "task": synthesis.task,
            "action": synthesis.action,
            "result": synthesis.result,
        }
        executive_summary = synthesis.executive_summary
        contradictions = synthesis.contradictions_resolved
    else:
        star = _build_star(opportunity)
        executive_summary = ""
        contradictions = []

    html = template.render(
        palette=PALETTE,
        version=__version__,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        fiscal_year=fiscal_year,
        arch_labels=ARCH_LABELS,
        opportunity=opportunity,
        scope_plan=scope_serialized,
        findings=findings,
        integration=integration,
        bom=bom,
        financial_case=financial_case,
        financial_scenarios=financial_scenarios,
        review=review,
        critique=critique,
        verification=verification,
        star=star,
        executive_summary=executive_summary,
        contradictions=contradictions,
        kpis=_build_kpis(bom, findings),
        use_cases=_default_use_cases(findings),
        roadmap=_default_roadmap(),
        diagram_data_uri=diagram_data_uri,
    )

    html_path = out / f"propuesta_{slug}.html"
    html_path.write_text(html, encoding="utf-8")

    result = {"html": str(html_path), "pdf": None, "pdf_engine": None, "pdf_error": None}
    result["diagram_png"] = diagram_png
    result["diagram_drawio"] = diagram_drawio

    # Exportación a PowerPoint / Word (best-effort; requiere el extra office/web).
    result["pptx"] = None
    result["docx"] = None
    result["office_error"] = None
    try:
        from .office import build_docx, build_pptx

        common = dict(
            opportunity=opportunity, scope_plan=scope_plan, findings=findings,
            integration=integration, bom=bom, financial_case=financial_case,
            review=review, verification=verification, fiscal_year=fiscal_year,
            out_dir=out_dir, basename=basename, synthesis=synthesis,
            diagram_png=diagram_png,
        )
        result["pptx"] = build_pptx(**common)
        result["docx"] = build_docx(**common, critique=critique)
    except ImportError:
        result["office_error"] = (
            "Exportación a PPTX/DOCX no disponible. Instala: pip install -e '.[office]'."
        )
    except Exception as exc:  # pragma: no cover - depende del entorno
        result["office_error"] = f"No se pudo exportar a Office: {exc}"

    pdf_path = out / f"propuesta_{slug}.pdf"

    # Motor 1 (máxima fidelidad): WeasyPrint. Requiere libs de sistema (pango/cairo).
    try:
        from weasyprint import HTML  # type: ignore

        HTML(string=html, base_url=str(TEMPLATES_DIR)).write_pdf(str(pdf_path))
        result["pdf"] = str(pdf_path)
        result["pdf_engine"] = "weasyprint"
        return result
    except Exception as exc:  # ImportError o error de libs nativas
        weasy_error = str(exc).splitlines()[0] if str(exc) else "no disponible"

    # Motor 2 (pure-Python, sin libs de sistema): xhtml2pdf.
    try:
        from xhtml2pdf import pisa  # type: ignore

        with open(pdf_path, "wb") as fh:
            status = pisa.CreatePDF(html, dest=fh, encoding="utf-8")
        if not status.err:
            result["pdf"] = str(pdf_path)
            result["pdf_engine"] = "xhtml2pdf"
            return result
        result["pdf_error"] = "xhtml2pdf reportó errores al generar el PDF."
    except ImportError:
        result["pdf_error"] = (
            f"WeasyPrint no disponible ({weasy_error}) y xhtml2pdf no está instalado. "
            "El HTML sí se generó."
        )
    except Exception as exc:  # pragma: no cover - depende del entorno
        result["pdf_error"] = f"No se pudo generar PDF: {exc}. El HTML sí se generó."

    return result
