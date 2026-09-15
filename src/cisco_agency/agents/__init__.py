"""Agentes de la agencia: coordinador, especialistas y revisor."""

from .coordinator import Coordinator  # noqa: F401
from .datacenter_ai import DatacenterAISpecialist  # noqa: F401
from .it_ot import ItOtSpecialist  # noqa: F401
from .observability_soc import ObservabilitySocSpecialist  # noqa: F401
from .secure_networking import SecureNetworkingSpecialist  # noqa: F401
from .security import SecuritySpecialist  # noqa: F401
from .technical_reviewer import TechnicalReviewer  # noqa: F401

SPECIALIST_REGISTRY = {
    "secure_networking": SecureNetworkingSpecialist,
    "security": SecuritySpecialist,
    "it_ot": ItOtSpecialist,
    "observability_soc": ObservabilitySocSpecialist,
    "datacenter_ai": DatacenterAISpecialist,
}
