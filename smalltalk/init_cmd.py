from pathlib import Path
from smalltalk.converter import is_convertible
from rich.console import Console
from rich.table import Table

console = Console()

SKIP_DIRS = {
    "node_modules", ".git", ".next", ".venv", "__pycache__",
    "archive", ".originals", "dist", "build",
}


def collect_md_files(directory: Path) -> list[Path]:
    files = []
    for path in sorted(directory.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        # Skip hidden plugin dirs
        if any(part.startswith(".") for part in path.relative_to(directory).parts[:-1]):
            continue
        files.append(path)
    return files


def run_init(directory: Path):
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise SystemExit(1)

    directory = directory.resolve()
    console.print()
    console.print("=" * 60)
    console.print("  Smalltalk — Init Scan")
    console.print("=" * 60)
    console.print(f"\n  Scanning: [bold]{directory}[/bold]\n")

    md_files = collect_md_files(directory)

    if not md_files:
        console.print("  [yellow]No .md files found.[/yellow]")
        return

    convertible = [f for f in md_files if is_convertible(f)]
    skipped = [f for f in md_files if not is_convertible(f)]
    already_done = [f for f in convertible if f.with_suffix(".st").exists()]
    ready = [f for f in convertible if not f.with_suffix(".st").exists()]

    table = Table(show_header=True, header_style="bold", box=None)
    table.add_column("File", style="cyan")
    table.add_column("Status")
    table.add_column("Path")

    for f in ready:
        table.add_row(f.name, "[yellow]ready[/yellow]", str(f.relative_to(directory)))
    for f in already_done:
        table.add_row(f.name, "[green]converted[/green]", str(f.relative_to(directory)))
    for f in skipped:
        table.add_row(f.name, "[dim]skipped[/dim]", str(f.relative_to(directory)))

    console.print(table)
    console.print()
    console.print(f"  [bold]{len(ready)}[/bold] ready to convert")
    console.print(f"  [bold]{len(already_done)}[/bold] already converted")
    console.print(f"  [bold]{len(skipped)}[/bold] skipped (human-maintained)")
    console.print()
    console.print("  Next steps:")
    console.print("    [bold]smalltalk backup <dir>[/bold]   ← back up originals first")
    console.print("    [bold]smalltalk mine <dir>[/bold]     ← convert to .st")
    console.print()
