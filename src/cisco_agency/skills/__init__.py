"""Skills compartidas de la agencia.

Cada skill define qué información necesita, qué decisión toma, cómo verifica y
qué entrega. Se invocan desde los nodos del grafo (`cisco_agency.graph`).
"""

from .bom_licensing import consolidate_bom  # noqa: F401
from .customer_discovery import build_opportunity  # noqa: F401
from .financial_case import build_financial_case  # noqa: F401
from .integration import integrate_architectures  # noqa: F401
from .portfolio_verification import verify_portfolio  # noqa: F401
