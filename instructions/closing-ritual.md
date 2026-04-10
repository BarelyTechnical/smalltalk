# Smalltalk — Closing Ritual

The closing ritual is what turns a session into compounding memory.

Without it: every session starts from the same brain.
With it: every session makes the next one smarter.

---

## When to run

At the end of every session — before closing the terminal or switching projects.

Trigger the ritual when:
- A task is complete
- A decision was made
- A bug was fixed
- Something worked unexpectedly well
- Something broke in an unexpected way

---

## The ritual (3 steps)

### Step 1 — Identify what happened

Before writing anything, answer these four questions:

1. Did I make a decision that chose one option over another?
2. Did I find a pattern — something that broke, why, and how to fix it?
3. Did I discover a technique that worked well enough to repeat?
4. Did I encounter an error that could recur?

Write one Smalltalk entry per answer. One line. No prose.

### Step 2 — Write entries via diary

```bash
# Decisions — chose one thing over another
smalltalk diary write <agent-id> "DECISION: auth | clerk>auth0 | sdk-simplicity | 2026-04"

# Patterns — something broke, why, how to fix
smalltalk diary write <agent-id> "PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y"

# Wins — techniques worth repeating
smalltalk diary write <agent-id> "WIN: palace | score-wing-then-room | 34pct-retrieval-boost | repeat:y"

# Errors — failures worth remembering
smalltalk diary write <agent-id> "ERROR: deploy | broke:env-vars | cause:missing-quotes | state:recovered"
```

Via MCP (for autonomous agents):
```
smalltalk_diary_write("reviewer", "DECISION: auth | clerk>auth0 | sdk-simplicity | 2026-04")
smalltalk_diary_write("reviewer", "PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y")
```

### Step 3 — Check for contradictions

```bash
smalltalk check _brain/
```

If contradictions are found:
```bash
smalltalk kg invalidate <file> <line_no>
smalltalk check _brain/   # confirm cleared
```

---

## Entry types

| What happened | Entry type | Example |
|---|---|---|
| Chose tech A over tech B | `DECISION` | `DECISION: deploy \| railway>vercel \| scale \| 2026-04` |
| Bug found (fixed) | `PATTERN` | `PATTERN: jwt \| broke:auth \| cause:missing-exp \| fix:add-exp-claim \| reuse:y` |
| Technique that worked | `WIN` | `WIN: palace \| score-wing-then-room \| 34pct-boost \| repeat:y` |
| Client preference noted | `CLIENT` | `CLIENT: kai \| pref:dark-mode \| avoid:animations \| updated:2026-04` |
| Bug found (unresolved) | `ERROR` | `ERROR: auth \| broke:token-refresh \| cause:unknown \| state:unresolved` |

---

## Hard rule

```
RULE: session-end | write-decisions-patterns-wins-to-brain | hard
TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write
```

Add this to your `CLAUDE.md` or system prompt. The bootstrap command writes it automatically.

---

## Wire it once — runs everywhere

The global hook template at `examples/hooks/CLAUDE.md` wires this automatically across every project:

```bash
# macOS / Linux
cp examples/hooks/CLAUDE.md ~/.claude/CLAUDE.md

# Windows PowerShell
Copy-Item examples\hooks\CLAUDE.md $env:USERPROFILE\.claude\CLAUDE.md
```

After that, every Claude Code session starts with `smalltalk_wake_up` and ends with the closing ritual — no manual trigger needed.

---

## What good looks like

At session end, you should have written at minimum:
- 1 DECISION if you chose a direction
- 1 PATTERN if anything broke
- 1 WIN if something worked well enough to repeat

Three lines. Two minutes. The agent that opens this project next week starts already knowing what you learned today.
