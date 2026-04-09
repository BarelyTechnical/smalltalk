<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/smalltalk-dark.svg">
  <img src="docs/smalltalk-light.svg" alt="smalltalk" width="400">
</picture>

# Smalltalk

**PAG — Pre-loaded Augmented Generation.**

*RAG finds the answer. PAG already knows it.*

---

RAG retrieves knowledge when asked. There is always a query, a search step, an embedding lookup, a retrieval failure mode.

Smalltalk eliminates the retrieval step entirely.

The agent loads your decisions, rules, patterns, and skills at session start — before the first message. It doesn't search for what it needs. It already has it.

> [!IMPORTANT]
> This is not a memory tool. It is an orientation layer. The difference: memory stores what happened. Orientation changes how the agent *starts*.

---

## The Problem With RAG for Persistent Knowledge

RAG is the right tool for large document corpora — "search these 10,000 PDFs." It's the wrong tool for persistent domain knowledge — "know my stack, my decisions, my rules, and my active state."

For persistent knowledge, RAG has real failure modes:

- Wrong chunk retrieved — low similarity score, wrong context loaded
- Hallucinated entity extraction — the mining step introduces noise
- Infrastructure cost — vector DB, embedding model, query pipeline, all required
- Still reactive — the agent starts blank and retrieves when asked

Smalltalk has none of these failure modes. There is no retrieval happening. You either loaded the `.st` file or you didn't.

---

## How It Works

Compress your skill files, memory logs, agent specs, and decision records into `.st` format — typed, pipe-delimited, one line per entry.

```st
DECISION: deploy  | railway>vercel     | scale+cost      | 2026-04
RULE:     brand   | no-purple-gradient | hard
PATTERN:  jwt     | broke:auth         | cause:missing-exp | fix:add-exp-claim | reuse:y
SKILL:    seo     | when:any-web-build | stack:schema+meta
WIN:      palette  | score-wing-room   | 34pct-boost      | repeat:y
```

A 200-line skill file becomes 20 lines. A full `_brain/` in prose becomes a few hundred tokens. The model reads it without a decoder — any LLM, any platform.

At session start, the agent loads the `.st` files. It already knows your world. It doesn't discover it.

---

## The Numbers

| | Without Smalltalk | With Smalltalk |
|---|---|---|
| One skill file | ~1,800 tokens | ~180 tokens |
| Full `_brain/` | ~20,000–50,000 tokens | ~2,000–5,000 tokens |
| Session start cost | varies, often high | ~300–500 tokens (fixed) |
| Retrieval failures | possible | none — no retrieval |
| Compounds over time | no | yes |
| Requires infrastructure | no (RAG does) | no — plain files |

---

## The Closing Loop

PAG is only half the system.

**Read side** — `wake-up` loads what's currently true at session start. Works now.

**Write side** — the closing ritual writes back what was learned. This is what makes the brain grow.

```
Session start → load oriented context → do work →
closing ritual → write DECISION + PATTERN + WIN entries →
next session starts smarter than the last
```

Without the closing ritual: every session starts from the same brain.  
With it: every session compounds. The brain grows by doing the work.

```bash
# At session end — the agent writes back
smalltalk diary write reviewer "DECISION: auth | clerk>auth0 | sdk-simplicity | 2026-04"
smalltalk diary write reviewer "PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y"
smalltalk check _brain/

# Or via MCP (autonomous agents)
smalltalk_diary_write("reviewer", "WIN: clerk-setup | one-sdk-all-platforms | repeat:y")
smalltalk_check("_brain/")
```

The rule that closes the loop — add this to your `CLAUDE.md` or system prompt:

```
RULE: session-end | write-decisions-patterns-wins-to-brain | hard
TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write
```

Full protocol: `smalltalk instructions closing-ritual`

> **This is what makes Smalltalk different from everything else.**
> RAG gets better when you add documents. Fine-tuning gets better when you retrain.
> A Smalltalk agent with a closing ritual gets better by doing the work.

---

## Oriented vs Unoriented — In Practice

**Without Smalltalk:**
> "Build me a plumbing demo for Drip Masters."

The agent starts blank. Guesses which skill applies. Loads files. Reads them. Infers the rules. Burns token budget on discovery before writing a single line.

**With Smalltalk:**

The agent already knows — before your message finishes — that this job triggers `seo-expert`, `ui-designer`, `conversion-copy`, and `web-dev` skills. It navigates directly to those rooms. No discovery. No guessing. No wasted tokens.

