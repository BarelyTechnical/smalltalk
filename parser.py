"""
Shared .st file parser used by searcher, checker, and wake_up.
"""
import re
from pathlib import Path

ST_LINE_PATTERN = re.compile(r'^([A-Z]+):\s+(\S+?)\s+\|(.*)')


def parse_st_files(target: Path) -> list[dict]:
    """
    Parse .st files into a list of entry dicts.
    Accepts a directory (recursive) or a single file.

    Each dict has keys:
        type     — entry type (DECISION, RULE, SKILL, etc.)
        subject  — identifier immediately after the type
        fields   — list of pipe-delimited fields (after subject)
        raw      — the original line
        file     — absolute path string
        line_no  — 1-indexed line number
    """
    if target.is_file():
        st_files = [target] if target.suffix == ".st" else []
    elif target.is_dir():
        st_files = sorted(target.rglob("*.st"))
    else:
        return []

    entries: list[dict] = []

    for st_file in st_files:
        try:
            text = st_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        for i, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            m = ST_LINE_PATTERN.match(stripped)
            if not m:
                continue
            entry_type = m.group(1)
            subject = m.group(2)
            fields = [f.strip() for f in m.group(3).split("|")]
            entries.append({
                "type": entry_type,
                "subject": subject,
                "fields": fields,
                "raw": stripped,
                "file": str(st_file),
                "line_no": i,
            })

    return entries
