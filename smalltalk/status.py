from pathlib import Path
from smalltalk.converter import is_convertible
from smalltalk.init_cmd import collect_md_files, SKIP_DIRS
from rich.console import Console
from rich.table import Table

console = Console()


def run_status(directory: Path):
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise SystemExit(1)

    directory = directory.resolve()

    console.print()
    console.print("=" * 60)
    console.print("  Smalltalk — Status")
    console.print("=" * 60)
    console.print(f"\n  Directory: [bold]{directory}[/bold]\n")

    md_files = collect_md_files(directory)
    convertible = [f for f in md_files if is_convertible(f)]
    converted = [f for f in convertible if f.with_suffix(".st").exists()]
    pending = [f for f in convertible if not f.with_suffix(".st").exists()]
    skipped = [f for f in md_files if not is_convertible(f)]

    total = len(convertible)
    pct = int((len(converted) / total) * 100) if total > 0 else 0
    bar_filled = pct // 5
    bar = "█" * bar_filled + "░" * (20 - bar_filled)

    console.print(f"  [{bar}] {pct}%  ({len(converted)}/{total} files converted)\n")

    if converted:
        console.print("  [bold green]Converted[/bold green]")
        for f in converted:
            st = f.with_suffix(".st")
            md_lines = len(f.read_text(encoding="utf-8").splitlines())
            st_lines = len(st.read_text(encoding="utf-8").splitlines())
            reduction = int((1 - st_lines / md_lines) * 100) if md_lines > 0 else 0
            console.print(
                f"    [green]✓[/green] {f.relative_to(directory)}"
                f"  [dim]{md_lines}→{st_lines} lines ({reduction}% reduction)[/dim]"
            )
        console.print()

    if pending:
        console.print("  [bold yellow]Pending[/bold yellow]")
        for f in pending:
            console.print(f"    [yellow]○[/yellow] {f.relative_to(directory)}")
        console.print()

    if skipped:
        console.print("  [bold dim]Skipped (human-maintained)[/bold dim]")
        for f in skipped:
            console.print(f"    [dim]–[/dim] {f.relative_to(directory)}")
        console.print()

    if pending:
        console.print("  Run [bold]smalltalk mine <dir>[/bold] to convert pending files.")
    else:
        console.print("  [green]All convertible files compressed.[/green]")
    console.print()
