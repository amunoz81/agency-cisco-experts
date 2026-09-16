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

try:  # ubicación del API Send según versión de LangGraph
    from langgraph.types import Send
except ImportError:  # pragma: no cover
    from langgraph.constants import Send

from .agents import SPECIALIST_REGISTRY, Coordinator, TechnicalReviewer
from .approval import Approver, AutoApprover
from .config import Settings, get_settings
from .knowledge import KnowledgeBase
from .reporting import build_proposal
from .routing import ModelRouter
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


def _make_scope_gate(approver: Approver):
    """Compuerta HITL: un humano aprueba o edita el alcance antes de diseñar."""

    def _node_scope_gate(state: AgencyState) -> AgencyState:
        decision = approver.approve_scope(state["opportunity"], state["scope_plan"])
        return {
            "scope_plan": decision.scope_plan,
            "selected_specialists": decision.selected_specialists,
            "scope_approved": decision.approved,
            "log": ["HITL alcance: " + " ".join(decision.notes)],
        }

    return _node_scope_gate


def _route_after_gate(state: AgencyState):
    if not state.get("scope_approved", True):
        return END
    return _dispatch_specialists(state)


MAX_REVISIONS = 1


def _make_specialist_worker(settings: Settings, router: ModelRouter, kb: KnowledgeBase):
    """Worker de un especialista (se ejecuta en paralelo vía fan-out `Send`)."""

    def _worker(payload: dict) -> AgencyState:
        name = payload["role"]
        opportunity = payload["opportunity"]
        feedback = payload.get("feedback") or None
        agent_cls = SPECIALIST_REGISTRY[name]
        agent = agent_cls(settings, router, kb)
        finding = agent.analyze(opportunity, feedback=feedback)
        cfg = router.resolve(name)
        engine = "offline" if router.is_offline(name) else f"{cfg.provider}/{cfg.model}"
        tag = " (revisión)" if feedback else ""
        return {
            "findings": [finding],
            "log": [
                f"Especialista {name} · motor {engine}{tag} · "
                f"hallazgo generado ({finding.scope.value})."
            ],
        }

    return _worker


def _dispatch_specialists(state: AgencyState, only: list[str] | None = None):
    """Devuelve los `Send` para ejecutar los especialistas en paralelo."""
    selected = state.get("selected_specialists", [])
    roles = [r for r in (only or selected) if r in SPECIALIST_REGISTRY]
    if not roles:
        return "integration"
    opportunity = state["opportunity"]
    feedback = state.get("review_feedback", "")
    return [
        Send("specialist_worker", {"role": r, "opportunity": opportunity, "feedback": feedback})
        for r in roles
    ]


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


def _make_review(settings: Settings, router: ModelRouter):
    def _node_review(state: AgencyState) -> AgencyState:
        reviewer = TechnicalReviewer(settings, router)
        review = reviewer.review(
            state.get("findings", []), state["bom"], state["financial_case"]
        )
        n = len(review.issues)
        return {
            "review": review,
            "log": [f"Revisión técnica: {'aprobada' if review.passed else 'con bloqueantes'} "
                    f"({n} observación/es)."],
        }

    return _node_review


def _make_critic(settings: Settings, router: ModelRouter):
    """Crítico cualitativo + decisión de reflexión acotada."""

    def _node_critic(state: AgencyState) -> AgencyState:
        reviewer = TechnicalReviewer(settings, router)
        critique = reviewer.critique(
            state.get("findings", []), state.get("integration", {}), state["review"]
        )
        count = state.get("revision_count", 0)
        should_revise = critique.revision_requested and count < MAX_REVISIONS
        out: AgencyState = {"critique": critique, "should_revise": should_revise}
        if should_revise:
            out["revision_count"] = count + 1
            out["review_feedback"] = critique.rationale + " " + "; ".join(critique.issues)
            out["log"] = [
                f"Crítico: solicita revisión #{count + 1} "
                f"→ {', '.join(critique.revision_targets) or 'todas'}."
            ]
        else:
            reason = "sin observaciones cualitativas" if not critique.revision_requested \
                else f"límite de revisiones ({MAX_REVISIONS}) alcanzado"
            out["log"] = [f"Crítico: diseño aceptado ({reason})."]
        return out

    return _node_critic


def _route_after_critic(state: AgencyState):
    if not state.get("should_revise"):
        return "synthesis"
    critique = state.get("critique")
    selected = state.get("selected_specialists", [])
    targets = [t for t in (critique.revision_targets if critique else []) if t in selected]
    return _dispatch_specialists(state, only=targets or selected)


def _make_synthesis(settings: Settings, router: ModelRouter):
    def _node_synthesis(state: AgencyState) -> AgencyState:
        coordinator = Coordinator(settings, router)
        synthesis = coordinator.synthesize(
            state["opportunity"], state.get("findings", []), state.get("integration", {})
        )
        engine = "offline" if router.is_offline("coordinator") else "LLM"
        return {
            "synthesis": synthesis,
            "log": [f"Coordinador · síntesis ejecutiva ({engine}) integrada."],
        }

    return _node_synthesis


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
            synthesis=state.get("synthesis"),
            critique=state.get("critique"),
        )
        return {"proposal": result, "log": [f"Propuesta generada: {result['html']}"]}

    return _node_proposal


def build_graph(
    settings: Settings | None = None,
    out_dir: str = "output",
    approver: Approver | None = None,
):
    """Compila y devuelve el grafo ejecutable de la agencia.

    `approver` implementa la compuerta HITL de aprobación del alcance.
    Por defecto `AutoApprover` (desatendido); usa `CLIApprover` para interactivo.
    """
    settings = settings or get_settings()
    router = ModelRouter(settings)
    # La agencia mantiene su conocimiento de CVDs al día automáticamente:
    # si el catálogo cambió, regenera el corpus antes de cargar la base.
    if settings.auto_ingest_cvd:
        from .knowledge import ensure_corpus

        ensure_corpus()
    kb = KnowledgeBase()
    approver = approver or AutoApprover()
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    g = StateGraph(AgencyState)
    g.add_node("discovery", _node_discovery)
    g.add_node("planning", _make_planning(settings))
    g.add_node("scope_gate", _make_scope_gate(approver))
    g.add_node("specialist_worker", _make_specialist_worker(settings, router, kb))
    g.add_node("integration", _node_integration)
    g.add_node("bom", _node_bom)
    g.add_node("finance", _make_finance(settings))
    g.add_node("review", _make_review(settings, router))
    g.add_node("critic", _make_critic(settings, router))
    g.add_node("synthesis", _make_synthesis(settings, router))
    g.add_node("proposal", _make_proposal(settings, out_dir))

    g.add_edge(START, "discovery")
    g.add_edge("discovery", "planning")
    g.add_edge("planning", "scope_gate")
    # Fan-out paralelo de especialistas (o END si se rechaza el alcance).
    g.add_conditional_edges(
        "scope_gate", _route_after_gate, ["specialist_worker", "integration", END]
    )
    g.add_edge("specialist_worker", "integration")
    g.add_edge("integration", "bom")
    g.add_edge("bom", "finance")
    g.add_edge("finance", "review")
    g.add_edge("review", "critic")
    # Reflexión acotada: el crítico puede re-despachar especialistas (paralelo).
    g.add_conditional_edges(
        "critic", _route_after_critic, ["specialist_worker", "integration", "synthesis"]
    )
    g.add_edge("synthesis", "proposal")
    g.add_edge("proposal", END)

    return g.compile()