An oriented 70B model outperforms an unoriented 405B model on your specific domain. The difference is not intelligence. It's the absence of wasted discovery.

---

## Quick Start

> **Full guide with screenshots, troubleshooting, and all tools:** [docs/getting-started.md](docs/getting-started.md)

### 1. Install

```bash
# Option A — pip (CLI + MCP server)
pip install smalltalk-cli

# Option B — clone (also gets examples, hook templates, spec, plugin files)
git clone https://github.com/ApexAutomate/smalltalk.git
cd smalltalk/smalltalk
pip install -e .
```

### 2. Register the MCP server

```bash
# Claude Code
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"

# Cursor: Settings → MCP Servers → add:
# {"smalltalk": {"command": "python", "args": ["-m", "smalltalk.mcp_server"]}}
```

> **Windows / PowerShell:** quotes are required — `-- "python -m smalltalk.mcp_server"`

### 3. Add the global session hook

Copy `examples/hooks/CLAUDE.md` to `~/.claude/CLAUDE.md`.

This wires automatic wake-up at session start and the closing ritual at session end — across every project.

```bash
# macOS / Linux
cp examples/hooks/CLAUDE.md ~/.claude/CLAUDE.md

# Windows PowerShell
Copy-Item examples\hooks\CLAUDE.md $env:USERPROFILE\.claude\CLAUDE.md
```

### 4. Orient your first project

```bash
# One command — backup → mine → palace init → writes CLAUDE.md to project
smalltalk bootstrap ~/Dev/my-project/_brain --api-key YOUR_KEY

# Local Ollama (free, no API key needed)
smalltalk bootstrap ~/Dev/my-project/_brain \
  --base-url http://localhost:11434/v1 \
  --api-key ollama --model llama3.1

# Preview without making changes
smalltalk bootstrap ~/Dev/my-project/_brain --dry-run
```

### 5. Keep files updated automatically

```bash
# Watch a directory — auto-convert on save
smalltalk mine ~/Dev/my-project/_brain --watch

# Or: auto-convert on every git commit (one-time install per repo)
smalltalk install-hook ~/Dev/my-project
```

### 6. Verify

Open your AI tool and ask:
```
Load session context and tell me what you know about this project.
```

A correctly oriented agent calls `smalltalk_wake_up`, reports active decisions and rules, and knows where everything lives without being told. If it doesn't, run:

```bash
smalltalk status _brain/    # are .st files there?
smalltalk wake-up _brain/   # what will the agent see?
smalltalk check _brain/     # any contradictions?
```

> [!TIP]
> Per-tool setup guides (Claude Code, Cursor, Codex, Windsurf, Antigravity): [docs/setup.md](docs/setup.md)

---

## The Grammar

```
TYPE: identifier | field | field | field
```

| Symbol | Meaning | Example |
|---|---|---|
| `\|` | Field separator | |
| `+` | Multiple values | `when:next+vite+remix` |
| `:` | Key-value pair | `broke:token-refresh` |
| `>` | Choice over alternative | `railway>vercel` |

Values: lowercase-hyphenated. One line per entry. Append — never overwrite.

### Universal Types
```st
RULE:     id | description | hard|soft
DECISION: id | choice>rejected | reason | date
PATTERN:  id | broke:what | cause:why | fix:what | reuse:y/n
REF:      id | path/to/file.st | covers:topic
NOTE:     id | observation
CONFIG:   id | key | value
```

### Memory Types
```st
WIN:       id | technique | outcome | repeat:y/n
CLIENT:    id | pref:what | avoid:what | updated:date
COMPONENT: id | stack | does:what | use-when
PROMPT:    id | task-type | approach | why-worked | reuse:y/n
```

### Knowledge Graph
```st
LINK:   source | rel:relationship | target | [valid_from:YYYY-MM] | [ended:YYYY-MM] | [stability:x]
TUNNEL: wing-id | connects:wing-id | via:shared-topic
```

Temporal fields work on **any** entry type:
```
valid_from:YYYY-MM    when this fact became true
ended:YYYY-MM         when this fact stopped being true (set by contradiction resolution only)
stability:permanent   always load — never auto-expire
stability:stable      valid until explicitly ended (default)
stability:transient   time-windowed — assignments, sprints, current status
```

### Skill Types
```st
SKILL:  id | triggers | stack | version
USE:    id | when:context
PHASE:  id | number | name | what-happens
STEP:   id | phase | number | action | required|optional
STACK:  id | layer | tool | why
CHECK:  id | verification-item | required|optional
AVOID:  id | antipatterns+separated
SCRIPT: id | path/to/script | what-it-does
```

