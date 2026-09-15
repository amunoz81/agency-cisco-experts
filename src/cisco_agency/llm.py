"""Fábrica multi-proveedor de modelos de chat (LangChain).

Permite seleccionar el proveedor con la variable de entorno `LLM_PROVIDER`
sin cambiar el código de los agentes.
"""

from __future__ import annotations

from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from .config import Settings, get_settings


def build_chat_model(settings: Settings | None = None, **overrides: Any) -> BaseChatModel:
    """Construye el modelo de chat según el proveedor configurado.

    Lanza ImportError/ValueError con un mensaje claro si falta el paquete o
    las credenciales del proveedor elegido.
    """
    settings = settings or get_settings()
    temperature = overrides.pop("temperature", settings.llm_temperature)
    max_tokens = overrides.pop("max_tokens", settings.llm_max_tokens)

    provider = settings.llm_provider
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        if not settings.anthropic_api_key:
            raise ValueError("Falta ANTHROPIC_API_KEY para el proveedor 'anthropic'.")
        return ChatAnthropic(
            model=settings.anthropic_model,
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
            model=settings.openai_model,
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
            azure_deployment=settings.azure_openai_deployment,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            **overrides,
        )

    raise ValueError(f"Proveedor LLM no soportado: {provider!r}")
