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
    yes: bool = typer.Option(
        False, "--yes", "-y",
        help="Desatendido: aprueba el alcance sin preguntar (para CI/scripts).",
    ),
) -> None:
    """Ejecuta el pipeline completo y genera la propuesta."""
    from .approval import AutoApprover, CLIApprover
    from .routing import ModelRouter

    settings = get_settings()
    approver = AutoApprover() if yes else CLIApprover()
    router = ModelRouter(settings)
    rows = router.table()
    llm_roles = sum(1 for r in rows if r["mode"] == "llm")

    if settings.offline:
        mode = "OFFLINE global (respuestas plantilladas)"
    elif llm_roles == 0:
        mode = "OFFLINE (sin credenciales; respuestas plantilladas)"
    else:
        mode = f"Multi-modelo por agente ({llm_roles}/{len(rows)} roles con LLM)"
    console.print(
        Panel.fit(
            f"[bold]Agencia de Expertos Cisco[/bold]\nModo: {mode}\n"
            "[dim]Ver asignación: cisco-agency models[/dim]",
            border_style="cyan",
        )
    )

    import time

    from .metrics import run_report

    raw = _load_input(opportunity_file)
    graph = build_graph(settings, out_dir=out, approver=approver)
    t0 = time.perf_counter()
    final = graph.invoke({"raw_input": raw, "offline": settings.offline})
    duration = time.perf_counter() - t0

    if not final.get("scope_approved", True):
        console.print("[yellow]Alcance rechazado por el revisor. No se generó propuesta.[/yellow]")
        return

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

    # Reporte de métricas (observabilidad)
    report = run_report(final, duration_s=duration)
    report_path = Path(out) / f"run_report_{report['customer'].lower().replace(' ', '_')}.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    mtable = Table(title="Métricas de la corrida", border_style="magenta")
    mtable.add_column("Métrica", style="bold")
    mtable.add_column("Valor")
    mtable.add_row("Duración (s)", str(report["duration_s"]))
    mtable.add_row("Arquitecturas", str(report["n_findings"]))
    mtable.add_row("Líneas BOM (dups)", f"{report['bom_lines']} ({report['bom_duplicates']})")
    mtable.add_row(
        "Evidencia verificada",
        f"{report['evidence_verified']}/{report['evidence_total']}",
    )
    mtable.add_row("Cobertura evidencia", f"{report['evidence_coverage']:.0%}")
    mtable.add_row("Revisiones (reflexión)", str(report["revision_count"]))
    console.print(mtable)
    console.print(f"[dim]Reporte: {report_path}[/dim]")


@app.command()
def eval(
    cases_dir: str = typer.Option("evals/cases", help="Directorio de casos .yaml."),
    out: str = typer.Option("output/evals", help="Directorio de salida."),
) -> None:
    """Corre la batería de evaluaciones (offline, determinista)."""
    from .evals import run_all

    results = run_all(cases_dir, out)
    if not results:
        console.print(f"[yellow]No se encontraron casos en {cases_dir}.[/yellow]")
        raise typer.Exit(code=1)

    table = Table(title="Evaluaciones", border_style="blue")
    table.add_column("Caso", style="bold")
    table.add_column("Checks")
    table.add_column("Estado")
    total_ok = 0
    for r in results:
        ok = sum(c.ok for c in r.checks)
        passed = r.passed
        total_ok += passed
        estado = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
        table.add_row(r.case, f"{ok}/{len(r.checks)}", estado)
    console.print(table)

    for r in results:
        if not r.passed:
            console.print(f"[red]FAIL {r.case}[/red]:")
            for c in r.checks:
                if not c.ok:
                    console.print(f"    ✗ {c.name} — {c.detail}")

    console.print(f"\n[bold]{total_ok}/{len(results)} casos aprobados.[/bold]")
    if total_ok < len(results):
        raise typer.Exit(code=1)


@app.command("ingest-cvd")
def ingest_cvd(
    arch: str = typer.Option(
        None, help="Ingesta solo una arquitectura (p. ej. secure_networking)."
    ),
) -> None:
    """Aprende de los Cisco Validated Designs: genera el corpus desde el catálogo."""
    from .knowledge.ingest import ingest

    ids = ingest(architecture=arch)
    console.print(
        Panel.fit(
            f"[bold]Ingesta de CVDs completada[/bold]\n"
            f"{len(ids)} documento(s) escritos en el corpus.\n"
            "[dim]Los especialistas ya se fundamentan en ellos en cada corrida.[/dim]",
            border_style="green",
        )
    )
    for i in ids:
        console.print(f"  · {i}")


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Host de escucha."),
    port: int = typer.Option(8000, help="Puerto."),
    reload: bool = typer.Option(False, help="Auto-reload (desarrollo)."),
) -> None:
    """Levanta la interfaz web (formulario + generación de propuesta)."""
    try:
        import uvicorn  # noqa: F401
    except ImportError:
        console.print(
            "[red]Falta el extra web.[/red] Instala: pip install -e '.[web]'"
        )
        raise typer.Exit(code=1) from None
    console.print(
        Panel.fit(
            f"[bold]Cisco Experts Agency — Web[/bold]\nhttp://{host}:{port}",
            border_style="cyan",
        )
    )
    import uvicorn

    uvicorn.run("cisco_agency.web.app:app", host=host, port=port, reload=reload)


@app.command()
def info() -> None:
    """Muestra la configuración efectiva."""
    s = get_settings()
    console.print(Panel.fit(
        f"Proveedor global: {s.llm_provider}\n"
        f"Offline global: {s.offline}\n"
        f"Año fiscal: {s.fiscal_year} · Moneda: {s.currency}",
        title="Configuración", border_style="cyan",
    ))


@app.command()
def models() -> None:
    """Muestra el modelo asignado a cada agente (enrutamiento por rol)."""
    from .routing import ModelRouter

    router = ModelRouter(get_settings())
    table = Table(title="Enrutamiento de modelos por agente", border_style="blue")
    table.add_column("Rol", style="bold")
    table.add_column("Proveedor")
    table.add_column("Modelo")
    table.add_column("Modo")
    for row in router.table():
        mode = "[green]llm[/green]" if row["mode"] == "llm" else "[yellow]offline[/yellow]"
        table.add_row(row["role"], row["provider"], row["model"], mode)
    console.print(table)
    console.print(
        "[dim]Edita config/models.yaml para cambiar la asignación. "
        "Un rol queda 'offline' si su proveedor no tiene credenciales en .env.[/dim]"
    )


if __name__ == "__main__":
    app()
