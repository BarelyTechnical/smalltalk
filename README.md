<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/smalltalk-dark.svg">
    <img src="docs/smalltalk-light.svg" alt="smalltalk" width="380">
  </picture>

  <h3>Institutional memory for AI agents. Cloud or local.</h3>

  <p><em>The best context is the context that's already there.</em></p>

  <p>
    <a href="https://pypi.org/project/smalltalk-cli"><img src="https://img.shields.io/pypi/v/smalltalk-cli?color=4f46e5&label=pip" alt="PyPI"></a>
    <a href="https://pypi.org/project/smalltalk-cli"><img src="https://img.shields.io/pypi/pyversions/smalltalk-cli?color=4f46e5" alt="Python"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-4f46e5" alt="MIT License"></a>
    <img src="https://img.shields.io/badge/MCP%20tools-20-4f46e5" alt="20 MCP tools">
    <img src="https://img.shields.io/badge/zero%20dependencies-stdlib%20only-4f46e5" alt="zero dependencies">
  </p>

</div>

---

Anthropic Managed Agents. OpenAI Agents SDK. AWS agent infrastructure. These platforms handle orchestration, sandboxing, credential management, and long-running execution.

None of them solve this: **the agent still starts blank.**

It doesn't know your team decided against microservices six months ago. It doesn't know the auth token bug was fixed in March. It doesn't know the senior engineer who owned the billing domain left last month. It doesn't know your deploy targets, your brand rules, or which patterns already broke three times.

There's a second problem. The industry assumes you need a frontier model for complex coding work. That assumption has the same root cause — unoriented models burn intelligence figuring things out from scratch. Give any model the right context upfront, and the gap closes dramatically.

Smalltalk is the layer that fills both. Your decisions, rules, patterns, and wins — structured, compressed, contradiction-detected, and pre-loaded before the first token of work. Works with Claude, GPT-4, and your local Ollama instance equally.

---

## Contradiction Detection

Every codebase accumulates conflicting decisions. Two DECISION entries pointing to different deploy targets. A RULE flagged hard in one file and soft in another. A PATTERN with two different fixes for the same bug.

When an agent reads contradictory facts, it picks one arbitrarily. Wrong decisions at scale, made confidently.

Smalltalk catches this before the agent acts. Rules-based, no LLM required.

```bash
smalltalk check _brain/
```

```
[CONFLICT] Found 1 contradiction(s)  (0 CRITICAL, 1 WARNING)

  1. [WARNING] DECISION: deploy | diverging-choices  stability:stable
     Values: railway | vercel
     decisions.st:3  DECISION: deploy | vercel>railway | cost | 2026-01  << older
     decisions.st:7  DECISION: deploy | railway>vercel | scale | 2026-04  << newer

     Resolution:
       Close the older entry by adding `ended:2026-04` to:
           DECISION: deploy | vercel>railway | cost | 2026-01
```

Resolution — one command:

```bash
smalltalk kg invalidate _brain/decisions.st 3
# → writes | ended:2026-04 to line 3

smalltalk check _brain/
# → OK  No active contradictions detected.
```

Agents running via MCP execute this full cycle autonomously — detect, invalidate, confirm — without human intervention.

What gets detected:
- `DECISION` — same subject, two active choices
- `RULE` — same subject, hard in one file and soft in another
- `PATTERN` — same cause, conflicting fixes
- `WIN` — same subject, repeat:y and repeat:n
- `LINK` — exclusive relationships with multiple active targets

---

## The Closing Loop

At session start the agent reads oriented context. At session end it writes back what it learned. The brain grows by doing the work.

```
start → load context → do work → closing ritual → write DECISION + PATTERN + WIN
→ next session starts smarter than the last
```

```bash
# At session end
smalltalk diary write reviewer "DECISION: auth | clerk>auth0 | sdk-simplicity | 2026-04"
smalltalk diary write reviewer "PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y"
smalltalk check _brain/

# Or via MCP (autonomous agents)
smalltalk_diary_write("reviewer", "WIN: clerk-setup | one-sdk-all-platforms | repeat:y")
smalltalk_check("_brain/")
```

Add this to your `CLAUDE.md` or system prompt to wire it automatically:

```
RULE: session-end | write-decisions-patterns-wins-to-brain | hard
TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write
```

Without the closing ritual: every session starts from the same brain. With it: every session compounds.

