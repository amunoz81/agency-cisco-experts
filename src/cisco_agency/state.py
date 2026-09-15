"""Estado compartido del grafo LangGraph."""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict

from .schemas import (
    Bom,
    FinancialCase,
    Opportunity,
    ReviewResult,
    ScopeClassification,
    SpecialistFinding,
)


class AgencyState(TypedDict, total=False):
    """Estado que fluye por el grafo.

    `findings` usa un reducer aditivo para que los nodos de especialistas
    puedan aportar hallazgos sin pisarse (soporta futura ejecución en paralelo).
    """

    # Entrada cruda de la oportunidad (dict libre desde YAML/JSON)
    raw_input: dict

    # Ficha estructurada tras el descubrimiento
    opportunity: Opportunity

    # Decisión de alcance del coordinador: arquitectura -> clasificación
    scope_plan: dict[str, ScopeClassification]
    selected_specialists: list[str]

    # Hallazgos de especialistas (formato común)
    findings: Annotated[list[SpecialistFinding], operator.add]

    # Integración entre arquitecturas (texto narrativo + flujos)
    integration: dict

    # BOM consolidado y caso financiero
    bom: Bom
    financial_case: FinancialCase

    # Revisión técnica independiente
    review: ReviewResult

    # Propuesta final (rutas de artefactos generados)
    proposal: dict

    # Log de ejecución legible
    log: Annotated[list[str], operator.add]

    # Bandera de ejecución sin LLM
    offline: bool
