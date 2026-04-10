"""
Bootstrap command — one-command Smalltalk project setup.

Runs: backup → mine → palace init → generates CLAUDE.md snippet + MCP command.
Turns a directory of .md files into a fully oriented Smalltalk palace in one step.
"""
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

from smalltalk.backup import run_backup
from smalltalk.mine import run_mine
from smalltalk.palace import init_palace, palace_status_text

console = Console()

_SKIP_FILES = {
    "README.md", "readme.md", "CHANGELOG.md", "CONTRIBUTING.md",
    "LICENSE.md", "stack.md", "CONTEXT.md", "context.md",
}

_CLAUDE_MD_SNIPPET = """\
# Smalltalk — session orientation

## Session Start (always)
1. Run `smalltalk_wake_up` on `_brain/` — load current decisions, rules, patterns
2. Run `smalltalk_diary_read` for this session's agent id — load accumulated expertise
3. Note the active entries. Do not ask for context that is already loaded.

## During Work
- Use `smalltalk_navigate` to find relevant files before `smalltalk_search`
- Use `smalltalk_kg_query` to understand entity relationships
- Use `smalltalk_check` before any deployment or production push

## Session End (required — hard rule)
Run the closing ritual:
1. Identify decisions made, patterns found, wins, errors
2. Write each as a Smalltalk entry via `smalltalk_diary_write`
3. Run `smalltalk_check` on `_brain/`
4. Resolve any contradictions found

Full protocol: `smalltalk instructions closing-ritual`

RULE: session-end | write-decisions-patterns-wins-to-brain | hard
TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write
"""

_CURSOR_SNIPPET = """\
# Smalltalk orientation
Read .st files before .md files. .st is Smalltalk compressed format — load as session context.
At session start: call smalltalk_wake_up on _brain/ and smalltalk_diary_read for active agent.
At session end: run smalltalk instructions closing-ritual and follow it exactly.
Use smalltalk_navigate for domain queries. Use smalltalk_check before any deploy.
"""


def run_bootstrap(
    directory: Path,
    api_key: Optional[str] = None,
    model: str = "anthropic/claude-haiku-4-5",
    base_url: str = "https://openrouter.ai/api/v1",
    dry_run: bool = False,
) -> None:
    directory = directory.resolve()

    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise SystemExit(1)

    console.print(Rule(f"[bold cyan]Smalltalk Bootstrap — {directory.name}[/bold cyan]"))
    console.print()

    # ── Step 1: Backup ────────────────────────────────────────────────────────
    console.print("[bold]Step 1/4[/bold] Backing up originals...")
    if not dry_run:
        run_backup(directory)
    else:
        console.print("  [dim]dry-run: skipping backup[/dim]")
    console.print()

    # ── Step 2: Mine ──────────────────────────────────────────────────────────
    console.print("[bold]Step 2/4[/bold] Converting .md files to .st format...")
    if not dry_run:
        if not api_key:
            console.print(
                "  [yellow]No API key provided.[/yellow] "
                "Set OPENROUTER_API_KEY or pass --api-key.\n"
                "  [dim]Skipping mine. Run: smalltalk mine <dir>[/dim]"
            )
        else:
            run_mine(directory, api_key, model, base_url, keep_originals=True, dry_run=False)
    else:
        console.print("  [dim]dry-run: skipping mine[/dim]")
    console.print()

    # ── Step 3: Palace init ───────────────────────────────────────────────────
    console.print("[bold]Step 3/4[/bold] Generating palace index...")
    if not dry_run:
        try:
            index_path = init_palace(directory)
            console.print(f"  [green]+[/green] Index: {index_path}")
            console.print()
            console.print(palace_status_text(directory))
        except Exception as exc:
            console.print(f"  [yellow]Palace init skipped:[/yellow] {exc}")
    else:
        console.print("  [dim]dry-run: skipping palace init[/dim]")
    console.print()

    # ── Step 4: Generate config snippets ─────────────────────────────────────
    console.print("[bold]Step 4/4[/bold] Generating integration snippets...")
    console.print()

    _write_snippet(directory / "CLAUDE.md", _CLAUDE_MD_SNIPPET, "CLAUDE.md", dry_run)
    console.print()

    # ── Summary ──────────────────────────────────────────────────────────────
    console.print(Rule("[bold green]Bootstrap complete[/bold green]"))
    console.print()

    console.print(Panel(
        f"[bold]MCP registration (Claude Code):[/bold]\n\n"
        f"  claude mcp add smalltalk -- \"python -m smalltalk.mcp_server\"\n\n"
        f"[bold]Cursor integration:[/bold]\n\n"
        f"  Add to .cursorrules:\n"
        f"  {_CURSOR_SNIPPET.splitlines()[0]}\n\n"
        f"[bold]Verify setup:[/bold]\n\n"
        f"  smalltalk status {directory}\n"
        f"  smalltalk wake-up {directory}\n"
        f"  smalltalk check {directory}",
        title="Next steps",
        border_style="cyan",
    ))


def _write_snippet(path: Path, content: str, label: str, dry_run: bool) -> None:
    if dry_run:
        console.print(f"  [dim]dry-run: would write {label}[/dim]")
        return
    if path.exists():
        console.print(f"  [yellow]Skipped:[/yellow] {label} already exists at {path}")
        console.print(f"  Add manually:\n")
        for line in content.strip().splitlines()[:6]:
            console.print(f"    {line}")
        console.print(f"    ...")
    else:
        path.write_text(content, encoding="utf-8")
        console.print(f"  [green]+[/green] Written: {path}")