Full protocol: `smalltalk instructions closing-ritual`

---

## How It Works

Your skill files, decision logs, and agent specs compress into `.st` format — typed, pipe-delimited, one line per entry.

```
DECISION: deploy  | railway>vercel     | scale+cost        | 2026-04
RULE:     brand   | no-purple-gradient | hard
PATTERN:  jwt     | broke:auth         | cause:missing-exp  | fix:add-exp-claim | reuse:y
SKILL:    seo     | when:any-web-build | stack:schema+meta
WIN:      palace  | score-wing-room    | 34pct-boost        | repeat:y
```

A 200-line skill file becomes 20 lines. A full `_brain/` in prose becomes a few hundred tokens. Any LLM reads it without a decoder — no fine-tuning, no special API, no vector index.

At session start, the agent loads the `.st` files. It already knows your world.

---

## Quick Start

> Full guide with screenshots and per-tool setup: [docs/getting-started.md](docs/getting-started.md)

### 1. Install

```bash
pip install smalltalk-cli
```

```bash
# Or clone (also gets examples, hook templates, spec)
git clone https://github.com/ApexAutomate/smalltalk.git
cd smalltalk/smalltalk && pip install -e .
```

### 2. Register the MCP server

```bash
# Claude Code
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"

# Cursor / Codex / Windsurf — add to MCP config:
# {"smalltalk": {"command": "python", "args": ["-m", "smalltalk.mcp_server"]}}
```

> **Windows / PowerShell:** quotes are required — `-- "python -m smalltalk.mcp_server"`

### 3. Bootstrap your first project

```bash
# One command — backup → mine → palace init → writes CLAUDE.md
smalltalk bootstrap ~/Dev/my-project/_brain --api-key YOUR_KEY

# With local Ollama — no API key, no cloud, free
smalltalk bootstrap ~/Dev/my-project/_brain \
  --base-url http://localhost:11434/v1 \
  --api-key ollama --model llama3.1

# Preview without making changes
smalltalk bootstrap ~/Dev/my-project/_brain --dry-run
```

### 4. Add the global session hook

Copy `examples/hooks/CLAUDE.md` to `~/.claude/CLAUDE.md`. This wires automatic wake-up at session start and the closing ritual at session end — across every project.

```bash
# macOS / Linux
cp examples/hooks/CLAUDE.md ~/.claude/CLAUDE.md

# Windows PowerShell
Copy-Item examples\hooks\CLAUDE.md $env:USERPROFILE\.claude\CLAUDE.md
```

### 5. Keep files updated automatically

```bash
# Watch a directory — auto-convert on save
smalltalk mine ~/Dev/my-project/_brain --watch

# Or auto-convert on every git commit (one-time install per repo)
smalltalk install-hook ~/Dev/my-project
```

### 6. Verify

```bash
smalltalk check _brain/     # run this first — catch contradictions
smalltalk wake-up _brain/   # see what the agent will load
smalltalk status _brain/    # are .st files present?
```

Then open your AI tool and ask it to load session context. A correctly oriented agent calls `smalltalk_wake_up`, reports active decisions and rules, and knows where everything lives.

> Per-tool setup guides (Claude Code, Cursor, Codex, Windsurf, Antigravity): [docs/setup.md](docs/setup.md)

---

## The Numbers

| | Without Smalltalk | With Smalltalk |
|---|---|---|
| Session start | agent starts blank | agent starts oriented |
| Contradictions caught | never — agent picks one | before the agent acts |
| Context compounds | no | yes — every session writes back |
| One skill file | ~1,800 tokens | ~180 tokens |
| Full `_brain/` | ~20,000–50,000 tokens | ~2,000–5,000 tokens |
| Local 7B/14B on domain work | unreliable | competitive |
| Requires infrastructure | no (RAG does) | no — plain files |
| Works with Managed Agents | — | yes — sits on top |

---

## The Local Model Case

The industry assumes complex coding requires frontier models. Smalltalk challenges that directly.

> Intelligence is contextual, not absolute.

The gap between a 7B and a 70B model on your specific codebase isn't raw intelligence — it's orientation. A large model isn't smarter about your project. It's just better at figuring things out from scratch. Remove that need, and the gap closes.

Small models fail at complex tasks for specific, fixable reasons:

