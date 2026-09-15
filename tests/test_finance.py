from cisco_agency.finance import compute_scenario
from cisco_agency.finance.calculator import npv, payback_years
from cisco_agency.schemas import FinancialScenario


def test_npv_zero_rate_is_sum():
    assert npv(0.0, [-100, 50, 50, 50]) == 50


def test_payback_years():
    assert payback_years(1000, 250) == 4.0
    assert payback_years(1000, 0) is None


def test_compute_scenario_metrics():
    s = FinancialScenario(
        name="x", capex=1000, annual_opex=100, annual_benefit=600, horizon_years=3
    )
    r = compute_scenario(s, discount_rate=0.10)
    assert r["tco"] == 1300  # 1000 + 100*3
    assert r["annual_net"] == 500  # 600 - 100
    assert r["payback_years"] == 2.0  # 1000 / 500
    # NPV: -1000 + 500*(1/1.1 + 1/1.21 + 1/1.331) ≈ 243.4 (positivo)
    assert r["npv"] > 0
