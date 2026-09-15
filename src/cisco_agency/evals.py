"""Batería de evaluaciones (evals) del pipeline.

Corre la agencia en modo offline (determinista) sobre un dataset dorado de
oportunidades y verifica propiedades estructurales del resultado: alcance
correcto, BOM sin duplicados, cobertura de evidencia, revisión aprobada y
generación de la propuesta.

Uso:
    cisco-agency eval            # todas las casos en evals/cases/
    python -m cisco_agency.evals
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .approval import AutoApprover
from .config import Settings
from .graph import build_graph
from .metrics import run_report

CASES_DIR = Path.cwd() / "evals" / "cases"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""


@dataclass
class EvalResult:
    case: str
    checks: list[Check] = field(default_factory=list)
    report: dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return all(c.ok for c in self.checks)


def _offline_settings() -> Settings:
    # Determinista: fuerza offline e ignora el .env del repo.
    return Settings(_env_file=None, OFFLINE=True, LLM_PROVIDER="openai")


def run_case(case: dict, out_dir: str | Path) -> EvalResult:
    name = case.get("name", "sin_nombre")
    expect = case.get("expect", {})
    raw = case["opportunity"]

    graph = build_graph(_offline_settings(), out_dir=str(out_dir), approver=AutoApprover())
    final = graph.invoke({"raw_input": raw, "offline": True})
    report = run_report(final)

    checks: list[Check] = []
    specialists = set(report["specialists"])

    for arch in expect.get("specialists_include", []):
        checks.append(Check(f"incluye:{arch}", arch in specialists,
                            f"esperado en {sorted(specialists)}"))
    for arch in expect.get("specialists_exclude", []):
        checks.append(Check(f"excluye:{arch}", arch not in specialists))

    if "min_findings" in expect:
        checks.append(Check("min_findings",
                            report["n_findings"] >= expect["min_findings"],
                            f"{report['n_findings']} >= {expect['min_findings']}"))
    if "min_bom_lines" in expect:
        checks.append(Check("min_bom_lines",
                            report["bom_lines"] >= expect["min_bom_lines"],
                            f"{report['bom_lines']} >= {expect['min_bom_lines']}"))
    if expect.get("no_duplicate_bom"):
        checks.append(Check("no_duplicate_bom", report["bom_duplicates"] == 0,
                            f"duplicados={report['bom_duplicates']}"))
    if "review_passes" in expect:
        checks.append(Check("review_passes",
                            report["review_passed"] == expect["review_passes"],
                            f"passed={report['review_passed']}"))
    if "min_verified_evidence" in expect:
        checks.append(Check("min_verified_evidence",
                            report["evidence_verified"] >= expect["min_verified_evidence"],
                            f"{report['evidence_verified']} >= {expect['min_verified_evidence']}"))
    if expect.get("proposal_generated", True):
        html = report.get("proposal_html")
        checks.append(Check("proposal_generated", bool(html) and Path(html).exists()))

    return EvalResult(case=name, checks=checks, report=report)


def load_cases(cases_dir: Path | str | None = None) -> list[dict]:
    d = Path(cases_dir) if cases_dir else CASES_DIR
    cases = []
    if d.exists():
        for path in sorted(d.glob("*.yaml")):
            cases.append(yaml.safe_load(path.read_text(encoding="utf-8")))
    return cases


def run_all(
    cases_dir: Path | str | None = None,
    out_dir: str | Path = "output/evals",
) -> list[EvalResult]:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    return [run_case(c, out_dir) for c in load_cases(cases_dir)]


if __name__ == "__main__":
    results = run_all()
    total_ok = sum(r.passed for r in results)
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"[{status}] {r.case}")
        for c in r.checks:
            if not c.ok:
                print(f"    ✗ {c.name}: {c.detail}")
    print(f"\n{total_ok}/{len(results)} casos aprobados.")