### Agent Types
```st
AGENT:   id | role | capabilities | scope
TASK:    id | action | target | priority:high|mid|low
TRIGGER: id | event | condition | then:action
OUTPUT:  id | type | destination | format
ERROR:   id | broke:what | cause:why | state:recovered|unresolved
```

Full spec: [`spec/grammar.md`](spec/grammar.md)

---

## Two-Tier Loading

Keeps session cost low without losing depth.

**Tier 1 — Session start (always, ~150–300 tokens)**
Agent loads `.st` files. Full orientation. Fixed cost.

**Tier 2 — On demand (targeted)**
When depth is needed, agent reads the original `.md` via its `REF` link.

```st
REF: ui-skill | references/components.md | covers:component-catalog
```

You never pay for both upfront.

---

## Wake-Up

Every session, extract only what is currently true:

```bash
smalltalk wake-up ~/Dev/_brain/
```

Output (~120 tokens):
```st
# Smalltalk wake-up — 5 current entries

# permanent (core truth)
RULE: brand | never-change-without-legal-review | hard | stability:permanent

# current
DECISION: deploy  | railway>vercel | scale | 2026-04
DECISION: auth    | clerk>auth0    | sdk-simplicity | 2026-02
PATTERN:  jwt     | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y
WIN:      palace  | score-wing-then-room | 34pct-retrieval-boost | repeat:y
```

Entries with `ended:` are excluded automatically. Permanent facts load first.

Compare to loading raw `_brain/` markdown: 10,000–40,000 tokens.

---

## Knowledge Graph

A temporal entity-relationship graph built entirely from `.st` files. No database. No vector store. Human-readable, git-trackable.

```st
LINK: kai         | rel:works-on  | nova     | valid_from:2026-03 | stability:transient
LINK: kai         | rel:works-on  | orion    | valid_from:2026-01 | ended:2026-03
LINK: auth        | rel:depends   | billing  | stability:stable
LINK: brand-color | rel:defined-as | indigo  | stability:permanent
```

History is never deleted. `ended:` closes the fact. The past stays readable.

```bash
smalltalk kg query _brain/ kai           # active + historical
smalltalk kg timeline _brain/ kai        # chronological story
smalltalk kg visualize _brain/           # interactive graph in browser
```

---

## Palace Navigation

Structures `.st` files into wings, rooms, and tunnels. Agents navigate — they don't scan.

```
_brain/
├── _index.st          ← palace map (auto-generated)
├── decisions.st
├── patterns.st
└── projects/
    ├── nova.st
    └── auth.st
```

```bash
smalltalk palace init _brain/
smalltalk palace index _brain/     # refresh after adding files
```

Navigate with a natural language query:
```bash
smalltalk navigate _brain/ "auth decisions"
# → _brain/decisions.st  (score: high)
# → _brain/projects/auth.st  (score: medium)
```

34%+ better retrieval than flat-file scanning. `_index.st` session cost: ~150 tokens.

---

## Contradiction Detection

Rules-based. No LLM required.

```bash
smalltalk check _brain/
```

Detects: `DECISION` diverging choices, `RULE` strength conflicts, `PATTERN` conflicting fixes, `WIN` repeat disagreements, `LINK` simultaneous exclusivity violations.

Resolution cycle:
```bash
smalltalk check _brain/
# [WARNING] DECISION: deploy | diverging-choices
# decisions.st:3  DECISION: deploy | vercel>railway | 2026-01  << older

smalltalk kg invalidate _brain/decisions.st 3
# Appends | ended:2026-04 to line 3

smalltalk check _brain/
# OK  No active contradictions detected.
```

Agents running via MCP run this cycle autonomously — detect, invalidate, confirm.

---

## MCP Server — 20 Tools

```bash
python -m smalltalk.mcp_server
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
```