| Failure mode | Root cause | What Smalltalk does |
|---|---|---|
| Wrong tool selection | Model has to infer which tool fits which context | `USE: db-skill \| when:schema-changes` — pre-declared, not inferred |
| State drift across steps | State maintained through reasoning, not read from facts | DECISION + PATTERN entries = structured state the model reads |
| Reasoning burned on orientation | Working memory used to rediscover context | Orientation is free, capacity goes to the actual problem |
| Shallow domain knowledge | Model generalises from training, not your codebase | RULE entries encode your specific constraints |
| Repeated debugging of known issues | Model has no memory of past failures | PATTERN entries surface known failure modes upfront |

A well-oriented local 14B model competes with a disoriented frontier model on domain-specific tasks.

```bash
# Run everything locally — zero cloud, zero API cost
smalltalk bootstrap _brain/ \
  --base-url http://localhost:11434/v1 \
  --api-key ollama --model llama3.1

# Contradiction detection never needs an LLM — always local
smalltalk check _brain/
```

Two buyer conversations, same product:

| | Problem | What they need |
|---|---|---|
| Enterprise teams | Knowledge leaves with people. Agents act on stale decisions. | Institutional memory. Contradiction prevention before agents act. |
| Local-first / air-gapped | Can't afford frontier API costs at scale. Can't send code externally. | A way to run small models seriously. No API costs. Data stays local. |

Full philosophy: [docs/local-model-philosophy.md](docs/local-model-philosophy.md)

---

## The Grammar

Every `.st` entry follows one pattern:

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

### Universal types

| Type | Fields |
|---|---|
| `RULE` | `id \| description \| hard\|soft` |
| `DECISION` | `id \| choice>rejected \| reason \| date` |
| `PATTERN` | `id \| broke:what \| cause:why \| fix:what \| reuse:y/n` |
| `REF` | `id \| path/to/file.st \| covers:topic` |
| `NOTE` | `id \| observation` |
| `CONFIG` | `id \| key \| value` |

### Memory types

| Type | Fields |
|---|---|
| `WIN` | `id \| technique \| outcome \| repeat:y/n` |
| `CLIENT` | `id \| pref:what \| avoid:what \| updated:date` |
| `COMPONENT` | `id \| stack \| does:what \| use-when` |
| `PROMPT` | `id \| task-type \| approach \| why-worked \| reuse:y/n` |

### Knowledge graph types

| Type | Fields |
|---|---|
| `LINK` | `source \| rel:relationship \| target \| [valid_from:YYYY-MM] \| [ended:YYYY-MM] \| [stability:x]` |
| `TUNNEL` | `wing-id \| connects:wing-id \| via:shared-topic` |

Temporal fields work on **any** entry type:

| Field | Meaning |
|---|---|
| `valid_from:YYYY-MM` | when this fact became true |
| `ended:YYYY-MM` | when this fact stopped being true |
| `stability:permanent` | always load — never auto-expire |
| `stability:stable` | valid until explicitly ended (default) |
| `stability:transient` | time-windowed — assignments, sprints, current status |

### Skill types

| Type | Fields |
|---|---|
| `SKILL` | `id \| triggers \| stack \| version` |
| `USE` | `id \| when:context` |
| `PHASE` | `id \| number \| name \| what-happens` |
| `STEP` | `id \| phase \| number \| action \| required\|optional` |
| `STACK` | `id \| layer \| tool \| why` |
| `CHECK` | `id \| verification-item \| required\|optional` |
| `AVOID` | `id \| antipatterns+separated` |
| `SCRIPT` | `id \| path/to/script \| what-it-does` |

### Agent types

| Type | Fields |
|---|---|
| `AGENT` | `id \| role \| capabilities \| scope` |
| `TASK` | `id \| action \| target \| priority:high\|mid\|low` |
| `TRIGGER` | `id \| event \| condition \| then:action` |
| `OUTPUT` | `id \| type \| destination \| format` |
| `ERROR` | `id \| broke:what \| cause:why \| state:recovered\|unresolved` |

Full spec: [`spec/grammar.md`](spec/grammar.md)

---

## Two-Tier Loading

Keeps session cost low without losing depth.

**Tier 1 — session start (~150–300 tokens)**
The agent loads `.st` files. Full orientation. Fixed cost.

**Tier 2 — on demand**
When depth is needed, the agent reads the original `.md` via its `REF` link.

