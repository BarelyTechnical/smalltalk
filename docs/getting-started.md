# Getting Started with Smalltalk

> PAG — Pre-loaded Augmented Generation.
> This guide takes you from zero to a fully oriented AI agent in under 10 minutes.

---

## What you're setting up

Smalltalk does three things:

1. **Compresses** your knowledge files (skills, agent specs, decisions, patterns) to `.st` format — 90% fewer tokens, same information.
2. **Orients** your AI agent at session start — it loads your domain knowledge before the first message.
3. **Grows** the brain over time — the closing ritual writes back what was learned each session.

By the end of this guide, your agent will start every session already knowing your stack, decisions, rules, and patterns — without you telling it.

---

## Step 0: Prerequisites

- Python 3.9 or higher
- One of: Claude Code, Cursor, Codex, Windsurf, Antigravity, or any MCP-compatible AI tool
- An API key for compression (OpenRouter, Anthropic, or a local Ollama — free)

Check Python:
```bash
python --version
# Python 3.9+
```

---

## Step 1: Install

### Option A — pip install (recommended for most users)

```bash
pip install smalltalk-cli
```

Verify:
```bash
smalltalk --help
```

You should see the command list. If not, check that Python's `Scripts/` folder is in your PATH.

---

### Option B — Clone the repo (recommended if you want examples)

Cloning gives you:
- All **example files** (`examples/skills/`, `examples/agents/`, `examples/knowledge-graph/`)
- The **CLAUDE.md hook template** (`examples/hooks/CLAUDE.md`)
- The **full spec** (`spec/grammar.md`, `spec/compression-guide.md`)
- Plugin folders for Claude Code and Codex

```bash
git clone https://github.com/ApexAutomate/smalltalk.git
cd smalltalk/smalltalk
pip install -e .
```

The `-e` (editable) flag means the CLI picks up any local changes immediately.

Verify:
```bash
smalltalk --version
```

---

## Step 2: Register the MCP Server

The MCP server gives your agent 20 tools — navigation, contradiction detection, KG queries, diary write, skill routing.

### Claude Code

```bash
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
```

> **Windows / PowerShell:** wrap in quotes exactly as shown — prevents PowerShell parsing the dashes as arguments.

Verify:
```bash
claude mcp list
# You should see: smalltalk   python -m smalltalk.mcp_server
```

Or, if you cloned the repo, install from the plugin folder (auto-discovers tools and SKILL.md):
```bash
cd path/to/smalltalk/smalltalk
claude mcp install .claude-plugin/
```

### Cursor

Open Cursor settings → **MCP Servers** → Add:
```json
{
  "smalltalk": {
    "command": "python",
    "args": ["-m", "smalltalk.mcp_server"]
  }
}
```

### Other tools
See [docs/setup.md](setup.md) for step-by-step guides for Codex, Windsurf, Antigravity.

---

## Step 3: Add the Global Hook

This is what makes your agent automatically wake up and run the closing ritual — on every project, without you prompting it.

### Claude Code — global CLAUDE.md

Create or edit `~/.claude/CLAUDE.md` (on Windows: `C:\Users\<you>\.claude\CLAUDE.md`):

```markdown
# Smalltalk — Global Session Protocol

## Session Start (always)
1. Check if the project has a `_brain/` or `_index.st`
2. If yes: run `smalltalk_wake_up` on `_brain/` — load DECISION, RULE, PATTERN, WIN context
3. If yes: run `smalltalk_diary_read` for the active agent id — load accumulated expertise
4. If a task is given: run `smalltalk_route` on skills/ for the task description
5. Load the top-scored skill files. Do not re-ask for context that's already in scope.

## Session End (hard rule — not optional)
RULE: session-end | write-decisions-patterns-wins-to-brain | hard
TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write

Before ending the session:
1. Write DECISION / PATTERN / WIN / ERROR entries via smalltalk_diary_write
2. Run smalltalk_check on _brain/
3. Resolve any contradictions via smalltalk_kg_invalidate

Entry format:
  DECISION: <subject> | <choice>><rejected> | <reason> | <YYYY-MM>
  PATTERN:  <subject> | broke:<what> | cause:<why> | fix:<what> | reuse:y/n
  WIN:      <subject> | <technique> | <outcome> | repeat:y/n

Full protocol: smalltalk instructions closing-ritual
```

A ready-to-copy version is in `examples/hooks/CLAUDE.md` if you cloned the repo.

### Cursor — .cursorrules

Add to your global or project `.cursorrules`:

```
Read .st files before .md files. .st is Smalltalk compressed format — load as session context.
At session start: call smalltalk_wake_up on _brain/ and smalltalk_route on skills/ for the task.
At session end: run smalltalk instructions closing-ritual and follow it exactly.
```

