"""Estado compartido del grafo LangGraph."""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict

from .schemas import (
    Architecture,
    Bom,
    CritiqueResult,
    ExecutiveSynthesis,
    FinancialCase,
    Opportunity,
    ReviewResult,
    ScopeClassification,
    SpecialistFinding,
)

# Orden canónico para presentar los hallazgos de forma determinista.
_ARCH_ORDER = {a.value: i for i, a in enumerate(Architecture)}


def upsert_findings(
    old: list[SpecialistFinding] | None,
    new: list[SpecialistFinding],
) -> list[SpecialistFinding]:
    """Reducer para el fan-out paralelo de especialistas.

    Inserta/actualiza por arquitectura: cada especialista aparece una sola vez,
    y una revisión (segundo aporte de la misma arquitectura) reemplaza al previo
    en lugar de duplicarlo. Ordena por el orden canónico de `Architecture`.
    """
    by_arch: dict[str, SpecialistFinding] = {
        f.architecture.value: f for f in (old or [])
    }
    for f in new:
        by_arch[f.architecture.value] = f
    return sorted(by_arch.values(), key=lambda f: _ARCH_ORDER.get(f.architecture.value, 99))


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

    # Hallazgos de especialistas (formato común). Reducer upsert por arquitectura:
    # soporta el fan-out paralelo (cada worker aporta su hallazgo) y el loop de
    # revisión (reemplaza el aporte de la arquitectura objetivo sin duplicar).
    findings: Annotated[list[SpecialistFinding], upsert_findings]

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
