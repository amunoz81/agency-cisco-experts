"""Construcción del grafo LangGraph de la agencia.

Pipeline:
    discovery → planning → specialists → integration → bom
              → finance → review → proposal

El coordinador (planning) decide qué especialistas ejecutar. Los especialistas
aportan hallazgos en el formato común; luego se integran, se consolida el BOM,
se calcula el caso financiero, el revisor valida y se genera la propuesta.
"""

from __future__ import annotations

from pathlib import Path

from langgraph.graph import END, START, StateGraph

from .agents import SPECIALIST_REGISTRY, Coordinator, TechnicalReviewer
from .config import Settings, get_settings
from .reporting import build_proposal
from .schemas import Bom
from .skills import (
    build_financial_case,
    build_opportunity,
    consolidate_bom,
    integrate_architectures,
    verify_portfolio,
)
from .state import AgencyState


def _node_discovery(state: AgencyState) -> AgencyState:
    opportunity = build_opportunity(state.get("raw_input", {}))
    return {
        "opportunity": opportunity,
        "log": [f"Descubrimiento: ficha de '{opportunity.customer}' con "
                f"{len(opportunity.sites)} sede(s)."],
    }


def _make_planning(settings: Settings):
    coordinator = Coordinator(settings)

    def _node_planning(state: AgencyState) -> AgencyState:
        opportunity = state["opportunity"]
        plan = coordinator.plan_scope(opportunity)
        selected = coordinator.selected(plan)
        return {
            "scope_plan": plan,
            "selected_specialists": selected,
            "log": [f"Coordinador: especialistas seleccionados → {', '.join(selected)}."],
        }

    return _node_planning


def _make_specialists(settings: Settings):
    def _node_specialists(state: AgencyState) -> AgencyState:
        opportunity = state["opportunity"]
        selected = state.get("selected_specialists", [])
        findings = []
        log = []
        for name in selected:
            agent_cls = SPECIALIST_REGISTRY.get(name)
            if not agent_cls:
                continue
            finding = agent_cls(settings).analyze(opportunity)
            findings.append(finding)
            log.append(f"Especialista {name}: hallazgo generado ({finding.scope.value}).")
        return {"findings": findings, "log": log}

    return _node_specialists


def _node_integration(state: AgencyState) -> AgencyState:
    integration = integrate_architectures(state.get("findings", []))
    return {"integration": integration, "log": ["Integración entre arquitecturas resuelta."]}


def _node_bom(state: AgencyState) -> AgencyState:
    bom: Bom = consolidate_bom(state.get("findings", []))
    return {"bom": bom, "log": [f"BOM consolidado: {len(bom.lines)} línea(s)."]}


def _make_finance(settings: Settings):
    def _node_finance(state: AgencyState) -> AgencyState:
        case = build_financial_case(state["opportunity"], state["bom"], settings)
        return {"financial_case": case, "log": ["Caso financiero calculado."]}

    return _node_finance


def _node_review(state: AgencyState) -> AgencyState:
    reviewer = TechnicalReviewer()
    review = reviewer.review(
        state.get("findings", []), state["bom"], state["financial_case"]
    )
    n = len(review.issues)
    return {
        "review": review,
        "log": [f"Revisión técnica: {'aprobada' if review.passed else 'con bloqueantes'} "
                f"({n} observación/es)."],
    }


def _make_proposal(settings: Settings, out_dir: str):
    def _node_proposal(state: AgencyState) -> AgencyState:
        verification = verify_portfolio(state.get("findings", []))
        result = build_proposal(
            opportunity=state["opportunity"],
            scope_plan=state["scope_plan"],
            findings=state.get("findings", []),
            integration=state["integration"],
            bom=state["bom"],
            financial_case=state["financial_case"],
            review=state["review"],
            verification=verification,
            fiscal_year=settings.fiscal_year,
            out_dir=out_dir,
        )
        return {"proposal": result, "log": [f"Propuesta generada: {result['html']}"]}

    return _node_proposal


def build_graph(settings: Settings | None = None, out_dir: str = "output"):
    """Compila y devuelve el grafo ejecutable de la agencia."""
    settings = settings or get_settings()
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    g = StateGraph(AgencyState)
    g.add_node("discovery", _node_discovery)
    g.add_node("planning", _make_planning(settings))
    g.add_node("specialists", _make_specialists(settings))
    g.add_node("integration", _node_integration)
    g.add_node("bom", _node_bom)
    g.add_node("finance", _make_finance(settings))
    g.add_node("review", _node_review)
    g.add_node("proposal", _make_proposal(settings, out_dir))

    g.add_edge(START, "discovery")
    g.add_edge("discovery", "planning")
    g.add_edge("planning", "specialists")
    g.add_edge("specialists", "integration")
    g.add_edge("integration", "bom")
    g.add_edge("bom", "finance")
    g.add_edge("finance", "review")
    g.add_edge("review", "proposal")
    g.add_edge("proposal", END)

    return g.compile()