### Other tools

The same block works in any system prompt or context file. The agent reads it, the tools do the work.

---

## Step 4: Orient Your First Project

You have two options — manual (more control) or bootstrap (faster).

### Option A — Bootstrap (recommended)

One command does everything:

```bash
smalltalk bootstrap ~/Dev/my-project/_brain --api-key YOUR_KEY
```

This runs:
1. `backup` — copies all `.md` files to `.originals/`
2. `mine` — converts `.md` to `.st` using the LLM
3. `palace init` — generates `_index.st` (the palace map)
4. Writes a `CLAUDE.md` to the project root

Preview without making changes:
```bash
smalltalk bootstrap ~/Dev/my-project/_brain --dry-run
```

### Option B — Manual (step by step)

```bash
# 1. See what can be compressed
smalltalk init ~/Dev/my-project/_brain

# 2. Back up originals (always do this first)
smalltalk backup ~/Dev/my-project/_brain

# 3. Convert to .st format
smalltalk mine ~/Dev/my-project/_brain --api-key YOUR_KEY

# 4. Check conversion
smalltalk status ~/Dev/my-project/_brain

# 5. Generate the palace index
smalltalk palace init ~/Dev/my-project/_brain

# 6. Verify output
smalltalk wake-up ~/Dev/my-project/_brain
```

**Using a local model (no API key needed):**
```bash
# Ollama
smalltalk mine _brain/ \
  --base-url http://localhost:11434/v1 \
  --api-key ollama \
  --model llama3.1
```

**Windows / PowerShell — use full paths:**
```powershell
smalltalk bootstrap C:\Users\you\Dev\my-project\_brain --api-key YOUR_KEY
```

---

## Step 5: Keep It Updated Automatically

### Watch mode — convert new files on save

Leave this running in a terminal while you work:
```bash
smalltalk mine ~/Dev/my-project/_brain --watch
```

Any new or modified `.md` file is auto-converted within 3 seconds. No manual step.

### Git hook — convert on commit

Install once per repo:
```bash
smalltalk install-hook ~/Dev/my-project
```

After each commit, staged `.md` files are automatically mined and the `.st` files are staged for the next commit.

---

## Step 6: Verify It Works

Open a session with your AI tool and ask:

```
Load session context and tell me what you know about this project.
```

A correctly oriented agent will:
1. Call `smalltalk_wake_up` on `_brain/`
2. Report active decisions, hard rules, known patterns
3. Know where everything lives without being told
4. Not ask you for context that's already in the files

If it doesn't respond correctly, run the diagnostic:

```bash
smalltalk status _brain/     # confirms .st files exist
smalltalk wake-up _brain/    # shows what the agent will load
smalltalk check _brain/      # confirms no contradictions blocking it
```

Common issues:

| Symptom | Fix |
|---|---|
| Agent says "I don't have context" | Check `smalltalk status` — are `.st` files there? |
| MCP tools not available | Run `claude mcp list` — is smalltalk registered? |
| Agent doesn't wake up automatically | Check CLAUDE.md / .cursorrules — is the hook instruction there? |
| Windows: `smalltalk` not found | Add Python Scripts to PATH, or use `python -m smalltalk.cli` |
| Windows: MCP registration fails | Wrap command in quotes: `-- "python -m smalltalk.mcp_server"` |

---

## Step 7: Close the Loop (Closing Ritual)

> This is what makes the brain grow every session.

Add this rule to your context file (CLAUDE.md, .cursorrules, or system prompt):

```
RULE: session-end | write-decisions-patterns-wins-to-brain | hard
TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write
```

At the end of every session, the agent will:
1. Identify decisions made, patterns found, wins
2. Write them to the diary via `smalltalk_diary_write`
3. Run `smalltalk_check` to confirm no contradictions

Next session starts knowing everything from last session. The brain compounds.

Full protocol:
```bash
smalltalk instructions closing-ritual
```

---

## What You Have Now

```
Session start  → agent loads oriented context automatically (wake-up + route)
During work    → agent navigates using palace, checks contradictions
New files      → auto-converted (watch mode or git hook)
Session end    → agent writes back what was learned (closing ritual)
Next session   → starts smarter than the last
```

This is the full PAG loop — Pre-loaded Augmented Generation. Every session compounds. The brain grows by doing the work.

---

## Next Steps

- **Grammar reference:** `smalltalk instructions help` or `spec/grammar.md`
- **Tool-specific setup:** [docs/setup.md](setup.md)
- **Examples:** `examples/skills/`, `examples/agents/`, `examples/knowledge-graph/`
- **Skill routing:** `smalltalk route <dir> "<task description>"`
- **KG visualizer:** `smalltalk kg visualize <dir>`

---

*Back to [README.md](../README.md)*
