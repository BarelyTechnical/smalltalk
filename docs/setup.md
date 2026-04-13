# Per-Tool Setup Guide

Smalltalk can integrate with your environment in two ways:
1. **Model Context Protocol (MCP)**: Smalltalk acts as a tool server containing 25+ capabilities that the AI can explicitly invoke (e.g. `smalltalk_wake_up`, `smalltalk_check`).
2. **Invisible Proxy (V4.1)**: Smalltalk acts as a silent interceptor. Point your AI's OpenAI Base URL to Smalltalk's proxy server (`http://localhost:8765/v1`), and Smalltalk will automatically resolve the brain context, inject orienting system prompts natively, and forward the request to the upstream model.

Here is the exact setup for your AI tool.

---

## Cursor / Windsurf
*Architecture: Invisible Proxy (Recommended) or MCP*

### The Proxy Route (Zero-config inside the IDE)
1. In a split terminal, start the smalltalk proxy for your project:
   ```bash
   smalltalk serve _brain/
   ```
2. Open Cursor/Windsurf Settings.
3. Locate **OpenAI Base URL** (or equivalent Custom Model Endpoint).
4. Set the URL to: `http://localhost:8765/v1`
5. *Now every chat interaction transparently passes through Smalltalk, enriching context automatically.*

### The MCP Route (If you prefer manual tool calling)
Add to `.cursor/mcp.json` or Windsurf's GUI MCP config:

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

---

## Continue (VS Code Extension)
*Architecture: Invisible Proxy*

Continue supports both MCP and direct API integration. The smalltalk proxy is best as it reduces the back-and-forth tool call token overhead.

1. Start the proxy in your terminal:
   ```bash
   smalltalk serve _brain/
   ```
2. In `~/.continue/config.json`, add this model profile:
   ```json
   "models": [
     {
       "title": "Smalltalk Brain",
       "provider": "openai",
       "model": "claude-3-5-sonnet", 
       "apiBase": "http://127.0.0.1:8765/v1"
     }
   ]
   ```
   *(Note: The `model` field should match the target model configuring in your `_brain/modelmap.st` / `routing.st` limits, otherwise the proxy defaults to what you configured during `smalltalk init`)*

---

## Claude Code
*Architecture: MCP*

### MCP registration

```bash
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
```

**Windows / PowerShell** — quotes around the command are required:
```powershell
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
```

### Global session hook

Create `~/.claude/CLAUDE.md`. This ensures Claude Code always checks the brain automatically across every project.
```bash
# macOS / Linux
cp examples/hooks/CLAUDE.md ~/.claude/CLAUDE.md

# Windows PowerShell
Copy-Item examples\hooks\CLAUDE.md $env:USERPROFILE\.claude\CLAUDE.md
```

---

## Google's Antigravity (Gemini)
*Architecture: MCP*

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

## Gemini CLI
*Architecture: MCP*

Google's Gemini CLI workflows handle MCP similarly through a declarative config or command flag.

If the CLI reads from a config file (like `.geminirc`):
```json
{
  "mcp_servers": {
    "smalltalk": "python -m smalltalk.mcp_server"
  }
}
```
*(If the CLI uses prompt injection, use the same system prompt hooks defined in the Antigravity section above).*

---

## Codex (OpenAI)
*Architecture: MCP*

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

## Local Ollama (Unwrapped)
*Architecture: Pure CLI or Proxy*

Run the MCP server and connect from any MCP-compatible client, OR use the proxy server if your local UI allows Custom OpenAI URLs:

```bash
# Proxy server
smalltalk serve _brain/ --port 8765
```

Or just use the CLI natively in your terminal workflow:

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

Then open your AI tool and ask it to load session context. A correctly oriented agent using MCP:
1. Calls `smalltalk_wake_up` without being asked
2. Reports active decisions and rules
3. Navigates with `smalltalk_navigate`, not raw search
4. Runs `smalltalk_check` before any deploy or production change

If using the **Proxy Architecture**, start chatting; Smalltalk will silently inject the `wake-up` context behind the scenes without the agent needing to manually fetch it.
