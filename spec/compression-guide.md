# Compression Guide

How to convert any agent `.md` file to Smalltalk `.st` — manually or via CLI.

---

## What Gets Compressed vs What Stays Markdown

| File type | Compress? |
|---|---|
| Skill definitions (`SKILL.md`, `.cursorrules`, routing files) | Yes |
| Memory logs (`_brain/decisions/`, `patterns/`, `wins/`, etc.) | Yes |
| Agent specs and pipeline definitions | Yes |
| Design system and style guides | Yes |
| Config and environment mapping | Yes |
| Human-maintained context (`stack.md`, `CONTEXT.md`) | No — keep as `.md` |
| Rich reference docs loaded on demand | No — keep as `.md`, link via `REF` |
| READMEs and documentation | No — keep as `.md` |

**Rule:** if an agent loads it on every session start → compress it.
If an agent loads it only when a specific topic comes up → keep `.md`, link via `REF`.

---

## Prose to Type Mapping

Every sentence in a skill file maps to a type:

| Prose | Smalltalk type |
|---|---|
| "Use this when building X" | `USE` |
| "Always do X" / "Never do X" | `RULE` |
| "Step N: do X" | `STEP` |
| "See file Y for Z" | `REF` |
| "The stack is X + Y" | `STACK` |
| "Before shipping, verify X" | `CHECK` |
| "Avoid X, Y, Z" | `AVOID` |
| "The visual style is X" | `STYLE` |
| "The font is X" | `FONT` |
| "The colors are X" | `COLOR` |

If a prose block doesn't map to any type — it's scaffolding. Drop it.

---

## Keep Entries Short

Bad — prose preserved:
```
RULE: my-skill | you should always make sure to compose your components from simple primitives rather than building monolithic components | hard
```

Good — signal only:
```
RULE: my-skill | compose-from-primitives-not-monoliths | hard
```

If the agent needs more detail, it reads the original `.md` via `REF`.

---

## Handle Sub-Files With REF

If a skill references other files, compress those too and link with `REF`:

```
REF: my-skill | references/components.st | covers:component-catalog
```

Agent loads the top-level `.st` on session start.
Loads the `REF` target only when that topic is needed.

---

## LLM Conversion Prompt

```
Convert the following agent file to Smalltalk .st compressed format.

SYNTAX: TYPE: identifier | field | field | field
SEPARATORS: | field boundary  + multiple values  : key:value  > choice>rejected
VALUES: lowercase-hyphenated, no spaces inside field values

TYPES:
Universal:  RULE REF NOTE CONFIG CONTEXT DECISION PATTERN
Memory:     WIN CLIENT COMPONENT PROMPT
Skills:     SKILL USE PHASE STEP STACK CHECK AVOID SCRIPT STYLE FONT COLOR
Agents:     AGENT TASK TRIGGER OUTPUT ERROR

RULES:
- Output .st entries ONLY — no markdown, no prose, no code fences
- One line per entry
- Extract every rule, step, reference, and fact — drop scaffolding prose
- Sub-file references become REF: entries pointing to .st versions
- Keep values as short as unambiguous

[paste file here]
```

---

*See `spec/grammar.md` for the full type reference.*
