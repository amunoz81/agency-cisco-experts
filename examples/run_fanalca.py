"""Ejemplo mínimo: ejecuta la agencia sobre la oportunidad Fanalca.

Uso:
    OFFLINE=true python examples/run_fanalca.py
"""

from __future__ import annotations

from pathlib import Path

import yaml

from cisco_agency.config import get_settings
from cisco_agency.graph import build_graph

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    raw = yaml.safe_load(
        (ROOT / "data" / "samples" / "fanalca_opportunity.yaml").read_text(encoding="utf-8")
    )
    settings = get_settings()
    graph = build_graph(settings, out_dir=str(ROOT / "output"))
    final = graph.invoke({"raw_input": raw, "offline": settings.effective_offline()})

    for line in final.get("log", []):
        print("·", line)
    print("\nPropuesta:", final.get("proposal", {}).get("html"))


if __name__ == "__main__":
    main()
