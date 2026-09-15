"""Pruebas de la compuerta HITL de aprobación de alcance."""

import os
from pathlib import Path

import yaml

os.environ["OFFLINE"] = "true"

from cisco_agency.approval import ScopeDecision  # noqa: E402
from cisco_agency.config import get_settings  # noqa: E402
from cisco_agency.graph import build_graph  # noqa: E402
from cisco_agency.schemas import ScopeClassification  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def _raw():
    return yaml.safe_load(
        (ROOT / "data" / "samples" / "fanalca_opportunity.yaml").read_text(encoding="utf-8")
    )


class _RejectApprover:
    def approve_scope(self, opportunity, scope_plan):
        return ScopeDecision(approved=False, scope_plan=scope_plan, selected_specialists=[],
                             notes=["rechazado en prueba"])


class _ExcludeDatacenterApprover:
    def approve_scope(self, opportunity, scope_plan):
        plan = dict(scope_plan)
        plan["datacenter_ai"] = ScopeClassification.OUT_OF_SCOPE
        selected = [
            a for a, c in plan.items()
            if c in (ScopeClassification.NECESSARY, ScopeClassification.OPTIONAL)
        ]
        return ScopeDecision(approved=True, scope_plan=plan, selected_specialists=selected)


def test_reject_scope_stops_pipeline(tmp_path):
    get_settings.cache_clear()
    graph = build_graph(get_settings(), out_dir=str(tmp_path), approver=_RejectApprover())
    final = graph.invoke({"raw_input": _raw()})
    assert final.get("scope_approved") is False
    assert not final.get("findings")
    assert "proposal" not in final


def test_human_edit_excludes_specialist(tmp_path):
    get_settings.cache_clear()
    graph = build_graph(
        get_settings(), out_dir=str(tmp_path), approver=_ExcludeDatacenterApprover()
    )
    final = graph.invoke({"raw_input": _raw()})
    archs = {f.architecture.value for f in final["findings"]}
    assert "datacenter_ai" not in archs
    assert Path(final["proposal"]["html"]).exists()
