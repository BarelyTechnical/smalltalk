import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from smalltalk.wizard_cmd import run_wizard
from smalltalk.scan_cmd import run_scan
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
from smalltalk.backend_cmd import run_detect_backends
from smalltalk.session_cmd import run_reinforce, run_session_end
from smalltalk.eval_cmd import EvalCase, run_eval, run_eval_batch, format_eval_result
from smalltalk.orchestrator import run_orchestrate, resolve_model, TASK_TYPES

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
def init():
    """Interactive zero-to-hero setup wizard for Smalltalk."""
    run_wizard()

@app.command()
def scan(
    directory: Path = typer.Argument(..., help="Directory to scan"),
):
    """Scan a directory and show what can be compressed."""
    run_scan(directory)


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
    causal: bool = typer.Option(
        False, "--causal",
        help="Extract evidence chains and causality (for articles, threads, guides)",
    ),
):
    """Convert .md files to .st format. Add --watch to auto-convert on file change.

    Use --causal to extract evidence chains and causality (for articles, threads, guides).
    Causal mode encodes the WHY behind rules, not just the rule itself.
    """
    if watch:
        run_mine_watch(directory, api_key, model, base_url, keep_originals, interval)
    else:
        run_mine(directory, api_key, model, base_url, keep_originals, dry_run, causal)


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


@app.command("install-hook")
def install_hook_cmd(
    brain_dir: Path = typer.Argument(..., help="Path to the brain directory"),
    repo_path: Path = typer.Option(".", "--repo", help="Path to the git repository"),
):
    """
    Install a passive post-commit Git hook that extracts knowledge automatically.
    """
    try:
        from smalltalk.git_hook import install_post_commit_hook
        msg = install_post_commit_hook(brain_dir, repo_path)
        console.print(f"[green]SUCCESS:[/green] {msg}")
    except Exception as exc:
        console.print(f"[red]ERROR:[/red] {exc}")
        raise typer.Exit(1)


