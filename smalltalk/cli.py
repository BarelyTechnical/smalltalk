import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from smalltalk.init_cmd import run_init
from smalltalk.backup import run_backup
from smalltalk.mine import run_mine
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
from smalltalk.bootstrap_cmd import run_bootstrap
from smalltalk.watch_cmd import run_mine_watch
from smalltalk.hook_cmd import run_install_hook
from smalltalk.router import route as _route, format_route_results

console = Console()

app = typer.Typer(
    name="smalltalk",
    help=(
        "Smalltalk — institutional memory for AI agents.\n\n"
        "The agent doesn't know your history. Smalltalk changes that.\n\n"
        "Start here:   smalltalk bootstrap <dir>\n"
        "Check first:  smalltalk check <dir>   ← catches contradictions before agents act\n"
        "Load context: smalltalk wake-up <dir>"
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
        help="Watch for new/modified .md files and auto-convert (Ctrl+C to stop)",
    ),
    interval: int = typer.Option(
        3, "--interval",
        help="Watch mode polling interval in seconds (default: 3)",
    ),
):
    """Convert .md files to .st format. Add --watch to auto-convert on file change."""
    if watch:
        run_mine_watch(directory, api_key, model, base_url, keep_originals, interval)
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
        help="Command name: help, init, mine, backup, status, check, wake-up, diary, palace, kg, closing-ritual, bootstrap, route",
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
    Detect contradictions across .st files. Run this before any agent acts.

    When an agent reads conflicting facts — two active DECISION entries pointing
    to different deploy targets, a RULE flagged hard in one file and soft in
    another — it picks one arbitrarily. Smalltalk catches this before it acts.

    Detects:
        DECISION  — same subject, diverging active choices
        RULE      — same id, hard in one file / soft in another
        PATTERN   — same cause, conflicting fixes
        WIN       — same subject, repeat:y vs repeat:n
        LINK      — exclusive relationships pointing to multiple active targets

    Rules-based — no LLM required.

    Resolution cycle:
        1. smalltalk check <dir>             ← see contradictions + file/line
        2. smalltalk kg invalidate <f> <n>   ← close the older entry
        3. smalltalk check <dir>             ← confirm cleared
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
    """
    Query the knowledge graph for an entity — relationships, active and historical.
    """
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
    """
    Show the chronological story of an entity via LINK entries.
    """
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
# New commands: bootstrap, install-hook, route
# ---------------------------------------------------------------------------

@app.command()
def bootstrap(
    directory: Path = typer.Argument(..., help="Directory to bootstrap (skills, _brain, agents)"),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", "-k",
        envvar="OPENROUTER_API_KEY",
        help="API key for mine step (optional — skips mine if not provided)",
    ),
    model: str = typer.Option(
        "anthropic/claude-haiku-4-5", "--model", "-m",
        help="Model for conversion",
    ),
    base_url: str = typer.Option(
        "https://openrouter.ai/api/v1", "--base-url",
        help="OpenAI-compatible API base URL",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Preview without making changes",
    ),
):
    """
    One-command setup: backup → mine → palace init → generate CLAUDE.md.

    Gets a directory fully oriented in one step.
    Equivalent to running init, backup, mine, palace init, and config generation manually.
    """
    run_bootstrap(directory, api_key, model, base_url, dry_run)


@app.command(name="install-hook")
def install_hook(
    directory: Path = typer.Argument(
        ".",
        help="Directory inside the git repo (default: current directory)",
    ),
    force: bool = typer.Option(
        False, "--force",
        help="Overwrite existing hook files",
    ),
):
    """
    Install a git post-commit hook that auto-converts staged .md files to .st.

    Finds the nearest .git directory from <directory> and installs the hook.
    After each commit, any staged .md files are mined automatically.
    """
    run_install_hook(directory, force)


@app.command()
def route(
    directory: Path = typer.Argument(..., help="Directory containing .st files"),
    task: str = typer.Argument(..., help="Task description to route, e.g. 'build a landing page'"),
    top: int = typer.Option(5, "--top", "-n", help="Number of files to return"),
):
    """
    Route a task description to the most relevant .st skill/agent files.

    Scores files using both structural (file/dir name) and content-based
    (SKILL trigger fields, USE when: fields, AGENT capabilities) matching.

    Use this at session start to know which files to load for a given task.
    """
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    results = _route(directory.resolve(), task, top_n=top)
    console.print(format_route_results(results, task, directory.resolve()))


# ---------------------------------------------------------------------------


def main():
    app()


if __name__ == "__main__":
    main()
