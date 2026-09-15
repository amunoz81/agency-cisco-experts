"""Revisor técnico independiente.

Comprueba compatibilidad, dimensionamiento, dependencias, licencias y coherencia
entre arquitecturas antes de cerrar la oferta. Las comprobaciones son
deterministas y auditables; un revisor con LLM puede añadir análisis cualitativo.
"""

from __future__ import annotations

from pathlib import Path

from ..config import Settings, get_settings
from ..routing import ModelRouter
from ..schemas import (
    Bom,
    CritiqueResult,
    EvidenceStatus,
    FinancialCase,
    ReviewIssue,
    ReviewResult,
    SpecialistFinding,
)

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class TechnicalReviewer:
    def __init__(
        self,
        settings: Settings | None = None,
        router: ModelRouter | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.router = router or ModelRouter(self.settings)

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

    # -- Crítico cualitativo (capa LLM híbrida) ----------------------------
    def critique(
        self,
        findings: list[SpecialistFinding],
        integration: dict,
        review: ReviewResult,
    ) -> CritiqueResult:
        """Juicio cualitativo de coherencia del diseño. En offline no solicita
        revisión (las verificaciones deterministas ya son el guardrail); en línea
        un LLM puede pedir revisión acotada de arquitecturas específicas."""
        if self.router.is_offline("technical_reviewer"):
            return CritiqueResult(
                revision_requested=False,
                rationale="Crítica heurística (sin LLM): se apoya en las "
                "verificaciones deterministas.",
            )
        from langchain_core.messages import HumanMessage, SystemMessage

        model = self.router.for_role("technical_reviewer")
        structured = model.with_structured_output(CritiqueResult)
        system = self._prompt("technical_reviewer.md")
        findings_brief = "\n".join(
            f"- [{f.architecture.value}] {f.proposed_solution} "
            f"(dep: {', '.join(f.dependencies) or 'ninguna'})"
            for f in findings
        )
        det_issues = "; ".join(i.detail for i in review.issues) or "sin observaciones"
        user = (
            "Evalúa la COHERENCIA CUALITATIVA del diseño integrado (no repitas las "
            "verificaciones deterministas). Si hay incoherencias de diseño que "
            "ameriten rehacer el aporte de alguna arquitectura, solicita revisión "
            "e indica las arquitecturas objetivo. Sé conservador: solo pide revisión "
            "si aporta valor real.\n\n"
            f"Hallazgos:\n{findings_brief}\n\n"
            f"Integración: {integration}\n\n"
            f"Observaciones deterministas: {det_issues}"
        )
        result: CritiqueResult = structured.invoke(
            [SystemMessage(content=system), HumanMessage(content=user)]
        )  # type: ignore[assignment]
        return result

    @staticmethod
    def _prompt(name: str) -> str:
        path = PROMPTS_DIR / name
        return path.read_text(encoding="utf-8") if path.exists() else ""
