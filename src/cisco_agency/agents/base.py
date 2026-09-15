"""Base para agentes especialistas.

Cada especialista carga su prompt de sistema desde `prompts/` y devuelve un
`SpecialistFinding` en el formato común. En modo offline, cada subclase provee
un hallazgo plantillado determinista (para demos y CI sin credenciales).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from ..config import Settings, get_settings
from ..llm import build_chat_model
from ..schemas import Architecture, Opportunity, SpecialistFinding

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class SpecialistAgent(ABC):
    architecture: Architecture
    prompt_file: str

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    # -- Prompt ------------------------------------------------------------
    def system_prompt(self) -> str:
        path = PROMPTS_DIR / self.prompt_file
        if path.exists():
            return path.read_text(encoding="utf-8")
        return f"Eres el especialista Cisco de {self.architecture.value}."

    # -- Interfaz principal ------------------------------------------------
    def analyze(self, opportunity: Opportunity) -> SpecialistFinding:
        if self.settings.effective_offline():
            return self._offline_finding(opportunity)
        return self._llm_finding(opportunity)

    # -- Ejecución con LLM -------------------------------------------------
    def _llm_finding(self, opportunity: Opportunity) -> SpecialistFinding:
        model = build_chat_model(self.settings)
        structured = model.with_structured_output(SpecialistFinding)
        messages = [
            SystemMessage(content=self.system_prompt()),
            HumanMessage(content=self._user_prompt(opportunity)),
        ]
        finding: SpecialistFinding = structured.invoke(messages)  # type: ignore[assignment]
        finding.architecture = self.architecture
        return finding

    def _user_prompt(self, opportunity: Opportunity) -> str:
        return (
            "Analiza la siguiente oportunidad y entrega tu hallazgo en el formato "
            "común (necesidad → solución → dependencias → dimensionamiento → "
            "licencias → beneficio medible → evidencia → riesgos y pendientes).\n\n"
            f"Oportunidad:\n{opportunity.model_dump_json(indent=2)}"
        )

    # -- Modo offline (subclases lo implementan) ---------------------------
    @abstractmethod
    def _offline_finding(self, opportunity: Opportunity) -> SpecialistFinding:
        ...
