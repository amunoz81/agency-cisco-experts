"""Arquitecto coordinador.

Entiende el negocio, define el alcance y selecciona especialistas. Conserva la
responsabilidad del diseño completo: integra las recomendaciones en una sola
arquitectura y narrativa. Aquí decide qué arquitecturas convocar aplicando las
cuatro preguntas de valor.
"""

from __future__ import annotations

from ..config import Settings, get_settings
from ..schemas import Architecture, Opportunity, ScopeClassification


class Coordinator:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

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
