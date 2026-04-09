# Smalltalk

**A cognitive orientation layer for AI agents. Not just compression.**

Most agents are reactive. Every session starts from zero. The model knows *how* to do things, but not *where* your things live, *what* was decided, or *when* to invoke which tool.

So it greps. It loads files and reads them to figure out what they mean. It guesses which skill applies. It rediscovers state that was fully resolved yesterday. It burns thousands of tokens before writing a single line of code.

> [!IMPORTANT]
> Smalltalk changes this. It shifts the cognitive posture from **reactive** to **oriented**.

An oriented agent already knows your stack decisions, your brand rules, your current deployments, your failure patterns, and which skill to invoke for each task type — before the first token of user input.

---

## How It Works

Smalltalk is built on four components:

**Grammar**
A typed, pipe-delimited, one-line-per-entry format. `DECISION`, `RULE`, `PATTERN`, `SKILL`, `AGENT`, `LINK`. Each type carries semantic meaning that any LLM reads without a decoder. A 200-line skill file becomes 20 lines. A full `_brain/` in prose becomes a few hundred tokens of structured, queryable facts.

**Knowledge Graph**
A temporal entity-relationship graph built entirely from `.st` files. No database. No vector store. The KG maps who works on what, what depends on what, what changed and when. The model reads it — it doesn't discover it.

**The Palace**
A wing/room/tunnel navigation layer. Instead of scanning everything flat, the agent navigates to what's relevant. `_index.st` is the map. `navigate()` is the route. The model goes directly. It doesn't search.

**Tooling**
A Python CLI and MCP server exposing 18 tools. Integrates with Claude Code, Cursor, Codex, Windsurf, Antigravity, and any MCP-compatible client.

---

## The Numbers

| Without Smalltalk | With Smalltalk |
|---|---|
| grep / search to find context | palace navigate — direct retrieval |
| infer which tool or skill to use | `SKILL` + `USE` entries declare it |
| rediscover current state every session | `wake-up` delivers it in ~150 tokens |
| relitigate past decisions | `DECISION` entries carry them forward |
| repeat resolved failures | `PATTERN` entries surface fixes instantly |
| scan everything flat | load only the relevant room |

| Metric | Unoriented | Smalltalk |
|---|---|---|
| One skill file | ~1,800 tokens | ~180 tokens |
| Full `_brain/` | ~20,000-50,000 tokens | ~2,000-5,000 tokens |
| Session start cost | varies, often high | ~300-500 tokens (fixed) |
| Compounds over time | no | yes |

---

## Quick Start

```bash
pip install smalltalk-cli

# See what's convertible
smalltalk init ~/Dev/skills

# Back up originals
smalltalk backup ~/Dev/skills

# Convert to .st
smalltalk mine ~/Dev/skills

# Check compression state
smalltalk status ~/Dev/skills
```

`mine` uses OpenRouter by default. Swap in any OpenAI-compatible endpoint:

```bash
# Anthropic
smalltalk mine ~/Dev/skills \
  --base-url https://api.anthropic.com/v1 \
  --api-key YOUR_KEY

# Local Ollama (free, no API key)
smalltalk mine ~/Dev/skills \
  --base-url http://localhost:11434/v1 \
  --api-key ollama \
  --model llama3.1
```

Then add one line to your `CLAUDE.md`, `GEMINI.md`, or system prompt:

```
Read .st files before .md files. .st is the Smalltalk compressed format.
Load as session context. Load .md references only when a specific topic
requires deep detail.
```

> [!TIP]
> See the full setup guide for Claude Code, Cursor, Codex, and Windsurf: [docs/setup.md](docs/setup.md)

---

## The Grammar

Every entry follows one pattern:

```
TYPE: identifier | field | field | field
```

| Symbol | Meaning | Example |
|---|---|---|
| `TYPE` | Uppercase semantic prefix | `DECISION`, `RULE`, `SKILL` |
| `identifier` | Subject this entry belongs to | `auth`, `deploy`, `ui-skill` |
| `\|` | Field separator | |
| `+` | Multiple values in one field | `when:next+vite+remix` |
| `:` | Key-value pair | `broke:token-refresh` |
| `>` | Choice over alternative | `railway>vercel` |

**Before (markdown, 7 lines for 3 rules)**

