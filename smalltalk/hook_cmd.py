"""
Git hook installer for Smalltalk.

Installs a post-commit hook that automatically mines any .md files
staged in the commit. Works cross-platform via Python (no bash required).
"""
import os
import stat
from pathlib import Path

from rich.console import Console

console = Console()

_HOOK_SCRIPT = """\
#!/usr/bin/env python3
\"\"\"
Smalltalk post-commit hook.
Auto-converts any staged .md files to .st format after each commit.
Installed by: smalltalk install-hook <dir>
\"\"\"
import subprocess
import sys
from pathlib import Path

# Files that should never be compressed
SKIP_FILES = {
    "README.md", "CHANGELOG.md", "CONTRIBUTING.md", "LICENSE.md",
    "stack.md", "CONTEXT.md", "CLAUDE.md", "GEMINI.md", "AGENTS.md",
}

def main():
    # Get list of files changed in the last commit
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "-r", "--name-only", "HEAD"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        sys.exit(0)

    changed = [Path(f) for f in result.stdout.strip().splitlines()]
    md_files = [
        f for f in changed
        if f.suffix == ".md"
        and f.name not in SKIP_FILES
        and f.exists()
    ]

    if not md_files:
        sys.exit(0)

    print(f"[smalltalk] {len(md_files)} .md file(s) staged — converting to .st...")
    for md_file in md_files:
        st_file = md_file.with_suffix(".st")
        if st_file.exists():
            # Already has a .st — check if .md is newer
            if md_file.stat().st_mtime <= st_file.stat().st_mtime:
                print(f"  skip: {md_file.name} (no change)")
                continue

        result = subprocess.run(
            ["smalltalk", "mine", str(md_file.parent), "--keep-originals"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"  + {md_file.name} → {st_file.name}")
        else:
            print(f"  ! {md_file.name}: {result.stderr.strip()}")

    # Stage the generated .st files
    st_files = [str(f.with_suffix(".st")) for f in md_files if f.with_suffix(".st").exists()]
    if st_files:
        subprocess.run(["git", "add"] + st_files, capture_output=True)
        print(f"[smalltalk] Staged {len(st_files)} .st file(s)")

    sys.exit(0)

if __name__ == "__main__":
    main()
"""

_HOOK_SCRIPT_BASH = """\
#!/bin/sh
# Smalltalk post-commit hook (bash fallback)
# Installed by: smalltalk install-hook <dir>
python3 "$(git rev-parse --show-toplevel)/.git/hooks/post-commit.py" "$@"
"""


def run_install_hook(directory: Path, force: bool = False) -> None:
    directory = directory.resolve()

    # Find the .git directory
    git_dir = _find_git_dir(directory)
    if not git_dir:
        console.print(f"[red]ERROR:[/red] No .git directory found in {directory} or its parents.")
        console.print("  Run this from inside a git repository.")
        raise SystemExit(1)

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)

    hook_py   = hooks_dir / "post-commit.py"
    hook_sh   = hooks_dir / "post-commit"

    # ── Write Python hook ─────────────────────────────────────────────────────
    if hook_py.exists() and not force:
        console.print(f"[yellow]Skipped:[/yellow] {hook_py} already exists. Use --force to overwrite.")
    else:
        hook_py.write_text(_HOOK_SCRIPT, encoding="utf-8")
        _make_executable(hook_py)
        console.print(f"[green]+[/green] Written: {hook_py}")

    # ── Write shell hook (calls the Python file) ──────────────────────────────
    if hook_sh.exists() and not force:
        console.print(f"[yellow]Skipped:[/yellow] {hook_sh} already exists (existing hook preserved). Use --force to overwrite.")
    else:
        hook_sh.write_text(_HOOK_SCRIPT_BASH, encoding="utf-8")
        _make_executable(hook_sh)
        console.print(f"[green]+[/green] Written: {hook_sh}")

    console.print()
    console.print("[bold]Git hook installed.[/bold]")
    console.print("  After each commit, staged .md files are automatically converted to .st.")
    console.print(f"  Repo: {git_dir.parent}")
    console.print()
    console.print("[dim]To uninstall:[/dim]")
    console.print(f"  del {hook_sh}  &&  del {hook_py}")


def _find_git_dir(start: Path) -> Path | None:
    """Walk up from start to find a .git directory."""
    current = start
    for _ in range(10):  # max 10 levels up
        candidate = current / ".git"
        if candidate.is_dir():
            return candidate
        if current == current.parent:
            break
        current = current.parent
    return None


def _make_executable(path: Path) -> None:
    """Add execute permission (no-op on Windows but git respects it)."""
    try:
        current = os.stat(path).st_mode
        os.chmod(path, current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except OSError:
        pass  # Windows — git handles this via core.fileMode