```
REF: ui-skill | references/components.md | covers:component-catalog
```

You never pay for both upfront.

---

## Wake-Up

Extracts only what is currently true from a directory of `.st` files:

```bash
smalltalk wake-up ~/Dev/_brain/
```

Output (~120 tokens):

```
# Smalltalk wake-up — 5 current entries

# permanent (core truth)
RULE: brand | never-change-without-legal-review | hard | stability:permanent

# current
DECISION: deploy  | railway>vercel | scale | 2026-04
DECISION: auth    | clerk>auth0    | sdk-simplicity | 2026-02
PATTERN:  jwt     | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y
WIN:      palace  | score-wing-then-room | 34pct-retrieval-boost | repeat:y
```

Entries with `ended:` are excluded automatically. Permanent facts load first. Compare to loading raw `_brain/` markdown: 10,000–40,000 tokens.

---

## Knowledge Graph

A temporal entity-relationship graph built from `.st` files. No database. No vector store. Human-readable, git-trackable.

```
LINK: kai         | rel:works-on   | nova     | valid_from:2026-03 | stability:transient
LINK: kai         | rel:works-on   | orion    | valid_from:2026-01 | ended:2026-03
LINK: auth        | rel:depends    | billing  | stability:stable
LINK: brand-color | rel:defined-as | indigo   | stability:permanent
```

History is never deleted. `ended:` closes the fact. The past stays readable.

```bash
smalltalk kg query _brain/ kai        # active + historical
smalltalk kg timeline _brain/ kai     # chronological story
smalltalk kg visualize _brain/        # interactive graph in browser
```

---

## Palace Navigation

Structures `.st` files into wings, rooms, and tunnels so agents navigate instead of scan.

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
smalltalk navigate _brain/ "auth decisions"
# → _brain/decisions.st  (score: high)
# → _brain/projects/auth.st  (score: medium)
```

34%+ better retrieval than flat-file scanning. `_index.st` session cost: ~150 tokens.

---

## MCP Server — 20 Tools

```bash
python -m smalltalk.mcp_server
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
```

| Tool | What it does |
|---|---|
| `smalltalk_check` | Contradiction detection — catch conflicts before agents act |
| `smalltalk_kg_invalidate` | Write `ended:` to resolve a contradiction |
| `smalltalk_wake_up` | Extract L1 context for session start |
| `smalltalk_route` | Route a task to the most relevant skill/agent files |
| `smalltalk_status` | Overview — file count, entries, types |
| `smalltalk_get_spec` | Full grammar reference |
| `smalltalk_list_files` | List .st files with entry counts |
| `smalltalk_read_file` | Read a .st file |
| `smalltalk_search` | Keyword search across .st files |
| `smalltalk_palace_init` | Generate `_index.st` |
| `smalltalk_palace_index` | Refresh `_index.st` |
| `smalltalk_navigate` | Load relevant rooms for a domain query |
| `smalltalk_list_wings` | List palace wings |
| `smalltalk_list_rooms` | List rooms in a wing |
| `smalltalk_kg_query` | Entity relationships — current or point-in-time |
| `smalltalk_kg_timeline` | Chronological story of an entity |
| `smalltalk_kg_visualize` | Interactive knowledge graph as HTML |
| `smalltalk_diary_write` | Write a closing ritual entry |
| `smalltalk_diary_read` | Read agent diary |
| `smalltalk_bootstrap_info` | Bootstrap protocol for new projects |

---

## CLI Reference

```bash
# First-time setup
smalltalk bootstrap <dir>                   # backup → mine → palace init → CLAUDE.md
smalltalk bootstrap <dir> --api-key <key>
smalltalk bootstrap <dir> --dry-run         # preview without changes

# Standard conversion
smalltalk init <dir>                        # scan — see what's convertible
smalltalk backup <dir>                      # copy originals to .originals/
smalltalk mine <dir>                        # convert .md to .st
smalltalk mine <dir> --watch               # auto-convert on file change
smalltalk mine <dir> --watch --interval 5  # poll every 5s
smalltalk mine <dir> --dry-run             # preview without converting
smalltalk mine <dir> --base-url http://... # any OpenAI-compatible endpoint
smalltalk status <dir>                     # conversion progress

