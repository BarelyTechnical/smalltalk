"""
Wake-up context builder.

Extracts the critical L1 layer from a directory of .st files.
Output is sized for ~150 tokens — designed for injection into a system prompt.

Temporal awareness:
  - Filters out entries where ended: date has passed
  - Filters out entries where valid_from: date is in the future
  - stability:permanent entries are always included when unended
  - stability:transient entries are included if within their validity window

The result is what the brain CURRENTLY believes — not historical facts.
"""
from pathlib import Path
from typing import Optional

from smalltalk.parser import parse_st_files
from smalltalk.kg import is_currently_valid, get_stability

# Types included in wake-up context
# Excluded intentionally: CLIENT, COMPONENT, PROMPT (reference data — load on demand via REF)
# Excluded intentionally: SKILL, USE, PHASE, STEP, STACK, CHECK, AVOID (load via route)
# Excluded intentionally: AGENT, TASK, TRIGGER, OUTPUT, ERROR (operational, not orienting)
# Result: ~150 tokens of current truth — decisions, hard rules, known patterns, repeatable wins
WAKE_UP_TYPES = {"DECISION", "RULE", "PATTERN", "WIN"}


def build_wake_up_context(directory: Path, as_of: Optional[str] = None) -> str:
    """
    Extract current critical context from .st files.

    Includes:
        DECISION — all unended entries
        RULE     — hard rules only (soft excluded), unended
        PATTERN  — all unended entries
        WIN      — repeat:y only, unended

    Temporal filtering:
        Entries with ended: <= today are excluded (historical, not current truth).
        Entries with valid_from: > today are excluded (not yet active).
        stability:permanent entries are always included unless explicitly ended.

    Returns a compact .st block ready to paste as a system prompt.
    """
    entries = parse_st_files(directory)

    selected_permanent: list[str] = []
    selected_standard:  list[str] = []

    for e in entries:
        t = e["type"]
        if t not in WAKE_UP_TYPES:
            continue

        # Temporal filter — skip stale or future entries
        if not is_currently_valid(e, as_of):
            continue

        # Type-specific filters
        if t == "RULE":
            strength = e["fields"][1].strip().lower() if len(e["fields"]) >= 2 else ""
            if strength != "hard":
                continue

        if t == "WIN":
            rv = next((f.strip() for f in e["fields"] if f.strip().startswith("repeat:")), "repeat:n")
            if rv != "repeat:y":
                continue

        # Bucket by stability — permanent goes first
        stability = get_stability(e)
        if stability == "permanent":
            selected_permanent.append(e["raw"])
        else:
            selected_standard.append(e["raw"])

    all_selected = selected_permanent + selected_standard

    if not all_selected:
        return (
            "# Smalltalk wake-up — no current context found\n"
            "# Mine your directory first: smalltalk mine <dir>\n"
            "# Note: entries with ended: in the past are filtered out"
        )

    header = f"# Smalltalk wake-up — {len(all_selected)} current entries from {directory}"
    parts  = [header, ""]

    if selected_permanent:
        parts.append("# permanent (core truth)")
        parts.extend(selected_permanent)
        parts.append("")

    if selected_standard:
        parts.append("# current")
        parts.extend(selected_standard)

    return "\n".join(parts)
