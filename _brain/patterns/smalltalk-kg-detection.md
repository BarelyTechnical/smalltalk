# Smalltalk KG Contradiction Detection — wiring pattern

## Context
Building file-based AI brain system (Smalltalk). Had flat-entry contradiction detection
working but KG LINK entries were not being checked.

## The Fix
`checker.py` — two-pass detection:

**Pass 1 (flat entries):** group by `(type, subject)`, detect DECISION/RULE/PATTERN/WIN conflicts

**Pass 2 (LINK entries):** group by `(source, rel)` — NOT `(type, subject)` — then:
- Skip non-exclusive relationships (`member-of`, `contributes-to`, `references`, etc.)
- Flag exclusive relationships (`works-on`, `assigned-to`, `defined-as`, etc.) when
  > 1 unique target is active simultaneously
- Severity: CRITICAL for known-exclusive rels, WARNING for unknown rels

## Key lesson
LINK contradictions can't be detected in the same pass as flat entries because LINK
entries for the same entity all have different `subject` values (the source entity name),
so grouping by `(type, subject)` would group them together but miss the `rel:` axis.
Must group by `(source, rel)` instead.

## Also fixed
- `is_currently_valid()` now validates date format before comparing strings
  (malformed dates like 'soon' or 'TBD' were silently passing through)
- `_extract_date()` fallback uses `file:filename:lineno` instead of just `line_no`
  for stable cross-file ordering when no date is present

## Test
`test_kg.py` — all 16 temporal validity tests pass
LINK overlap: `kai works-on orion` + `kai works-on nova` (no ended:) → CRITICAL
LINK non-exclusive: `kai member-of team` + `kai member-of guild` → NOT flagged