```markdown
## Best Practices

1. **Component Composition**: Build complex UIs from simple, composable
   primitives rather than monolithic components.
2. **Mobile-First**: Start with mobile styles, layer up with responsive
   variants. Never desktop-first.
3. **No Dynamic Classes**: Avoid dynamically constructed Tailwind class
   names — they get purged at build time.
```

**After (Smalltalk, 3 lines, same rules)**

```st
RULE: ui-skill | compose-from-primitives-not-monoliths | hard
RULE: ui-skill | mobile-first-always | hard
RULE: ui-skill | no-dynamic-class-names | hard
```

### Two-Tier Loading

`.st` files unlock a loading pattern that keeps session cost low without losing depth:

**Tier 1 — Session start (always, cheap)**
Agent loads `.st` files. Full orientation context in ~180 tokens instead of ~1,800.

**Tier 2 — On demand (targeted)**
When depth is needed, agent reads the original `.md` via its `REF` link:

```st
REF: ui-skill | references/components.st | covers:component-catalog
```

> [!NOTE]
> Tier 1 is broad and cheap. Tier 2 is targeted and on demand. You never pay for both upfront.

---

## Memory System

Facts are stored as typed entries — not raw conversation logs. Structured, queryable, temporally-aware records.

```st
DECISION: deploy | railway>vercel | scale | 2026-04
PATTERN:  auth   | broke:token-refresh | cause:missing-exp | fix:add-exp-claim | reuse:y
WIN:      palace-navigate | score-wing-then-room | 34pct-retrieval-boost | repeat:y
RULE:     brand  | never-change-without-legal-review | hard | stability:permanent
```

### Wake-Up

Every session, load only what's currently true:

```bash
smalltalk wake-up ~/Dev/_brain/
```

Output looks like this (~150 tokens):

```st
# Smalltalk wake-up: 4 current entries

# permanent (always first)
RULE: brand | never-change-without-legal-review | hard | stability:permanent

# current
DECISION: deploy | railway>vercel | scale | 2026-04
PATTERN: auth | broke:token-refresh | cause:missing-exp | fix:add-exp-claim | reuse:y
WIN: palace-navigate | score-wing-then-room | 34pct-retrieval-boost | repeat:y
```

> [!NOTE]
> Entries with `ended:` are excluded automatically. Permanent entries always appear first. No cleanup required.

---

## Knowledge Graph

The KG is a temporal entity-relationship graph built entirely from `.st` files. No database, no dependencies. Human-readable, git-trackable, diffable.

### The LINK Type

```
LINK: source | rel:relationship | target | [valid_from:YYYY-MM] | [ended:YYYY-MM] | [stability:x]
```

```st
LINK: kai         | rel:works-on   | nova     | valid_from:2026-03 | stability:transient
LINK: kai         | rel:works-on   | orion    | valid_from:2026-01 | ended:2026-03 | stability:transient
LINK: auth        | rel:depends    | billing  | stability:stable
LINK: brand-color | rel:defined-as | indigo   | stability:permanent
LINK: kai         | rel:member-of  | team     | valid_from:2025-06 | stability:stable
```

The second `works-on` entry has `ended:2026-03`. Kai moved from orion to nova. Both facts are preserved. History is never deleted.

### Stability Levels

| Level | Meaning |
|---|---|
| `stability:permanent` | Core truth. Always in wake-up. Changing it requires contradiction resolution. |
| `stability:stable` | Valid until explicitly ended. Default for most facts. |
| `stability:transient` | Time-windowed. Assignments, sprints, current status. |

### Temporal Fields

Work on **any** `.st` entry type, not just `LINK`:

```st
DECISION: auth | clerk>auth0 | easier-sdk | 2026-01 | stability:stable
DECISION: auth | auth0>clerk | legacy     | ended:2026-01
```

The second entry has `ended:` — the checker ignores it. `wake-up` skips it.

### Querying

```bash
smalltalk kg query _brain/ kai
# KG: kai (as of 2026-04)
#   Active (2):
#     kai -> works-on -> nova   [transient] since 2026-03
#     kai -> member-of -> team  since 2025-06
#   Historical (1):
#     kai -> works-on -> orion  [2026-01 to 2026-03]

smalltalk kg query _brain/ kai --as-of 2026-02
# Point-in-time: what was true in February 2026?

smalltalk kg timeline _brain/ kai
# Timeline: kai
#   2025-06  kai -> member-of -> team  [active]
#   2026-01  kai -> works-on -> orion  [closed 2026-03]
#   2026-03  kai -> works-on -> nova   [active]

smalltalk kg visualize _brain/
# Opens an interactive graph in your browser.
# Nodes coloured by stability. Historical edges faded.
```

