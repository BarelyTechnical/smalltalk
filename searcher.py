"""
Keyword search across .st files.
No vector DB — pure string match. Fast, local, zero dependencies.

Supports wing scoping (reads palace _index.st) and hall filtering
(MemPalace hall names map to Smalltalk TYPE lists).
"""
from pathlib import Path
from typing import Optional

from smalltalk.parser import parse_st_files

# MemPalace hall name → Smalltalk TYPE list
HALL_TO_TYPES: dict[str, list[str]] = {
    "facts":        ["DECISION", "RULE", "CONFIG"],
    "events":       ["PATTERN", "WIN"],
    "discoveries":  ["WIN", "NOTE"],
    "preferences":  ["RULE", "CLIENT"],
    "advice":       ["PATTERN"],
}


def _resolve_wing_files(directory: Path, wing: str) -> Optional[set[str]]:
    """
    Return absolute paths of files belonging to a wing via _index.st.
    Returns None if the index doesn't exist or the wing isn't found.
    """
    index_path = directory / "_index.st"
    if not index_path.exists():
        return None
    try:
        entries = parse_st_files(index_path)
    except Exception:
        return None

    files: set[str] = set()
    for e in entries:
        if e["type"] != "ROOM":
            continue
        w = next((f[5:] for f in e["fields"] if f.startswith("wing:")), "")
        if w != wing:
            continue
        file_rel = next((f[5:] for f in e["fields"] if f.startswith("file:")), "")
        if file_rel:
            files.add(str((directory / file_rel).resolve()))

    return files if files else None


def search_st_files(
    directory: Path,
    query: str,
    entry_type: Optional[str] = None,
    wing: Optional[str] = None,
    hall: Optional[str] = None,
) -> list[dict]:
    """
    Search for a keyword across .st files.

    Args:
        directory:   Path to search (directory = recursive, .st file = single)
        query:       Case-insensitive keyword or phrase
        entry_type:  Optional TYPE filter (e.g. "DECISION")
        wing:        Optional wing id — scopes search to that wing's files via palace index
        hall:        Optional hall name — maps to TYPE filter:
                     facts / events / discoveries / preferences / advice

    Returns:
        List of matching entry dicts with keys: type, subject, fields, raw, file, line_no
    """
    # Determine type filter
    type_filter: Optional[set[str]] = None
    if hall:
        lower = hall.lower()
        if lower in HALL_TO_TYPES:
            type_filter = set(HALL_TO_TYPES[lower])
        else:
            type_filter = {hall.upper()}
    elif entry_type:
        type_filter = {entry_type.upper()}

    # Resolve wing scope
    wing_files: Optional[set[str]] = None
    search_dir = directory

    if wing:
        wing_files = _resolve_wing_files(directory, wing)
        if not wing_files:
            # Fallback: search the subdirectory named after the wing
            candidate = directory / wing
            if candidate.exists():
                search_dir = candidate

    # Parse entries from the resolved scope
    entries = parse_st_files(search_dir)

    # Narrow to wing files if we found them via the index
    if wing_files:
        entries = [
            e for e in entries
            if str(Path(e["file"]).resolve()) in wing_files
        ]

    query_lower = query.lower()
    results = []
    for e in entries:
        if type_filter and e["type"] not in type_filter:
            continue
        if query_lower in e["raw"].lower():
            results.append(e)

    return results


def format_search_results(results: list[dict], base: Path) -> str:
    if not results:
        return "No matches found."

    lines = [f"Found {len(results)} match(es):\n"]
    for r in results:
        try:
            rel = Path(r["file"]).relative_to(base)
        except ValueError:
            rel = Path(r["file"]).name
        lines.append(f"  [{r['type']}] {rel}:{r['line_no']}")
        lines.append(f"    {r['raw']}")
        lines.append("")

    return "\n".join(lines)
