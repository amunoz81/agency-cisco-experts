"""Prueba del loop de reflexión acotado (crítico -> especialistas -> crítico)."""

import os
from pathlib import Path

import yaml

os.environ["OFFLINE"] = "true"

import cisco_agency.agents.technical_reviewer as tr  # noqa: E402
from cisco_agency.config import get_settings  # noqa: E402
from cisco_agency.graph import MAX_REVISIONS, build_graph  # noqa: E402
from cisco_agency.schemas import CritiqueResult  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def _raw():
    return yaml.safe_load(
        (ROOT / "data" / "samples" / "fanalca_opportunity.yaml").read_text(encoding="utf-8")
    )


def test_bounded_reflection_loop(monkeypatch, tmp_path):
    get_settings.cache_clear()
    calls = {"n": 0}

    def always_revise(self, findings, integration, review):
        calls["n"] += 1
        return CritiqueResult(
            revision_requested=True,
            rationale="Reforzar dependencias entre capas.",
            revision_targets=["security"],
            issues=["Falta detallar el punto de aplicación de política."],
        )

    monkeypatch.setattr(tr.TechnicalReviewer, "critique", always_revise)

    graph = build_graph(get_settings(), out_dir=str(tmp_path))
    final = graph.invoke({"raw_input": _raw()})

    # El crítico corre dos veces: pide revisión una vez y en la segunda ya no
    # puede (límite alcanzado), así que el pipeline termina.
    assert calls["n"] == MAX_REVISIONS + 1
    assert final["revision_count"] == MAX_REVISIONS
    assert final["should_revise"] is False
    # Aun con reflexión, se genera la propuesta.
    assert Path(final["proposal"]["html"]).exists()


def test_no_revision_when_critic_satisfied(tmp_path):
    get_settings.cache_clear()
    graph = build_graph(get_settings(), out_dir=str(tmp_path))
    final = graph.invoke({"raw_input": _raw()})
    # En offline el crítico no pide revisión.
    assert final.get("revision_count", 0) == 0
    assert final["critique"].revision_requested is False
