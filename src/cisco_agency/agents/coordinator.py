"""Arquitecto coordinador.

Entiende el negocio, define el alcance y selecciona especialistas. Conserva la
responsabilidad del diseño completo: integra las recomendaciones en una sola
arquitectura y narrativa. Aquí decide qué arquitecturas convocar aplicando las
cuatro preguntas de valor.
"""

from __future__ import annotations

from pathlib import Path

from ..config import Settings, get_settings
from ..routing import ModelRouter
from ..schemas import (
    Architecture,
    ExecutiveSynthesis,
    Opportunity,
    ScopeClassification,
    SpecialistFinding,
)

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class Coordinator:
    def __init__(
        self,
        settings: Settings | None = None,
        router: ModelRouter | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.router = router or ModelRouter(self.settings)

    def plan_scope(self, opportunity: Opportunity) -> dict[str, ScopeClassification]:
        """Clasifica cada arquitectura: necesaria | opcional | fuera de alcance.

        Reglas base (deterministas). En modo online, un coordinador con LLM puede
        refinar esta decisión con la narrativa del negocio.
        """
        has_plants = any(s.kind == "planta" for s in opportunity.sites)

        plan: dict[str, ScopeClassification] = {
            # Secure Networking es la arquitectura base para conectividad y segmentación
            Architecture.SECURE_NETWORKING.value: ScopeClassification.NECESSARY,
            # Security es capa de protección necesaria de extremo a extremo
            Architecture.SECURITY.value: ScopeClassification.NECESSARY,
        }

        plan[Architecture.IT_OT.value] = (
            ScopeClassification.NECESSARY
            if (opportunity.it_ot_present or has_plants)
            else ScopeClassification.OUT_OF_SCOPE
        )

        plan[Architecture.OBSERVABILITY_SOC.value] = (
            ScopeClassification.NECESSARY
            if opportunity.needs_correlation_soc
            else ScopeClassification.OPTIONAL
        )

        plan[Architecture.DATACENTER_AI.value] = (
            ScopeClassification.NECESSARY
            if opportunity.needs_datacenter_ai
            else ScopeClassification.OPTIONAL
        )

        plan[Architecture.COLLABORATION.value] = (
            ScopeClassification.NECESSARY
            if opportunity.needs_collaboration
            else ScopeClassification.OPTIONAL
        )
        return plan

    @staticmethod
    def selected(plan: dict[str, ScopeClassification]) -> list[str]:
        """Especialistas a ejecutar: necesarios y opcionales justificados."""
        return [
            arch
            for arch, cls in plan.items()
            if cls in (ScopeClassification.NECESSARY, ScopeClassification.OPTIONAL)
        ]

    # -- Síntesis ejecutiva (capa LLM híbrida) -----------------------------
    def synthesize(
        self,
        opportunity: Opportunity,
        findings: list[SpecialistFinding],
        integration: dict,
    ) -> ExecutiveSynthesis:
        """Integra las recomendaciones en una narrativa de negocio (STAR) y
        resuelve contradicciones. Determinista en offline; LLM en línea."""
        if self.router.is_offline("coordinator"):
            return self._offline_synthesis(opportunity, findings)
        return self._llm_synthesis(opportunity, findings, integration)

    def _offline_synthesis(
        self, opportunity: Opportunity, findings: list[SpecialistFinding]
    ) -> ExecutiveSynthesis:
        objectives = "; ".join(opportunity.objectives) or "objetivos por confirmar"
        archs = ", ".join(sorted({f.architecture.value for f in findings}))
        return ExecutiveSynthesis(
            situation=(
                f"{opportunity.customer}"
                + (f" ({opportunity.industry})" if opportunity.industry else "")
                + f" opera {len(opportunity.sites)} sede(s) y requiere modernizar su "
                "arquitectura de red y seguridad de extremo a extremo."
            ),
            task=f"Objetivos declarados: {objectives}.",
            action=(
                "El coordinador integró las arquitecturas necesarias "
                f"({archs}) en un diseño único con identidad, segmentación y "
                "observabilidad coherentes."
            ),
            result=(
                "Arquitectura Zero Trust de extremo a extremo, BOM consolidado y caso "
                "financiero con escenarios, lista para validación técnica y ejecutiva."
            ),
            contradictions_resolved=[],
            executive_summary=(
                f"Propuesta integral para {opportunity.customer} que combina {archs} "
                "bajo una estrategia Zero Trust, con dependencias y responsabilidades "
                "operativas explícitas."
            ),
        )

    def _llm_synthesis(
        self,
        opportunity: Opportunity,
        findings: list[SpecialistFinding],
        integration: dict,
    ) -> ExecutiveSynthesis:
        from langchain_core.messages import HumanMessage, SystemMessage

        model = self.router.for_role("coordinator")
        structured = model.with_structured_output(ExecutiveSynthesis)
        system = self._prompt("coordinator.md")
        findings_brief = "\n".join(
            f"- [{f.architecture.value}] {f.customer_need} → {f.proposed_solution}"
            for f in findings
        )
        user = (
            "Integra las recomendaciones de los especialistas en una narrativa "
            "ejecutiva (STAR) y resuelve contradicciones si las hay. Devuelve la "
            "estructura pedida.\n\n"
            f"Cliente: {opportunity.customer} · Industria: {opportunity.industry}\n"
            f"Objetivos: {'; '.join(opportunity.objectives)}\n\n"
            f"Hallazgos:\n{findings_brief}\n\n"
            f"Integración: {integration}"
        )
        result: ExecutiveSynthesis = structured.invoke(
            [SystemMessage(content=system), HumanMessage(content=user)]
        )  # type: ignore[assignment]
        return result

    @staticmethod
    def _prompt(name: str) -> str:
        path = PROMPTS_DIR / name
        return path.read_text(encoding="utf-8") if path.exists() else ""
