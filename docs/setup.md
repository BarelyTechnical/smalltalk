# Per-Tool Setup Guide

How to wire Smalltalk into your specific AI tool.

---

## Claude Code

### MCP registration

```bash
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
```

**Windows / PowerShell** — quotes required:
```powershell
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
```

### Global session hook

Copy `examples/hooks/CLAUDE.md` to `~/.claude/CLAUDE.md`. This wires wake-up at session start and the closing ritual at session end — across every project, automatically.

```bash
# macOS / Linux
cp examples/hooks/CLAUDE.md ~/.claude/CLAUDE.md

# Windows PowerShell
Copy-Item examples\hooks\CLAUDE.md $env:USERPROFILE\.claude\CLAUDE.md
```

### Per-project hook

Run `smalltalk bootstrap <dir>` — it writes a `CLAUDE.md` into your project directory automatically.

### Verify

Open Claude Code and type:
```
load session context from _brain/
```

The agent should call `smalltalk_wake_up` and report active entries.

---

## Cursor

### MCP config

Add to `.cursor/mcp.json` (create if it doesn't exist):

```json
{
  "mcpServers": {
    "smalltalk": {
      "command": "python",
      "args": ["-m", "smalltalk.mcp_server"]
    }
  }
}
```

### `.cursorrules` snippet

Add to your `.cursorrules` file:

```
# Smalltalk orientation
Read .st files before .md files. .st is Smalltalk compressed format — load as session context.
At session start: call smalltalk_wake_up on _brain/ and smalltalk_diary_read for active agent.
At session end: run smalltalk instructions closing-ritual and follow it exactly.
Use smalltalk_navigate for domain queries. Use smalltalk_check before any deploy.
```

---

## Codex (OpenAI)

### MCP config

Add to your Codex MCP configuration:

```json
{
  "smalltalk": {
    "command": "python",
    "args": ["-m", "smalltalk.mcp_server"]
  }
}
```

### System prompt addition

Add to your Codex system prompt:

```
RULE: session-start | run-smalltalk-wake-up-before-asking-for-context | hard
RULE: session-end | write-decisions-patterns-wins-to-brain | hard
```

---

## Windsurf

### MCP config

Add to Windsurf's MCP settings:

```json
{
  "mcpServers": {
    "smalltalk": {
      "command": "python",
      "args": ["-m", "smalltalk.mcp_server"]
    }
  }
}
```

### Cascade instruction

Add to your global Cascade instructions:

```
At session start: call smalltalk_wake_up on _brain/ to load orientation.
Use smalltalk_navigate before searching by keyword.
At session end: follow smalltalk instructions closing-ritual.
```

---

## Antigravity

### Global rules

Add to `~/.gemini/CONTEXT.md`:

```
## Smalltalk orientation

At every session start:
1. Run smalltalk_wake_up on the _brain/ of the current project
2. Report active DECISION, RULE, and PATTERN entries
3. Do not ask for context that is already loaded

At session end:
1. Run the closing ritual via smalltalk instructions closing-ritual
2. Write decisions, patterns, and wins via smalltalk_diary_write
3. Run smalltalk_check to clear contradictions
```

### MCP registration

Register via Antigravity's MCP tool panel using:
```
python -m smalltalk.mcp_server
```

---

## Local Ollama (no Claude Code / Cursor)

Run the MCP server and connect from any MCP-compatible client:

```bash
python -m smalltalk.mcp_server
```

Or use the CLI directly in your workflow:

```bash
# Session start
smalltalk wake-up _brain/ | pbcopy   # macOS — paste into model context
smalltalk wake-up _brain/            # output to terminal — paste manually

# Session end
smalltalk diary write myagent "DECISION: auth | clerk>auth0 | sdk | 2026-04"
smalltalk check _brain/
```

---

## Verify any integration

After setup, test with these three commands:

```bash
smalltalk status _brain/     # are .st files present?
smalltalk wake-up _brain/    # see what the agent will load
smalltalk check _brain/      # are there any contradictions?
```

Then open your AI tool and ask it to load session context. A correctly oriented agent:
1. Calls `smalltalk_wake_up` without being asked
2. Reports active decisions and rules
3. Navigates with `smalltalk_navigate`, not raw search
4. Runs `smalltalk_check` before any deploy or production change