@app.command("git-analyze", hidden=True)
def git_analyze_cmd(
    brain_dir: Path = typer.Argument(...),
    repo_path: Path = typer.Argument(...),
):
    """Hidden command invoked by the post-commit hook."""
    try:
        from smalltalk.git_hook import analyze_last_commit
        analyze_last_commit(brain_dir, repo_path)
    except Exception:
        pass


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
    (SKILL trigger fields, USE when: fields, AGENT capabilities, HABIT triggers) matching.

    Use this at session start to know which files to load for a given task.
    """
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    results = _route(directory.resolve(), task, top_n=top)
    console.print(format_route_results(results, task, directory.resolve()))


# ---------------------------------------------------------------------------
# New commands: detect-backends, reinforce, session-end, eval, eval-batch
# ---------------------------------------------------------------------------

@app.command(name="detect-backends")
def detect_backends(
    brain: Optional[Path] = typer.Option(
        None, "--brain", "-b",
        help="Brain directory to write BACKEND entries into (optional)",
    ),
):
    """
    Detect running local inference backends (Ollama, llama.cpp, ik-llama, bitnet).

    Checks ports 11434, 8080, 8081, 8082. Warns if only Ollama found (context cap).
    Use --brain <dir> to write BACKEND .st entries to your brain directory.
    """
    run_detect_backends(brain_dir=brain)


@app.command()
def reinforce(
    directory: Path = typer.Argument(..., help="Brain directory containing .st files"),
    agent: str = typer.Option("default", "--agent", "-a", help="Agent ID"),
    every: int = typer.Option(5, "--every", "-n", help="Reinforce every N responses"),
    force: bool = typer.Option(False, "--force", "-f", help="Force reinforce regardless of counter"),
):
    """
    Emit a compact brain-context reminder block to prevent mid-session drift.

    The 0.95^N problem: every response that drifts slightly from your encoded
    decisions compounds. After 14 responses at 5% drift each, cumulative alignment
    is below 50%. This command re-injects your brain context every N responses.

    Returns empty string if reinforcement not due yet (safe to call every response).
    Wire into CLAUDE.md:
        TRIGGER: every-response | event:response-complete | then:smalltalk_reinforce
    """
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    block = run_reinforce(directory.resolve(), agent_id=agent, reinforce_every=every, force=force)
    if block:
        console.print(block)
    else:
        console.print("[dim]No reinforcement due yet. (Safe no-op.)[/dim]")


@app.command(name="session-end")
def session_end(
    directory: Path = typer.Argument(..., help="Brain directory"),
    summary: str = typer.Option(
        "", "--summary", "-s",
        help="Session summary text (what was done, decisions made, patterns found)",
    ),
    summary_file: Optional[Path] = typer.Option(
        None, "--file", "-f",
        help="Read session summary from file instead of --summary",
    ),
    agent: str = typer.Option("default", "--agent", "-a", help="Agent ID for diary writes"),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", "-k",
        envvar="OPENROUTER_API_KEY",
        help="API key for LLM extraction (optional — manual mode if not provided)",
    ),
    model: str = typer.Option("anthropic/claude-haiku-4-5", "--model", "-m", help="Extraction model"),
    base_url: str = typer.Option("https://openrouter.ai/api/v1", "--base-url"),
):
    """
    Automated closing ritual — extracts DECISION/PATTERN/WIN/ERROR from session.

    Provide a session summary (what you did, what was decided, what broke).
    The LLM extracts structured .st entries, writes them to the brain, and
    runs a contradiction check. Closes the session state tracker.

    Example:
        smalltalk session-end _brain/ -s "Built auth with clerk, chose over auth0.
        JWT refresh was breaking due to missing exp claim. SEO cluster approach worked."
    """
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)

    if summary_file:
        if not summary_file.exists():
            console.print(f"[red]ERROR:[/red] Summary file not found: {summary_file}")
            raise typer.Exit(1)
        text = summary_file.read_text(encoding="utf-8")
    elif summary:
        text = summary
    else:
        console.print("[yellow]No summary provided.[/yellow] Running without LLM extraction.")
        text = ""

    run_session_end(
        brain_dir=directory.resolve(),
        session_summary=text,
        agent_id=agent,
        api_key=api_key,
        model=model,
        base_url=base_url,
    )


@app.command()
def eval(
    directory: Path = typer.Argument(..., help="Brain directory"),
    task: str = typer.Option(..., "--task", "-t", help="What the agent was asked to do"),
    expected: str = typer.Option(..., "--expected", "-e", help="Expected behaviour"),
    actual: str = typer.Option(..., "--actual", "-a", help="What the agent actually did"),
    agent: str = typer.Option("default", "--agent", help="Agent ID"),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", "-k",
        envvar="OPENROUTER_API_KEY",
        help="API key for drift detection LLM call",
    ),
    model: str = typer.Option("anthropic/claude-haiku-4-5", "--model", "-m"),
    base_url: str = typer.Option("https://openrouter.ai/api/v1", "--base-url"),
):
    """
    Evaluate an agent response for drift from its brain.

    Compares what the agent did against its active DECISION/RULE/PATTERN/HABIT entries.
    If drift detected: writes PATTERN+RULE entries immediately, returns reinforce block.

    Use this after important responses to catch drift before it compounds.
    The 0.95^14 problem: after 14 responses at 5% drift each, alignment drops below 50%.
    """
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    if not api_key:
        console.print("[red]ERROR:[/red] --api-key required for eval.")
        raise typer.Exit(1)

    case   = EvalCase(task=task, expected=expected, actual=actual,
                      brain_dir=str(directory.resolve()), agent_id=agent)
    result = run_eval(case, api_key=api_key, model=model, base_url=base_url)
    console.print(format_eval_result(result))
    if result.reinforce_block:
        console.print(result.reinforce_block)


@app.command(name="eval-batch")
def eval_batch(
    directory: Path = typer.Argument(..., help="Brain directory"),
    cases: Path = typer.Option(..., "--cases", "-c", help="JSONL file of eval cases"),
    agent: str = typer.Option("default", "--agent"),
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", envvar="OPENROUTER_API_KEY"),
    model: str = typer.Option("anthropic/claude-haiku-4-5", "--model", "-m"),
    base_url: str = typer.Option("https://openrouter.ai/api/v1", "--base-url"),
):
    """
    Run eval on a batch of JSONL cases.

    Each line: {"task": "...", "expected": "...", "actual": "..."}
    """
    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise typer.Exit(1)
    if not api_key:
        console.print("[red]ERROR:[/red] --api-key required.")
        raise typer.Exit(1)
    run_eval_batch(cases, directory.resolve(), agent_id=agent,
                   api_key=api_key, model=model, base_url=base_url)


# ---------------------------------------------------------------------------
# orchestrate — external LLM task orchestration
# ---------------------------------------------------------------------------

@app.command(name="orchestrate")
def orchestrate(
    brain: Path = typer.Argument(
        ...,
        help="Brain directory containing .st files",
        exists=False,
    ),
    task: str = typer.Argument(
        ...,
        help="The task to execute (quoted string)",
    ),
    task_type: str = typer.Option(
        "code",
        "--task-type", "-t",
        help=f"Task type for MODELMAP routing: {', '.join(sorted(TASK_TYPES))}",
    ),
    api_key: str = typer.Option(
        "",
        "--api-key", "-k",
        help="API key (or set OPENROUTER_API_KEY env)",
        envvar="OPENROUTER_API_KEY",
    ),
    model: str = typer.Option(
        "",
        "--model", "-m",
        help="Override model from MODELMAP (e.g. qwen2.5-coder:14b)",
    ),
    base_url: str = typer.Option(
        "",
        "--base-url",
        help="Override backend URL (default: auto-resolved from BACKEND entries)",
    ),
    ctx_limit: int = typer.Option(
        0,
        "--ctx",
        help="Override context window size in tokens (default: from BACKEND entries)",
    ),
    agent: str = typer.Option(
        "default",
        "--agent",
        help="Agent ID for diary entries",
    ),
    resume: bool = typer.Option(
        False,
        "--resume",
        help="Resume an interrupted orchestration run",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet", "-q",
        help="Suppress verbose step output",
    ),
):
    """
    Run a multi-step task using the Smalltalk Orchestrator.

    The orchestrator wraps the LLM externally — managing token budgets,
    task decomposition, and context handoffs so the model always operates
    within its context window.

    \\b
    How it works:
      1. Reads MODELMAP from brain -> selects model + backend for task type
      2. Calls LLM once to decompose task into atomic steps
      3. Loops through each step with token budget management
      4. Triggers context handoffs when budget approaches limit
      5. Writes DECISION/PATTERN entries to brain throughout

    \\b
    Examples:
      smalltalk orchestrate _brain/ "build a login system" --task-type code
      smalltalk orchestrate _brain/ "write onboarding email sequence" --task-type write
      smalltalk orchestrate _brain/ "audit the API security" --task-type analyse
      smalltalk orchestrate _brain/ "build login" --model llama3.2:3b --ctx 4096
      smalltalk orchestrate _brain/ "continue build" --resume

    \\b
    Model selection (reads from brain/modelmap.st):
      code     -> qwen2.5-coder:14b (or what MODELMAP says)
      plan     -> llama3.3:70b
      write    -> llama3.2:3b
      analyse  -> mistral:7b
      chat     -> llama3.2:3b

    \\b
    No MODELMAP entries? Defaults to Ollama on localhost:11434.
    """
    # Resolve and display model info before running
    _model, _url, _ctx = resolve_model(brain.resolve(), task_type)
    effective_model = model or _model
    effective_url   = base_url or _url
    effective_ctx   = ctx_limit or _ctx

    if not quiet:
        console.print()
        console.print(f"  Model:   [bold]{effective_model}[/bold]")
        console.print(f"  Backend: [dim]{effective_url}[/dim]")
        console.print(f"  Context: {effective_ctx:,} tokens")
        console.print()

    try:
        results = run_orchestrate(
            brain_dir  = brain.resolve(),
            task       = task,
            task_type  = task_type,
            api_key    = api_key,
            model      = effective_model,
            base_url   = effective_url,
            ctx_limit  = effective_ctx,
            agent_id   = agent,
            verbose    = not quiet,
            resume     = resume,
        )
    except Exception as exc:
        console.print(f"[red]ERROR:[/red] {exc}")
        raise typer.Exit(1)

    # Summary
    ok      = sum(1 for r in results if r.ok)
    failed  = len(results) - ok
    handoffs= sum(1 for r in results if r.handoff_triggered)

    console.print()
    console.print("  [bold green]Orchestration complete[/bold green]")
    console.print(f"  Steps completed: {ok}/{len(results)}")
    if failed:
        console.print(f"  [yellow]Steps failed:    {failed}[/yellow]")
    if handoffs:
        console.print(f"  Context handoffs: {handoffs}")
    console.print()


# ---------------------------------------------------------------------------
# serve — REST API server
# ---------------------------------------------------------------------------

@app.command(name="serve")
def serve(
    brain: Path = typer.Argument(
        ...,
        help="Brain directory containing .st files",
        exists=False,
    ),
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        help="Bind host (use 0.0.0.0 for network access)",
    ),
    port: int = typer.Option(
        8765,
        "--port", "-p",
        help="Bind port (default: 8765)",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet", "-q",
        help="Suppress startup banner",
    ),
):
    """
    Start the Smalltalk REST API server.

    Exposes all Smalltalk capabilities as HTTP endpoints — usable from
    n8n, EvoNexus, web apps, Node.js, shell scripts, or any language.

    \\b
    Examples:
      smalltalk serve _brain/
      smalltalk serve _brain/ --port 9000
      smalltalk serve _brain/ --host 0.0.0.0   # accessible on network

    \\b
    Key endpoints:
      GET  /health         — liveness check
      GET  /wake-up        — brain context for session start
      GET  /check          — contradiction check (no LLM)
      POST /reinforce      — drift prevention block (call every response)
      POST /session-end    — automated closing ritual
      POST /eval           — per-response drift detection
      POST /diary/write    — write to agent diary
      GET  /diary/read     — read agent diary
      GET  /navigate       — navigate brain by domain query
      GET  /search         — keyword search across .st files
      GET  /status         — entry counts and type breakdown

    \\b
    Wire into EvoNexus CLAUDE.md:
      TRIGGER: every-response | then:POST http://localhost:8765/reinforce
    """
    from smalltalk.server import run_server
    run_server(brain.resolve(), host=host, port=port, quiet=quiet)


# ---------------------------------------------------------------------------


def main():
    app()


if __name__ == "__main__":
    main()
