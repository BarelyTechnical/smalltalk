# smalltalk kg

Knowledge Graph — temporal entity relationships from .st files.
No database. No dependencies. Everything lives in .st files.

---

## Why it works differently from MemPalace

MemPalace KG uses SQLite for temporal triples.
Smalltalk's KG lives entirely in .st files — human-readable, git-trackable, zero dependencies.

Key difference: `ended:` is never set by a clock or scheduler.
It is set by CONTRADICTION RESOLUTION. This is the only correct update mechanism.

Draft new fact → contradiction detected → older entry gets ended: → brain is updated.

---

## The LINK type

```
LINK: source-entity | rel:relationship | target-entity | [valid_from:YYYY-MM] | [ended:YYYY-MM] | [stability:x]
```

Examples:

```
LINK: kai         | rel:works-on     | nova     | valid_from:2026-03 | stability:transient
LINK: auth        | rel:depends      | billing  | stability:stable
LINK: brand-color | rel:defined-as   | purple   | stability:permanent
LINK: kai         | rel:works-on     | orion    | valid_from:2026-01 | ended:2026-03 | stability:transient
```

---

## Stability levels

```
stability:permanent   Core truth. Always loaded in wake-up. Only closed via contradiction resolution.
stability:stable      Valid until explicitly ended. Default for most facts.
stability:transient   Time-windowed. Expected to change. Use for assignments, sprints, status.
```

Rule: once you mark something `stability:permanent`, changing it requires contradiction resolution.
The checker will flag it as CRITICAL.

---

## Temporal fields (optional on ANY entry type)

These fields work on LINK entries AND on any other .st entry type:

```
valid_from:2026-01     This fact became true in January 2026
ended:2026-03          This fact stopped being true in March 2026
```

DECISION example with temporal fields:
```
DECISION: auth | clerk>auth0 | easier-sdk | 2026-01 | stability:stable
DECISION: auth | auth0>clerk | legacy     | ended:2026-01
```

checker.py will NOT flag these as a contradiction — the second one has ended:.
wake_up.py will NOT load the ended entry.

---

## Full resolution cycle (detect → write → confirm)

This is the complete closed loop. Works for ALL entry types (LINK, DECISION, RULE, PATTERN, WIN).

**Step 1 — Detect:** run check to see what's in conflict
```bash
smalltalk check _brain/
```
Output:
```
[WARNING] DECISION: deploy | diverging-choices  stability:stable
  Values: railway>vercel | vercel>railway
  people.st:7  DECISION: deploy | vercel>railway | cost | 2026-01  << older
  people.st:8  DECISION: deploy | railway>vercel | scale | 2026-04  << newer

  Resolution:
    Close the older entry by adding `ended:2026-04` to:
        DECISION: deploy | vercel>railway | cost | 2026-01
```

**Step 2 — Resolve:** write ended: to the older entry using the file + line_no from Step 1
```bash
smalltalk kg invalidate people.st 7
# or with explicit date:
smalltalk kg invalidate people.st 7 --ended 2026-04
```
Output:
```
+ Invalidated entry in people.st:7

  Before: DECISION: deploy | vercel>railway | cost | 2026-01
  After:  DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04

  ended:2026-04 appended.
  Run smalltalk_check() to confirm the contradiction is cleared.
```

**Step 3 — Confirm:** re-run check
```bash
smalltalk check _brain/
# → OK  No active contradictions detected.
```

---

## Via MCP tools (agent workflow)

The same three-step cycle, fully automatable:

```
smalltalk_check("_brain/")
→ [WARNING] DECISION: deploy | diverging-choices
  people.st:7  ... << older

smalltalk_kg_invalidate("_brain/people.st", 7)
→ Invalidated entry in people.st:7
  Before: DECISION: deploy | vercel>railway | cost | 2026-01
  After:  DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04

smalltalk_check("_brain/")
→ OK  No active contradictions detected.
```

An agent can run the full cycle without human intervention. It reads the conflict,
identifies the older entry, calls invalidate on it, and confirms clearance.

---

## Querying the graph

Via CLI:
```bash
smalltalk kg query _brain/ kai
smalltalk kg query _brain/ kai --as-of 2026-02
smalltalk kg timeline _brain/ kai
```

Via MCP tools:
```
smalltalk_kg_query(directory, entity)               Current relationships
smalltalk_kg_query(directory, entity, as_of)        As of a specific date
smalltalk_kg_timeline(directory, entity)            Chronological story
```

Live example:
```
smalltalk_kg_query("_brain/", "kai")
→ KG: kai (as of 2026-04)
    Active (1):
      kai → works-on → nova  [transient]  since 2026-03
    Historical (1):
      kai → works-on → orion  [2026-01 – 2026-03]

smalltalk_kg_timeline("_brain/", "kai")
→ Timeline: kai
    2026-01  kai → works-on → orion  [closed 2026-03]
    2026-03  kai → works-on → nova   [active]
```