---

## Palace Navigation

The palace structures your `.st` files into wings, rooms, and tunnels. Agents navigate — they don't scan.

```
_brain/
├── _index.st          <- palace map (auto-generated)
├── decisions.st       <- wing: decisions
├── patterns.st        <- wing: patterns + wins
└── projects/
    ├── nova.st        <- wing: nova
    └── auth.st        <- wing: auth
```

```bash
# Generate the palace from your directory
smalltalk palace init _brain/

# Refresh after adding files
smalltalk palace index _brain/

# Show structure
smalltalk palace status _brain/
```

Agents navigate with a natural language query:

```bash
smalltalk navigate _brain/ "database decisions"
# Loads decisions.st (hall:DECISION, score:high)
# Loads projects/nova.st (keyword:nova+db, score:medium)
```

Tunnels link rooms across wings automatically when shared topics are detected.

> [!NOTE]
> Palace navigation delivers 34%+ better retrieval than flat-file scanning. Session start cost for `_index.st`: ~150 tokens.

---

## Contradiction Detection

Rules-based. No LLM required. The typed format makes it mechanically tractable.

```bash
smalltalk check _brain/
```

| Type | Flagged when |
|---|---|
| `DECISION` | Same subject, two different active choices |
| `RULE` | Same subject, one `hard`, another `soft` |
| `PATTERN` | Same subject + cause, different `fix:` values |
| `WIN` | Same subject with both `repeat:y` and `repeat:n` |
| `LINK` | Same source + rel pointing to multiple targets simultaneously |

> [!NOTE]
> Entries with `ended:` are excluded from checks. A superseded entry next to a new one is correct resolution, not a contradiction.

**Example output:**

```
[CONFLICT] Found 2 contradiction(s)  (1 CRITICAL, 1 WARNING)

  1. [CRITICAL] LINK: kai | simultaneous-works-on
     brain.st:3  LINK: kai | rel:works-on | orion | valid_from:2026-01  << older
     brain.st:4  LINK: kai | rel:works-on | nova  | valid_from:2026-03  << newer

     Resolution: add ended:2026-04 to brain.st:3

  2. [WARNING] DECISION: deploy | diverging-choices
     brain.st:1  DECISION: deploy | vercel>railway | cost | 2026-01  << older
     brain.st:2  DECISION: deploy | railway>vercel | scale | 2026-04  << newer
```

### Resolution Cycle

```bash
# Step 1: detect
smalltalk check _brain/

# Step 2: resolve (writes ended: to the older entry)
smalltalk kg invalidate _brain/brain.st 1

# Step 3: confirm
smalltalk check _brain/
# OK  No active contradictions detected.
```

Agents running via MCP can do this autonomously — detect the conflict, call `smalltalk_kg_invalidate`, confirm clearance.

---

## CLI Reference

```bash
# Scan: what's convertible
smalltalk init <dir>

# Back up: copy originals to .originals/
smalltalk backup <dir>

# Convert: produce .st files
smalltalk mine <dir>
smalltalk mine <dir> --dry-run
smalltalk mine <dir> --no-keep-originals
smalltalk mine <dir> --model openai/gpt-4o-mini
smalltalk mine <dir> --base-url http://localhost:11434/v1

# Status: conversion progress
smalltalk status <dir>

# Wake-up: current-truth context for session start
smalltalk wake-up <dir>

# Contradiction detection
smalltalk check <dir>

# Knowledge Graph
smalltalk kg query <dir> <entity>
smalltalk kg query <dir> <entity> --as-of YYYY-MM
smalltalk kg timeline <dir> <entity>
smalltalk kg invalidate <file> <line_no>
smalltalk kg invalidate <file> <line_no> --ended 2026-04
smalltalk kg visualize <dir>
smalltalk kg visualize <dir> --out graph.html --no-browser

# Palace
smalltalk palace init <dir>
smalltalk palace index <dir>
smalltalk palace status <dir>

# Diary
smalltalk diary write <agent-id> <entry>
smalltalk diary read <agent-id>

# Instruction files (for agent use)
smalltalk instructions help | mine | kg | palace | check
```

