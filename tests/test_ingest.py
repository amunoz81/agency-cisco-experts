"""Pruebas de la ingesta/auto-sincronización de CVDs."""

import os

from cisco_agency.knowledge.ingest import (
    ARCHITECTURES,
    CATALOG_PATH,
    CORPUS_DIR,
    ensure_corpus,
    ingest,
)


def test_catalog_covers_every_architecture():
    import yaml

    catalog = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    for arch in ARCHITECTURES:
        assert catalog.get(arch, {}).get("cvds"), f"{arch} sin CVDs en el catálogo"


def test_ingest_writes_docs_for_all_architectures():
    ids = ingest()
    assert len(ids) >= 10
    # Debe haber al menos un CVD por arquitectura.
    for arch in ARCHITECTURES:
        assert any(i.startswith(f"cvd-{arch}-") for i in ids), arch


def test_ensure_corpus_is_idempotent_then_refreshes():
    ensure_corpus()  # deja el corpus al día
    assert ensure_corpus() == 0  # sin cambios -> no reescribe
    os.utime(CATALOG_PATH, None)  # simula edición del catálogo
    assert ensure_corpus() > 0  # detecta el cambio y regenera


def test_corpus_dir_has_cvd_documents():
    ensure_corpus()
    assert len(list(CORPUS_DIR.glob("cvd-*.md"))) >= 10
