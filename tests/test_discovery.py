"""Pruebas de la skill de descubrimiento (mapeo del formulario web)."""

from cisco_agency.skills import build_opportunity


def test_sites_built_from_counts():
    opp = build_opportunity({"customer": "X", "n_sites": 3, "n_datacenters": 2})
    kinds = [s.kind for s in opp.sites]
    assert kinds.count("campus") == 3
    assert kinds.count("datacenter") == 2
    # Datacenter presente => datacenter_ai entra en alcance.
    assert opp.needs_datacenter_ai is True


def test_remote_users_trigger_collaboration():
    opp = build_opportunity({"customer": "X", "remote_users": 120})
    assert opp.remote_users == 120
    assert opp.needs_collaboration is True


def test_cloud_providers_captured():
    opp = build_opportunity(
        {"customer": "X", "cloud_providers": ["AWS", "Microsoft Azure"]}
    )
    assert "AWS" in opp.cloud_providers
    assert "Microsoft Azure" in opp.cloud_providers


def test_explicit_sites_take_precedence():
    opp = build_opportunity(
        {"customer": "X", "n_sites": 5, "sites": [{"name": "HQ", "kind": "planta"}]}
    )
    assert len(opp.sites) == 1
    assert opp.it_ot_present is True  # planta
