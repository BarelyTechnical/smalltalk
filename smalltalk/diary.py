"""
Specialist agent diary.
Append-only per-agent knowledge base stored in ~/.smalltalk/diaries/<agent-id>.st
Global, cross-project — agents accumulate expertise across all sessions and repos.
"""
from pathlib import Path
from datetime import datetime

DIARY_DIR = Path.home() / ".smalltalk" / "diaries"


def _diary_path(agent_id: str) -> Path:
    return DIARY_DIR / f"{agent_id}.st"


def diary_write(agent_id: str, entry: str) -> Path:
    """
    Append a diary entry for an agent.
    Adds a date comment suffix if not already present.
    Returns the diary file path.
    """
    DIARY_DIR.mkdir(parents=True, exist_ok=True)
    path = _diary_path(agent_id)

    line = entry.strip()
    if not line:
        raise ValueError("Entry cannot be empty.")

    # Stamp with today's date unless already timestamped
    if "# 20" not in line:
        today = datetime.now().strftime("%Y-%m-%d")
        line = f"{line}  # {today}"

    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

    return path


def diary_read(agent_id: str, last_n: int = 20) -> list[str]:
    """
    Read the last N diary entries for an agent.
    Returns an empty list if no diary exists.
    """
    path = _diary_path(agent_id)
    if not path.exists():
        return []

    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return lines[-last_n:] if last_n > 0 else lines


def list_agents() -> list[str]:
    """List all agent IDs that have diary files."""
    if not DIARY_DIR.exists():
        return []
    return sorted(p.stem for p in DIARY_DIR.glob("*.st"))
