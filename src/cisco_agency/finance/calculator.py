"""Cálculos financieros reproducibles.

Fórmulas explícitas y deterministas (sin LLM) para que el caso financiero
sea auditable. Los supuestos se transportan aparte en `FinancialCase`.
"""

from __future__ import annotations

from ..schemas import FinancialCase, FinancialScenario


def npv(rate: float, cashflows: list[float]) -> float:
    """Valor presente neto. cashflows[0] es el flujo en t=0."""
    return sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cashflows))


def payback_years(capex: float, annual_net: float) -> float | None:
    """Periodo de recuperación simple en años (None si no se recupera)."""
    if annual_net <= 0:
        return None
    return round(capex / annual_net, 2)


def compute_scenario(scenario: FinancialScenario, discount_rate: float = 0.10) -> dict[str, float]:
    """Métricas de un escenario. TCO = capex + opex acumulado en el horizonte."""
    years = scenario.horizon_years
    tco = scenario.capex + scenario.annual_opex * years
    total_benefit = scenario.annual_benefit * years
    annual_net = scenario.annual_benefit - scenario.annual_opex

    # Flujos: -capex en t0; (beneficio - opex) cada año siguiente.
    cashflows = [-scenario.capex] + [annual_net] * years
    scenario_npv = npv(discount_rate, cashflows)

    roi = ((total_benefit - tco) / tco) if tco else 0.0
    pb = payback_years(scenario.capex, annual_net)

    return {
        "tco": round(tco, 2),
        "total_benefit": round(total_benefit, 2),
        "annual_net": round(annual_net, 2),
        "npv": round(scenario_npv, 2),
        "roi": round(roi, 4),
        "payback_years": pb if pb is not None else -1.0,
        "discount_rate": discount_rate,
    }


def compute_case(case: FinancialCase, discount_rate: float = 0.10) -> FinancialCase:
    """Rellena `results` con las métricas de cada escenario."""
    case.results = {
        s.name: compute_scenario(s, discount_rate) for s in case.scenarios
    }
    return case
