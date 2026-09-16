"""Configuración central de la agencia (variables de entorno / .env)."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Provider = Literal["anthropic", "openai", "azure"]


class Settings(BaseSettings):
    """Ajustes leídos desde el entorno o `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    llm_provider: Provider = Field(default="anthropic", alias="LLM_PROVIDER")
    offline: bool = Field(default=False, alias="OFFLINE")

    # Ruta al YAML de enrutamiento de modelos por rol (opcional).
    models_config: str | None = Field(default=None, alias="MODELS_CONFIG")

    # La agencia sincroniza el corpus de CVDs con el catálogo en cada arranque.
    auto_ingest_cvd: bool = Field(default=True, alias="AUTO_INGEST_CVD")

    # Anthropic
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-opus-4-8", alias="ANTHROPIC_MODEL")

    # OpenAI
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")

    # Azure OpenAI
    azure_openai_api_key: str | None = Field(default=None, alias="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: str | None = Field(default=None, alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_version: str = Field(
        default="2024-10-21", alias="AZURE_OPENAI_API_VERSION"
    )
    azure_openai_deployment: str | None = Field(
        default=None, alias="AZURE_OPENAI_DEPLOYMENT"
    )

    # Generación
    llm_temperature: float = Field(default=0.2, alias="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=4096, alias="LLM_MAX_TOKENS")

    # Contexto comercial (se consulta por oportunidad)
    fiscal_year: str = Field(default="FY26", alias="FISCAL_YEAR")
    currency: str = Field(default="USD", alias="CURRENCY")

    def has_credentials(self) -> bool:
        """¿Hay credenciales para el proveedor seleccionado?"""
        if self.llm_provider == "anthropic":
            return bool(self.anthropic_api_key)
        if self.llm_provider == "openai":
            return bool(self.openai_api_key)
        if self.llm_provider == "azure":
            return bool(self.azure_openai_api_key and self.azure_openai_endpoint)
        return False

    def effective_offline(self) -> bool:
        """Se ejecuta offline si se pidió explícitamente o faltan credenciales."""
        return self.offline or not self.has_credentials()


@lru_cache
def get_settings() -> Settings:
    return Settings()
