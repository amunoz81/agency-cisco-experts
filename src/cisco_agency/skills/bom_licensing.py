"""Skill: BOM y licenciamiento.

Consolida las contribuciones de BOM de cada especialista en una sola lista,
sin duplicados, separando hardware de licencias.
"""

from __future__ import annotations

from ..schemas import Bom, SpecialistFinding


def consolidate_bom(findings: list[SpecialistFinding]) -> Bom:
    combined = Bom()
    for f in findings:
        combined.lines.extend(f.bom_contribution.lines)
    return combined.deduplicated()
