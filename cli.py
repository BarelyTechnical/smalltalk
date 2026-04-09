import typer
from pathlib import Path
from typing import Optional
from rich.console import Console

from smalltalk.init_cmd import run_init
from smalltalk.backup import run_backup
from smalltalk.mine import run_mine, run_watch
from smalltalk.status import run_status
from smalltalk.instructions_cmd import run_instructions
from smalltalk.wake_up import build_wake_up_context
from smalltalk.checker import check_contradictions, format_check_results
from smalltalk.diary import diary_write as _diary_write, diary_read as _diary_read, list_agents
from smalltalk.kg import (
    query_entity as _kg_query,
    get_timeline as _kg_timeline,
    invalidate_entry as _kg_invalidate,
    format_entity_query,
    format_timeline,
    format_invalidate_result,
    _today,
)
from smalltalk.kg_viz import visualize as _kg_visualize
from smalltalk.palace_cmd import palace_app
from smalltalk.route import route as _route, format_route_results
from smalltalk.bootstrap_cmd import run_bootstrap
from smalltalk.hook_cmd import run_install_hook

console = Console()

app = typer.Typer(
    name="smalltalk",
    help=(
        "Smalltalk — institutional memory for AI agents.\n\n"
        "The agent doesn't know your history. Smalltalk changes that.\n\n"
        "Quick start:  smalltalk bootstrap <_brain/>\n"
        "Check first:  smalltalk check <_brain/>   ← detects decision contradictions\n"
        "Load context: smalltalk wake-up <_brain/>"
    ),
    add_completion=False,
)

# Sub-apps
kg_app    = typer.Typer(help="Knowledge Graph — query, timeline, and contradiction resolution.")
diary_app = typer.Typer(help="Specialist agent diary commands.")
app.add_typer(kg_app,    name="kg")
app.add_typer(diary_app, name="diary")
app.add_typer(palace_app, name="palace")


# ---------------------------------------------------------------------------
# Bootstrap — one-command full setup
# ---------------------------------------------------------------------------

@app.command()
def bootstrap(
    directory: Path = typer.Argument(..., help="Directory to set up (_brain/ or project root)"),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", "-k",
        envvar="OPENROUTER_API_KEY",
        help="API key for mine step (OpenRouter by default)",
    ),
    model: str = typer.Option(
        "anthropic/claude-haiku-4-5",
        "--model", "-m",
        help="Model to use for .md → .st conversion",
    ),
    base_url: str = typer.Option(
        "https://openrouter.ai/api/v1",
        "--base-url",
        help="OpenAI-compatible API base URL",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Preview steps without making changes",
    ),
):
    """
    One-command setup: backup → mine → palace init → write CLAUDE.md.

    The fastest way to orient a new project. Run once, then use wake-up and check
    at every session start. Mine step is skipped if no API key is provided.
    """
    run_bootstrap(directory, api_key, model, base_url, dry_run)


# ---------------------------------------------------------------------------
# Route — task-to-skill routing
# ---------------------------------------------------------------------------

@app.command()
def route(
    directory: Path = typer.Argument(..., help="Directory containing .st files (skills/, _brain/, etc.)"),
    task: str       = typer.Argument(..., help="Natural language task description"),
    top: int        = typer.Option(5, "--top", "-n", help="Number of results to return"),
):
    """
    Find the most relevant skill/agent files for a task.

    Run at session start before the first message to know which skills to load.
    Scores by file name match and entry content — no LLM required.

    Example:
        smalltalk route skills/ "build a landing page for a plumbing company"
        → skills/seo-expert.st       [score: 6.0]
        → skills/ui-designer.st      [score: 4.5]
        → skills/conversion-copy.st  [score: 3.0]
    """
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)

    results = _route(directory.resolve(), task, top_n=top)
    console.print(format_route_results(results, task))


# ---------------------------------------------------------------------------
# Install-hook — git post-commit auto-mine
# ---------------------------------------------------------------------------

@app.command(name="install-hook")
def install_hook(
    project_dir: Path = typer.Argument(
        ..., help="Root of the git repository (must contain .git/)"
    ),
    force: bool = typer.Option(
        False, "--force", "-f",
        help="Overwrite an existing post-commit hook",
    ),
):
    """
    Install a git post-commit hook that auto-mines staged .md files.

    After each commit, the hook converts any .md files in the commit to .st
    format and stages the results. Requires OPENROUTER_API_KEY in your shell
    environment. Without it the hook exits cleanly — commits are never blocked.

    Uninstall: delete .git/hooks/post-commit
    """
    run_install_hook(project_dir, force)


