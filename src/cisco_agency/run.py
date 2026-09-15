"""CLI de la Agencia de Expertos Cisco."""

from __future__ import annotations

import json
from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .config import get_settings
from .graph import build_graph

app = typer.Typer(add_completion=False, help="Agencia agéntica de expertos Cisco.")
console = Console()


def _load_input(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        return yaml.safe_load(text)
    return json.loads(text)


@app.command()
def run(
    opportunity_file: Path = typer.Argument(..., help="YAML/JSON con la oportunidad."),
    out: str = typer.Option("output", help="Directorio de salida."),
) -> None:
    """Ejecuta el pipeline completo y genera la propuesta."""
    settings = get_settings()
    offline = settings.effective_offline()

    mode = (
        "OFFLINE (respuestas plantilladas)"
        if offline
        else f"LLM: {settings.llm_provider}"
    )
    console.print(
        Panel.fit(
            f"[bold]Agencia de Expertos Cisco[/bold]\nModo: {mode}",
            border_style="cyan",
        )
    )

    raw = _load_input(opportunity_file)
    graph = build_graph(settings, out_dir=out)
    final = graph.invoke({"raw_input": raw, "offline": offline})

    # Log de ejecución
    table = Table(title="Ejecución del grafo", show_header=False, border_style="blue")
    for line in final.get("log", []):
        table.add_row(line)
    console.print(table)

    proposal = final.get("proposal", {})
    console.print(f"\n[green]✓ HTML:[/green] {proposal.get('html')}")
    if proposal.get("pdf"):
        engine = proposal.get("pdf_engine")
        console.print(f"[green]✓ PDF:[/green] {proposal.get('pdf')} (motor: {engine})")
    elif proposal.get("pdf_error"):
        console.print(f"[yellow]PDF no generado:[/yellow] {proposal.get('pdf_error')}")

    review = final.get("review")
    if review is not None:
        status = "APROBADA" if review.passed else "CON BLOQUEANTES"
        console.print(
            f"\n[bold]Revisión técnica:[/bold] {status} · "
            f"{len(review.issues)} observación/es"
        )


@app.command()
def info() -> None:
    """Muestra la configuración efectiva."""
    s = get_settings()
    console.print(Panel.fit(
        f"Proveedor: {s.llm_provider}\n"
        f"Offline efectivo: {s.effective_offline()}\n"
        f"Año fiscal: {s.fiscal_year} · Moneda: {s.currency}",
        title="Configuración", border_style="cyan",
    ))


if __name__ == "__main__":
    app()
