"""
Smalltalk MCP Server — 18 tools.

Exposes Smalltalk operations to MCP-compatible clients:
Claude Code, Cursor, Codex, Windsurf, Antigravity, and any tool that speaks MCP.

Run:
    python -m smalltalk.mcp_server

Register with Claude Code:
    claude mcp add smalltalk -- python -m smalltalk.mcp_server
"""
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from smalltalk.parser import parse_st_files
from smalltalk.searcher import search_st_files, format_search_results
from smalltalk.checker import check_contradictions, format_check_results
from smalltalk.wake_up import build_wake_up_context
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
from smalltalk.palace import (
    navigate as _navigate,
    list_wings as _list_wings,
    list_rooms as _list_rooms,
    palace_status_text,
)
from smalltalk.kg_viz import visualize as _kg_visualize

mcp = FastMCP("smalltalk")

_SPEC_PATH = Path(__file__).parent / "instructions" / "help.md"


# ===========================================================================
# Palace (read + navigate)
# ===========================================================================

@mcp.tool()
def smalltalk_status(directory: str) -> str:
    """
    Get an overview of .st files in a directory.
    Returns file count, total entries, and a breakdown by type.
    Use this first when working with any Smalltalk-compressed directory.
    """
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"

    entries  = parse_st_files(d)
    st_files = sorted(d.rglob("*.st")) if d.is_dir() else ([d] if d.suffix == ".st" else [])

    type_counts: dict[str, int] = {}
    for e in entries:
        type_counts[e["type"]] = type_counts.get(e["type"], 0) + 1

    lines = [
        f"Smalltalk Status — {d}",
        "",
        f"Files:   {len(st_files)} .st file(s)",
        f"Entries: {len(entries)} total",
        "",
        "Breakdown by type:",
    ]
    for t, count in sorted(type_counts.items()):
        lines.append(f"  {t:<14} {count}")

    lines += [
        "",
        "Next steps:",
        "  smalltalk_get_spec()                   — learn the grammar",
        "  smalltalk_palace_init(dir)             — set up palace navigation",
        "  smalltalk_navigate(dir, query)         — navigate to relevant file",
        "  smalltalk_search(dir, query)           — keyword search",
        "  smalltalk_check(dir)                   — detect contradictions",
        "  smalltalk_wake_up(dir)                 — extract system prompt context",
    ]
    return "\n".join(lines)


@mcp.tool()
def smalltalk_get_spec() -> str:
    """
    Return the full Smalltalk grammar specification.
    Covers: RULE, REF, NOTE, CONFIG, CONTEXT, DECISION, PATTERN, WIN, CLIENT,
            COMPONENT, PROMPT, SKILL, USE, PHASE, STEP, STACK, CHECK, AVOID,
            SCRIPT, STYLE, FONT, COLOR, AGENT, TASK, TRIGGER, OUTPUT, ERROR,
            WING, ROOM, TUNNEL, LAYER.
    Read this before writing any .st entries.
    """
    if _SPEC_PATH.exists():
        return _SPEC_PATH.read_text(encoding="utf-8")
    return "Spec not found. Run: smalltalk instructions help"


@mcp.tool()
def smalltalk_list_files(directory: str) -> str:
    """List all .st files in a directory with entry counts."""
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"

    st_files = sorted(d.rglob("*.st")) if d.is_dir() else ([d] if d.suffix == ".st" else [])
    if not st_files:
        return f"No .st files found in {directory}."

    lines = [f"Found {len(st_files)} .st file(s) in {d}:\n"]
    for f in st_files:
        try:
            count = len([l for l in f.read_text(encoding="utf-8").splitlines()
                         if l.strip() and not l.startswith("#")])
        except OSError:
            count = 0
        try:
            rel = f.relative_to(d)
        except ValueError:
            rel = f
        lines.append(f"  {rel}  ({count} entries)")

    return "\n".join(lines)


@mcp.tool()
def smalltalk_read_file(file_path: str) -> str:
    """
    Read the full contents of a .st file.
    Use smalltalk_get_spec() first to understand the format.
    """
    p = Path(file_path)
    if not p.exists():
        return f"ERROR: File not found: {file_path}"
    if p.suffix != ".st":
        return f"ERROR: Not a .st file: {file_path}"
    try:
        return p.read_text(encoding="utf-8")
    except OSError as exc:
        return f"ERROR: Could not read file: {exc}"


