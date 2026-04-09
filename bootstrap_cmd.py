"""
Bootstrap — one-command full setup for a new _brain/ or skills/ directory.

Sequence:
  1. backup   — copy .md originals to .originals/
  2. mine     — convert .md to .st (skipped if no api_key)
  3. palace init — generate _index.st
  4. write CLAUDE.md — global session hook to project root

The CLAUDE.md is written to the project root:
  - If directory is named _brain, brain, or skills → parent is the project root.
  - Otherwise → the directory itself is treated as the project root.
"""
from pathlib import Path
from typing import Optional

from rich.console import Console

from smalltalk.backup import run_backup
from smalltalk.mine import run_mine
from smalltalk.palace import init_palace

console = Console()

# Embedded CLAUDE.md template — mirrors examples/hooks/CLAUDE.md
_CLAUDE_MD_TEMPLATE = """\
# Smalltalk — Global Session Protocol

## Session Start (always — every session, every project)

1. Check if the project has a `_brain/` or `_index.st` — if yes:
   - Run `smalltalk_wake_up` on `_brain/` — load DECISION, RULE, PATTERN, WIN context
   - Run `smalltalk_diary_read` for the active agent id — load accumulated expertise
2. Check if a task has been given — if yes:
   - Run `smalltalk_route` on the skills directory for the task description
   - Load the top-scored skill files via `smalltalk_read_file`
3. Note what was loaded. Do not re-ask for context that is already in scope.

## During Work

- Use `smalltalk_navigate` to find relevant files before `smalltalk_search`
- Use `smalltalk_route` when selecting which skill or agent to activate
- Use `smalltalk_kg_query` to understand entity relationships
- Use `smalltalk_check` before any deployment or production push

## Session End (hard rule — not optional)

RULE: session-end | write-decisions-patterns-wins-to-brain | hard
TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write

Run the closing ritual before the session ends:
1. Identify decisions made, patterns found, wins, errors this session
2. Write each as a Smalltalk entry via `smalltalk_diary_write(agent_id, entry)`
3. Run `smalltalk_check` on `_brain/`
4. Resolve any contradictions found via `smalltalk_kg_invalidate`

Entry formats:
    DECISION: <subject> | <choice>><rejected> | <reason> | <YYYY-MM>
    PATTERN:  <subject> | broke:<what> | cause:<why> | fix:<what> | reuse:y/n
    WIN:      <subject> | <technique> | <outcome> | repeat:y/n
    ERROR:    <subject> | broke:<what> | cause:<why> | state:recovered|unresolved

Full protocol: `smalltalk instructions closing-ritual`

## If a project has no Smalltalk setup yet

Run: `smalltalk_bootstrap_info()` — returns exact setup commands.
Or:  `smalltalk bootstrap <dir>` — one-command full setup.

## Grammar reference

Run: `smalltalk_get_spec()` for the full type reference.
Run: `smalltalk instructions <command>` for step-by-step guides.
"""


def run_bootstrap(
    directory: Path,
    api_key: Optional[str],
    model: str,
    base_url: str,
    dry_run: bool,
) -> None:
    directory = directory.resolve()

    console.print()
    console.print("=" * 60)
    console.print("  Smalltalk — Bootstrap")
    console.print("=" * 60)
    console.print(f"\n  Directory: [bold]{directory}[/bold]")
    if dry_run:
        console.print("  Mode:      [yellow]DRY RUN — no files will be written[/yellow]")
    console.print()

    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise SystemExit(1)

    # ── Step 1: Backup ────────────────────────────────────────────
    console.print("[bold]Step 1/4 — Backup originals[/bold]")
    if dry_run:
        console.print("  [dim]Would copy .md files to .originals/[/dim]")
    else:
        run_backup(directory)
    console.print()

    # ── Step 2: Mine ─────────────────────────────────────────────
    console.print("[bold]Step 2/4 — Convert .md → .st[/bold]")
    if not api_key:
        console.print("  [yellow]No API key — skipping mine step.[/yellow]")
        console.print("  Run after: smalltalk mine <dir> --api-key <key>")
    elif dry_run:
        console.print("  [dim]Would convert .md files via LLM[/dim]")
    else:
        run_mine(directory, api_key, model, base_url, keep_originals=True, dry_run=False)
    console.print()

    # ── Step 3: Palace init ───────────────────────────────────────
    console.print("[bold]Step 3/4 — Palace init[/bold]")
    if dry_run:
        console.print("  [dim]Would generate _index.st[/dim]")
    else:
        try:
            index_path = init_palace(directory)
            console.print(f"  [green]✓[/green] Index: {index_path}")
        except Exception as exc:
            console.print(f"  [yellow]⚠[/yellow] Palace init failed: {exc}")
    console.print()

    # ── Step 4: Write CLAUDE.md ───────────────────────────────────
    console.print("[bold]Step 4/4 — Write CLAUDE.md[/bold]")

    # Project root = parent of _brain/brain/skills, else directory itself
    project_root = (
        directory.parent
        if directory.name.lower() in ("_brain", "brain", "skills", "_skills")
        else directory
    )
    claude_path = project_root / "CLAUDE.md"

    if dry_run:
        console.print(f"  [dim]Would write: {claude_path}[/dim]")
    elif claude_path.exists():
        console.print(f"  [yellow]⚠[/yellow] CLAUDE.md already exists — not overwritten.")
        console.print(f"       Path: {claude_path}")
        console.print("       Delete it first or merge manually.")
    else:
        claude_path.write_text(_CLAUDE_MD_TEMPLATE, encoding="utf-8")
        console.print(f"  [green]✓[/green] Written: {claude_path}")

    console.print()

    # ── Summary ───────────────────────────────────────────────────
    console.print("=" * 60)
    if dry_run:
        console.print("  [yellow]Dry run complete — no files written.[/yellow]")
    else:
        console.print("  [green]Bootstrap complete.[/green]")
    console.print()
    console.print("  Next steps:")
    console.print("  1. Copy CLAUDE.md to ~/.claude/CLAUDE.md (global orientation):")
    console.print("       macOS/Linux: cp CLAUDE.md ~/.claude/CLAUDE.md")
    console.print("       Windows:     Copy-Item CLAUDE.md $env:USERPROFILE\\.claude\\CLAUDE.md")
    console.print("  2. Register MCP server:")
    console.print('       claude mcp add smalltalk -- "python -m smalltalk.mcp_server"')
    console.print("  3. Open your AI tool and ask: 'Load session context'")
    console.print()
