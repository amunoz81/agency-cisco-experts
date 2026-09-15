"""Skill: Verificación de portafolio y compatibilidad.

Comprueba que cada hallazgo tenga evidencia con fuente/fecha/versión/estado y
resume el nivel de sustento del diseño. En una versión con integración
autorizada, aquí se consultarían matrices de compatibilidad, notas de versión y
anuncios de ciclo de vida (EoL/EoS).
"""

from __future__ import annotations

from ..schemas import EvidenceStatus, SpecialistFinding


def verify_portfolio(findings: list[SpecialistFinding]) -> dict:
    verified = conditioned = pending = 0
    gaps: list[str] = []

    for f in findings:
        if not f.evidence:
            gaps.append(f"{f.architecture.value}: sin evidencia declarada.")
        for e in f.evidence:
            if e.status == EvidenceStatus.VERIFIED:
                verified += 1
            elif e.status == EvidenceStatus.CONDITIONED:
                conditioned += 1
            else:
                pending += 1

    total = verified + conditioned + pending
    return {
        "verified": verified,
        "conditioned": conditioned,
        "pending": pending,
        "coverage_ratio": round(verified / total, 2) if total else 0.0,
        "gaps": gaps,
        "note": (
            "Verificación basada en evidencia declarada por los especialistas. "
            "Confirmar contra matrices de compatibilidad y ciclo de vida oficiales "
            "antes de cotizar."
        ),
    }
