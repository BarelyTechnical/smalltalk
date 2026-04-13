"""
Contradiction detection across .st files.
Rules-based — no LLM required. The typed, pipe-delimited format makes this tractable.

Detects:
  DECISION — same subject with diverging active choices
  RULE     — same subject flagged hard in one file, soft in another (both active)
  PATTERN  — same subject + cause, but conflicting fix: values (both active)
  WIN      — same subject with repeat:y and repeat:n (both active)
  LINK     — same source+rel pointing to different targets with no temporal separation

Temporal awareness:
  Entries with ended: <= today are HISTORICAL — they are EXCLUDED from conflict detection.
  A superseded entry next to a new one is NOT a contradiction — it's correct resolution.
  Only ACTIVE entries (no ended:, or ended: in the future) are compared.

Stability awareness:
  stability:permanent conflicts are flagged as CRITICAL.
  Contradictions show suggested resolution: add ended:YYYY-MM to the older entry.
"""
from pathlib import Path
from collections import defaultdict
from typing import Optional

from smalltalk.parser import parse_st_files
from smalltalk.kg import is_currently_valid, get_stability, _parse_link, _today


def _extract_date(entry: dict) -> str:
    """
    Extract the most reliable date from an entry for ordering.
    Checks valid_from: first, then looks for a bare date field (YYYY-MM or YYYY-MM-DD).
    Falls back to a stable file+line composite so cross-file ordering is consistent.
    """
    for field in entry.get("fields", []):
        if field.startswith("valid_from:"):
            return field[11:].strip()
    for field in entry.get("fields", []):
        stripped = field.strip()
        if len(stripped) >= 7 and stripped[:4].isdigit() and stripped[4] == "-":
            return stripped[:7]
    # Fallback: stable cross-file ordering via filename + line number
    file_key = Path(entry.get("file", "unknown")).name
    line_key  = f"{entry.get('line_no', 0):06d}"
    return f"file:{file_key}:{line_key}"


# ---------------------------------------------------------------------------
# Relationship exclusivity — used by LINK overlap detection
# ---------------------------------------------------------------------------

# Relationships that imply one active target at a time (flag when > 1 target active)
_EXCLUSIVE_RELS = frozenset({
    "works-on", "assigned-to", "reports-to",
    "deployed-to", "defined-as", "blocks",
})

# Relationships that are naturally many-to-many — never flag these
_NON_EXCLUSIVE_RELS = frozenset({
    "member-of", "contributes-to", "references",
    "shares-topic", "depends", "knows", "related-to",
})


# ---------------------------------------------------------------------------
# Main detection
# ---------------------------------------------------------------------------

def check_contradictions(
    directory: Path,
    as_of: Optional[str] = None,
) -> dict:
    """
    Scan .st files for contradictions between ACTIVE entries.

    Detects two classes of conflict:

      1. Flat-entry contradictions (DECISION / RULE / PATTERN / WIN / HABIT / MODELMAP)
         — same subject, conflicting active values.

      2. LINK relational overlaps
         — same source entity, same rel:, pointing to different targets,
           both active simultaneously (no temporal separation via ended:).

    Historical entries (ended: <= today) are excluded — they have already
    been resolved. Only currently-valid entries are compared.

    Args:
        directory: Path to scan
        as_of:     YYYY-MM override for 'today' (useful for testing)

    Returns:
        dict with keys:
            total         — total number of conflicts
            contradictions — list of conflict dicts, each with:
                type, subject, conflict_type, values, entries,
                stability, severity, suggestion, older, newer
    """
    entries  = parse_st_files(directory)
    conflicts: list[dict] = []
    now = as_of or _today()

    # Only consider currently active entries
    active = [e for e in entries if is_currently_valid(e, now)]

    # ── Pass 1: Flat-entry contradictions ──────────────────────────────────────
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for e in active:
        groups[(e["type"], e["subject"])].append(e)

    for (entry_type, subject), group in groups.items():
        if len(group) < 2:
            continue

        conflict = _detect_flat_conflict(entry_type, subject, group)
        if conflict:
            conflicts.append(_enrich(conflict, now))

    # ── Pass 2: LINK relational overlap detection ────────────────────────────
    link_entries = [e for e in active if e["type"] == "LINK"]
    conflicts.extend(_detect_link_overlaps(link_entries, now))

    return {"total": len(conflicts), "contradictions": conflicts}


