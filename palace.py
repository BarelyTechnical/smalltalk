"""
Smalltalk Palace — navigation layer.

The file system IS the palace. No database required.

Convention:
  Category folder (projects/, people/) → each child is a wing
  Wing folder  → each .st file is a room
  Root .st files → single-file wings (type:topic)
  _index.st → always load first (~150 tokens)
  Tunnels → auto-detected when same room id appears in 2+ wings
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from smalltalk.parser import parse_st_files

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PERSON_FOLDERS: frozenset[str] = frozenset(
    {"people", "persons", "team", "members", "clients", "contacts", "humans", "users"}
)
PROJECT_FOLDERS: frozenset[str] = frozenset(
    {"projects", "work", "products", "apps", "repos", "codebases", "services", "features"}
)
_SKIP_PREFIXES = (".", "_")

# Query words → TYPE hint (for navigate scoring)
_TYPE_SIGNALS: dict[str, frozenset[str]] = {
    "DECISION": frozenset({"decided", "chose", "decision", "pick", "choice", "why", "switched", "selected"}),
    "PATTERN":  frozenset({"bug", "broke", "error", "fix", "fixed", "pattern", "issue", "problem", "solved"}),
    "WIN":      frozenset({"worked", "win", "repeat", "good", "success", "helped"}),
    "RULE":     frozenset({"rule", "always", "never", "must", "should", "policy", "forbidden"}),
    "SKILL":    frozenset({"skill", "how", "approach", "method"}),
    "AGENT":    frozenset({"agent", "workflow", "pipeline"}),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _kw_from_name(name: str) -> list[str]:
    """Split a hyphen/underscore name into keyword parts."""
    parts = re.split(r"[-_]", name.lower())
    return [p for p in parts if len(p) > 1]


def _infer_type(folder_name: str) -> str:
    n = folder_name.lower()
    if n in PERSON_FOLDERS:
        return "person"
    if n in PROJECT_FOLDERS:
        return "project"
    return "topic"


def _detect_halls(st_file: Path) -> list[str]:
    """Return sorted list of TYPEs present in a .st file (excluding structural types)."""
    _SKIP = {"WING", "ROOM", "TUNNEL", "LAYER", "REF"}
    try:
        return sorted({e["type"] for e in parse_st_files(st_file) if e["type"] not in _SKIP})
    except Exception:
        return []


def _make_wing(wing_id: str, wing_type: str, st_files: list[Path], base: Path) -> dict:
    rooms = []
    for f in sorted(st_files):
        if any(f.stem.startswith(p) for p in _SKIP_PREFIXES):
            continue
        halls = _detect_halls(f)
        rooms.append({
            "id":   f.stem,
            "file": str(f.relative_to(base)).replace("\\", "/"),
            "hall": "+".join(halls) if halls else "general",
        })
    kws = [wing_id] + _kw_from_name(wing_id)
    return {
        "type":     wing_type,
        "keywords": "+".join(dict.fromkeys(kws)),
        "rooms":    rooms,
    }


# ---------------------------------------------------------------------------
# Index builder
# ---------------------------------------------------------------------------

def _build_index(directory: Path) -> Path:
    """
    Scan directory and generate _index.st.

    Detection priority:
    1. Item is a file (.st) at root → single-file wing (type:topic)
    2. Item is a dir with sub-dirs → CATEGORY: each sub-dir = wing
    3. Item is a dir whose own name is in PERSON/PROJECT_FOLDERS → each .st inside = wing
    4. Item is a plain dir with only .st files → WING: .st files are rooms
    """
    directory = directory.resolve()
    wings: dict[str, dict] = {}

    for item in sorted(directory.iterdir()):
        if any(item.name.startswith(p) for p in _SKIP_PREFIXES):
            continue

        # ── root-level .st file → single-file wing ──────────────────────────
        if item.is_file():
            if item.suffix != ".st":
                continue
            halls = _detect_halls(item)
            kws   = [item.stem] + _kw_from_name(item.stem)
            wings[item.stem] = {
                "type":     "topic",
                "keywords": "+".join(dict.fromkeys(kws)),
                "rooms": [{"id": item.stem, "file": item.name,
                            "hall": "+".join(halls) if halls else "general"}],
            }
            continue

        if not item.is_dir():
            continue

        child_dirs = sorted(
            x for x in item.iterdir()
            if x.is_dir() and not any(x.name.startswith(p) for p in _SKIP_PREFIXES)
        )
        child_st = sorted(
            x for x in item.glob("*.st")
            if not any(x.stem.startswith(p) for p in _SKIP_PREFIXES)
        )

        if child_dirs:
            # ── CATEGORY folder (projects/, people/) ────────────────────────
            cat_type = _infer_type(item.name)
            for sub in child_dirs:
                sub_st = sorted(sub.rglob("*.st"))  # rglob: pick up nested rooms too
                wings[sub.name] = _make_wing(sub.name, cat_type, sub_st, directory)
            # .st files directly in the category folder → individual wings
            for st_f in child_st:
                halls = _detect_halls(st_f)
                kws   = [st_f.stem] + _kw_from_name(st_f.stem)
                wings[st_f.stem] = {
                    "type":     _infer_type(item.name),
                    "keywords": "+".join(dict.fromkeys(kws)),
                    "rooms": [{"id": st_f.stem,
                                "file": str(st_f.relative_to(directory)).replace("\\", "/"),
                                "hall": "+".join(halls) if halls else "general"}],
                }

        elif item.name.lower() in PERSON_FOLDERS and child_st:
            # ── people/ with no sub-dirs: each .st = person wing ────────────
            for st_f in child_st:
                halls = _detect_halls(st_f)
                kws   = [st_f.stem] + _kw_from_name(st_f.stem)
                wings[st_f.stem] = {
                    "type":     "person",
                    "keywords": "+".join(dict.fromkeys(kws)),
                    "rooms": [{"id": st_f.stem,
                                "file": str(st_f.relative_to(directory)).replace("\\", "/"),
                                "hall": "+".join(halls) if halls else "general"}],
                }

        elif item.name.lower() in PROJECT_FOLDERS and child_st:
            # ── projects/ with no sub-dirs: each .st = project wing ─────────
            for st_f in child_st:
                halls = _detect_halls(st_f)
                kws   = [st_f.stem] + _kw_from_name(st_f.stem)
                wings[st_f.stem] = {
                    "type":     "project",
                    "keywords": "+".join(dict.fromkeys(kws)),
                    "rooms": [{"id": st_f.stem,
                                "file": str(st_f.relative_to(directory)).replace("\\", "/"),
                                "hall": "+".join(halls) if halls else "general"}],
                }

        elif child_st:
            # ── plain dir: the dir IS a wing, its .st files are rooms ────────
            wings[item.name] = _make_wing(item.name, "topic", child_st, directory)

    # Tunnel detection: room id appearing in ≥2 wings
    room_to_wings: dict[str, list[str]] = defaultdict(list)
    for wid, wdata in wings.items():
        for room in wdata["rooms"]:
            room_to_wings[room["id"]].append(wid)
    tunnels = {rid: ws for rid, ws in room_to_wings.items() if len(ws) >= 2}

    # Write _index.st
    index_path = directory / "_index.st"
    lines = [
        "# Smalltalk Palace Index",
        f"# palace root: {directory.name}",
        "# Always load first (~150 tokens). Navigate with smalltalk_navigate().",
        "",
        "# Memory Stack",
        "LAYER:  L0 | file:identity.st | load:always",
        "LAYER:  L1 | file:_index.st   | load:always",
        "LAYER:  L2 | trigger:topic    | source:navigate",
        "LAYER:  L3 | trigger:search   | command:smalltalk_search",
        "",
    ]

    if wings:
        lines.append("# Wings")
        for wid, w in wings.items():
            lines.append(f"WING:   {wid} | type:{w['type']} | keywords:{w['keywords']}")
        lines.append("")

        lines.append("# Rooms")
        for wid, w in wings.items():
            for room in w["rooms"]:
                lines.append(
                    f"ROOM:   {room['id']} | wing:{wid} | hall:{room['hall']} | file:{room['file']}"
                )
        lines.append("")

    if tunnels:
        lines.append("# Tunnels — same topic appears in multiple wings")
        for rid, twings in sorted(tunnels.items()):
            lines.append(f"TUNNEL: {rid} | wings:{'+'.join(twings)} | topic:{rid}")
        lines.append("")

    index_path.write_text("\n".join(lines), encoding="utf-8")
    return index_path


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def init_palace(directory: Path) -> Path:
    """Scan directory structure and generate _index.st."""
    return _build_index(directory)


def index_palace(directory: Path) -> Path:
    """Regenerate _index.st from current directory structure."""
    return _build_index(directory)


def navigate(directory: Path, query: str) -> list[str]:
    """
    Resolve a query to the most relevant room file paths.

    Reads _index.st, scores wings and rooms by keyword match + hall type signals.
    Returns up to 3 absolute file paths. Falls back to empty list if no index.

    Best when file/folder names are descriptive (auth.st, kai.st, billing.st).
    Falls back to smalltalk_search for content that isn't reflected in names.
    """
    index_path = directory / "_index.st"
    if not index_path.exists():
        return []

    entries = parse_st_files(index_path)
    query_words = frozenset(re.split(r"\W+", query.lower()))

    # Build wing keyword sets
    wing_kws: dict[str, frozenset[str]] = {}
    for e in entries:
        if e["type"] != "WING":
            continue
        kw_field = next((f for f in e["fields"] if f.startswith("keywords:")), "")
        kws = frozenset(kw_field.replace("keywords:", "").split("+")) if kw_field else frozenset()
        kws = kws | {e["subject"]} | frozenset(re.split(r"[-_]", e["subject"].lower()))
        wing_kws[e["subject"]] = frozenset(k.lower() for k in kws)

    scored: list[tuple[int, str]] = []

    for e in entries:
        if e["type"] != "ROOM":
            continue

        wing     = next((f[5:] for f in e["fields"] if f.startswith("wing:")),  "")
        file_rel = next((f[5:] for f in e["fields"] if f.startswith("file:")),  "")
        hall     = next((f[5:] for f in e["fields"] if f.startswith("hall:")),  "")

        if not file_rel:
            continue

        score = 0

        # Wing keyword match (max 4 pts)
        w_match = len(query_words & wing_kws.get(wing, {wing}))
        score += min(w_match * 2, 4)

        # Room topic match (max 6 pts)
        room_words = frozenset(re.split(r"[-_]", e["subject"].lower()))
        score += min(len(query_words & room_words) * 3, 6)

        # Hall/TYPE bonus (max 2 pts)
        hall_types = frozenset(hall.upper().split("+"))
        for entry_type, signals in _TYPE_SIGNALS.items():
            if entry_type in hall_types and query_words & signals:
                score += 1
                break

        if score > 0:
            abs_path = str((directory / file_rel).resolve())
            scored.append((score, abs_path))

    scored.sort(key=lambda x: -x[0])

    seen: set[str] = set()
    result: list[str] = []
    for _, path in scored:
        if path not in seen:
            seen.add(path)
            result.append(path)
        if len(result) >= 3:
            break
    return result


def list_wings(directory: Path) -> list[dict]:
    """List all wings declared in _index.st."""
    index_path = directory / "_index.st"
    if not index_path.exists():
        return []

    entries = parse_st_files(index_path)
    counts: dict[str, int] = {}
    for e in entries:
        if e["type"] == "ROOM":
            w = next((f[5:] for f in e["fields"] if f.startswith("wing:")), "")
            counts[w] = counts.get(w, 0) + 1

    result = []
    for e in entries:
        if e["type"] != "WING":
            continue
        t  = next((f[5:] for f in e["fields"] if f.startswith("type:")),     "topic")
        kw = next((f[9:] for f in e["fields"] if f.startswith("keywords:")), "")
        result.append({"id": e["subject"], "type": t, "keywords": kw,
                       "room_count": counts.get(e["subject"], 0)})
    return result


def list_rooms(directory: Path, wing_id: str = "") -> list[dict]:
    """List rooms in the palace, optionally filtered by wing."""
    index_path = directory / "_index.st"
    if not index_path.exists():
        return []

    entries = parse_st_files(index_path)
    result = []
    for e in entries:
        if e["type"] != "ROOM":
            continue
        wing     = next((f[5:] for f in e["fields"] if f.startswith("wing:")),  "")
        file_rel = next((f[5:] for f in e["fields"] if f.startswith("file:")),  "")
        hall     = next((f[5:] for f in e["fields"] if f.startswith("hall:")),  "")
        if wing_id and wing != wing_id:
            continue
        result.append({"id": e["subject"], "wing": wing, "hall": hall, "file": file_rel})
    return result


def palace_status_text(directory: Path) -> str:
    """Return a formatted text description of the palace."""
    index_path = directory / "_index.st"
    if not index_path.exists():
        return (
            f"No palace index in {directory}\n"
            f"Run: smalltalk palace init {directory}"
        )

    entries = parse_st_files(index_path)
    wings   = [e for e in entries if e["type"] == "WING"]
    rooms   = [e for e in entries if e["type"] == "ROOM"]
    tunnels = [e for e in entries if e["type"] == "TUNNEL"]
    layers  = [e for e in entries if e["type"] == "LAYER"]

    per_wing: dict[str, int] = {}
    for e in rooms:
        w = next((f[5:] for f in e["fields"] if f.startswith("wing:")), "")
        per_wing[w] = per_wing.get(w, 0) + 1

    sep   = "=" * 56
    lines = [
        "", sep,
        "  Smalltalk Palace",
        sep,
        f"  Root:     {directory}",
        "",
        f"  Wings:   {len(wings)}",
        f"  Rooms:   {len(rooms)}",
        f"  Tunnels: {len(tunnels)}",
        f"  Layers:  {len(layers)}",
        "",
    ]

    if wings:
        lines.append("  WINGS")
        for w in wings:
            wt = next((f[5:] for f in w["fields"] if f.startswith("type:")), "topic")
            lines.append(f"    {w['subject']:<24} [{wt:<8}]  {per_wing.get(w['subject'], 0)} room(s)")
        lines.append("")

    if tunnels:
        lines.append("  TUNNELS (cross-wing connections)")
        for t in tunnels:
            wf = next((f for f in t["fields"] if f.startswith("wings:")), "")
            lines.append(f"    {t['subject']:<24} {wf}")
        lines.append("")

    if layers:
        lines.append("  MEMORY STACK")
        for layer in layers:
            lines.append(f"    {layer['subject']:<6}  {' | '.join(layer['fields'][:2])}")
        lines.append("")

    return "\n".join(lines)
