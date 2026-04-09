# smalltalk check

Scan a directory for contradictions across .st files.
Rules-based detection — no LLM required. Uses temporal fields to distinguish history from conflict.

---

## Command

    smalltalk check <dir>

---

## What it detects

    DECISION — same subject, two active entries with different choices
               e.g. "vercel>railway" in one file, "railway>vercel" in another

    RULE     — same subject, same rule flagged hard in one file and soft in another

    PATTERN  — same subject, same cause:, but different fix: values

    WIN      — same subject with repeat:y in one entry and repeat:n in another

    LINK     — same source entity, same exclusive relationship (e.g. rel:works-on),
               pointing to two different targets simultaneously

CRITICAL vs WARNING:
  CRITICAL — stability:permanent entries, or LINK exclusive-rel overlaps
  WARNING  — standard stable entries with diverging values

Temporal exclusion:
  Entries with ended: <= today are EXCLUDED from scanning.
  A superseded entry next to a new one is correct resolution — not a contradiction.

---

## Output format

Clean directory:

    OK  No active contradictions detected.
    (Historical entries with ended: are excluded from this scan.)

With conflicts:

    [CONFLICT] Found 2 contradiction(s)  (1 CRITICAL, 1 WARNING)

      1. [CRITICAL] LINK: kai | simultaneous-works-on  stability:stable
         Values: nova | orion
         brain.st:3  LINK: kai | rel:works-on | orion | valid_from:2026-01  << older
         brain.st:4  LINK: kai | rel:works-on | nova  | valid_from:2026-03  << newer

         Resolution:
           Close the older entry by adding `ended:2026-04` to:
               LINK: kai | rel:works-on | orion | valid_from:2026-01

      2. [WARNING] DECISION: deploy | diverging-choices  stability:stable
         Values: railway>vercel | vercel>railway
         brain.st:1  DECISION: deploy | vercel>railway | cost | 2026-01  << older
         brain.st:2  DECISION: deploy | railway>vercel | scale | 2026-04  << newer

         Resolution:
           Close the older entry by adding `ended:2026-04` to:
               DECISION: deploy | vercel>railway | cost | 2026-01

    ──────────────────────────────────────────
      ended: = resolution mechanism. Set it on the OLDER entry.
      Ended entries are excluded from future contradiction scans.

---

## Full resolution cycle (detect → resolve → confirm)

    Step 1:  smalltalk check <dir>
             Note the file + line number shown next to << older

    Step 2:  smalltalk kg invalidate <file> <line_no>
             This writes ended:YYYY-MM onto that line in the file

    Step 3:  smalltalk check <dir>
             Confirms the contradiction is cleared

Example:

    $ smalltalk check _brain/
    [WARNING] DECISION: deploy | diverging-choices
    decisions.st:7  DECISION: deploy | vercel>railway | cost | 2026-01  << older

    $ smalltalk kg invalidate _brain/decisions.st 7
    Invalidated entry in decisions.st:7
      Before: DECISION: deploy | vercel>railway | cost | 2026-01
      After:  DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04

    $ smalltalk check _brain/
    OK  No active contradictions detected.

---

## Critical rule

ended: is NEVER set by a clock or scheduler.
It is set ONLY when a contradiction is resolved.
Meaning: the older entry stays in the file as history. It is just excluded from active scans.
The audit trail is always preserved.

---

## MCP equivalents

    smalltalk_check(directory="<dir>")

    # Full autonomous cycle via MCP:
    smalltalk_check("<dir>")  →  note file + line_no
    smalltalk_kg_invalidate("<file>", line_no)
    smalltalk_check("<dir>")  →  confirm cleared
