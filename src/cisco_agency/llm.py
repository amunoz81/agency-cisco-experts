"""Fábrica multi-proveedor de modelos de chat (LangChain).

Permite seleccionar el proveedor y el modelo, ya sea de forma global (variables
de entorno) o **por rol/agente** (ver `cisco_agency.routing`), sin cambiar el
código de los agentes.
"""

from __future__ import annotations

from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from .config import Settings, get_settings

Provider = str


def credentials_available(settings: Settings, provider: str) -> bool:
    """¿Hay credenciales en el entorno para ese proveedor?"""
    if provider == "anthropic":
        return bool(settings.anthropic_api_key)
    if provider == "openai":
        return bool(settings.openai_api_key)
    if provider == "azure":
        return bool(settings.azure_openai_api_key and settings.azure_openai_endpoint)
    return False


def default_model_for(settings: Settings, provider: str) -> str:
    """Modelo por defecto de cada proveedor según la configuración."""
    return {
        "anthropic": settings.anthropic_model,
        "openai": settings.openai_model,
        "azure": settings.azure_openai_deployment or settings.openai_model,
    }.get(provider, settings.openai_model)


def build_chat_model(
    settings: Settings | None = None,
    *,
    provider: str | None = None,
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
    **overrides: Any,
) -> BaseChatModel:
    """Construye un `BaseChatModel`.

    Si no se pasa `provider`/`model`, se usan los globales de `settings`. Esto
    permite tanto un modelo único como uno distinto por agente.
    """
    settings = settings or get_settings()
    provider = provider or settings.llm_provider
    model = model or default_model_for(settings, provider)
    temperature = settings.llm_temperature if temperature is None else temperature
    max_tokens = settings.llm_max_tokens if max_tokens is None else max_tokens

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        if not settings.anthropic_api_key:
            raise ValueError("Falta ANTHROPIC_API_KEY para el proveedor 'anthropic'.")
        return ChatAnthropic(
            model=model,
            api_key=settings.anthropic_api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            **overrides,
        )

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        if not settings.openai_api_key:
            raise ValueError("Falta OPENAI_API_KEY para el proveedor 'openai'.")
        return ChatOpenAI(
            model=model,
            api_key=settings.openai_api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            **overrides,
        )

    if provider == "azure":
        from langchain_openai import AzureChatOpenAI

        if not (settings.azure_openai_api_key and settings.azure_openai_endpoint):
            raise ValueError(
                "Faltan AZURE_OPENAI_API_KEY / AZURE_OPENAI_ENDPOINT para 'azure'."
            )
        return AzureChatOpenAI(
            azure_deployment=model,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            **overrides,
        )

    raise ValueError(f"Proveedor LLM no soportado: {provider!r}")