def _detect_flat_conflict(
    entry_type: str,
    subject: str,
    group: list[dict],
) -> Optional[dict]:
    """Return a raw conflict dict (no enrichment yet) or None."""

    # ── DECISION: same subject, different active choices ─────────────────────
    if entry_type == "DECISION":
        choices = {e["fields"][0] for e in group if e["fields"]}
        if len(choices) > 1:
            return {
                "type":          "DECISION",
                "subject":       subject,
                "conflict_type": "diverging-choices",
                "values":        sorted(choices),
                "entries":       group,
            }

    # ── RULE: same subject, hard in one place, soft in another ───────────────
    elif entry_type == "RULE":
        strengths = set()
        for e in group:
            if len(e["fields"]) >= 2:
                strengths.add(e["fields"][1].strip().lower())
        if "hard" in strengths and "soft" in strengths:
            return {
                "type":          "RULE",
                "subject":       subject,
                "conflict_type": "strength-conflict",
                "values":        sorted(strengths),
                "entries":       group,
            }

    # ── PATTERN: same subject + cause, different fix: values ─────────────────
    elif entry_type == "PATTERN":
        cause_to_fixes: dict[str, set] = defaultdict(set)
        for e in group:
            cause = next((f for f in e["fields"] if f.startswith("cause:")), None)
            fix   = next((f for f in e["fields"] if f.startswith("fix:")),   None)
            if cause and fix:
                cause_to_fixes[cause].add(fix)
        for cause, fixes in cause_to_fixes.items():
            if len(fixes) > 1:
                affected = [
                    e for e in group
                    if any(f.startswith("cause:" + cause.split(":", 1)[-1]) for f in e["fields"])
                ]
                return {
                    "type":          "PATTERN",
                    "subject":       subject,
                    "conflict_type": "conflicting-fixes",
                    "cause":         cause,
                    "values":        sorted(fixes),
                    "entries":       affected or group,
                }

    # ── WIN: repeat:y vs repeat:n for same subject ───────────────────────────
    elif entry_type == "WIN":
        repeat_vals = set()
        for e in group:
            rv = next((f.strip() for f in e["fields"] if f.strip().startswith("repeat:")), None)
            if rv:
                repeat_vals.add(rv)
        if "repeat:y" in repeat_vals and "repeat:n" in repeat_vals:
            return {
                "type":          "WIN",
                "subject":       subject,
                "conflict_type": "repeat-conflict",
                "values":        sorted(repeat_vals),
                "entries":       group,
            }

    # ── HABIT: same subject, enforce:hard in one file, enforce:soft in another ─
    elif entry_type == "HABIT":
        enforce_vals = set()
        for e in group:
            ev = next((f.strip() for f in e["fields"] if f.strip().startswith("enforce:")), None)
            if ev:
                enforce_vals.add(ev)
        if "enforce:hard" in enforce_vals and "enforce:soft" in enforce_vals:
            return {
                "type":          "HABIT",
                "subject":       subject,
                "conflict_type": "enforce-level-conflict",
                "values":        sorted(enforce_vals),
                "entries":       group,
            }

    # ── MODELMAP: same task-type routing to different models ─────────────────
    elif entry_type == "MODELMAP":
        models = set()
        for e in group:
            if e["fields"]:
                models.add(e["fields"][0].strip())
        if len(models) > 1:
            return {
                "type":          "MODELMAP",
                "subject":       subject,
                "conflict_type": "ambiguous-model-routing",
                "values":        sorted(models),
                "entries":       group,
            }

    return None


def _detect_link_overlaps(
    link_entries: list[dict],
    now: str,
) -> list[dict]:
    """
    Detect LINK entries where the same source+rel points to different targets
    with both active simultaneously (no ended: separating them).

    A valid progression (no conflict):
        LINK: kai | rel:works-on | orion | valid_from:2026-01 | ended:2026-03
        LINK: kai | rel:works-on | nova  | valid_from:2026-03

    A conflict (simultaneously active, different targets):
        LINK: kai | rel:works-on | orion | valid_from:2026-01
        LINK: kai | rel:works-on | nova  | valid_from:2026-03

    Non-exclusive relationships (member-of, contributes-to, etc.) are skipped.
    Unknown relationships are flagged as WARNING.
    """
    # Group by (source, rel)
    by_source_rel: dict[tuple, list] = defaultdict(list)
    for e in link_entries:
        link = _parse_link(e)
        if not link["target"]:
            continue
        key = (link["source"], link["rel"])
        by_source_rel[key].append((link, e))

    conflicts = []

    for (source, rel), pairs in by_source_rel.items():
        if len(pairs) < 2:
            continue
        if rel in _NON_EXCLUSIVE_RELS:
            continue

        # Collect unique targets from the active set
        targets = {link["target"] for link, _ in pairs}
        if len(targets) < 2:
            continue  # same target repeated — not a conflict

        # Re-fetch raw entries for enrichment
        raw_entries = [e for _, e in pairs]

        severity = "CRITICAL" if rel in _EXCLUSIVE_RELS else "WARNING"

        conflict = {
            "type":           "LINK",
            "subject":        source,
            "conflict_type":  f"simultaneous-{rel}",
            "values":         sorted(targets),
            "entries":        raw_entries,
            "_severity_hint": severity,
        }
        conflicts.append(_enrich(conflict, now))

    return conflicts