@mcp.tool()
def smalltalk_search(
    directory: str,
    query: str,
    entry_type: str = "",
    wing: str = "",
    hall: str = "",
) -> str:
    """
    Search for a keyword across .st files in a directory.

    Prefer smalltalk_navigate() first — it's faster and more precise.
    Use search when navigate returns nothing, or for broad/content queries.

    Args:
        directory:   Path to search
        query:       Keyword or phrase (case-insensitive)
        entry_type:  Filter by type: DECISION, RULE, PATTERN, WIN, SKILL, AGENT, etc.
        wing:        Scope to a wing's files (reads palace _index.st)
        hall:        Filter by hall name: facts, events, discoveries, preferences, advice
    """
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"

    results = search_st_files(
        d, query,
        entry_type=entry_type.upper() if entry_type else None,
        wing=wing or None,
        hall=hall or None,
    )
    return format_search_results(results, d)


# ===========================================================================
# Palace navigation
# ===========================================================================

@mcp.tool()
def smalltalk_palace_init(directory: str) -> str:
    """
    Initialise a palace — scan directory structure and generate _index.st.

    Run this once on a new _brain/ or skills/ directory.
    After adding/renaming files, run smalltalk_palace_index() to refresh.

    Detection rules:
      Category folder (projects/, people/) → each child dir = wing
      Wing folder (no sub-dirs) → each .st file = room
      Root-level .st files → single-file wings

    Returns a summary of wings, rooms, and tunnels detected.
    """
    from smalltalk.palace import init_palace
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"
    try:
        index_path = init_palace(d.resolve())
        return f"Palace index: {index_path}\n" + palace_status_text(d.resolve())
    except Exception as exc:
        return f"ERROR: {exc}"


@mcp.tool()
def smalltalk_palace_index(directory: str) -> str:
    """
    Regenerate _index.st from current directory structure.
    Run after adding, renaming, or deleting .st files.
    """
    from smalltalk.palace import index_palace
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"
    try:
        index_path = index_palace(d.resolve())
        return f"Index regenerated: {index_path}"
    except Exception as exc:
        return f"ERROR: {exc}"


@mcp.tool()
def smalltalk_navigate(directory: str, query: str) -> str:
    """
    Navigate the palace to find the most relevant .st file(s) for a query.

    Reads _index.st, scores wings and rooms by keyword match.
    Returns 1–3 file paths to read directly — no content scan needed.

    RECOMMENDED WORKFLOW:
      1. smalltalk_navigate(dir, query) → get file path(s)
      2. smalltalk_read_file(path)      → read the relevant file
      3. smalltalk_search(dir, query)   → fallback if navigate returns nothing

    Args:
        directory: Palace root (must contain _index.st — run smalltalk_palace_init first)
        query:     What you're looking for — e.g. "auth decision" or "billing pattern"

    Works best with descriptive file/folder names (auth.st, kai.st, deploy.st).
    Falls back to search for content not reflected in names.
    """
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"

    paths = _navigate(d.resolve(), query)

    if not paths:
        index_path = d / "_index.st"
        if not index_path.exists():
            return (
                f"No palace index in {directory}.\n"
                f"Run: smalltalk_palace_init('{directory}')\n"
                f"Then retry. Fallback: smalltalk_search('{directory}', '{query}')"
            )
        return (
            f"No relevant files found for '{query}' by name.\n"
            f"Fallback: smalltalk_search('{directory}', '{query}')"
        )

    lines = [f"Navigate '{query}' → {len(paths)} file(s):\n"]
    for i, path in enumerate(paths, 1):
        try:
            entry_count = len(parse_st_files(Path(path)))
        except Exception:
            entry_count = 0
        lines.append(f"  {i}. {path}  ({entry_count} entries)")

    lines += [
        "",
        "Next: smalltalk_read_file(path) on the most relevant file.",
        "      smalltalk_search(directory, query) if none seem right.",
    ]
    return "\n".join(lines)


@mcp.tool()
def smalltalk_list_wings(directory: str) -> str:
    """
    List all wings in the palace — projects, people, topic namespaces.
    Requires _index.st (run smalltalk_palace_init first).
    """
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"

    wings = _list_wings(d.resolve())
    if not wings:
        idx = d / "_index.st"
        if not idx.exists():
            return f"No palace index. Run: smalltalk_palace_init('{directory}')"
        return "No wings declared in _index.st."

    lines = [f"Wings ({len(wings)}):\n"]
    for w in wings:
        lines.append(f"  {w['id']:<22} [{w['type']:<8}]  {w['room_count']} room(s)")
    lines += ["", "Use smalltalk_list_rooms(dir, wing) to see rooms in a specific wing."]
    return "\n".join(lines)


