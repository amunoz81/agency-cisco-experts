"""Pruebas de la base de conocimiento y el grounding."""

import os

os.environ["OFFLINE"] = "true"

from cisco_agency.agents import SecuritySpecialist  # noqa: E402
from cisco_agency.config import get_settings  # noqa: E402
from cisco_agency.knowledge import KnowledgeBase  # noqa: E402
from cisco_agency.schemas import EvidenceStatus, Opportunity, Site  # noqa: E402


def _opp() -> Opportunity:
    return Opportunity(
        customer="ACME",
        industry="Manufactura",
        objectives=["Zero Trust de extremo a extremo", "identidad segura"],
        sites=[Site(name="HQ", kind="campus", users=100)],
        workloads=["ERP"],
    )


def test_corpus_loads():
    kb = KnowledgeBase()
    assert len(kb.docs) >= 6


def test_search_security_returns_verified_standards():
    kb = KnowledgeBase()
    ev = kb.evidence_for("security", _opp())
    sources = " ".join(e.source for e in ev)
    assert "NIST" in sources or "CISA" in sources
    assert any(e.status == EvidenceStatus.VERIFIED for e in ev)


def test_it_ot_grounds_on_iec_62443():
    kb = KnowledgeBase()
    ev = kb.evidence_for("it_ot", _opp())
    assert any("62443" in e.source for e in ev)


def test_agent_attaches_retrieved_evidence_offline():
    get_settings.cache_clear()
    agent = SecuritySpecialist(get_settings(), kb=KnowledgeBase())
    finding = agent.analyze(_opp())
    # Debe incluir evidencia verificada proveniente del corpus (NIST/CISA).
    assert any(e.status == EvidenceStatus.VERIFIED for e in finding.evidence)
    assert len(finding.evidence) >= 2
