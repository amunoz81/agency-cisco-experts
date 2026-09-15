"""Enrutamiento de modelos por rol/agente.

Cada agente puede usar un proveedor y modelo distintos para equilibrar
**calidad vs costo**: modelos potentes para roles críticos (coordinador,
security, revisor) y modelos económicos para el resto.

La configuración es declarativa (YAML) y se puede editar sin tocar código.
Orden de resolución de la config de un rol:
    rol específico  →  `default` del YAML  →  valores globales de `Settings`.

Las credenciales SIEMPRE se leen del entorno (`.env`) por proveedor; un rol
cuyo proveedor no tenga credenciales se ejecuta en **modo offline** de forma
individual (el resto de los agentes puede seguir usando su LLM).
"""

from __future__ import annotations

from pathlib import Path

import yaml
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import BaseModel, Field

from .config import Settings, get_settings
from .llm import build_chat_model, credentials_available, default_model_for

# Roles conocidos (coinciden con las claves de agentes/arquitecturas).
KNOWN_ROLES = (
    "coordinator",
    "secure_networking",
    "security",
    "it_ot",
    "observability_soc",
    "datacenter_ai",
    "collaboration",
    "technical_reviewer",
)


def _first_not_none(*values):
    """Devuelve el primer valor que no sea None."""
    for v in values:
        if v is not None:
            return v
    return None


class RoleModelConfig(BaseModel):
    provider: str | None = None
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = Field(default=None)


class RoutingConfig(BaseModel):
    default: RoleModelConfig = Field(default_factory=RoleModelConfig)
    roles: dict[str, RoleModelConfig] = Field(default_factory=dict)


def _candidate_paths(settings: Settings) -> list[Path]:
    paths: list[Path] = []
    if settings.models_config:
        paths.append(Path(settings.models_config))
    paths.append(Path.cwd() / "config" / "models.yaml")
    paths.append(Path(__file__).resolve().parent / "models.yaml")
    return paths


def load_routing_config(settings: Settings | None = None) -> RoutingConfig:
    settings = settings or get_settings()
    for path in _candidate_paths(settings):
        if path.exists():
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            return RoutingConfig(**data)
    return RoutingConfig()


class ModelRouter:
    """Resuelve y cachea un `BaseChatModel` por rol."""

    def __init__(
        self,
        settings: Settings | None = None,
        config: RoutingConfig | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.config = config or load_routing_config(self.settings)
        self._cache: dict[str, BaseChatModel] = {}

    # -- Resolución de la config efectiva de un rol ------------------------
    def resolve(self, role: str) -> RoleModelConfig:
        default = self.config.default
        role_cfg = self.config.roles.get(role, RoleModelConfig())
        provider = role_cfg.provider or default.provider or self.settings.llm_provider
        model = role_cfg.model or default.model or default_model_for(self.settings, provider)
        temperature = _first_not_none(
            role_cfg.temperature, default.temperature, self.settings.llm_temperature
        )
        max_tokens = _first_not_none(
            role_cfg.max_tokens, default.max_tokens, self.settings.llm_max_tokens
        )
        return RoleModelConfig(
            provider=provider, model=model, temperature=temperature, max_tokens=max_tokens
        )

    # -- ¿El rol corre offline? -------------------------------------------
    def is_offline(self, role: str) -> bool:
        if self.settings.offline:
            return True
        cfg = self.resolve(role)
        return not credentials_available(self.settings, cfg.provider or "")

    # -- Construye (y cachea) el modelo del rol ----------------------------
    def for_role(self, role: str) -> BaseChatModel:
        if role not in self._cache:
            cfg = self.resolve(role)
            self._cache[role] = build_chat_model(
                self.settings,
                provider=cfg.provider,
                model=cfg.model,
                temperature=cfg.temperature,
                max_tokens=cfg.max_tokens,
            )
        return self._cache[role]

    # -- Tabla legible de asignaciones (para CLI/diagnóstico) --------------
    def table(self) -> list[dict[str, str]]:
        rows = []
        for role in KNOWN_ROLES:
            cfg = self.resolve(role)
            rows.append(
                {
                    "role": role,
                    "provider": cfg.provider or "",
                    "model": cfg.model or "",
                    "mode": "offline" if self.is_offline(role) else "llm",
                }
            )
        return rows
