.PHONY: help install install-pdf demo run test lint fmt clean

help:
	@echo "Comandos disponibles:"
	@echo "  make install      Instala dependencias base en un venv (.venv)"
	@echo "  make install-pdf  Instala extras para exportar a PDF (WeasyPrint)"
	@echo "  make demo         Ejecuta la agencia en modo OFFLINE con la oportunidad Fanalca"
	@echo "  make run          Ejecuta la agencia (usa .env; requiere API key)"
	@echo "  make test         Corre la batería de pruebas"
	@echo "  make lint         Ruff + mypy"
	@echo "  make fmt          Formatea con ruff"
	@echo "  make clean        Limpia artefactos generados"

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -e ".[dev]"

install-pdf:
	. .venv/bin/activate && pip install -e ".[pdf]"

demo:
	OFFLINE=true python -m cisco_agency.run run data/samples/fanalca_opportunity.yaml --out output

run:
	python -m cisco_agency.run run data/samples/fanalca_opportunity.yaml --out output

test:
	pytest -q

lint:
	ruff check src tests
	mypy src || true

fmt:
	ruff check --fix src tests
	ruff format src tests

clean:
	rm -rf output/*.html output/*.pdf output/*.json
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
