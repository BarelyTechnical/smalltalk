"""
Skill router — maps a task description to the most relevant .st files to load.

Extends palace navigation with content-based scoring:
- Structural: file/dir name keyword match (like navigate)
- Semantic: SKILL trigger fields, USE when: fields, AGENT capability fields

Usage:
    smalltalk route "build a landing page for a plumbing business"
    → ui-designer.st  (SKILL triggers: landing-page+demo-build, score: 9)
    → seo-expert.st   (USE when: any-web-build, score: 7)
    → conversion-copy.st (USE when: demo+cold-outreach, score: 5)
"""
from pathlib import Path
from collections import defaultdict
from typing import Optional

from smalltalk.parser import parse_st_files


# Entry types whose fields contribute to routing scores
_ROUTING_TYPES = {"SKILL", "USE", "AGENT", "TRIGGER", "RULE", "STEP", "PHASE"}

# Boost multipliers per entry type
_TYPE_WEIGHT = {
    "SKILL":   3,   # direct skill declaration — highest signal
    "USE":     3,   # explicit trigger condition
    "AGENT":   2,   # agent capability declaration
    "TRIGGER": 2,   # event-based trigger
    "RULE":    1,
    "STEP":    1,
    "PHASE":   1,
}


def _tokenize(text: str) -> set[str]:
    """Lowercase, split on separators, return keyword set."""
    text = text.lower()
    for sep in ["|", "+", ":", ">", "/", "\\", "-", "_", ".", ",", ";"]:
        text = text.replace(sep, " ")
    return {w for w in text.split() if len(w) > 2}


def route(
    directory: Path,
    task: str,
    top_n: int = 5,
) -> list[dict]:
    """
    Score every .st file in directory against the task description.

    Returns a sorted list of dicts:
        file, score, reasons, entry_count
    """
    directory = directory.resolve()
    task_tokens = _tokenize(task)

    if not task_tokens:
        return []

    # Parse all entries from all .st files
    entries = parse_st_files(directory)
    st_files = sorted(directory.rglob("*.st")) if directory.is_dir() else [directory]

    # Group entries by file
    by_file: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_file[e["file"]].append(e)

    scores = []

    for st_file in st_files:
        file_path = str(st_file)
        file_entries = by_file.get(file_path, [])
        score = 0
        reasons: list[str] = []

        # ── Structural score: file/dir name ───────────────────────────────────
        name_tokens = _tokenize(st_file.stem) | _tokenize(st_file.parent.name)
        name_hits = task_tokens & name_tokens
        if name_hits:
            boost = len(name_hits) * 2
            score += boost
            reasons.append(f"name:{'+'.join(sorted(name_hits))} (+{boost})")

        # ── Content score: SKILL/USE/AGENT/TRIGGER fields ────────────────────
        for e in file_entries:
            if e["type"] not in _ROUTING_TYPES:
                continue

            weight = _TYPE_WEIGHT.get(e["type"], 1)
            entry_text = " ".join(e.get("fields", []))
            entry_tokens = _tokenize(entry_text) | _tokenize(e.get("subject", ""))
            hits = task_tokens & entry_tokens

            if hits:
                boost = len(hits) * weight
                score += boost
                reasons.append(
                    f"{e['type'].lower()}:{e.get('subject', '?')}:{'+'.join(sorted(hits))} (+{boost})"
                )

        if score > 0:
            scores.append({
                "file":        file_path,
                "score":       score,
                "reasons":     reasons[:5],   # cap reasons for display
                "entry_count": len(file_entries),
            })

    # Sort by score descending
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:top_n]


def format_route_results(
    results: list[dict],
    task: str,
    directory: Path,
) -> str:
    if not results:
        return (
            f"No matching files found for: '{task}'\n"
            f"  Ensure .st files exist in {directory}\n"
            f"  Try: smalltalk mine {directory}"
        )

    lines = [
        f"Route: '{task}'\n"
        f"  Found {len(results)} relevant file(s):\n"
    ]

    for i, r in enumerate(results, 1):
        try:
            rel = Path(r["file"]).relative_to(directory)
        except ValueError:
            rel = Path(r["file"]).name

        lines.append(f"  {i}. {rel}  (score:{r['score']}  entries:{r['entry_count']})")
        for reason in r["reasons"]:
            lines.append(f"       match: {reason}")
        lines.append("")

    lines += [
        "Load these files at session start with:",
        "  smalltalk_read_file(path)  — via MCP",
        "  smalltalk wake-up <dir>    — for L1 context",
    ]
    return "\n".join(lines)
