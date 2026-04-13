# Getting Started with Smalltalk

This guide takes you from zero to a fully oriented session in about 10 minutes.

---

## Prerequisites

- Python 3.9+
- An AI tool with MCP support (Claude Code, Cursor, Codex, Windsurf) — or any local model via Ollama
- An API key for conversion (OpenRouter, Anthropic, OpenAI, or Ollama for free local conversion)

---

## Step 1 — Install

```bash
pip install smalltalk-cli

# Verify
smalltalk --help
```

Or clone for the examples, hooks, and spec:

```bash
git clone https://github.com/BarelyTechnical/smalltalk.git
cd smalltalk && pip install -e .
```

---

## Step 2 — Register the MCP server

**Claude Code:**
```bash
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
```

> Windows / PowerShell: quotes are required.

**Cursor / Codex / Windsurf** — add to your MCP config file:
```json
{
  "smalltalk": {
    "command": "python",
    "args": ["-m", "smalltalk.mcp_server"]
  }
}
```

Verify the server is running:
```bash
python -m smalltalk.mcp_server
# Should start without errors
```

---

## Step 3 — Bootstrap your first project

Point Smalltalk at your project's knowledge directory (typically `_brain/` or `docs/`).

```bash
# With OpenRouter (recommended for first run)
smalltalk bootstrap ~/Dev/my-project/_brain \
  --api-key YOUR_OPENROUTER_KEY

# With Anthropic directly
smalltalk bootstrap ~/Dev/my-project/_brain \
  --base-url https://api.anthropic.com/v1 \
  --api-key YOUR_ANTHROPIC_KEY

# With Ollama (local, free, no API key)
smalltalk bootstrap ~/Dev/my-project/_brain \
  --base-url http://localhost:11434/v1 \
  --api-key ollama --model llama3.1

# Preview without converting anything
smalltalk bootstrap ~/Dev/my-project/_brain --dry-run
```

What bootstrap does:
1. **Backs up** all `.md` files to `.originals/`
2. **Converts** them to `.st` format via the LLM (skipping README, CONTEXT, stack.md)
3. **Indexes** the directory into a palace (`_index.st`)
4. **Writes** a `CLAUDE.md` snippet with wake-up and closing ritual instructions

---

## Step 4 — Add the global hook (optional but recommended)

Copy the hook template to wire Smalltalk into every Claude Code session globally:

```bash
# macOS / Linux
cp examples/hooks/CLAUDE.md ~/.claude/CLAUDE.md

# Windows PowerShell
Copy-Item examples\hooks\CLAUDE.md $env:USERPROFILE\.claude\CLAUDE.md
```

After this, every Claude Code session automatically:
- Runs `smalltalk_wake_up` at start
- Runs the closing ritual at end

---

## Step 5 — Verify

```bash
# Check the orientation output
smalltalk wake-up ~/Dev/my-project/_brain/

# Check for contradictions
smalltalk check ~/Dev/my-project/_brain/

# See the palace structure
smalltalk palace status ~/Dev/my-project/_brain/
```

If wake-up returns entries, you're oriented. If check returns OK, you're clean. You're ready.

---

## Step 6 — Run your first oriented session

Open Claude Code (or your AI tool) and ask:

> "Load session context from _brain/ and tell me the active decisions and rules."

A correctly oriented agent will:
1. Call `smalltalk_wake_up` on `_brain/`
2. Report active DECISION, RULE, and PATTERN entries
3. Know where to navigate for deeper context

---

## Step 7 — Run the closing ritual

At session end:

```bash
smalltalk instructions closing-ritual
```

Follow the protocol. Write at minimum:
- 1 `DECISION` if you chose a direction
- 1 `PATTERN` if anything broke
- 1 `WIN` if a technique worked well

The next session opens smarter than this one.

---

## What to compress, what to keep

| File type | Action |
|---|---|
| Skill definitions, routing files | Compress → `.st` |
| Decision logs, memory entries | Compress → `.st` |
| Agent specs, pipeline definitions | Compress → `.st` |
| Design system, style rules | Compress → `.st` |
| `README.md`, `CONTEXT.md`, `stack.md` | Keep as `.md` — not session context |
| Reference docs loaded on demand | Keep as `.md`, link via `REF` entry |
| Code, API schemas, configs | Never compress |

**Rule:** if the agent loads it every session → compress. If only when a specific topic comes up → keep `.md` and link via `REF`. If it must be syntactically exact → never compress.

---

## Auto-convert on save or commit

```bash
# Watch a directory — converts .md to .st on every save
smalltalk mine ~/Dev/my-project/_brain/ --watch

# Or install a git hook — converts on every commit
smalltalk install-hook ~/Dev/my-project/
```

---

## Next

- [Per-tool setup guide](setup.md) — Claude Code, Cursor, Codex, Windsurf, Antigravity
- [Local model philosophy](local-model-philosophy.md) — why local models work with Smalltalk
- [Grammar reference](../spec/grammar.md) — all entry types and fields
- [Closing ritual](../instructions/closing-ritual.md) — the full compounding protocol
