"""Pruebas de la interfaz web (FastAPI)."""

import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient  # noqa: E402

from cisco_agency.web.app import app  # noqa: E402
from cisco_agency.web.parsing import parse_install_base  # noqa: E402

client = TestClient(app)


def test_config_lists_verticals_localized():
    r = client.get("/api/config", params={"lang": "es"})
    assert r.status_code == 200
    data = r.json()
    ids = {v["id"] for v in data["verticals"]}
    assert {"manufacturing", "healthcare", "retail"} <= ids
    # Etiqueta en español
    manu = next(v for v in data["verticals"] if v["id"] == "manufacturing")
    assert manu["label"] == "Manufactura"


def test_proposal_endpoint_offline_generates():
    r = client.post(
        "/api/proposal",
        data={
            "customer": "ACME Web",
            "vertical": "manufacturing",
            "situation": "Planta industrial con red heterogénea.",
            "problem": "Zero Trust, visibilidad OT y correlación en el SOC.",
            "current_products": "Catalyst 9300, ISE",
            "lang": "es",
            "offline": "true",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["html_file"]
    assert "security" in data["specialists"]
    assert "it_ot" in data["specialists"]
    # Exportación a Office disponible (extra web instalado).
    assert data["pptx_file"] and data["pptx_file"].endswith(".pptx")
    assert data["docx_file"] and data["docx_file"].endswith(".docx")
    # Los archivos generados se pueden descargar.
    for key in ("html_file", "pptx_file", "docx_file"):
        dl = client.get(f"/files/{data[key]}")
        assert dl.status_code == 200


def test_proposal_with_detailed_sites():
    import json

    sites = [
        {"name": "HQ Cali", "kind": "campus", "users": 800},
        {"name": "Planta Yumbo", "kind": "planta", "users": 350},
        {"name": "DC Principal", "kind": "datacenter"},
    ]
    r = client.post(
        "/api/proposal",
        data={
            "customer": "Fanalca",
            "vertical": "manufacturing",
            "problem": "Modernizar red y seguridad.",
            "sites_json": json.dumps(sites),
            "lang": "es",
            "offline": "true",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    # Planta => IT/OT; Datacenter => Data Center/AI.
    assert "it_ot" in data["specialists"]
    assert "datacenter_ai" in data["specialists"]


def test_parse_install_base_csv():
    csv_bytes = b"SKU,Descripcion,Cantidad\nC9300-48P,Catalyst 9300,10\nISE-VM,ISE,2\n"
    parsed = parse_install_base("base.csv", csv_bytes)
    assert parsed["items"]
    assert any("C9300-48P" in line for line in parsed["items"])