**Environment variable:**
```bash
OPENROUTER_API_KEY   # default key for mine
```

**Windows / PowerShell:**
Use full paths. Tilde expansion doesn't work in PowerShell:
```powershell
smalltalk init C:\Users\yourname\Dev\skills
smalltalk kg query C:\Users\yourname\Dev\_brain auth
```

---

## MCP Server

18 tools exposed via FastMCP. Works with Claude Code, Cursor, Codex, Windsurf, Antigravity.

```bash
# Run the server
python -m smalltalk.mcp_server

# Register with Claude Code
claude mcp add smalltalk -- python -m smalltalk.mcp_server

# Or install from repo root
claude mcp install .claude-plugin/
```

> [!TIP]
> Full setup instructions for all supported tools: [docs/setup.md](docs/setup.md)

### Tool Reference

| Tool | What it does |
|---|---|
| `smalltalk_status` | Conversion progress for a directory |
| `smalltalk_get_spec` | Load grammar spec and instruction files |
| `smalltalk_list_files` | List .st files in a directory |
| `smalltalk_read_file` | Read a specific .st file |
| `smalltalk_search` | Keyword search across .st files |
| `smalltalk_wake_up` | Extract current-truth context for session start |
| `smalltalk_check` | Run contradiction detection |
| `smalltalk_palace_init` | Generate `_index.st` |
| `smalltalk_palace_index` | Refresh `_index.st` |
| `smalltalk_navigate` | Load relevant rooms for a query |
| `smalltalk_list_wings` | List all palace wings |
| `smalltalk_list_rooms` | List rooms in a wing |
| `smalltalk_kg_query` | Entity relationships (current or point-in-time) |
| `smalltalk_kg_timeline` | Chronological story of an entity |
| `smalltalk_kg_invalidate` | Write `ended:` to resolve a contradiction |
| `smalltalk_kg_visualize` | Generate interactive KG graph HTML |
| `smalltalk_diary_write` | Append to agent diary |
| `smalltalk_diary_read` | Read agent diary |

### Autonomous Resolution Example

```
smalltalk_check("_brain/")
  [WARNING] DECISION: deploy | diverging-choices
  decisions.st:3  DECISION: deploy | vercel>railway | 2026-01  << older

smalltalk_kg_invalidate("_brain/decisions.st", 3)
  Invalidated line 3
  Before: DECISION: deploy | vercel>railway | cost | 2026-01
  After:  DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04

smalltalk_check("_brain/")
  OK  No active contradictions detected.
```

---

## Type Reference

### Universal
```st
RULE:     identifier | rule-description | hard|soft
REF:      identifier | path/to/file.st  | covers:topic
NOTE:     identifier | observation
CONFIG:   identifier | key | value
CONTEXT:  identifier | scope | value
DECISION: identifier | choice>rejected | reason | date
PATTERN:  identifier | broke:what | cause:why | fix:what | reuse:y/n
```

### Memory
```st
WIN:       identifier | technique | outcome | repeat:y/n
CLIENT:    identifier | pref:what | avoid:what | updated:date
COMPONENT: identifier | stack | does:what | use-when
PROMPT:    identifier | task-type | approach | why-worked | reuse:y/n
```

### Knowledge Graph
```st
LINK:   source-entity | rel:relationship | target-entity | [valid_from:YYYY-MM] | [ended:YYYY-MM] | [stability:x]
TUNNEL: wing-id | connects:wing-id | via:shared-topic
```

Common `rel:` values: `works-on`, `depends`, `defined-as`, `member-of`, `reports-to`, `assigned-to`, `deployed-to`, `blocks`, `contributes-to`, `references`

### Skills
```st
SKILL:   identifier | triggers | stack | version
USE:     identifier | when:context
PHASE:   identifier | number | name | what-happens
STEP:    identifier | phase | number | action | required|optional
STACK:   identifier | layer | tool | why
CHECK:   identifier | verification-item | required|optional
AVOID:   identifier | antipatterns+separated
SCRIPT:  identifier | path/to/script | what-it-does
STYLE:   identifier | style-name | description
FONT:    identifier | preference | weights | style | usage
COLOR:   identifier | system | key:value | key:value
```

### Agents
```st
AGENT:   identifier | role | capabilities | scope
TASK:    identifier | action | target | priority:high|mid|low
TRIGGER: identifier | event | condition | then:action
OUTPUT:  identifier | type | destination | format
ERROR:   identifier | broke:what | cause:why | state:recovered|unresolved
```

