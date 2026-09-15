"""Prueba de humo: el grafo corre de punta a punta en modo offline."""

import os
from pathlib import Path

import yaml

os.environ["OFFLINE"] = "true"

from cisco_agency.config import get_settings  # noqa: E402
from cisco_agency.graph import build_graph  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def test_graph_end_to_end_offline(tmp_path):
    get_settings.cache_clear()  # asegurar OFFLINE=true
    settings = get_settings()
    assert settings.effective_offline() is True

    raw = yaml.safe_load(
        (ROOT / "data" / "samples" / "fanalca_opportunity.yaml").read_text(encoding="utf-8")
    )
    graph = build_graph(settings, out_dir=str(tmp_path))
    final = graph.invoke({"raw_input": raw, "offline": True})

    # Se generaron hallazgos, BOM, caso financiero y propuesta HTML.
    assert len(final["findings"]) >= 2
    assert len(final["bom"].lines) > 0
    assert final["financial_case"].results
    html = final["proposal"]["html"]
    assert Path(html).exists()
    content = Path(html).read_text(encoding="utf-8")
    assert "Fanalca" in content
    assert "STAR" in content

    # IT/OT, SOC y Colaboración deben entrar por las banderas del ejemplo Fanalca.
    archs = [f.architecture.value for f in final["findings"]]
    assert "it_ot" in archs
    assert "observability_soc" in archs
    assert "collaboration" in archs
    # El fan-out paralelo no debe duplicar arquitecturas (reducer upsert).
    assert len(archs) == len(set(archs))