# ---------------------------------------------------------------------------
# Existing commands
# ---------------------------------------------------------------------------

@app.command()
def init(
    directory: Path = typer.Argument(..., help="Directory to scan"),
):
    """Scan a directory and show what can be compressed."""
    run_init(directory)


@app.command()
def backup(
    directory: Path = typer.Argument(..., help="Directory to back up"),
):
    """Copy all .md originals to .originals/ before conversion."""
    run_backup(directory)


@app.command()
def mine(
    directory: Path = typer.Argument(..., help="Directory to convert"),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", "-k",
        envvar="OPENROUTER_API_KEY",
        help="API key (OpenRouter by default)",
    ),
    model: str = typer.Option(
        "anthropic/claude-haiku-4-5",
        "--model", "-m",
        help="Model to use for conversion",
    ),
    base_url: str = typer.Option(
        "https://openrouter.ai/api/v1",
        "--base-url",
        help="OpenAI-compatible API base URL",
    ),
    keep_originals: bool = typer.Option(
        True,
        "--keep-originals/--no-keep-originals",
        help="Keep .md files after conversion",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Preview what would be converted without converting",
    ),
    watch: bool = typer.Option(
        False, "--watch", "-w",
        help="Watch directory and auto-convert on file change (Ctrl+C to stop)",
    ),
    interval: int = typer.Option(
        3, "--interval",
        help="Watch poll interval in seconds (default 3)",
    ),
):
    """
    Convert detected .md files to Smalltalk .st format.

    Use --watch to auto-convert whenever a .md file is saved.
    Use --dry-run to preview without making changes.
    """
    if watch:
        run_watch(directory, api_key, model, base_url, interval)
    else:
        run_mine(directory, api_key, model, base_url, keep_originals, dry_run)


@app.command()
def status(
    directory: Path = typer.Argument(..., help="Directory to check"),
):
    """Show converted vs unconverted files in a directory."""
    run_status(directory)


@app.command()
def instructions(
    command: str = typer.Argument(
        ...,
        help=(
            "Command name: help, init, mine, backup, status, check, wake-up, "
            "diary, palace, kg, closing-ritual, bootstrap, route"
        ),
    ),
):
    """Print step-by-step instructions for a command. Designed for agents."""
    run_instructions(command)


# ---------------------------------------------------------------------------
# Runtime commands
# ---------------------------------------------------------------------------

@app.command(name="wake-up")
def wake_up(
    directory: Path = typer.Argument(..., help="Directory containing .st files"),
):
    """
    Output compressed L1 context for injection into a local model's system prompt.

    Extracts DECISION, hard RULE, PATTERN, and WIN (repeat:y) entries.
    Pipe to a file:  smalltalk wake-up ~/brain > context.txt
    """
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    console.print(build_wake_up_context(directory.resolve()))


@app.command()
def check(
    directory: Path = typer.Argument(..., help="Directory to check for contradictions"),
):
    """
    Detect contradictions across .st files.

    Flags conflicting DECISION entries, RULE strength mismatches,
    PATTERN conflicting fixes, WIN repeat disagreements, and LINK
    exclusivity violations. Rules-based — no LLM required.

    Run this before any deployment or production push. Agents running
    via MCP can resolve contradictions autonomously using kg invalidate.
    """
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    console.print(format_check_results(check_contradictions(directory.resolve()), directory.resolve()))


# ---------------------------------------------------------------------------
# Diary subcommands
# ---------------------------------------------------------------------------

@diary_app.command("write")
def diary_write_cmd(
    agent_id: str = typer.Argument(..., help="Agent id, e.g. 'reviewer'"),
    entry:    str = typer.Argument(..., help="Smalltalk .st formatted entry line"),
):
    """Write a diary entry for a specialist agent. Stored in ~/.smalltalk/diaries/"""
    try:
        path = _diary_write(agent_id, entry)
        console.print(f"[green]+[/green] Written to {path}")
    except (ValueError, OSError) as exc:
        console.print(f"[red]ERROR:[/red] {exc}")
        raise typer.Exit(1)


