"""Pruebas del enrutamiento de modelos por rol."""

from cisco_agency.config import Settings
from cisco_agency.routing import ModelRouter, RoleModelConfig, RoutingConfig


def _settings(**aliases) -> Settings:
    # _env_file=None ignora el .env del repo para tener un entorno controlado.
    return Settings(_env_file=None, **aliases)


def _routing() -> RoutingConfig:
    return RoutingConfig(
        default=RoleModelConfig(provider="openai", model="gpt-4o-mini"),
        roles={
            "coordinator": RoleModelConfig(model="gpt-4o", temperature=0.0),
            "security": RoleModelConfig(provider="openai", model="gpt-4o"),
        },
    )


def test_role_specific_model_wins():
    router = ModelRouter(_settings(LLM_PROVIDER="openai"), _routing())
    assert router.resolve("coordinator").model == "gpt-4o"
    assert router.resolve("security").model == "gpt-4o"
    # Un rol sin entrada usa el default del YAML.
    assert router.resolve("collaboration").model == "gpt-4o-mini"


def test_default_temperature_overridden_per_role():
    router = ModelRouter(_settings(LLM_PROVIDER="openai"), _routing())
    assert router.resolve("coordinator").temperature == 0.0


def test_offline_when_provider_lacks_credentials():
    # Sin OPENAI_API_KEY -> el rol openai queda offline.
    router = ModelRouter(_settings(LLM_PROVIDER="openai", OPENAI_API_KEY=""), _routing())
    assert router.is_offline("coordinator") is True


def test_llm_mode_when_credentials_present():
    router = ModelRouter(
        _settings(LLM_PROVIDER="openai", OPENAI_API_KEY="sk-test", OFFLINE=False),
        _routing(),
    )
    assert router.is_offline("coordinator") is False


def test_global_offline_forces_all_offline():
    router = ModelRouter(
        _settings(LLM_PROVIDER="openai", OPENAI_API_KEY="sk-test", OFFLINE=True),
        _routing(),
    )
    assert router.is_offline("security") is True