# Session start — run in this order
smalltalk check <dir>                      # first: catch contradictions
smalltalk wake-up <dir>                    # L1 context for system prompt
smalltalk route <dir> "<task>"             # which skills to load for this task

# Contradiction resolution
smalltalk check <dir>
smalltalk kg invalidate <file> <line_no>
smalltalk check <dir>                      # confirm cleared

# Knowledge graph
smalltalk kg query <dir> <entity>
smalltalk kg query <dir> <entity> --as-of YYYY-MM
smalltalk kg timeline <dir> <entity>
smalltalk kg visualize <dir>

# Palace
smalltalk palace init <dir>
smalltalk palace index <dir>
smalltalk palace status <dir>

# Diary (closing ritual)
smalltalk diary write <agent-id> "<entry>"
smalltalk diary read  <agent-id>

# Git hook — auto-mine on commit
smalltalk install-hook <dir>
smalltalk install-hook <dir> --force

# Instructions (for agents reading their own docs)
smalltalk instructions <command>
# commands: help | mine | kg | palace | check | closing-ritual | bootstrap | route
```

**Windows / PowerShell:** use full paths, tilde expansion doesn't work.

MCP registration on Windows — wrap in quotes to prevent PowerShell parsing dashes:

```powershell
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"
```

Global hook template: `examples/hooks/CLAUDE.md` — copy to `~/.claude/CLAUDE.md` for automatic session orientation across every project.

---

## Requirements

- Python 3.9+
- `typer>=0.9.0`, `httpx>=0.27.0`, `rich>=10.11.0`, `mcp>=1.0.0`
- An API key is only needed for `mine`. Reading `.st` files needs nothing — any agent, any platform.

```bash
pip install smalltalk-cli
```

---

## Waza + Smalltalk

[Waza](https://github.com/tw93/Waza) by [@tw93](https://github.com/tw93) packages 8 engineering habits as Claude Code slash commands, refined over 500+ hours of real use across 7 projects and 300+ sessions:

| Habit | When to invoke |
|---|---|
| `/think` | Before writing code for a new feature or architecture decision |
| `/hunt` | Debugging any error — root cause before touching code |
| `/check` | After implementing, before merging |
| `/design` | Building any UI, component, or page |
| `/health` | When the agent ignores instructions or hooks misfire |
| `/write` | Explicitly asked to write or polish prose |
| `/learn` | Diving deep into an unfamiliar domain |
| `/read` | Given any URL or PDF to read |

The problem: these habits only work in Claude Code. A local Ollama model, Cursor, or Gemini CLI can't use them.

`examples/waza-habits.st` encodes all 8 habits as model-agnostic `.st` entries — 99 entries including the RULE enforcement logic and real failure PATTERN entries from Waza's gotcha tables. Any model reads this file at session start and operates with the same methodology.

```bash
# Add to your _brain/ and it loads automatically
cp examples/waza-habits.st ~/Dev/my-project/_brain/

smalltalk wake-up _brain/   # habits load alongside project context
```

Smalltalk gives the model what to know. Waza gives it how to think. Combined on a local 7B or 14B model — the project memory, the decisions, and a senior engineer's discipline — pre-loaded.

See [examples/waza-habits.md](examples/waza-habits.md) for the full breakdown.

---

## Credits

**[MemPalace](https://github.com/MemPalace/mempalace)** — Smalltalk is a direct evolution of the AAAK dialect from MemPalace. MemPalace established that LLMs read structured compressed text natively — no fine-tuning, no decoder, no special API. The AAAK shorthand showed that `DECISION: auth | clerk>auth0 | easier-sdk | 2026-01` is understood as fluently as a paragraph, at 90% fewer tokens. MemPalace also introduced the Palace metaphor — rooms, wings, halls — as a navigation layer for compressed agent memory.

**[Waza](https://github.com/tw93/Waza)** by [@tw93](https://github.com/tw93) — 8 engineering habits built from 500+ hours of real sessions. The `examples/waza-habits.st` encoding is Smalltalk's layer on top. Same philosophy, different distribution format — portable to any model, any platform. MIT licensed.

Smalltalk extends MemPalace into a full production system: formal versioned grammar, temporal Knowledge Graph, contradiction detection, 20-tool MCP server, full CLI, and the closing ritual that writes knowledge back — closing the loop.

---

## License

MIT

---

*Smalltalk v3.1.0 — the best context is the context that's already there.*
