"""Revisor técnico independiente.

Comprueba compatibilidad, dimensionamiento, dependencias, licencias y coherencia
entre arquitecturas antes de cerrar la oferta. Las comprobaciones son
deterministas y auditables; un revisor con LLM puede añadir análisis cualitativo.
"""

from __future__ import annotations

from ..schemas import (
    Bom,
    EvidenceStatus,
    FinancialCase,
    ReviewIssue,
    ReviewResult,
    SpecialistFinding,
)


class TechnicalReviewer:
    def review(
        self,
        findings: list[SpecialistFinding],
        bom: Bom,
        financial_case: FinancialCase,
    ) -> ReviewResult:
        issues: list[ReviewIssue] = []

        # 1. Coherencia de cantidades / duplicados en BOM
        raw_lines = len(bom.lines)
        dedup_lines = len(bom.deduplicated().lines)
        if dedup_lines < raw_lines:
            issues.append(
                ReviewIssue(
                    severity="warning",
                    category="cantidades",
                    detail=(
                        f"El BOM tiene {raw_lines - dedup_lines} línea(s) duplicada(s) "
                        "que deben consolidarse."
                    ),
                )
            )
        for line in bom.lines:
            if line.quantity <= 0:
                issues.append(
                    ReviewIssue(
                        severity="blocker",
                        category="cantidades",
                        detail=f"Cantidad no válida ({line.quantity}) en '{line.description}'.",
                    )
                )
            if not line.is_license and not line.sizing_basis:
                issues.append(
                    ReviewIssue(
                        severity="info",
                        category="dimensionamiento",
                        detail=f"Sin criterio de dimensionamiento en '{line.description}'.",
                    )
                )

        # 2. Licencias declaradas por cada especialista
        for f in findings:
            if not f.licenses:
                issues.append(
                    ReviewIssue(
                        severity="warning",
                        category="licencias",
                        detail=f"El especialista {f.architecture.value} no declara licencias.",
                    )
                )

        # 3. Evidencia: separar verificado de condicionado/pendiente
        for f in findings:
            weak = [e for e in f.evidence if e.status != EvidenceStatus.VERIFIED]
            if not f.evidence:
                issues.append(
                    ReviewIssue(
                        severity="warning",
                        category="coherencia",
                        detail=f"{f.architecture.value} no aporta evidencia.",
                    )
                )
            elif weak:
                issues.append(
                    ReviewIssue(
                        severity="info",
                        category="coherencia",
                        detail=(
                            f"{f.architecture.value}: {len(weak)} evidencia(s) "
                            "condicionada/pendiente por verificar."
                        ),
                    )
                )

        # 4. Financiero: distinguir métricas medidas de ejemplos/supuestos
        if financial_case.scenarios and not financial_case.assumptions:
            issues.append(
                ReviewIssue(
                    severity="warning",
                    category="financiero",
                    detail="El caso financiero no identifica supuestos.",
                )
            )
        for name, res in financial_case.results.items():
            if res.get("payback_years", -1) < 0:
                issues.append(
                    ReviewIssue(
                        severity="info",
                        category="financiero",
                        detail=f"Escenario '{name}' no muestra recuperación en el horizonte.",
                    )
                )

        # 5. Dependencias declaradas entre arquitecturas
        for f in findings:
            if not f.dependencies:
                issues.append(
                    ReviewIssue(
                        severity="info",
                        category="coherencia",
                        detail=f"{f.architecture.value} no declara dependencias con otras capas.",
                    )
                )

        blockers = [i for i in issues if i.severity == "blocker"]
        return ReviewResult(passed=not blockers, issues=issues)