@mcp.tool()
def smalltalk_list_rooms(directory: str, wing: str = "") -> str:
    """
    List rooms in the palace, optionally filtered by wing.
    Each room = a .st file covering a specific topic.

    Args:
        directory: Palace root
        wing:      Optional wing id to filter (e.g. 'myapp', 'kai')
    """
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"

    rooms = _list_rooms(d.resolve(), wing)
    if not rooms:
        if wing:
            return f"No rooms found for wing '{wing}'."
        return f"No rooms found. Run: smalltalk_palace_init('{directory}')"

    title = f"Rooms in wing '{wing}'" if wing else f"All rooms ({len(rooms)})"
    lines = [f"{title}:\n"]
    current_wing = None
    for r in rooms:
        if not wing and r["wing"] != current_wing:
            current_wing = r["wing"]
            lines.append(f"  [{current_wing}]")
        prefix = "    " if not wing else "  "
        lines.append(f"{prefix}{r['id']:<22} hall:{r['hall']:<28}  {r['file']}")

    return "\n".join(lines)


# ===========================================================================
# Context injection
# ===========================================================================

@mcp.tool()
def smalltalk_wake_up(directory: str) -> str:
    """
    Extract compressed L1 context from .st files — sized for a system prompt.

    Includes:
        DECISION — all entries
        RULE     — hard rules only
        PATTERN  — all entries
        WIN      — repeat:y only

    Paste this block at the start of a local model's context window.
    Typically ~150 tokens — gives the model your full decision history.
    """
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"
    return build_wake_up_context(d)


# ===========================================================================
# Contradiction detection
# ===========================================================================

@mcp.tool()
def smalltalk_check(directory: str) -> str:
    """
    Run contradiction detection across all .st files in a directory.

    Detects:
        DECISION — same subject, diverging choices
        RULE     — same id flagged hard in one file, soft in another
        PATTERN  — same id + cause, but different fix: values
        WIN      — same id with repeat:y and repeat:n

    Rules-based — no LLM required. Works on any .st directory.
    """
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"
    return format_check_results(check_contradictions(d), d)


# ===========================================================================
# Agent diary
# ===========================================================================

@mcp.tool()
def smalltalk_diary_write(agent_id: str, entry: str) -> str:
    """
    Write a diary entry for a specialist agent.

    Stored in ~/.smalltalk/diaries/<agent-id>.st
    Global and cross-project — a reviewer agent accumulates expertise from all repos.

    Args:
        agent_id: Agent id, e.g. "reviewer", "architect", "ops"
        entry:    A valid Smalltalk .st line, e.g.:
                  "PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y"
    """
    try:
        path = _diary_write(agent_id, entry)
        return f"Written to {path}"
    except ValueError as exc:
        return f"ERROR: {exc}"
    except OSError as exc:
        return f"ERROR: Could not write diary: {exc}"


@mcp.tool()
def smalltalk_diary_read(agent_id: str, last_n: int = 20) -> str:
    """
    Read recent diary entries for a specialist agent.

    Args:
        agent_id: Agent id, e.g. "reviewer", "architect", "ops"
        last_n:   Number of most recent entries to return (default 20)
    """
    entries = _diary_read(agent_id, last_n)
    agents  = list_agents()

    if not entries:
        if agent_id not in agents:
            available = ", ".join(agents) if agents else "none"
            return f"No diary for '{agent_id}'. Available: {available}"
        return f"Diary for '{agent_id}' is empty."

    lines = [f"Diary: {agent_id} (last {len(entries)} entries)\n"]
    lines.extend(entries)
    return "\n".join(lines)



# ===========================================================================
# Knowledge Graph
# ===========================================================================

@mcp.tool()
def smalltalk_kg_query(directory: str, entity: str, as_of: str = "") -> str:
    """
    Query the knowledge graph for an entity — all its relationships, active and historical.

    Reads LINK, TUNNEL, and REF entries from .st files.
    Returns direct connections + extended (depth-2) connections.
    Pass as_of='YYYY-MM' for a historical point-in-time view.

    Stability levels:
      permanent  — core truth, always valid unless explicitly ended
      stable     — valid until superseded (default)
      transient  — time-windowed, changes frequently

    To build the graph, add LINK entries to .st files:
      LINK: kai  | rel:works-on  | orion | valid_from:2026-01 | stability:transient
      LINK: auth | rel:depends   | billing | stability:stable
      LINK: brand-color | rel:defined-as | purple | stability:permanent

    Args:
        directory: Directory containing .st files
        entity:    Entity to look up (e.g. 'kai', 'myapp', 'auth')
        as_of:     YYYY-MM — historical query (optional, defaults to today)
    """
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"
    result = _kg_query(d.resolve(), entity, as_of or None)
    return format_entity_query(result)