# ---------------------------------------------------------------------------
# Enrichment helper
# ---------------------------------------------------------------------------

def _enrich(conflict: dict, now: str) -> dict:
    """
    Attach stability, severity, older/newer markers, and resolution suggestion.
    Modifies conflict in place and returns it.
    """
    # Pull optional override from LINK detector before general stability logic
    forced_severity = conflict.pop("_severity_hint", None)

    stabilities   = {get_stability(e) for e in conflict["entries"]}
    has_permanent = "permanent" in stabilities

    severity  = forced_severity or ("CRITICAL" if has_permanent else "WARNING")
    stability = "permanent" if has_permanent else next(iter(stabilities), "stable")

    sorted_by_age = sorted(conflict["entries"], key=_extract_date)
    older = sorted_by_age[0]
    newer = sorted_by_age[-1]

    if has_permanent:
        suggestion = (
            f"[CRITICAL] A permanent fact is being contradicted.\n"
            f"  Resolve explicitly -- add `ended:{now}` to the older entry:\n"
            f"    {older['raw']}\n"
            f"  Then mark the new entry as permanent:\n"
            f"    Add `stability:permanent` to the newer entry."
        )
    else:
        suggestion = (
            f"Close the older entry by adding `ended:{now}` to:\n"
            f"    {older['raw']}"
        )

    conflict.update({
        "stability":  stability,
        "severity":   severity,
        "suggestion": suggestion,
        "older":      older,
        "newer":      newer,
        "older_date": _extract_date(older),
        "newer_date": _extract_date(newer),
    })
    return conflict


# ---------------------------------------------------------------------------
# Formatter
# ---------------------------------------------------------------------------

def format_check_results(result, base: Path) -> str:
    """
    Format contradiction check results for display.

    Accepts either:
      - dict: {"total": N, "contradictions": [...]}  (new API)
      - list: [conflict, ...]                         (legacy callers)
    """
    # Normalise: accept both dict and list
    if isinstance(result, dict):
        conflicts = result.get("contradictions", [])
    else:
        conflicts = result  # legacy list

    if not conflicts:
        return (
            "OK  No active contradictions detected.\n"
            "    (Historical entries with ended: are excluded from this scan.)"
        )

    critical = [c for c in conflicts if c.get("severity") == "CRITICAL"]
    warnings = [c for c in conflicts if c.get("severity") != "CRITICAL"]

    lines = [
        f"[CONFLICT] Found {len(conflicts)} contradiction(s)  "
        f"({len(critical)} CRITICAL, {len(warnings)} WARNING)\n"
    ]

    def _render(c: dict, idx: int) -> None:
        prefix = "[CRITICAL]" if c.get("severity") == "CRITICAL" else "[WARNING] "
        extra  = f" [{c.get('cause', '')}]" if c.get("cause") else ""
        stab   = f"  stability:{c.get('stability', 'stable')}"
        lines.append(
            f"  {idx}. {prefix} {c['type']}: {c['subject']}{extra} "
            f"| {c['conflict_type']}{stab}"
        )
        lines.append(f"     Values: {' | '.join(c['values'])}")
        for e in c["entries"]:
            try:
                rel_path = Path(e["file"]).relative_to(base)
            except ValueError:
                rel_path = Path(e["file"]).name
            marker = (
                " << older" if e is c.get("older") else
                (" << newer" if e is c.get("newer") else "")
            )
            lines.append(f"     {rel_path}:{e['line_no']}  {e['raw']}{marker}")
        lines.append("\n     Resolution:")
        for line in c["suggestion"].split("\n"):
            lines.append(f"       {line}")
        lines.append("")

    for i, c in enumerate(critical + warnings, 1):
        _render(c, i)

    lines.append("-" * 56)
    lines.append("  ended: = resolution mechanism. Set it on the OLDER entry.")
    lines.append("  Ended entries are excluded from future contradiction scans.")

    return "\n".join(lines)
