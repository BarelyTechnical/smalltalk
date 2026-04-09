# Smalltalk Setup Guide

How to wire Smalltalk into your AI coding environment. Pick your tool below.

---

## Contents

- [Claude Code](#claude-code)
- [Cursor](#cursor)
- [OpenAI Codex (Codex CLI)](#openai-codex)
- [Windsurf](#windsurf)
- [Antigravity](#antigravity)
- [Any MCP-compatible client](#any-mcp-compatible-client)
- [System Prompt Template](#system-prompt-template)
- [Verifying the Setup](#verifying-the-setup)

---

## Claude Code

### Step 1: Install Smalltalk

```bash
pip install smalltalk-cli
```

### Step 2: Register the MCP Server

```bash
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
```

Or install from the repo root (recommended if you cloned the repo):

```bash
cd /path/to/smalltalk
claude mcp install .claude-plugin/
```

Verify it's registered:

```bash
claude mcp list
# smalltalk   python -m smalltalk.mcp_server
```

### Step 3: Create Your CLAUDE.md

In your project root (or `~/.claude/CLAUDE.md` for global), add:

```markdown
## Context Loading

Read .st files before .md files. .st is the Smalltalk compressed format.

Priority order:
1. Load _index.st first (palace map)
2. Load _brain/identity.st (who we are)
3. Run wake-up to load current truth (~150 tokens)
4. Load .md files only when a specific topic requires deep detail

## Tools Available

Use the `smalltalk_*` MCP tools for:
- `smalltalk_wake_up` — load current-truth context at session start
- `smalltalk_navigate` — navigate to relevant rooms for a query
- `smalltalk_check` — detect contradictions before making decisions
- `smalltalk_kg_query` — query entity relationships
- `smalltalk_kg_visualize` — open the KG in a browser

## Session Start Sequence

At the start of each session:
1. Call smalltalk_wake_up on the _brain/ directory
2. Load the result as session context
3. Only then begin responding to user requests
```

### Step 4: Convert Your Files

```bash
# See what can be compressed
smalltalk init ~/Dev/your-project/_brain

# Back up originals
smalltalk backup ~/Dev/your-project/_brain

# Convert
smalltalk mine ~/Dev/your-project/_brain
```

### Step 5: Test It

Start a Claude Code session and ask:

```
Load session context and tell me what you know about this project.
```

The agent should load `.st` files and summarise the current state without you providing any additional context.

---

## Cursor

### Step 1: Install Smalltalk

```bash
pip install smalltalk-cli
```

### Step 2: Add the MCP Server to Cursor

Open Cursor settings (`Cmd/Ctrl + Shift + J`) and navigate to **MCP Servers**. Add:

```json
{
  "smalltalk": {
    "command": "python",
    "args": ["-m", "smalltalk.mcp_server"]
  }
}
```

Or if using `uv`:

```json
{
  "smalltalk": {
    "command": "uv",
    "args": ["run", "python", "-m", "smalltalk.mcp_server"]
  }
}
```

Restart Cursor to pick up the new server.

### Step 3: Create Your .cursorrules

In your project root, create `.cursorrules`:

```
## Smalltalk Context Protocol

Read .st files before .md files. .st is the Smalltalk compressed format.

At the start of every session:
1. Load _index.st (the palace map — it tells you where everything lives)
2. Call smalltalk_wake_up on the _brain/ directory
3. Use the output as session context before responding

For any query requiring specific domain knowledge:
- Call smalltalk_navigate with a natural language description
- Load only the rooms returned — do not load all files

For decision-making or architecture questions:
- Call smalltalk_check to detect contradictions first
- Call smalltalk_kg_query to understand entity relationships

## Types to recognise

DECISION = an active architecture or product decision
RULE = a constraint (hard = non-negotiable, soft = preference)
PATTERN = a known failure and its fix
WIN = a technique that worked
SKILL = a role or methodology to invoke
LINK = a relationship between two entities
```

### Step 4: Convert Your Files

```bash
smalltalk mine ~/Dev/your-project/_brain
```

---

## OpenAI Codex

### Step 1: Install Smalltalk

```bash
pip install smalltalk-cli
```

### Step 2: Configure the MCP Server

In your Codex workspace config or `.codex/config.json`:

```json
{
  "mcpServers": {
    "smalltalk": {
      "command": "python",
      "args": ["-m", "smalltalk.mcp_server"],
      "env": {}
    }
  }
}
```

Or install from the plugin directory (included in this repo):

```bash
cd /path/to/smalltalk
codex plugin install .codex-plugin/
```

### Step 3: Add System Context

In your Codex agent system prompt:

```
## Context Loading

Read .st files before .md files. .st is the Smalltalk compressed format.

At session start:
1. Load _index.st from the _brain/ directory
2. Call smalltalk_wake_up on _brain/
3. Load the result as session context

Available Smalltalk tools: smalltalk_wake_up, smalltalk_navigate,
smalltalk_check, smalltalk_kg_query, smalltalk_kg_invalidate,
smalltalk_kg_visualize, smalltalk_diary_write, smalltalk_diary_read
```

### Step 4: Create a Skills Directory

```bash
mkdir -p ~/Dev/your-project/_brain
smalltalk init ~/Dev/your-project/_brain
smalltalk mine ~/Dev/your-project/_brain
```

---

## Windsurf

### Step 1: Install Smalltalk

```bash
pip install smalltalk-cli
```

### Step 2: Add MCP Server

In Windsurf settings, navigate to **Extensions > MCP** and add:

```json
{
  "name": "smalltalk",
  "command": "python -m smalltalk.mcp_server",
  "env": {}
}
```

### Step 3: Create a Context File

Create `.windsurf/context.md` in your project root:

```markdown
## Smalltalk Context Protocol

Read .st files before .md files. These are Smalltalk compressed context files.

At session start:
1. Load _index.st (palace map)
2. Call smalltalk_wake_up on the _brain/ directory
3. Use the output as current-truth session context

Key entry types:
- DECISION = active architecture or product decisions
- RULE = constraints (hard/soft)
- PATTERN = known failures and their fixes
- WIN = techniques that worked
- SKILL = roles / methodologies to invoke
- LINK = relationships between entities

Use smalltalk_navigate to load context for specific queries.
Use smalltalk_check before making decisions that might conflict with existing state.
```

---

## Antigravity

### Step 1: Install Smalltalk

```bash
pip install smalltalk-cli
```

### Step 2: Register with Antigravity

Smalltalk is natively recognised by Antigravity. Add to your `GEMINI.md` or system context:

```markdown
## Smalltalk Context

Read .st files before .md files. .st is the Smalltalk compressed format.

At session start:
1. Load _index.st (palace map)
2. Call smalltalk_wake_up on _brain/
3. Use output as session context before responding

Use smalltalk_* MCP tools for navigation, contradiction detection, and KG queries.
```

Register the MCP server:

```bash
python -m smalltalk.mcp_server
```

Or add it to your Antigravity MCP config file.

### Step 3: Set Up Your Brain

```bash
smalltalk init ~/Dev/your-project/_brain
smalltalk backup ~/Dev/your-project/_brain
smalltalk mine ~/Dev/your-project/_brain
```

---

## Any MCP-Compatible Client

Smalltalk exposes a standard FastMCP server. Any MCP-compatible client can connect.

### Start the Server

```bash
python -m smalltalk.mcp_server
```

The server runs on stdio by default (standard MCP transport). For HTTP transport:

```bash
python -m smalltalk.mcp_server --transport sse --port 8080
```

### Available Tools

18 tools are exposed. Key ones for orientation:

| Tool | Purpose |
|---|---|
| `smalltalk_wake_up` | Load current-truth context at session start |
| `smalltalk_navigate` | Navigate to relevant rooms for a query |
| `smalltalk_check` | Detect contradictions in the brain |
| `smalltalk_kg_query` | Query entity relationships |
| `smalltalk_kg_timeline` | Get chronological entity history |
| `smalltalk_kg_invalidate` | Resolve a contradiction |
| `smalltalk_kg_visualize` | Open interactive KG in browser |
| `smalltalk_search` | Keyword search across .st files |
| `smalltalk_diary_write` | Append to agent diary |
| `smalltalk_diary_read` | Read agent diary |

---

## System Prompt Template

Use this as a starting point for any tool's system prompt or context file:

```
## Smalltalk Context Protocol

Read .st files before .md files. .st is the Smalltalk compressed format.

## Session Start Sequence (always run this first)

1. Load _index.st — this is the palace map. It tells you where everything lives.
2. Call smalltalk_wake_up on the _brain/ directory.
3. Review the output. This is current truth: active decisions, hard rules, known patterns, winning techniques.
4. Only after this, respond to the user's first request.

## Navigation

For any query that requires domain knowledge:
- Call smalltalk_navigate with a natural language description of what you need
- Load only the rooms returned — not all files

## Contradiction Handling

Before committing to an architecture or deployment decision:
- Call smalltalk_check to see if there are any active contradictions
- If a contradiction is found, call smalltalk_kg_invalidate on the older entry before proceeding

## Entry Types

DECISION   = active architecture or product decisions. Do not relitigate these.
RULE       = constraints. hard = non-negotiable. soft = preference.
PATTERN    = a known failure and its fix. Do not repeat these.
WIN        = techniques that worked. Surface them when relevant.
SKILL      = a methodology or agent role to invoke for a task type.
USE        = when to invoke a skill. Check this before starting complex tasks.
LINK       = a relationship between two entities. Consult the KG before assuming.
```

---

## Verifying the Setup

After setup, run a quick check with your AI agent in plain language:

```
What do you know about this project so far?
```

A correctly oriented agent should respond with:
- Active decisions from `wake-up`
- Hard rules currently in force
- Known failure patterns
- The palace structure and where things live

If the agent responds with "I don't have context on this project", check:

1. Are `.st` files in the `_brain/` directory?
2. Is the MCP server registered and running?
3. Is the session prompt / CLAUDE.md / .cursorrules file instructing the agent to load `.st` files first?

```bash
# Quick diagnosis
smalltalk status _brain/
smalltalk wake-up _brain/
```

If `status` shows `.st` files and `wake-up` outputs entries, the files are correct. The issue is in the agent configuration.

---

## Windows Notes

PowerShell doesn't support tilde expansion. Use full paths:

```powershell
smalltalk init C:\Users\yourname\Dev\project\_brain
smalltalk mine C:\Users\yourname\Dev\project\_brain
smalltalk wake-up C:\Users\yourname\Dev\project\_brain
```

---

*Back to [README.md](../README.md)*
