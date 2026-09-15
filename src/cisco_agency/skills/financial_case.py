"""Skill: Caso financiero.

Construye escenarios (conservador / esperado) a partir del BOM y del horizonte,
y calcula métricas con fórmulas reproducibles (ver `finance.calculator`).

NOTA: los precios reales se consultan por oportunidad (cotizaciones autorizadas).
En modo offline se usan factores de ejemplo, claramente marcados como supuestos.
"""

from __future__ import annotations

from ..config import Settings, get_settings
from ..finance import compute_case
from ..schemas import Bom, FinancialCase, FinancialScenario, Opportunity

# Factores de ejemplo (placeholder) — reemplazar con precios reales autorizados.
_EXAMPLE_UNIT_COST = 1500.0  # costo promedio por línea de HW (ejemplo)
_EXAMPLE_LICENSE_COST = 120.0  # costo anual promedio por licencia (ejemplo)


def build_financial_case(
    opportunity: Opportunity,
    bom: Bom,
    settings: Settings | None = None,
) -> FinancialCase:
    settings = settings or get_settings()

    hw_units = sum(line.quantity for line in bom.lines if not line.is_license)
    lic_units = sum(line.quantity for line in bom.lines if line.is_license)

    capex = hw_units * _EXAMPLE_UNIT_COST
    annual_opex = lic_units * _EXAMPLE_LICENSE_COST
    # Beneficio anual de ejemplo: ahorro operativo + reducción de riesgo (placeholder).
    annual_benefit = capex * 0.18

    horizon = opportunity.horizon_years
    case = FinancialCase(
        currency=settings.currency,
        fiscal_year=settings.fiscal_year,
        assumptions=[
            f"Costo unitario HW de ejemplo: {_EXAMPLE_UNIT_COST} {settings.currency} "
            "(reemplazar con cotización autorizada).",
            f"Costo anual por licencia de ejemplo: {_EXAMPLE_LICENSE_COST} {settings.currency}.",
            "Beneficio anual estimado en 18% del CAPEX (placeholder a validar con el cliente).",
            f"Horizonte de evaluación: {horizon} años. Tasa de descuento: 10%.",
        ],
        scenarios=[
            FinancialScenario(
                name="Conservador",
                capex=capex,
                annual_opex=annual_opex,
                annual_benefit=annual_benefit * 0.7,
                horizon_years=horizon,
            ),
            FinancialScenario(
                name="Esperado",
                capex=capex,
                annual_opex=annual_opex,
                annual_benefit=annual_benefit,
                horizon_years=horizon,
            ),
        ],
    )
    return compute_case(case, discount_rate=0.10)
