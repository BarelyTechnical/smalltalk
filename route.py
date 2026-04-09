"""
Task-to-skill router.

Scores every .st file in a directory against a natural language task description.
Returns ranked file paths — load the top results at session start before the first message.

Scoring:
  Structural (2x per match): file and directory name keyword match against task words.
  Content (type-weighted):
    SKILL / USE     → 3x   primary routing signals
    AGENT / TRIGGER → 2x
    RULE / CHECK    → 1x
    all others      → 0.5x

Zero dependencies. No LLM required.
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Optional

from smalltalk.parser import parse_st_files


# -------------------------------------------------------------------
# Type weights — controls how much each entry type influences routing
# -------------------------------------------------------------------

_TYPE_WEIGHTS: dict[str, float] = {
    "SKILL":   3.0,
    "USE":     3.0,
    "AGENT":   2.0,
    "TRIGGER": 2.0,
    "RULE":    1.0,
    "CHECK":   1.0,
    "AVOID":   1.0,
}
_DEFAULT_WEIGHT = 0.5


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def _tokenise(text: str) -> set[str]:
    """Lowercase word tokens, strips punctuation. Returns empty set for blank input."""
    return set(re.sub(r"[^\w\s]", " ", text.lower()).split())


# -------------------------------------------------------------------
# Public API
# -------------------------------------------------------------------

def route(
    directory: Path,
    task: str,
    top_n: int = 5,
) -> list[dict]:
    """
    Score every .st file in directory against a task description.

    Returns top_n results sorted by relevance (highest first).

    Each result dict contains:
        file        — absolute path string
        rel         — path relative to directory
        score       — relevance score (higher = more relevant)
        entry_count — number of entries in the file
        match_types — which entry types contributed matches
    """
    task_words = _tokenise(task)
    if not task_words:
        return []

    entries = parse_st_files(directory)

    # Group entries by file
    by_file: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_file[e["file"]].append(e)

    results = []

    for file_path, file_entries in by_file.items():
        score   = 0.0
        match_types: set[str] = set()

        # --- Structural scoring: file + directory name keyword match ---
        path       = Path(file_path)
        path_words = _tokenise(" ".join(path.parts))
        struct_matches = len(task_words & path_words)
        score += struct_matches * 2.0

        # --- Content scoring (type-weighted) ---
        for e in file_entries:
            t      = e["type"]
            weight = _TYPE_WEIGHTS.get(t, _DEFAULT_WEIGHT)

            # Match against subject + all field text
            content_words = _tokenise(e["subject"] + " " + " ".join(e["fields"]))
            n_matches = len(task_words & content_words)

            if n_matches:
                score += n_matches * weight
                match_types.add(t)

        if score > 0:
            try:
                rel = str(path.relative_to(directory))
            except ValueError:
                rel = path.name

            results.append({
                "file":        file_path,
                "rel":         rel,
                "score":       score,
                "entry_count": len(file_entries),
                "match_types": sorted(match_types),
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]


def format_route_results(results: list[dict], task: str) -> str:
    if not results:
        return (
            f"No skill/agent files matched '{task}'.\n"
            "Ensure your directory contains SKILL, USE, or AGENT entries.\n"
            "Fallback: smalltalk search <dir> <task>"
        )

    lines = [f"Route: '{task}' → {len(results)} file(s)\n"]

    for i, r in enumerate(results, 1):
        type_str = "+".join(r["match_types"]) if r["match_types"] else "name-only"
        lines.append(
            f"  {i}. [{r['score']:.1f}]  {r['rel']}"
            f"  ({r['entry_count']} entries)  via:{type_str}"
        )

    lines += [
        "",
        "Next: smalltalk_read_file(path) on top-ranked result(s).",
        "      These are the skills/agents most relevant to your task.",
    ]
    return "\n".join(lines)