Full reference with examples: [`spec/grammar.md`](spec/grammar.md)

---

## File Reference

| File | What |
|---|---|
| `smalltalk/cli.py` | CLI entry point |
| `smalltalk/converter.py` | File type detection + LLM conversion |
| `smalltalk/init_cmd.py` | `init`: directory scan |
| `smalltalk/backup.py` | `backup`: copy originals to `.originals/` |
| `smalltalk/mine.py` | `mine`: convert files to `.st` |
| `smalltalk/status.py` | `status`: conversion progress |
| `smalltalk/wake_up.py` | `wake-up`: L1 context builder |
| `smalltalk/checker.py` | `check`: contradiction detection (flat + KG) |
| `smalltalk/kg.py` | Knowledge Graph: build, query, timeline, invalidate |
| `smalltalk/kg_viz.py` | KG visualization via vis.js |
| `smalltalk/palace.py` | Palace navigation: `_index.st`, navigate, score |
| `smalltalk/palace_cmd.py` | `palace` CLI subcommands |
| `smalltalk/diary.py` | Agent diary at `~/.smalltalk/diaries/` |
| `smalltalk/searcher.py` | Keyword search across .st files |
| `smalltalk/parser.py` | Core regex parser |
| `smalltalk/mcp_server.py` | MCP server (18 tools) |
| `smalltalk/instructions_cmd.py` | `instructions`: serve instruction files to agents |
| `smalltalk/instructions/` | Per-command instruction files |
| `spec/grammar.md` | Canonical type reference |
| `spec/compression-guide.md` | Manual conversion guide + LLM prompt |
| `docs/setup.md` | Setup guide for Claude Code, Cursor, Codex, Windsurf |
| `docs/icm-integration.md` | ICM + Smalltalk composition reference |
| `examples/skills/` | Compressed skill examples |
| `examples/memory/` | Memory log examples |
| `examples/agents/` | Agent definition examples |
| `examples/knowledge-graph/` | KG examples: team, solopreneur, contradiction resolution |
| `tests/` | Pytest suite: 93 tests |
| `.claude-plugin/` | Claude Code plugin |
| `.codex-plugin/` | Codex plugin |

---

## Requirements

- Python 3.9+
- `typer>=0.9.0`
- `httpx>=0.27.0`
- `rich>=10.11.0`
- `mcp>=1.0.0`

API key only needed for `mine`. Anything OpenAI-compatible works — including local Ollama (free). Reading `.st` files needs nothing beyond the agent and the file.

```bash
pip install smalltalk-cli
```

---

## Contributing

The type system is intentionally minimal. To propose a new type, open an issue with:
- The use case it solves
- The prose it replaces
- A one-line example entry

Types are only added when the use case is genuinely distinct. Existing types are stretched before new ones are introduced.

---

## Theory: Why It Works

Smalltalk is not a memory tool. It is a **cognitive orientation layer**.

A memory tool stores information. Smalltalk changes how the model *starts*: what it knows before the first token of user input, where it goes to find more, and which tools it invokes without being told.

### The Problem With Reactive Agents

A default, unoriented agent runs like this every session:

1. Starts with blank context
2. Searches or greps files to find relevant information
3. Loads files, reads them, guesses what matters
4. Guesses which tool, skill, or agent to invoke
5. Rediscovers state that was fully resolved in a prior session
6. Burns token budget on discovery before doing any actual work

> [!WARNING]
> This is not a capability problem. The model is capable. It's an orientation problem. Capability without orientation wastes itself on navigation.

### What Orientation Gives You

With Smalltalk loaded at session start:

- Reads `SKILL: content-strategist` → knows **what agent** to invoke
- Reads `USE: content-strategist | when:...` → knows **when** to invoke it
- Reads `DECISION: deploy | railway>vercel` → knows the **current deployment** decision
- Reads `WING: auth | type:topic` → knows **where** auth context lives
- Reads `LINK: project | rel:in-stage | stage-03` → knows the project is in **active build**

> **The model doesn't ask. It doesn't search. It already knows.**

### The Cognitive Architecture

Six layers. Only the first three load at session start:

