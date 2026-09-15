from cisco_agency.schemas import (
    Architecture,
    Bom,
    BomLine,
    SpecialistFinding,
)


def test_bom_deduplication_sums_quantities():
    net = Architecture.SECURE_NETWORKING
    bom = Bom(
        lines=[
            BomLine(sku="A", description="switch", quantity=2, architecture=net),
            BomLine(sku="A", description="switch", quantity=3, architecture=net),
            BomLine(sku="B", description="fw", quantity=1, architecture=Architecture.SECURITY),
        ]
    )
    dedup = bom.deduplicated()
    assert len(dedup.lines) == 2
    switch = next(x for x in dedup.lines if x.sku == "A")
    assert switch.quantity == 5


def test_finding_default_scope_is_necessary():
    f = SpecialistFinding(
        architecture=Architecture.SECURITY,
        customer_need="n",
        proposed_solution="s",
    )
    assert f.scope.value == "necesaria"
