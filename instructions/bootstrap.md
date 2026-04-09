# Bootstrap — Full Setup Guide

Bootstrap runs the complete Smalltalk setup sequence in one command.

## When to use

Run `bootstrap` once when orienting a new project or a freshly cloned repo.
It is safe to re-run — it skips steps that are already complete.

## The sequence

```
backup → mine → palace init → write CLAUDE.md
```

| Step | What it does | Required |
|---|---|---|
| backup | Copies all .md files to `.originals/` | Always |
| mine | Converts .md → .st via LLM | Needs API key |
| palace init | Generates `_index.st` navigation map | Always |
| CLAUDE.md | Writes global session hook to project root | Always |

## Commands

```bash
# Full setup
smalltalk bootstrap <dir> --api-key <key>

# Preview without making changes
smalltalk bootstrap <dir> --dry-run

# Without API key — runs backup, palace init, CLAUDE.md (skips mine)
smalltalk bootstrap <dir>

# Local Ollama (free, no API key required)
smalltalk bootstrap <dir> --base-url http://localhost:11434/v1 --api-key ollama --model llama3.1
```

## After bootstrap

1. Copy CLAUDE.md to `~/.claude/CLAUDE.md` for global session orientation:
   ```bash
   # macOS / Linux
   cp CLAUDE.md ~/.claude/CLAUDE.md

   # Windows PowerShell
   Copy-Item CLAUDE.md $env:USERPROFILE\.claude\CLAUDE.md
   ```

2. Register the MCP server:
   ```bash
   claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
   ```

3. Verify the setup:
   ```bash
   smalltalk status <dir>    # are .st files present?
   smalltalk wake-up <dir>   # what will the agent see?
   smalltalk check <dir>     # any contradictions?
   ```

## Directory conventions

Bootstrap detects the project root automatically:
- If target is named `_brain`, `brain`, or `skills` → parent directory = project root
- Otherwise → the target directory itself = project root

CLAUDE.md is written to the project root. If CLAUDE.md already exists it is
NOT overwritten — merge manually or delete first.

## Via MCP

```
smalltalk_bootstrap_info()
```

Returns this protocol as a string for agent consumption.
