# smalltalk wake-up

Extract compressed L1 context from a directory of .st files.
Designed for injection into a model's system prompt before any project session.
Only loads what is currently true — historical and future entries are excluded.

---

## Command

    smalltalk wake-up <dir>

    # Pipe to a file
    smalltalk wake-up ~/my-project/_brain > context.txt

    # Paste context.txt into your local model's system prompt

---

## What it loads

    stability:permanent  — always loaded first, regardless of type
    DECISION             — all active entries (not ended, not future)
    RULE                 — hard rules only  (soft excluded)
    PATTERN              — all active entries
    WIN                  — repeat:y only   (repeat:n excluded)

Excluded:
    ended: <= today      — historical/superseded entries
    valid_from: > today  — future facts not yet active
    soft RULE entries    — too numerous, load on demand

---

## Example output

    # Smalltalk wake-up — 6 current entries

    # permanent (always first)
    RULE: brand | never-change-without-legal-review | hard | stability:permanent

    # current
    DECISION: deploy  | railway>vercel | scale | 2026-04
    DECISION: auth    | clerk>auth0    | sdk-simplicity | 2026-02
    DECISION: db      | postgres>sqlite | concurrent-writes | 2026-01
    PATTERN: n-plus-one | broke:slow-list | cause:orm-lazy | fix:select-related | reuse:y
    WIN: palace-navigate | score-wing-then-room | 34pct-retrieval-boost | repeat:y

This is ~120 tokens. Compare to loading raw _brain/ markdown: 10,000–40,000 tokens.

---

## Temporal awareness

wake-up reads the same temporal fields as the checker:

    valid_from:2026-03   → excluded before March 2026 (future facts)
    ended:2026-01        → excluded (historical/superseded)
    stability:permanent  → always included, always first

This means wake-up context is always a snapshot of what is currently true —
never stale, never showing superseded decisions.

---

## Usage with local models (Llama, Mistral, Ollama)

    # 1. Generate
    smalltalk wake-up ~/brain > context.txt

    # 2. Add to system prompt before asking questions:
    #    "Here is my project context: [paste context.txt]"
    #    "Now: why did we choose postgres?"

---

## Usage with MCP-enabled tools

    smalltalk_wake_up(directory="<dir>")

Claude Code / Cursor / Antigravity will call this automatically at session start
when configured via the MCP server.

---

## Workflow integration

    After: smalltalk mine <dir>          — run wake-up to verify output
    After: smalltalk kg invalidate       — re-run wake-up to confirm old entry gone
    Before: any AI session               — paste as system prompt context
    Before: pushing to production        — verify no contradictions first (smalltalk check)
