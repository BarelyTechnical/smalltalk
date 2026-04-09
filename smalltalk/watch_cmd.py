"""
Watch mode for smalltalk mine.

Polls a directory for new or modified .md files and converts them automatically.
No external dependencies — uses Python stdlib only (os.stat + time.sleep).

Usage:
    smalltalk mine <dir> --watch
    smalltalk mine <dir> --watch --interval 5
"""
import time
import os
from pathlib import Path
from typing import Optional

from rich.console import Console

from smalltalk.converter import detect_file_type, convert_file

console = Console()

_SKIP_FILES = {
    "README.md", "readme.md", "CHANGELOG.md", "CONTRIBUTING.md",
    "LICENSE.md", "stack.md", "CONTEXT.md", "context.md", "CLAUDE.md",
    "GEMINI.md", "AGENTS.md",
}


def _get_md_mtimes(directory: Path) -> dict[Path, float]:
    """Return {path: mtime} for all watchable .md files in directory."""
    result = {}
    for p in directory.rglob("*.md"):
        if p.name in _SKIP_FILES:
            continue
        if ".originals" in p.parts or "__pycache__" in p.parts:
            continue
        try:
            result[p] = os.stat(p).st_mtime
        except OSError:
            pass
    return result


def _st_path(md_path: Path) -> Path:
    return md_path.with_suffix(".st")


def _needs_conversion(md_path: Path) -> bool:
    """True if no .st sibling exists, or .st is older than .md."""
    st = _st_path(md_path)
    if not st.exists():
        return True
    try:
        return os.stat(md_path).st_mtime > os.stat(st).st_mtime
    except OSError:
        return True


def run_mine_watch(
    directory: Path,
    api_key: Optional[str],
    model: str,
    base_url: str,
    keep_originals: bool = True,
    interval: int = 3,
) -> None:
    directory = directory.resolve()

    if not directory.exists():
        console.print(f"[red]ERROR:[/red] Directory not found: {directory}")
        raise SystemExit(1)

    if not api_key:
        console.print("[red]ERROR:[/red] API key required for watch mode. Pass --api-key or set OPENROUTER_API_KEY.")
        raise SystemExit(1)

    console.print(f"[bold cyan]Watching[/bold cyan] {directory}")
    console.print(f"  Polling every {interval}s. Press Ctrl+C to stop.\n")

    # Initial pass — convert anything already pending
    known = _get_md_mtimes(directory)
    _initial_pass(directory, known, api_key, model, base_url, keep_originals)

    try:
        while True:
            time.sleep(interval)
            current = _get_md_mtimes(directory)

            # Detect new or modified files
            for path, mtime in current.items():
                if path not in known or mtime > known[path]:
                    if _needs_conversion(path):
                        _convert_one(path, api_key, model, base_url, keep_originals)

            # Detect deleted files — remove orphaned .st files
            for path in list(known):
                if path not in current:
                    st = _st_path(path)
                    if st.exists() and not keep_originals:
                        st.unlink()
                        console.print(f"  [dim]Removed:[/dim] {st.name}")

            known = current

    except KeyboardInterrupt:
        console.print("\n[bold]Watch stopped.[/bold]")


def _initial_pass(
    directory: Path,
    known: dict,
    api_key: str,
    model: str,
    base_url: str,
    keep_originals: bool,
) -> None:
    pending = [p for p in known if _needs_conversion(p)]
    if not pending:
        console.print("  [green]All files up to date.[/green] Watching for changes...\n")
        return

    console.print(f"  [yellow]{len(pending)} file(s) pending conversion.[/yellow] Converting now...")
    for path in pending:
        _convert_one(path, api_key, model, base_url, keep_originals)
    console.print("  [green]Initial pass complete.[/green] Watching for changes...\n")


def _convert_one(
    path: Path,
    api_key: str,
    model: str,
    base_url: str,
    keep_originals: bool,
) -> None:
    try:
        file_type = detect_file_type(path)
        original_lines = len(path.read_text(encoding="utf-8", errors="replace").splitlines())

        st_content = convert_file(
            file_path=path,
            file_type=file_type,
            api_key=api_key,
            model=model,
            base_url=base_url,
        )

        out_path = _st_path(path)
        out_path.write_text(st_content, encoding="utf-8")
        st_lines = len(st_content.splitlines())
        reduction = int((1 - st_lines / max(original_lines, 1)) * 100)

        console.print(
            f"  [green]+[/green] {path.name} → {out_path.name}  "
            f"([dim]{original_lines} → {st_lines} lines, {reduction}% reduction[/dim])"
        )

        if not keep_originals:
            path.unlink()

    except Exception as exc:
        console.print(f"  [red]✗[/red] {path.name}: {exc}")
