"""Compuerta Human-in-the-loop (HITL) para aprobar el alcance.

Antes de diseñar (que es lo costoso), un humano puede aprobar o editar la
selección de arquitecturas propuesta por el coordinador. La compuerta es
**conectable**: se inyecta un `Approver` en el grafo.

- `AutoApprover`: aprueba tal cual (modo desatendido / CI / pruebas).
- `CLIApprover`: pregunta por terminal y permite forzar incluir/excluir.

Para UIs asíncronas se puede sustituir por `langgraph.interrupt`; el contrato
(`Approver.approve_scope`) queda igual.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .schemas import Architecture, Opportunity, ScopeClassification


@dataclass
class ScopeDecision:
    approved: bool
    scope_plan: dict[str, ScopeClassification]
    selected_specialists: list[str]
    notes: list[str] = field(default_factory=list)


def _selected_from_plan(plan: dict[str, ScopeClassification]) -> list[str]:
    # Solo las arquitecturas necesarias entran en la propuesta.
    return [
        arch
        for arch, cls in plan.items()
        if cls == ScopeClassification.NECESSARY
    ]


class Approver(Protocol):
    def approve_scope(
        self,
        opportunity: Opportunity,
        scope_plan: dict[str, ScopeClassification],
    ) -> ScopeDecision:
        ...


class AutoApprover:
    """Aprueba el alcance sin intervención (desatendido / CI / pruebas)."""

    def approve_scope(
        self,
        opportunity: Opportunity,
        scope_plan: dict[str, ScopeClassification],
    ) -> ScopeDecision:
        return ScopeDecision(
            approved=True,
            scope_plan=dict(scope_plan),
            selected_specialists=_selected_from_plan(scope_plan),
            notes=["Alcance aprobado automáticamente (modo desatendido)."],
        )


class CLIApprover:
    """Aprobación interactiva por terminal (rich)."""

    def approve_scope(
        self,
        opportunity: Opportunity,
        scope_plan: dict[str, ScopeClassification],
    ) -> ScopeDecision:
        from rich.console import Console
        from rich.prompt import Prompt
        from rich.table import Table

        console = Console()
        plan = dict(scope_plan)

        table = Table(title=f"Alcance propuesto para {opportunity.customer}",
                      border_style="cyan")
        table.add_column("Arquitectura", style="bold")
        table.add_column("Clasificación")
        for arch, cls in plan.items():
            table.add_row(arch, cls.value)
        console.print(table)

        choice = Prompt.ask(
            "¿Aprobar el alcance?",
            choices=["si", "editar", "no"],
            default="si",
        )

        if choice == "no":
            return ScopeDecision(
                approved=False,
                scope_plan=plan,
                selected_specialists=[],
                notes=["Alcance RECHAZADO por el revisor humano."],
            )

        notes = []
        if choice == "editar":
            valid = {a.value for a in Architecture}
            inc = Prompt.ask(
                "Forzar INCLUIR (arquitecturas separadas por coma, Enter para omitir)",
                default="",
            )
            exc = Prompt.ask(
                "Forzar EXCLUIR (arquitecturas separadas por coma, Enter para omitir)",
                default="",
            )
            for a in [x.strip() for x in inc.split(",") if x.strip()]:
                if a in valid:
                    plan[a] = ScopeClassification.NECESSARY
                    notes.append(f"Humano forzó incluir: {a}.")
            for a in [x.strip() for x in exc.split(",") if x.strip()]:
                if a in valid:
                    plan[a] = ScopeClassification.OUT_OF_SCOPE
                    notes.append(f"Humano forzó excluir: {a}.")

        return ScopeDecision(
            approved=True,
            scope_plan=plan,
            selected_specialists=_selected_from_plan(plan),
            notes=notes or ["Alcance aprobado por el revisor humano."],
        )