| Tool | What it does |
|---|---|
| `smalltalk_status` | Overview — file count, entries, types |
| `smalltalk_get_spec` | Full grammar type reference |
| `smalltalk_list_files` | List .st files with entry counts |
| `smalltalk_read_file` | Read a .st file |
| `smalltalk_search` | Keyword search across .st files |
| `smalltalk_wake_up` | Extract L1 context for session start |
| `smalltalk_route` | **NEW** — route task to most relevant skill/agent files |
| `smalltalk_check` | Contradiction detection |
| `smalltalk_palace_init` | Generate `_index.st` |
| `smalltalk_palace_index` | Refresh `_index.st` |
| `smalltalk_navigate` | Load relevant rooms for a domain query |
| `smalltalk_list_wings` | List palace wings |
| `smalltalk_list_rooms` | List rooms in a wing |
| `smalltalk_kg_query` | Entity relationships current or point-in-time |
| `smalltalk_kg_timeline` | Chronological story of an entity |
| `smalltalk_kg_invalidate` | Write `ended:` to resolve a contradiction |
| `smalltalk_kg_visualize` | Interactive KG graph HTML |
| `smalltalk_diary_write` | Write closing ritual entry |
| `smalltalk_diary_read` | Read agent diary |
| `smalltalk_bootstrap_info` | **NEW** — bootstrap protocol for new projects |

---

## CLI Reference

```bash
# First time setup — one command
smalltalk bootstrap <dir>                   # backup → mine → palace init → CLAUDE.md
smalltalk bootstrap <dir> --api-key <key>
smalltalk bootstrap <dir> --dry-run         # preview without changes

# Standard workflow
smalltalk init <dir>                        # scan — see what's convertible
smalltalk backup <dir>                      # copy originals to .originals/
smalltalk mine <dir>                        # convert .md to .st
smalltalk mine <dir> --watch               # auto-convert on file change (Ctrl+C to stop)
smalltalk mine <dir> --watch --interval 5  # poll every 5s
smalltalk mine <dir> --dry-run             # preview without converting
smalltalk mine <dir> --base-url http://... # OpenAI-compatible endpoint (Ollama etc.)
smalltalk status <dir>                     # conversion progress

# Session start
smalltalk wake-up <dir>                    # L1 context for system prompt injection
smalltalk route <dir> "<task>"             # which skills/agents to load for this task
smalltalk route <dir> "<task>" --top 3

# Contradiction detection
smalltalk check <dir>

# Knowledge Graph
smalltalk kg query <dir> <entity>
smalltalk kg query <dir> <entity> --as-of YYYY-MM
smalltalk kg timeline <dir> <entity>
smalltalk kg invalidate <file> <line_no>
smalltalk kg visualize <dir>

# Palace
smalltalk palace init <dir>
smalltalk palace index <dir>
smalltalk palace status <dir>

# Diary (closing ritual)
smalltalk diary write <agent-id> "<entry>"
smalltalk diary read  <agent-id>

# Git hook — auto-mine on commit
smalltalk install-hook <dir>               # installs .git/hooks/post-commit
smalltalk install-hook <dir> --force       # overwrite existing hook

# Instructions (for agents)
smalltalk instructions <command>           # help | mine | kg | palace | check
                                           # closing-ritual | bootstrap | route
```

**Windows / PowerShell:** use full paths, tilde expansion doesn't work.  
**MCP registration on Windows:**
```powershell
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
# Wrap in quotes — prevents PowerShell parsing dashes as params
```

**Global CLAUDE.md hook template:**  
`examples/hooks/CLAUDE.md` — copy to `~/.claude/CLAUDE.md` for automatic session orientation on every project.

---

## Requirements

- Python 3.9+
- `typer>=0.9.0`, `httpx>=0.27.0`, `rich>=10.11.0`, `mcp>=1.0.0`
- API key only needed for `mine`. Reading `.st` files needs nothing beyond the agent and the file.

```bash
pip install smalltalk-cli
```

---

## Credits

Smalltalk is a direct evolution of the **AAAK dialect** from [MemPalace](https://github.com/MemPalace/mempalace).

MemPalace pioneered the insight that LLMs read structured compressed text natively — no fine-tuning, no decoder, no special API. The AAAK shorthand proved that `DECISION: auth | clerk>auth0 | easier-sdk | 2026-01` is understood as fluently as a paragraph, at 90% fewer tokens. MemPalace also introduced the Palace metaphor (rooms, wings, halls) as a navigation layer for compressed agent memory.

Smalltalk extends this into a full production system:
- Formal, versioned grammar spec covering all agent file types
- Temporal Knowledge Graph built entirely from `.st` files
- Contradiction detection and autonomous resolution cycles
- MCP server (18 tools) integrating with any modern AI coding tool
- Full CLI for compression, search, navigation, and visualisation
- The closing ritual — the write side that closes the PAG loop

If MemPalace is the proof of concept, Smalltalk is the production system.

---

## License

MIT

---

*Smalltalk v3.0.1 — the best context is the context that's already there.*
