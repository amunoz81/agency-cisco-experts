"""Corre la batería de evals dorada como parte de las pruebas."""

from pathlib import Path

from cisco_agency.evals import run_all

ROOT = Path(__file__).resolve().parent.parent


def test_all_eval_cases_pass(tmp_path):
    results = run_all(ROOT / "evals" / "cases", out_dir=tmp_path)
    assert results, "No se encontraron casos de evaluación."
    failures = [r for r in results if not r.passed]
    detail = "\n".join(
        f"{r.case}: " + ", ".join(f"{c.name}({c.detail})" for c in r.checks if not c.ok)
        for r in failures
    )
    assert not failures, f"Casos fallidos:\n{detail}"