```
Layer 0   Identity        Always loaded. Who we are, what we're building.
Layer 1   Index           Always loaded. The map. Where everything lives.
Layer 2   Wake-up state   ~150 tokens. What's currently true right now.
Layer 3   Navigation      On demand. Load the relevant room for this query.
Layer 4   Knowledge Graph On demand. Entity relationships, stage, assignments.
Layer 5   Deep reference  On demand. The full .md via REF when depth is needed.
```

Total session start cost: ~300-500 tokens (L0 + L1 + L2). Everything else loads only when needed.

### Why Typed Compression Beats Summarisation

When you summarise, the LLM decides what matters. That decision is invisible, lossy, and unrepeatable. You get a paragraph that sounds right but has no queryable structure. You can't ask "what decisions are currently active?" or "what changed last month?"

When you compress into typed entries, you preserve:

| Field | What it captures |
|---|---|
| Subject | What entity does this fact belong to? |
| Type | Decision, rule, pattern, win, link? |
| Value | What exactly was decided or linked? |
| Time | When did this become true? When did it stop? |
| Severity | Hard rule or soft preference? |

This is what the AAAK dialect first demonstrated: LLMs understand typed compressed shorthand without a decoder. `DECISION: deploy | railway>vercel | scale | 2026-04` is read as fluently as prose — at one-tenth the token cost.

### The Compounding Advantage

| Capability | Unoriented | With Smalltalk |
|---|---|---|
| Find relevant context | grep / semantic search | palace navigate |
| Choose a tool or skill | infer from task | `SKILL` + `USE` declare it |
| Know current state | reconstruct from history | `wake-up` in 150 tokens |
| Know what broke | re-read logs | `PATTERN` entries |
| Know what worked | re-read conversations | `WIN` entries |
| Understand entity relationships | query codebase | KG query or visualize |
| Detect contradictions | manual review | `check` (automated, zero LLM) |
| Resolve contradictions | manual edit | `kg invalidate` (one command) |

> [!IMPORTANT]
> An oriented 70B model outperforms an unoriented 405B model on your specific domain. The difference is not intelligence. It's the absence of wasted discovery.

### No Clever Prompts Required

Without Smalltalk, consistent output demands heavy session prompting:

> *"Write content for this automation project. Lead with the viewer's pain point, use you/your framing, open with a curiosity gap, don't be vague, niche down to one audience, make sure every claim has proof potential..."*

With `content-strategist-pro.st` loaded, the user writes:

> *"Write content for this automation project."*

The model already read the RULE, AVOID, PHASE, and USE entries. The entire methodology — the psychology, the sequencing, the anti-patterns — is pre-loaded. The user speaks naturally. The system has the playbook.

The knowledge is in the files. The files load at session start. The session starts oriented.

### A Living System

Every session, the brain compounds:

| Event | Entry written | Effect |
|---|---|---|
| Decision made | `DECISION` | Never relitigated again |
| Bug resolved | `PATTERN` | Can't be repeated |
| Technique worked | `WIN` | Surfaced next time it's relevant |
| Entity relationship changed | `LINK` | KG updated, history preserved |

When something becomes outdated: `check` detects the contradiction, `kg invalidate` writes `ended:`, and `wake-up` stops loading it. No cleanup. No manual pruning. The past is preserved. The present stays clean.

Six months in, you have a brain that knows your entire domain history — what was tried, what worked, what was decided, what changed, and why. `wake-up` surfaces only what's currently true.

> **The goal: a system that gets more useful the longer you use it, without getting heavier.**

---

## Credits

Smalltalk is a direct evolution of the **AAAK dialect** from [MemPalace](https://github.com/MemPalace/mempalace).

**MemPalace** pioneered the insight that LLMs can read structured compressed text natively — no fine-tuning, no decoder, no special API. The AAAK shorthand proved that a model given `DECISION: auth | clerk>auth0 | easier-sdk | 2026-01` understands the fact as well as a paragraph, at 90% fewer tokens. MemPalace also introduced the Palace metaphor — rooms, wings, halls — as a navigation layer for compressed agent memory.

Smalltalk v3 extends this foundation with:
- A formal, versioned grammar spec covering all agent file types
- A temporal Knowledge Graph built entirely from `.st` files
- Contradiction detection and autonomous resolution cycles
- An MCP server (18 tools) integrating with any modern AI coding tool
- A full CLI for compression, search, navigation, and visualisation

If MemPalace is the proof of concept, Smalltalk is the production system.

---

## License

MIT

---

*Smalltalk v3.0.1*