@mcp.tool()
def smalltalk_kg_timeline(directory: str, entity: str) -> str:
    """
    Return the chronological story of an entity.

    Shows all LINK entries where the entity appears as source or target,
    sorted by valid_from date. Active relationships vs closed ones.

    Useful for:
      - Tracking project history (who worked on what, when)
      - Seeing how a decision evolved over time
      - Auditing what was true before a change

    Example output:
      2025-06  kai → joined → brainroot   [active]
      2026-01  kai → works-on → orion     [closed 2026-03]
      2026-03  kai → works-on → nova      [active]

    Args:
        directory: Directory containing .st files
        entity:    Entity to trace (e.g. 'kai', 'orion', 'auth')
    """
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"
    events = _kg_timeline(d.resolve(), entity)
    return format_timeline(events, entity)


@mcp.tool()
def smalltalk_kg_invalidate(
    file_path: str,
    line_no: int,
    ended: str = "",
) -> str:
    """
    Close an active .st entry by writing ended:YYYY-MM onto it.

    This is the write side of the contradiction→resolution cycle:

      FULL WORKFLOW:
        1. smalltalk_check(dir)               → find contradictions
        2. Note the 'older' entry: file path + line_no from the output
        3. smalltalk_kg_invalidate(file, line_no)  → writes ended: to that line
        4. smalltalk_check(dir)               → confirm contradiction is cleared

    Works on ANY .st entry type (LINK, DECISION, RULE, PATTERN, WIN — anything
    that smalltalk_check flags). The file is written in place; the original line
    is preserved as the prefix with `| ended:YYYY-MM` appended.

    If ended: already exists on the line it is replaced, not duplicated.

    Args:
        file_path:  Absolute path to the .st file (shown in smalltalk_check output)
        line_no:    1-indexed line number of the entry (shown in smalltalk_check output)
        ended:      YYYY-MM date to set (defaults to current month)

    Example:
        smalltalk_check("_brain/")  →
          [WARNING] DECISION: deploy | diverging-choices
          people.st:7  DECISION: deploy | vercel>railway | cost | 2026-01  << older

        smalltalk_kg_invalidate("_brain/people.st", 7)
          → appends `| ended:2026-04` to line 7

        smalltalk_check("_brain/")  → OK  No active contradictions detected.
    """
    try:
        result = _kg_invalidate(
            file_path=file_path,
            line_no=line_no,
            ended=ended or None,
        )
        return format_invalidate_result(result)
    except (ValueError, OSError) as exc:
        return f"ERROR: {exc}"


@mcp.tool()
def smalltalk_kg_visualize(
    directory: str,
    out: str = "",
) -> str:
    """
    Generate an interactive Knowledge Graph visualization as an HTML file.

    Builds a vis.js graph from all .st files in the directory. Nodes are
    colour-coded by stability (permanent=purple/box, stable=blue, transient=cyan).
    Edges are colour-coded by relationship type. Historical edges (ended:) are
    faded and dashed. Conflict nodes are highlighted red (CRITICAL) or amber (WARNING).

    The HTML file loads vis.js from CDN (requires internet access to render).
    Does NOT open a browser — returns the path to the generated HTML file.

    Args:
        directory:  Path to directory containing .st files.
        out:        Optional output path for the HTML file.
                    Defaults to a temp file.

    Returns:
        Absolute path to the generated HTML file.

    Example:
        smalltalk_kg_visualize("_brain/")
        → "/tmp/st_kg_abc123.html"   (open in any browser to view)

        smalltalk_kg_visualize("_brain/", out="_brain/graph.html")
        → "_brain/graph.html"
    """
    d = Path(directory)
    if not d.exists():
        return f"ERROR: Directory not found: {directory}"
    try:
        path = _kg_visualize(
            directory    = d.resolve(),
            out          = Path(out) if out else None,
            open_browser = False,
        )
        return str(path)
    except Exception as exc:
        return f"ERROR: {exc}"


# ===========================================================================

if __name__ == "__main__":
    mcp.run()
