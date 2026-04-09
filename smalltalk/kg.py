"""
Smalltalk Knowledge Graph — temporal entity relationships.

No database. No dependencies. Everything lives in .st files.

Facts have three lifecycle properties:
  stability:permanent  — core truth, always loaded, only closed via contradiction
  stability:stable     — valid until explicitly ended (default)
  stability:transient  — time-windowed, changes frequently

ended: is set by contradiction resolution — not by a clock.
valid_from: is when the fact became true.

Sources built from:
  LINK:   entries — explicit entity relationships (primary source)
  TUNNEL: entries — shared topics across palace wings
  REF:    entries — file-level references / dependencies
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from smalltalk.parser import parse_st_files

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_KNOWN_LINK_PREFIXES = frozenset({"rel:", "valid_from:", "ended:", "stability:"})


# ---------------------------------------------------------------------------
# Temporal helpers
# ---------------------------------------------------------------------------

def _today() -> str:
    return datetime.now().strftime("%Y-%m")


def _is_valid_date(value: str) -> bool:
    """
    Return True if value looks like a valid YYYY-MM or YYYY-MM-DD string.
    Guards against malformed temporal fields (e.g. 'soon', 'TBD') that would
    produce silently wrong string comparisons.
    """
    v = value.strip()
    if len(v) < 7:
        return False
    if not (v[:4].isdigit() and v[4] == "-" and v[5:7].isdigit()):
        return False
    return True


def is_currently_valid(entry: dict, as_of: Optional[str] = None) -> bool:
    """
    Is this .st entry currently valid?

    Valid when:
      - No ended: field, OR ended: date is in the future
      - No valid_from: field, OR valid_from: <= today

    Malformed date values (non-YYYY-MM strings) are silently ignored
    rather than causing wrong comparisons.

    Used by wake_up.py, checker.py, and kg.py.
    """
    now = as_of or _today()
    for field in entry.get("fields", []):
        if field.startswith("ended:"):
            val = field[6:].strip()
            if _is_valid_date(val) and val[:7] <= now:
                return False
        elif field.startswith("valid_from:"):
            val = field[11:].strip()
            if _is_valid_date(val) and val[:7] > now:
                return False
    return True


def get_stability(entry: dict) -> str:
    """Return stability level from entry fields. Defaults to 'stable'."""
    for field in entry.get("fields", []):
        if field.startswith("stability:"):
            return field[10:].strip()
    return "stable"


# ---------------------------------------------------------------------------
# LINK entry parser
# ---------------------------------------------------------------------------

def _parse_link(entry: dict) -> dict:
    """
    Parse a LINK entry into components.

    Format: LINK: source | rel:type | target | [valid_from:YYYY-MM] | [ended:YYYY-MM] | [stability:x]

    The 'target' is the first field that doesn't start with a known prefix.
    """
    rel      = next((f[4:].strip()  for f in entry["fields"] if f.startswith("rel:")),       "related")
    target   = next((f.strip() for f in entry["fields"] if not any(f.startswith(p) for p in _KNOWN_LINK_PREFIXES)), "")
    vf       = next((f[11:].strip() for f in entry["fields"] if f.startswith("valid_from:")), None)
    ended    = next((f[6:].strip()  for f in entry["fields"] if f.startswith("ended:")),      None)
    # Note: LINK entries default to 'transient' stability — relationships are inherently
    # time-bound (who works on what, what deploys where). Other entry types (DECISION,
    # RULE, PATTERN) default to 'stable' via get_stability(). This is intentional.
    stab     = next((f[10:].strip() for f in entry["fields"] if f.startswith("stability:")),  "transient")
    return {
        "source":     entry["subject"],
        "rel":        rel,
        "target":     target,
        "valid_from": vf,
        "ended":      ended,
        "stability":  stab,
        "file":       entry["file"],
        "line_no":    entry["line_no"],
        "raw":        entry["raw"],
    }


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def build_graph(directory: Path, as_of: Optional[str] = None) -> dict[str, list[dict]]:
    """
    Build an adjacency graph from .st files.

    Sources:
      LINK:   → primary relationship entries
      TUNNEL: → shared topics across palace wings (bidirectional)
      REF:    → file references (source covers topic)

    Args:
        directory: Path to search
        as_of:     YYYY-MM — if given, only include entries valid at that point
    """
    entries = parse_st_files(directory)
    graph: dict[str, list[dict]] = defaultdict(list)

    for e in entries:
        # ── LINK entries ────────────────────────────────────────────────
        if e["type"] == "LINK":
            link = _parse_link(e)
            if not link["target"]:
                continue
            # If as_of is set, only include entries valid at that historical point
            if as_of and not is_currently_valid(e, as_of):
                continue
            graph[link["source"]].append({
                "rel":        link["rel"],
                "target":     link["target"],
                "valid_from": link["valid_from"],
                "ended":      link["ended"],
                "stability":  link["stability"],
                "active":     is_currently_valid(e),  # current real-time status (always today)
                "file":       link["file"],
                "line_no":    link["line_no"],
            })

        # ── TUNNEL entries (palace cross-wing connections) ───────────────
        elif e["type"] == "TUNNEL":
            wings_field = next((f for f in e["fields"] if f.startswith("wings:")), "")
            if wings_field:
                wings = wings_field.replace("wings:", "").split("+")
                topic = next((f[6:] for f in e["fields"] if f.startswith("topic:")), e["subject"])
                for i, w1 in enumerate(wings):
                    for w2 in wings[i + 1:]:
                        edge = {"rel": "shares-topic", "target": w2, "topic": topic, "active": True,
                                "valid_from": None, "ended": None, "stability": "stable"}
                        graph[w1].append(edge)
                        edge2 = dict(edge, target=w1)
                        graph[w2].append(edge2)

        # ── REF entries ──────────────────────────────────────────────────
        elif e["type"] == "REF":
            covers = next((f[7:] for f in e["fields"] if f.startswith("covers:")), "")
            if covers:
                graph[e["subject"]].append({
                    "rel": "references", "target": covers, "active": True,
                    "valid_from": None, "ended": None, "stability": "stable",
                })

    return dict(graph)


# ---------------------------------------------------------------------------
# Public query functions
# ---------------------------------------------------------------------------

def query_entity(
    directory: Path,
    entity: str,
    as_of: Optional[str] = None,
) -> dict:
    """
    Find all relationships for an entity.

    Returns direct connections and extended (depth-2) connections.
    Pass as_of='YYYY-MM' for a historical point-in-time view.
    """
    graph = build_graph(directory, as_of)

    direct = graph.get(entity, [])

    # Depth-2 BFS
    seen = {entity} | {e["target"] for e in direct}
    extended = []
    for edge in direct:
        for next_edge in graph.get(edge["target"], []):
            if next_edge["target"] not in seen:
                extended.append({
                    "via":    edge["target"],
                    "rel":    next_edge["rel"],
                    "target": next_edge["target"],
                    "active": next_edge.get("active", True),
                })
                seen.add(next_edge["target"])

    return {
        "entity":   entity,
        "as_of":    as_of or _today(),
        "direct":   direct,
        "extended": extended[:10],  # cap at 10 to keep output readable
    }


def get_timeline(directory: Path, entity: str) -> list[dict]:
    """
    Return the chronological story of an entity.

    Finds all LINK entries where entity is source or target.
    Sorted by valid_from date.
    """
    entries = parse_st_files(directory)
    events  = []

    for e in entries:
        if e["type"] != "LINK":
            continue
        link = _parse_link(e)
        if link["source"] != entity and link["target"] != entity:
            continue
        events.append({
            "date":      link["valid_from"] or "0000-00",
            "source":    link["source"],
            "rel":       link["rel"],
            "target":    link["target"],
            "ended":     link["ended"],
            "stability": link["stability"],
            "status":    "closed" if (link["ended"] and link["ended"] <= _today()) else "active",
        })

    events.sort(key=lambda x: x["date"])
    return events


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_entity_query(result: dict) -> str:
    entity   = result["entity"]
    as_of    = result["as_of"]
    direct   = result["direct"]
    extended = result["extended"]

    lines = [f"\nKG: {entity}  (as of {as_of})\n"]

    if not direct and not extended:
        lines += [
            f"  No relationships found for '{entity}'.",
            "",
            "  Add LINK entries to build the graph:",
            "    LINK: kai | rel:works-on | orion | valid_from:2026-01 | stability:transient",
        ]
        return "\n".join(lines)

    active   = [e for e in direct if e.get("active", True)]
    inactive = [e for e in direct if not e.get("active", True)]

    if active:
        lines.append(f"  Active ({len(active)}):")
        for edge in active:
            stab = f" [{edge['stability']}]" if edge["stability"] != "stable" else ""
            vf   = f"  since {edge['valid_from']}" if edge.get("valid_from") else ""
            lines.append(f"    {entity}  ->{edge['rel']}->  {edge['target']}{stab}{vf}")

    if inactive:
        lines.append(f"\n  Historical ({len(inactive)}):")
        for edge in inactive:
            period = f"{edge.get('valid_from', '?')} to {edge.get('ended', '?')}"
            lines.append(f"    {entity}  ->{edge['rel']}->  {edge['target']}  [{period}]")

    if extended:
        lines.append(f"\n  Extended ({len(extended)}):")
        for edge in extended:
            active_marker = "" if edge.get("active", True) else " [historical]"
            lines.append(f"    via {edge['via']}:  ->{edge['rel']}->  {edge['target']}{active_marker}")

    return "\n".join(lines)


def format_timeline(events: list[dict], entity: str) -> str:
    if not events:
        return (
            f"No timeline found for '{entity}'.\n"
            "Add LINK entries with valid_from: fields to build a timeline."
        )

    lines = [f"\nTimeline: {entity}\n"]
    for ev in events:
        date   = ev["date"] if ev["date"] != "0000-00" else "(undated)"
        status = f"active" if ev["status"] == "active" else f"closed {ev['ended']}"
        lines.append(f"  {date}  {ev['source']}  ->{ev['rel']}->  {ev['target']}  [{status}]")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Write operations — contradiction resolution
# ---------------------------------------------------------------------------

def invalidate_entry(
    file_path: Path,
    line_no: int,
    ended: Optional[str] = None,
) -> dict:
    """
    Close an active .st entry by writing ended:YYYY-MM onto it in the file.

    This is the write side of the contradiction→resolution cycle:
      1. smalltalk_check()        → identify the conflict + older entry file/line_no
      2. smalltalk_kg_invalidate  → call this function to write ended: to that line
      3. smalltalk_check()        → confirms the contradiction is cleared

    Args:
        file_path:  Absolute path to the .st file containing the entry
        line_no:    1-indexed line number of the entry (from check output)
        ended:      YYYY-MM month to set as ended (defaults to current month)

    Returns:
        dict with keys: success (bool), original (str), updated (str), message (str)

    Raises:
        ValueError:  If the file doesn't exist, is not a .st file, line_no is out of range,
                     or the targeted line doesn't contain a valid .st entry.
        OSError:     If the file cannot be read or written.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise ValueError(f"File not found: {file_path}")
    if file_path.suffix != ".st":
        raise ValueError(f"Not a .st file: {file_path}")

    ended_str = ended or _today()

    # Validate the ended date format
    if not _is_valid_date(ended_str):
        raise ValueError(
            f"Invalid ended date '{ended_str}'. Expected YYYY-MM (e.g. 2026-04)."
        )

    try:
        raw_lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
    except OSError as exc:
        raise OSError(f"Could not read {file_path}: {exc}") from exc

    if line_no < 1 or line_no > len(raw_lines):
        raise ValueError(
            f"Line {line_no} is out of range — file has {len(raw_lines)} lines."
        )

    # 0-indexed
    idx         = line_no - 1
    original    = raw_lines[idx].rstrip("\n").rstrip("\r")
    stripped    = original.strip()

    # Must look like a .st entry
    if not stripped or stripped.startswith("#"):
        raise ValueError(
            f"Line {line_no} is a comment or blank — nothing to invalidate:\n  {original}"
        )

    from smalltalk.parser import ST_LINE_PATTERN
    if not ST_LINE_PATTERN.match(stripped):
        raise ValueError(
            f"Line {line_no} doesn't look like a .st entry:\n  {original}"
        )

    # Already has ended: — update it in place
    if "ended:" in stripped:
        import re
        updated_stripped = re.sub(r"ended:[^\s|]+", f"ended:{ended_str}", stripped)
        action = "updated"
    else:
        # Append ended: field
        updated_stripped = f"{stripped} | ended:{ended_str}"
        action = "appended"

    # Preserve original line ending
    eol = "\r\n" if original.endswith("\r\n") else "\n"
    raw_lines[idx] = updated_stripped + eol

    try:
        file_path.write_text("".join(raw_lines), encoding="utf-8")
    except OSError as exc:
        raise OSError(f"Could not write {file_path}: {exc}") from exc

    return {
        "success":  True,
        "action":   action,
        "file":     str(file_path),
        "line_no":  line_no,
        "original": original,
        "updated":  updated_stripped,
        "ended":    ended_str,
    }


def format_invalidate_result(result: dict) -> str:
    """Format the result of invalidate_entry() for human/agent display."""
    return (
        f"Invalidated entry in {Path(result['file']).name}:{result['line_no']}\n\n"
        f"  Before: {result['original']}\n"
        f"  After:  {result['updated']}\n\n"
        f"  ended:{result['ended']} {result['action']}.\n"
        f"  Run smalltalk_check() to confirm the contradiction is cleared."
    )
