"""Base para agentes especialistas.

Cada especialista carga su prompt de sistema desde `prompts/`, se **fundamenta**
(grounding) en la base de conocimiento y devuelve un `SpecialistFinding` en el
formato común. El modelo LLM se resuelve por rol vía `ModelRouter`.

Grounding: antes de responder, el agente recupera evidencia del corpus
(`KnowledgeBase`) para el par (arquitectura, oportunidad). En modo LLM esa
evidencia se inyecta en el prompt como contexto citable; en ambos modos se
adjunta al hallazgo como `Evidence` con fuente/fecha/versión/estado.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from ..config import Settings, get_settings
from ..knowledge import KnowledgeBase
from ..routing import ModelRouter
from ..schemas import Architecture, Evidence, Opportunity, SpecialistFinding

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class SpecialistAgent(ABC):
    architecture: Architecture
    prompt_file: str

    def __init__(
        self,
        settings: Settings | None = None,
        router: ModelRouter | None = None,
        kb: KnowledgeBase | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.router = router or ModelRouter(self.settings)
        self.kb = kb if kb is not None else KnowledgeBase()

    @property
    def role(self) -> str:
        return self.architecture.value

    # -- Prompt ------------------------------------------------------------
    def system_prompt(self) -> str:
        path = PROMPTS_DIR / self.prompt_file
        if path.exists():
            return path.read_text(encoding="utf-8")
        return f"Eres el especialista Cisco de {self.architecture.value}."

    # -- Interfaz principal ------------------------------------------------
    def analyze(self, opportunity: Opportunity) -> SpecialistFinding:
        retrieved = self.kb.evidence_for(self.role, opportunity)
        if self.router.is_offline(self.role):
            finding = self._offline_finding(opportunity)
        else:
            finding = self._llm_finding(opportunity, retrieved)
        finding.evidence = _merge_evidence(retrieved, finding.evidence)
        return finding

    # -- Ejecución con LLM -------------------------------------------------
    def _llm_finding(
        self, opportunity: Opportunity, grounding: list[Evidence]
    ) -> SpecialistFinding:
        model = self.router.for_role(self.role)
        structured = model.with_structured_output(SpecialistFinding)
        messages = [
            SystemMessage(content=self.system_prompt()),
            HumanMessage(content=self._user_prompt(opportunity, grounding)),
        ]
        finding: SpecialistFinding = structured.invoke(messages)  # type: ignore[assignment]
        finding.architecture = self.architecture
        return finding

    def _user_prompt(self, opportunity: Opportunity, grounding: list[Evidence]) -> str:
        ctx = ""
        if grounding:
            lines = [
                f"- {e.claim} — {e.source}"
                + (f" ({e.version})" if e.version else "")
                + f" [{e.status.value}]"
                for e in grounding
            ]
            ctx = (
                "\n\nContexto de referencia (cita estas fuentes cuando apliquen; "
                "no inventes SKUs ni precios):\n" + "\n".join(lines)
            )
        return (
            "Analiza la siguiente oportunidad y entrega tu hallazgo en el formato "
            "común (necesidad → solución → dependencias → dimensionamiento → "
            "licencias → beneficio medible → evidencia → riesgos y pendientes)."
            + ctx
            + f"\n\nOportunidad:\n{opportunity.model_dump_json(indent=2)}"
        )

    # -- Modo offline (subclases lo implementan) ---------------------------
    @abstractmethod
    def _offline_finding(self, opportunity: Opportunity) -> SpecialistFinding:
        ...


def _merge_evidence(
    retrieved: list[Evidence], existing: list[Evidence]
) -> list[Evidence]:
    """Antepone la evidencia recuperada del corpus, sin duplicar por (fuente, claim)."""
    seen: set[tuple[str, str]] = set()
    merged: list[Evidence] = []
    for e in [*retrieved, *existing]:
        key = (e.source, e.claim)
        if key in seen:
            continue
        seen.add(key)
        merged.append(e)
    return merged
