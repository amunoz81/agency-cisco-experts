"""Estado compartido del grafo LangGraph."""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict

from .schemas import (
    Bom,
    CritiqueResult,
    ExecutiveSynthesis,
    FinancialCase,
    Opportunity,
    ReviewResult,
    ScopeClassification,
    SpecialistFinding,
)


class AgencyState(TypedDict, total=False):
    """Estado que fluye por el grafo."""

    # Entrada cruda de la oportunidad (dict libre desde YAML/JSON)
    raw_input: dict

    # Ficha estructurada tras el descubrimiento
    opportunity: Opportunity

    # Decisión de alcance del coordinador: arquitectura -> clasificación
    scope_plan: dict[str, ScopeClassification]
    selected_specialists: list[str]
    scope_approved: bool

    # Hallazgos de especialistas (formato común). Overwrite: el nodo de
    # especialistas devuelve la lista completa (así el loop de revisión reemplaza
    # en lugar de duplicar).
    findings: list[SpecialistFinding]

    # Integración entre arquitecturas (texto narrativo + flujos)
    integration: dict

    # BOM consolidado y caso financiero
    bom: Bom
    financial_case: FinancialCase

    # Revisión técnica (determinista) y crítica cualitativa (LLM)
    review: ReviewResult
    critique: CritiqueResult
    revision_count: int
    should_revise: bool
    review_feedback: str

    # Síntesis ejecutiva del coordinador (narrativa de negocio, STAR)
    synthesis: ExecutiveSynthesis

    # Propuesta final (rutas de artefactos generados)
    proposal: dict

    # Log de ejecución legible
    log: Annotated[list[str], operator.add]

    # Bandera de ejecución sin LLM
    offline: bool
