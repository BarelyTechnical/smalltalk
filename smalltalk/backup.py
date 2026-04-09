from pathlib import Path
import shutil
from smalltalk.init_cmd import collect_md_files
from rich.console import Console

console = Console()


def run_backup(directory: Path):
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise SystemExit(1)

    directory = directory.resolve()
    backup_root = directory / ".originals"

    console.print()
    console.print("=" * 60)
    console.print("  Smalltalk — Backup")
    console.print("=" * 60)
    console.print(f"\n  Source:  [bold]{directory}[/bold]")
    console.print(f"  Backup:  [bold]{backup_root}[/bold]\n")

    md_files = collect_md_files(directory)
    backed_up = 0
    skipped = 0

    for f in md_files:
        relative = f.relative_to(directory)
        dest = backup_root / relative
        dest.parent.mkdir(parents=True, exist_ok=True)

        if dest.exists():
            console.print(f"  [dim]already backed up:[/dim] {relative}")
            skipped += 1
        else:
            shutil.copy2(f, dest)
            console.print(f"  [green]backed up:[/green] {relative}")
            backed_up += 1

    console.print()
    console.print(f"  [bold]{backed_up}[/bold] files backed up to [bold].originals/[/bold]")
    if skipped:
        console.print(f"  [bold]{skipped}[/bold] already in backup — skipped")
    console.print()
    console.print("  Originals are safe. Run [bold]smalltalk mine <dir>[/bold] to convert.")
    console.print()
