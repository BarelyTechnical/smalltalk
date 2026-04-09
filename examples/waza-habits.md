# Waza + Smalltalk

[Waza](https://github.com/tw93/Waza) packages 8 engineering habits — think, hunt, check, design, health, write, learn, read — as Claude Code slash commands built from 500+ hours of real sessions.

The problem: they only work in Claude Code. They're not portable. A local Ollama model, Cursor, Gemini CLI, or any other tool can't use them.

This file encodes all 8 habits as Smalltalk `.st` entries — SKILL, USE, RULE, PATTERN, and AVOID — so any model reads them at session start and operates with the same methodology.

---

## What the habits do

| Habit | When to invoke | What it enforces |
|---|---|---|
| **think** | Before writing code for any new feature | Plan and validate direction first. No code until user approves. |
| **hunt** | When debugging any error or unexpected behavior | Root cause in one sentence before touching any code. |
| **check** | After implementation or before merging | Diff review, auto-fix safe issues, run tests, verify before declaring done. |
| **design** | When building any UI, component, or page | Lock aesthetic direction before first component. Point of view required. |
| **health** | When agent ignores instructions or hooks misfire | Six-layer config audit: CLAUDE.md → rules → skills → hooks → subagents → verifiers. |
| **write** | When explicitly asked to write or edit prose | Strip AI patterns. Preserve everything unless told to cut. |
| **learn** | Researching an unfamiliar domain or preparing an article | Six-phase workflow: collect → digest → outline → fill in → refine → publish. |
| **read** | Given any URL or PDF to read | Fetch as clean Markdown, save, stop. Don't analyze unless asked. |

---

## Using the file

```bash
# Place it in your _brain/ and it loads with wake-up
cp waza-habits.st ~/Dev/my-project/_brain/

# Or reference it from your project .st file
REF: habits | _brain/waza-habits.st | covers:engineering-habits

# Your agent reads it and gets the full methodology
smalltalk wake-up _brain/
```

Or load it directly via MCP:

```
smalltalk_read_file("_brain/waza-habits.st")
```

---

## Why this works for local models

Waza's slash command approach requires Claude Code. The `.st` encoding doesn't need anything — it's text that any model reads.

A local 7B or 14B model that reads `waza-habits.st` at session start knows:

- Don't touch code until you've written a root cause hypothesis (`RULE: hunt`)
- List all API keys and dependencies upfront, not mid-task (`RULE: think`)
- Don't declare done until verification runs and passes (`RULE: check`)
- Check typography rules before writing a UI component (`RULE: design`)

These aren't instilled via fine-tuning. They're in the context window. The model follows them the same way it follows any instruction — because they're right there.

The difference: a model without these rules rediscovers the lesson the hard way every session. A model with them front-loads the discipline.

---

## What's in the file

99 entries covering all 8 habits:

- **8 SKILL entries** — one per habit, with `when:` trigger conditions and phase
- **19 USE entries** — exact trigger conditions each habit activates on
- **48 RULE entries** — the hard and soft rules extracted from each habit
- **17 PATTERN entries** — real failure modes from Waza's gotcha tables
- **7 AVOID entries** — cross-habit anti-patterns that span all sessions

Each entry is one line, model-agnostic, and readable by any agent on any platform.

---

## Credits

All 8 habits are tw93's work, refined over 500 hours across 300+ sessions and 7 projects. The `.st` encoding is the Smalltalk layer on top — same philosophy, different distribution format.

Original: [github.com/tw93/Waza](https://github.com/tw93/Waza)  
License: MIT
