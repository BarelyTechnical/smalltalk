"""CLI command group for palace operations."""
import typer
from pathlib import Path
from rich.console import Console
from smalltalk.palace import init_palace, index_palace, palace_status_text

console = Console()

palace_app = typer.Typer(
    help="Palace navigation — structure .st files into wings and rooms for 34%+ better retrieval.",
)


@palace_app.command("init")
def cmd_init(
    directory: Path = typer.Argument(..., help="Directory to initialise as a palace"),
):
    """
    Scan a directory and generate _index.st.

    Detection rules:
      Category folder (projects/, people/) → each child = wing
      Wing folder (no sub-dirs) → each .st file = room
      Root .st files → single-file wings

    Run once, then use 'palace index' to refresh after adding files.
    """
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    try:
        index_path = init_palace(directory.resolve())
        console.print(f"\n[green]+[/green] Palace index: [bold]{index_path}[/bold]")
        console.print(palace_status_text(directory.resolve()))
    except Exception as exc:
        console.print(f"[red]ERROR:[/red] {exc}")
        raise typer.Exit(1)


@palace_app.command("index")
def cmd_index(
    directory: Path = typer.Argument(..., help="Palace root to re-index"),
):
    """Regenerate _index.st from current directory structure. Run after adding or renaming files."""
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    try:
        index_path = index_palace(directory.resolve())
        console.print(f"[green]+[/green] Index regenerated: [bold]{index_path}[/bold]")
    except Exception as exc:
        console.print(f"[red]ERROR:[/red] {exc}")
        raise typer.Exit(1)


@palace_app.command("status")
def cmd_status(
    directory: Path = typer.Argument(..., help="Palace root directory"),
):
    """Show palace structure: wings, rooms, tunnels, memory stack."""
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    console.print(palace_status_text(directory.resolve()))
