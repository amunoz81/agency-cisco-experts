"""Pruebas del diagrama de arquitectura de red."""

from xml.dom import minidom

from cisco_agency.reporting.diagram import build_topology, to_drawio, write_drawio
from cisco_agency.schemas import Architecture, Opportunity, Site, SpecialistFinding


def _findings(archs):
    return [
        SpecialistFinding(architecture=Architecture(a), customer_need="n", proposed_solution="s")
        for a in archs
    ]


def test_topology_only_includes_present_architectures():
    opp = Opportunity(customer="X", sites=[Site(name="HQ")])
    tiers = build_topology(opp, _findings(["secure_networking", "security"]))
    labels = " ".join(t.label for t in tiers)
    # No debe aparecer el tier de IT/OT ni Data Center si no están presentes.
    assert "IT/OT" not in labels
    assert "Data Center" not in labels
    assert "Campus" in labels


def test_cloud_providers_become_nodes():
    opp = Opportunity(customer="X", cloud_providers=["AWS", "Microsoft Azure"])
    tiers = build_topology(opp, _findings(["security"]))
    cloud_nodes = " ".join(n.label for n in tiers[0].nodes)
    assert "AWS" in cloud_nodes
    assert "Azure" in cloud_nodes


def test_drawio_is_valid_xml():
    opp = Opportunity(customer="ACME", cloud_providers=["AWS"])
    tiers = build_topology(opp, _findings(["secure_networking", "security", "it_ot"]))
    xml = to_drawio(tiers, opp.customer)
    # Debe parsear como XML y contener celdas y referencias a shapes Cisco.
    minidom.parseString(xml)
    assert "mxCell" in xml
    assert "mxgraph.cisco" in xml


def test_write_drawio_creates_file(tmp_path):
    opp = Opportunity(customer="ACME")
    tiers = build_topology(opp, _findings(["secure_networking", "security"]))
    path = write_drawio(tiers, tmp_path, "acme", opp.customer)
    assert path.endswith(".drawio")
    from pathlib import Path

    assert Path(path).exists()
