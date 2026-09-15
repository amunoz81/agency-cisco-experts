"""Métricas de corrida (observabilidad ligera, sin dependencias).

Resume una ejecución del grafo en un reporte reproducible que se guarda junto a
la propuesta. Para trazas profundas (por nodo, tokens, latencia) usa LangSmith:
exporta `LANGSMITH_API_KEY` y `LANGCHAIN_TRACING_V2=true` (ver .env.example).
"""

from __future__ import annotations

from typing import Any

from .schemas import EvidenceStatus
from .skills import verify_portfolio


def run_report(final: dict[str, Any], duration_s: float | None = None) -> dict:
    findings = final.get("findings", [])
    bom = final.get("bom")
    review = final.get("review")
    critique = final.get("critique")
    opportunity = final.get("opportunity")

    verification = verify_portfolio(findings)
    bom_lines = len(bom.lines) if bom else 0
    dup = 0
    if bom:
        dup = len(bom.lines) - len(bom.deduplicated().lines)

    evidence_total = sum(len(f.evidence) for f in findings)
    verified = sum(
        1 for f in findings for e in f.evidence if e.status == EvidenceStatus.VERIFIED
    )

    return {
        "customer": getattr(opportunity, "customer", None),
        "duration_s": round(duration_s, 3) if duration_s is not None else None,
        "scope_approved": final.get("scope_approved", True),
        "specialists": sorted({f.architecture.value for f in findings}),
        "n_findings": len(findings),
        "bom_lines": bom_lines,
        "bom_duplicates": dup,
        "evidence_total": evidence_total,
        "evidence_verified": verified,
        "evidence_coverage": verification["coverage_ratio"],
        "review_passed": bool(review.passed) if review else None,
        "review_issues": len(review.issues) if review else 0,
        "revision_count": final.get("revision_count", 0),
        "critic_requested_revision": bool(getattr(critique, "revision_requested", False)),
        "proposal_html": (final.get("proposal") or {}).get("html"),
        "proposal_pdf": (final.get("proposal") or {}).get("pdf"),
    }
