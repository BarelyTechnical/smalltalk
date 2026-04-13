from pathlib import Path
from typing import Optional
from smalltalk.converter import convert_file, convert_file_causal, is_convertible, detect_file_type
from smalltalk.init_cmd import collect_md_files
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def run_mine(
    directory: Path,
    api_key: Optional[str],
    model: str,
    base_url: str,
    keep_originals: bool,
    dry_run: bool,
    causal: bool = False,
):
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise SystemExit(1)

    if not api_key:
        console.print("[red]ERROR:[/red] No API key found.")
        console.print("  Set [bold]OPENROUTER_API_KEY[/bold] env var or pass [bold]--api-key[/bold]")
        console.print("  For other providers use [bold]--base-url[/bold] and [bold]--api-key[/bold]")
        console.print()
        console.print("  Examples:")
        console.print("    Anthropic:  --base-url https://api.anthropic.com/v1 --api-key <key>")
        console.print("    OpenAI:     --base-url https://api.openai.com/v1 --api-key <key>")
        console.print("    Ollama:     --base-url http://localhost:11434/v1 --api-key ollama")
        raise SystemExit(1)

    directory = directory.resolve()

    console.print()
    console.print("=" * 60)
    console.print("  Smalltalk — Mine")
    console.print("=" * 60)
    console.print(f"\n  Directory: [bold]{directory}[/bold]")
    console.print(f"  Model:     [bold]{model}[/bold]")
    if causal:
        console.print("  Mode:      [bold magenta]CAUSAL[/bold magenta] — extracting evidence chains and causality")
    if dry_run:
        console.print("  Mode:      [yellow]DRY RUN — no files will be written[/yellow]")
    console.print()

    md_files = collect_md_files(directory)
    to_convert = [
        f for f in md_files
        if is_convertible(f) and not f.with_suffix(".st").exists()
    ]

    if not to_convert:
        console.print("  [green]Nothing to convert.[/green] All files already have .st versions.")
        console.print("  Run [bold]smalltalk status <dir>[/bold] to see current state.")
        console.print()
        return

    console.print(f"  Found [bold]{len(to_convert)}[/bold] files to convert:\n")
    for f in to_convert:
        ftype = detect_file_type(f.read_text(encoding="utf-8", errors="ignore"), f.name)
        console.print(f"  [cyan]{f.relative_to(directory)}[/cyan]  [dim]({ftype})[/dim]")

    console.print()

    if dry_run:
        console.print("  [yellow]Dry run complete. No files written.[/yellow]")
        console.print()
        return

    converted = 0
    failed = 0

    for f in to_convert:
        relative = f.relative_to(directory)
        with Progress(
            SpinnerColumn(),
            TextColumn(f"  Converting [cyan]{relative}[/cyan]..."),
            transient=True,
            console=console,
        ) as progress:
            progress.add_task("converting")
            try:
                if causal:
                    st_content = convert_file_causal(f, api_key, model, base_url)
                else:
                    st_content = convert_file(f, api_key, model, base_url)
                st_path = f.with_suffix(".st")
                st_path.write_text(st_content, encoding="utf-8")
                md_lines = len(f.read_text(encoding="utf-8").splitlines())
                st_lines = len(st_content.splitlines())
                reduction = int((1 - st_lines / md_lines) * 100) if md_lines > 0 else 0
                console.print(
                    f"  [green]✓[/green] {relative}"
                    f"  [dim]{md_lines}→{st_lines} lines ({reduction}% reduction)[/dim]"
                )
                converted += 1
            except Exception as e:
                console.print(f"  [red]✗[/red] {relative}  [red]{e}[/red]")
                failed += 1

    console.print()
    console.print(f"  [bold]{converted}[/bold] files converted")
    if failed:
        console.print(f"  [red]{failed}[/red] files failed — originals untouched")

    if not keep_originals and converted > 0:
        console.print()
        console.print("  [dim]Removing .md originals...[/dim]")
        for f in to_convert:
            if f.with_suffix(".st").exists():
                f.unlink()
                console.print(f"  [dim]removed:[/dim] {f.relative_to(directory)}")

    console.print()
    console.print("  Run [bold]smalltalk status <dir>[/bold] to see full state.")
    console.print()