@diary_app.command("read")
def diary_read_cmd(
    agent_id: str = typer.Argument(..., help="Agent id, e.g. 'reviewer'"),
    last_n: int = typer.Option(20, "--last", "-n", help="Number of entries to show"),
):
    """Read recent diary entries for a specialist agent."""
    entries = _diary_read(agent_id, last_n)
    if not entries:
        agents = list_agents()
        console.print(f"[yellow]No diary for: {agent_id}[/yellow]")
        console.print(f"Available: {', '.join(agents) if agents else 'none'}")
        return
    console.print(f"\n[bold]Diary: {agent_id}[/bold] (last {len(entries)} entries)\n")
    for e in entries:
        console.print(f"  {e}")
    console.print()


@diary_app.command("list")
def diary_list_cmd():
    """List all specialist agents that have diary files."""
    agents = list_agents()
    if not agents:
        console.print("[yellow]No agent diaries found.[/yellow]")
        console.print('Start one: smalltalk diary write <id> "<entry>"')
        return
    console.print(f"\n[bold]Diary agents ({len(agents)}):[/bold]\n")
    for a in agents:
        console.print(f"  {a}")
    console.print()


# ---------------------------------------------------------------------------
# KG subcommands
# ---------------------------------------------------------------------------

@kg_app.command("query")
def kg_query_cmd(
    directory: Path = typer.Argument(..., help="Directory containing .st files"),
    entity:    str  = typer.Argument(..., help="Entity to query, e.g. 'kai' or 'auth'"),
    as_of:     str  = typer.Option("", "--as-of", help="YYYY-MM — point-in-time query"),
):
    """Query the knowledge graph for an entity — relationships, active and historical."""
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    result = _kg_query(directory.resolve(), entity, as_of or None)
    console.print(format_entity_query(result))


@kg_app.command("timeline")
def kg_timeline_cmd(
    directory: Path = typer.Argument(..., help="Directory containing .st files"),
    entity:    str  = typer.Argument(..., help="Entity to trace chronologically"),
):
    """Show the chronological story of an entity via LINK entries."""
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    events = _kg_timeline(directory.resolve(), entity)
    console.print(format_timeline(events, entity))


@kg_app.command("invalidate")
def kg_invalidate_cmd(
    file_path: Path = typer.Argument(..., help="Path to the .st file"),
    line_no:   int  = typer.Argument(..., help="Line number of the entry to close (1-indexed)"),
    ended:     str  = typer.Option("", "--ended", "-e",
                                   help="YYYY-MM date to set as ended (defaults to current month)"),
):
    """
    Close an active .st entry — writes ended:YYYY-MM onto the specified line.

    This is the resolution step after `smalltalk check` flags a contradiction.

    Workflow:
      1. smalltalk check <dir>              # see contradictions + file/line
      2. smalltalk kg invalidate <file> <line_no>   # close the older entry
      3. smalltalk check <dir>              # confirm cleared
    """
    if not file_path.exists():
        console.print(f"[red]ERROR:[/red] File not found: {file_path}")
        raise typer.Exit(1)
    try:
        result = _kg_invalidate(
            file_path=str(file_path),
            line_no=line_no,
            ended=ended or None,
        )
        console.print(f"[green]+[/green] {format_invalidate_result(result)}")
    except (ValueError, OSError) as exc:
        console.print(f"[red]ERROR:[/red] {exc}")
        raise typer.Exit(1)


@kg_app.command("visualize")
def kg_visualize_cmd(
    directory:  Path = typer.Argument(..., help="Directory containing .st files"),
    out:        Path = typer.Option(None, "--out", "-o", help="Save HTML to this path"),
    no_browser: bool = typer.Option(False, "--no-browser", help="Don't open browser"),
):
    """
    Open an interactive Knowledge Graph visualization in the browser.

    Shows entities as nodes (colour-coded by stability), relationships as edges
    (colour-coded by rel: type), historical entries as faded/dashed, and
    conflict/warning nodes highlighted in red/amber.

    Requires internet access to load vis.js from CDN (unpkg.com).
    """
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    try:
        path = _kg_visualize(
            directory    = directory.resolve(),
            out          = out,
            open_browser = not no_browser,
        )
        console.print(f"[green]+[/green] Graph generated: {path}")
        if no_browser:
            console.print("  Open the file in any browser to view.")
    except Exception as exc:
        console.print(f"[red]ERROR:[/red] {exc}")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------


def main():
    app()


if __name__ == "__main__":
    main()