---

## Sources the KG reads automatically

| Entry type | How it maps |
|---|---|
| LINK: | Primary relationship source |
| TUNNEL: | Cross-wing connections (palace auto-detected) |
| REF: | File-level references and dependencies |

---

## Tips

- Use descriptive relation names: rel:works-on, rel:depends, rel:defines, rel:blocks, rel:reports-to
- Always add valid_from: to transient links (otherwise timeline is undated)
- Run `smalltalk check` after adding a new fact that might contradict an old one
- `stability:permanent` is for things like brand names, core business rules, non-negotiable decisions
- You can add `valid_from:` and `ended:` to ANY .st entry type, not just LINK
- `smalltalk kg invalidate` works on LINK, DECISION, RULE, PATTERN, WIN — anything check flags


---

## Why it works differently from MemPalace

MemPalace KG uses SQLite for temporal triples.
Smalltalk's KG lives entirely in .st files — human-readable, git-trackable, zero dependencies.

Key difference: `ended:` is never set by a clock or scheduler.
It is set by CONTRADICTION RESOLUTION. This is the update mechanism.

Draft new fact → contradiction detected → older entry gets ended: → brain is updated.

---

## The LINK type

```
LINK: source-entity | rel:relationship | target-entity | [valid_from:YYYY-MM] | [ended:YYYY-MM] | [stability:x]
```

Examples:

```
LINK: kai         | rel:works-on     | nova     | valid_from:2026-03 | stability:transient
LINK: auth        | rel:depends      | billing  | stability:stable
LINK: brand-color | rel:defined-as   | purple   | stability:permanent
LINK: kai         | rel:works-on     | orion    | valid_from:2026-01 | ended:2026-03 | stability:transient
```

---

## Stability levels

```
stability:permanent   Core truth. Always loaded in wake-up. Only closed via contradiction resolution.
stability:stable      Valid until explicitly ended. Default for most facts. (default if not specified)
stability:transient   Time-windowed. Expected to change. Use for assignments, sprints, status.
```

Rule: once you mark something `stability:permanent`, changing it requires contradiction resolution.
The checker will flag it as CRITICAL.

---

## Temporal fields (optional on ANY entry type)

These fields work on LINK entries AND on any other .st entry type:

```
valid_from:2026-01     This fact became true in January 2026
ended:2026-03          This fact stopped being true in March 2026
```

DECISION example with temporal fields:
```
DECISION: auth | clerk>auth0 | easier-sdk | 2026-01 | stability:stable
DECISION: auth | auth0>clerk | legacy     | ended:2026-01
```

checker.py will NOT flag these as a contradiction — the second one has ended:.
wake_up.py will NOT load the ended entry.

---

## How to replace a fact (the correct workflow)

1. A new fact contradicts an existing one:
   ```
   # Old (active, no ended:)
   LINK: brand-color | rel:defined-as | purple | stability:permanent

   # New contradicting entry
   LINK: brand-color | rel:defined-as | green  | stability:permanent
   ```

2. Run `smalltalk check` — it will flag this as CRITICAL (permanent contradiction).

3. Resolve: add `ended:YYYY-MM` to the OLD entry:
   ```
   LINK: brand-color | rel:defined-as | purple | stability:permanent | ended:2026-08
   LINK: brand-color | rel:defined-as | green  | stability:permanent
   ```

4. Run `smalltalk check` again — no conflicts. wake-up now only loads green.

---

## Querying the graph

Via CLI:
    (coming soon — use MCP tools for now)

Via MCP tools:
    smalltalk_kg_query(directory, entity)               Current relationships
    smalltalk_kg_query(directory, entity, as_of)        As of a specific date
    smalltalk_kg_timeline(directory, entity)            Chronological story

Live example:
    smalltalk_kg_query("_brain/", "kai")
    → KG: kai (as of 2026-04)
        Active (1):
          kai → works-on → nova  [transient]  since 2026-03
        Historical (1):
          kai → works-on → orion  [2026-01 – 2026-03]

    smalltalk_kg_timeline("_brain/", "kai")
    → Timeline: kai
        2026-01  kai → works-on → orion  [closed 2026-03]
        2026-03  kai → works-on → nova   [active]

---

## Sources the KG reads automatically

| Entry type | How it maps |
|---|---|
| LINK: | Primary relationship source |
| TUNNEL: | Cross-wing connections (palace auto-detected) |
| REF: | File-level references and dependencies |

---

## Tips

- Use descriptive relation names: rel:works-on, rel:depends, rel:defines, rel:blocks, rel:reports-to
- Always add valid_from: to transient links (otherwise timeline is undated)
- Run `smalltalk check` after adding a new fact that might contradict an old one
- `stability:permanent` is for things like brand names, core business rules, non-negotiable decisions
- You can add `valid_from:` and `ended:` to ANY .st entry type, not just LINK
