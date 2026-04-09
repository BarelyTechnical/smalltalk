# Smalltalk

### A cognitive layer for AI agents. Not just compression — orientation.

Most agents are reactive. They search, discover, infer. Every session starts from zero. The model has capability but no persistent *orientation* — it knows HOW to do things, but not WHERE your things live, WHAT was decided, or WHEN to invoke which tool.

So the model greps. It loads files and reads them to figure out what they mean. It guesses what tool or skill applies. It rediscovers current state that existed in yesterday's session. It burns thousands of tokens before writing a single line of code.

Smalltalk changes the cognitive posture from **reactive to oriented**.

**The Grammar** — A typed, pipe-delimited, one-line-per-entry format. Every LLM understands it without a decoder or fine-tuning. `DECISION`, `RULE`, `PATTERN`, `SKILL`, `AGENT`, `LINK` — each type carries meaning the model can act on immediately. A 200-line skill file becomes 20 lines. A `_brain/` full of prose becomes one line per queryable fact.

**The Knowledge Graph** — A temporal entity-relationship graph built from `.st` files. No database. No vector store. The model knows who works on what, what depends on what, what changed and when. It doesn't discover this — it reads it.

**The Palace** — A wing/room/tunnel navigation layer. Instead of scanning everything flat, agents navigate to what's relevant. `_index.st` is the map. `navigate()` is the route. The model doesn't search — it goes directly.

**The Tooling** — A Python CLI and MCP server (18 tools) that plug into Claude Code, Cursor, Antigravity, and any MCP-compatible client.

&nbsp;

[Quick Start](#quick-start) · [Grammar](#the-grammar) · [Memory System](#the-memory-system) · [Knowledge Graph](#the-knowledge-graph) · [Palace Navigation](#palace-navigation) · [Contradiction Detection](#contradiction-detection) · [CLI Reference](#cli-reference) · [MCP Server](#mcp-server)

&nbsp;

### Oriented models outperform reactive ones.

| Reactive (no Smalltalk) | Oriented (with Smalltalk) |
|---|---|
| grep/search to find context | navigate directly via palace |
| infer which tool/agent/skill to use | `SKILL` + `USE` declare it explicitly |
| re-discover current state each session | `wake-up` delivers it in 150 tokens |
| figure out what was decided | `DECISION` entries carry it forward |
| re-learn what broke and what fixed it | `PATTERN` entries surface it instantly |
| unknown entity relationships | KG maps every connection |
| load everything flat to find anything | load only the relevant room |

| | | | | |
|---|---|---|---|---|
| **~20 lines** per skill (was ~200) | **~90% token reduction** on session start | **Any LLM** no decoder needed | **$0** local, no subscription | **Compounds** — gets smarter every session |

---

## Quick Start

```bash
pip install smalltalk-cli

# See what's convertible
smalltalk init ~/Dev/skills

# Back up originals first
smalltalk backup ~/Dev/skills

# Convert everything to .st
smalltalk mine ~/Dev/skills

# Check compression state
smalltalk status ~/Dev/skills
```

`mine` uses OpenRouter by default. Swap in any OpenAI-compatible endpoint:

```bash
# Anthropic direct
smalltalk mine ~/Dev/skills \
  --base-url https://api.anthropic.com/v1 \
  --api-key YOUR_KEY

# Local Ollama — no API cost
smalltalk mine ~/Dev/skills \
  --base-url http://localhost:11434/v1 \
  --api-key ollama \
  --model llama3.1
```

Then tell your agents to load `.st` files. One line in your `CLAUDE.md`, `GEMINI.md`, or system prompt:

```
Read .st files before .md files. .st is Smalltalk compressed format —
load as session context. Load .md references only when a specific topic
requires deep detail.
```

---

## The Grammar

Every Smalltalk entry follows one pattern:

```
TYPE: identifier | field | field | field
```

- `TYPE` — uppercase prefix defining the entry category
- `identifier` — the skill, agent, or subject this entry belongs to
- `fields` — pipe-delimited, as short as unambiguous
- `+` — multiple values in one field: `when:next+vite+remix`
- `:` — key-value: `broke:vite-build`
- `>` — choice over alternative: `cloudflare>vercel`

**Before — markdown (7 lines for 3 rules):**

```markdown
## Best Practices

1. **Component Composition**: Build complex UIs from simple, composable
   primitives rather than monolithic components.
2. **Mobile-First**: Start with mobile styles, layer up with responsive
   variants. Never desktop-first.
3. **No Dynamic Classes**: Avoid dynamically constructed Tailwind class
   names — they get purged at build time.
```

**After — Smalltalk (3 lines, same rules):**

```
RULE: ui-skill | compose-from-primitives-not-monoliths | hard
RULE: ui-skill | mobile-first-always | hard
RULE: ui-skill | no-dynamic-class-names | hard
```

### The Two-Tier Loading Pattern

`.st` files enable a retrieval pattern that keeps session costs low without losing depth:

**Tier 1 — Session start (always loaded, cheap):**
Agent loads `.st` files. Full context in ~180 tokens instead of ~1,800.

**Tier 2 — On demand (targeted):**
When a specific topic needs deep detail, agent loads the original `.md` via `REF`:

```
REF: ui-skill | references/components.st | covers:component-catalog
```

Broad context cheap. Deep context on demand.

---

## The Memory System

Smalltalk is built to be your agent's long-term memory. Facts are stored as typed entries — not raw conversation logs, but structured, queryable, temporally-aware records.

| Token cost | Context |
|---|---|
| ~1,800 tokens | One skill file (markdown) |
| ~4,500+ tokens | Skill + sub-references |
| ~20,000–50,000+ | Full `_brain/` in markdown |
| **~180 tokens** | **One skill in Smalltalk** |
| **~2,000–5,000 tokens** | **Full `_brain/` in Smalltalk** |

### Wake-Up Context

On every agent session start, load only what's currently true:

```bash
smalltalk wake-up ~/Dev/_brain/
```

Outputs ~150 tokens. Includes active DECISION entries, hard RULE entries, active PATTERN entries, and repeat:y WIN entries. Historical entries with `ended:` are excluded. Permanent entries appear first.

```
# Smalltalk wake-up — 4 current entries

# permanent (core truth)
RULE: brand | never-change-without-legal-review | hard | stability:permanent

# current
DECISION: deploy | railway>vercel | scale | 2026-04
PATTERN: auth | broke:token-refresh | cause:missing-exp | fix:add-exp-claim | reuse:y
WIN: palace-navigate | score-wing-then-room | 34pct-retrieval-boost | repeat:y
```

---

## The Knowledge Graph

The KG is a temporal entity-relationship graph built entirely from `.st` files. No database. No dependencies. Human-readable, git-trackable, diffable.

### The LINK Type

```
LINK: source | rel:relationship | target | [valid_from:YYYY-MM] | [ended:YYYY-MM] | [stability:x]
```

Real examples:

```
LINK: kai         | rel:works-on     | nova     | valid_from:2026-03 | stability:transient
LINK: kai         | rel:works-on     | orion    | valid_from:2026-01 | ended:2026-03 | stability:transient
LINK: auth        | rel:depends      | billing  | stability:stable
LINK: brand-color | rel:defined-as   | indigo   | stability:permanent
LINK: kai         | rel:member-of    | team     | valid_from:2025-06 | stability:stable
```

The resolution story: kai worked on orion until 2026-03 (`ended:2026-03`), then moved to nova. Both facts are preserved. History is never deleted.

### Stability Levels

```
stability:permanent   Core truth. Always loaded in wake-up. Only closed via contradiction resolution.
stability:stable      Valid until explicitly ended. Default for most facts.
stability:transient   Time-windowed. Expected to change. Use for assignments, sprints, status.
```

Once you mark something `stability:permanent`, changing it requires contradiction resolution — the checker will flag it as `CRITICAL`.

### Temporal Fields

These fields work on **any** `.st` entry type — not just LINK:

```
valid_from:2026-01     This fact became true in January 2026
ended:2026-03          This fact stopped being true in March 2026
```

```
DECISION: auth | clerk>auth0 | easier-sdk | 2026-01 | stability:stable
DECISION: auth | auth0>clerk | legacy     | ended:2026-01
```

The second entry has `ended:` — the checker won't flag this as a contradiction. `wake-up` won't load it.

### Querying the Graph

```bash
smalltalk kg query _brain/ kai
# → KG: kai (as of 2026-04)
#     Active (2):
#       kai  → works-on → nova  [transient]  since 2026-03
#       kai  → member-of → team  since 2025-06
#     Historical (1):
#       kai  → works-on → orion  [2026-01 – 2026-03]

smalltalk kg query _brain/ kai --as-of 2026-02
# Point-in-time: what was true in February 2026?

smalltalk kg timeline _brain/ kai
# → Timeline: kai
#     2025-06  kai → member-of → team  [active]
#     2026-01  kai → works-on → orion  [closed 2026-03]
#     2026-03  kai → works-on → nova   [active]

smalltalk kg visualize _brain/
# → Opens an interactive graph of entities, relationships, temporal edges, and conflicts in your browser.
#   Nodes are coloured by stability (permanent/stable/transient). Historical edges are faded.
```

---

## Palace Navigation

The palace structures your `.st` files into wings, rooms, and tunnels. Instead of loading everything flat, agents navigate to what's relevant.

```
_brain/
├── _index.st             ← palace map — generated automatically
├── decisions.st          ← wing: decisions, hall:DECISION
├── patterns.st           ← wing: patterns, hall:PATTERN+WIN
└── projects/
    ├── nova.st           ← wing: nova, rooms: decisions + patterns
    └── auth.st           ← wing: auth
```

The system automatically detects shared topics and creates `TUNNEL` entries to link relevant rooms across wings.

```bash
# Generate palace index from directory structure
smalltalk palace init _brain/

# Refresh after adding files
smalltalk palace index _brain/

# Show structure
smalltalk palace status _brain/
```

Agents navigate with a query:

```bash
smalltalk navigate _brain/ "database decisions"
# → Loads decisions.st (hall:DECISION, score:high)
# → Loads projects/nova.st (keyword:nova+db, score:medium)
```

34%+ better retrieval than flat-file scanning. Context loaded: `_index.st` (~150 tokens). Deep context: on-demand via `navigate()`.

---

## Contradiction Detection

Rules-based contradiction detection — no LLM required. The typed format makes it mechanically tractable.

```bash
smalltalk check _brain/
```

Detects:

| Type | What's flagged |
|---|---|
| `DECISION` | Same subject, two different active choices |
| `RULE` | Same subject, one says `hard`, another says `soft` |
| `PATTERN` | Same subject + cause, different `fix:` values |
| `WIN` | Same subject with `repeat:y` and `repeat:n` |
| `LINK` | Same source + rel pointing to different targets simultaneously (exclusive rels) |

Temporal awareness: entries with `ended: <= today` are **excluded** — a superseded entry next to a new one is correct resolution, not contradiction.

Example output:

```
[CONFLICT] Found 2 contradiction(s)  (1 CRITICAL, 1 WARNING)

  1. [CRITICAL] LINK: kai | simultaneous-works-on  stability:stable
     Values: nova | orion
     brain.st:3  LINK: kai | rel:works-on | orion | valid_from:2026-01  << older
     brain.st:4  LINK: kai | rel:works-on | nova  | valid_from:2026-03  << newer

     Resolution:
       Close the older entry by adding `ended:2026-04` to:
           LINK: kai | rel:works-on | orion | valid_from:2026-01

  2. [WARNING] DECISION: deploy | diverging-choices  stability:stable
     Values: railway>vercel | vercel>railway
     brain.st:1  DECISION: deploy | vercel>railway | cost | 2026-01  << older
     brain.st:2  DECISION: deploy | railway>vercel | scale | 2026-04  << newer
```

### The Full Resolution Cycle

The output tells you exactly what to do — and `kg invalidate` does it for you:

```bash
# Step 1 — detect (from output above, older entry is brain.st:1)
smalltalk check _brain/

# Step 2 — resolve (write ended: to the older entry)
smalltalk kg invalidate _brain/brain.st 1
# → Before: DECISION: deploy | vercel>railway | cost | 2026-01
# → After:  DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04

# Step 3 — confirm
smalltalk check _brain/
# → OK  No active contradictions detected.
```

Agents running via MCP can do this autonomously — read the conflict, call `smalltalk_kg_invalidate` with the file + line, confirm clearance.

---

## CLI Reference

```bash
# Scan — see what's convertible before touching anything
smalltalk init <dir>

# Back up — copy all .md originals to .originals/ preserving structure
smalltalk backup <dir>

# Convert — produce .st files for all convertible .md files
smalltalk mine <dir>
smalltalk mine <dir> --dry-run                            # preview without writing
smalltalk mine <dir> --no-keep-originals                  # remove .md after conversion
smalltalk mine <dir> --model openai/gpt-4o-mini           # swap model
smalltalk mine <dir> --base-url http://localhost:11434/v1  # use local Ollama

# Status — conversion progress with per-file reduction stats
smalltalk status <dir>

# Wake-up — extract L1 context for system prompt injection
smalltalk wake-up <dir>

# Contradiction detection
smalltalk check <dir>

# Knowledge Graph
smalltalk kg query <dir> <entity>             # current relationships
smalltalk kg query <dir> <entity> --as-of YYYY-MM  # point-in-time
smalltalk kg timeline <dir> <entity>          # chronological story
smalltalk kg invalidate <file> <line_no>      # write ended: to resolve contradiction
smalltalk kg invalidate <file> <line_no> --ended 2026-04
smalltalk kg visualize <dir>                  # open interactive graph in browser
smalltalk kg visualize <dir> --out graph.html --no-browser  # save without opening

# Palace navigation
smalltalk palace init <dir>      # scan directory, generate _index.st
smalltalk palace index <dir>     # refresh _index.st after adding files
smalltalk palace status <dir>    # show wings, rooms, tunnels

# Agent diary
smalltalk diary write <agent-id> <entry>   # append to diary
smalltalk diary read <agent-id>            # read all entries

# Instructions — full step-by-step guide for agents
smalltalk instructions help
smalltalk instructions mine
smalltalk instructions kg
smalltalk instructions palace
smalltalk instructions check
```

### Environment Variables

```bash
OPENROUTER_API_KEY    # default — no need to pass --api-key every time
```

### Windows

Use full paths — tilde expansion doesn't work in PowerShell:

```powershell
smalltalk init C:\Users\yourname\Dev\skills
smalltalk kg query C:\Users\yourname\Dev\_brain auth
```

---

## MCP Server

18 tools exposed via FastMCP. Works with Claude Code, Cursor, Codex, Windsurf, Antigravity.

```bash
# Install
python -m smalltalk.mcp_server

# Register with Claude Code
claude mcp add smalltalk -- python -m smalltalk.mcp_server

# Or from the repo root
claude mcp install .claude-plugin/
```

### Tool Reference

| Tool | What |
|---|---|
| `smalltalk_status` | Conversion progress for a directory |
| `smalltalk_get_spec` | Load grammar spec and instruction files |
| `smalltalk_list_files` | List .st files in a directory |
| `smalltalk_read_file` | Read a specific .st file |
| `smalltalk_search` | Keyword search across .st files |
| `smalltalk_wake_up` | Extract L1 context for session start |
| `smalltalk_check` | Run contradiction detection |
| `smalltalk_palace_init` | Generate _index.st |
| `smalltalk_palace_index` | Refresh _index.st |
| `smalltalk_navigate` | Load relevant rooms for a query |
| `smalltalk_list_wings` | List all palace wings |
| `smalltalk_list_rooms` | List rooms in a wing |
| `smalltalk_kg_query` | Entity relationships (current or as_of) |
| `smalltalk_kg_timeline` | Chronological story of an entity |
| `smalltalk_kg_invalidate` | Write ended: to resolve a contradiction |
| `smalltalk_kg_visualize` | Generate interactive KG graph HTML |
| `smalltalk_diary_write` | Append to agent diary |
| `smalltalk_diary_read` | Read agent diary |

### Autonomous Resolution Example

An agent with access to the MCP server can run the full contradiction resolution cycle without human intervention:

```
smalltalk_check("_brain/")
→ [WARNING] DECISION: deploy | diverging-choices
  decisions.st:3  DECISION: deploy | vercel>railway | cost | 2026-01  << older

smalltalk_kg_invalidate("_brain/decisions.st", 3)
→ Invalidated entry in decisions.st:3
  Before: DECISION: deploy | vercel>railway | cost | 2026-01
  After:  DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04

smalltalk_check("_brain/")
→ OK  No active contradictions detected.
```

---

## Type Reference

### Universal
```
RULE:     identifier | rule-description | hard|soft
REF:      identifier | path/to/file.st  | covers:topic
NOTE:     identifier | observation
CONFIG:   identifier | key | value
CONTEXT:  identifier | scope | value
DECISION: identifier | choice>rejected | reason | date
PATTERN:  identifier | broke:what | cause:why | fix:what | reuse:y/n
```

### Memory
```
WIN:       identifier | technique | outcome | repeat:y/n
CLIENT:    identifier | pref:what | avoid:what | updated:date
COMPONENT: identifier | stack | does:what | use-when
PROMPT:    identifier | task-type | approach | why-worked | reuse:y/n
```

### Knowledge Graph
```
LINK:    source-entity | rel:relationship | target-entity | [valid_from:YYYY-MM] | [ended:YYYY-MM] | [stability:x]
TUNNEL:  wing-id | connects:wing-id | via:shared-topic
```

Common `rel:` values: `works-on`, `depends`, `defined-as`, `member-of`, `reports-to`,
`assigned-to`, `deployed-to`, `blocks`, `contributes-to`, `references`

### Skills
```
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
```
AGENT:   identifier | role | capabilities | scope
TASK:    identifier | action | target | priority:high|mid|low
TRIGGER: identifier | event | condition | then:action
OUTPUT:  identifier | type | destination | format
ERROR:   identifier | broke:what | cause:why | state:recovered|unresolved
```

Full reference with examples: `spec/grammar.md`

---

## File Reference

| File | What |
|---|---|
| `smalltalk/cli.py` | CLI entry point |
| `smalltalk/converter.py` | File type detection + LLM conversion |
| `smalltalk/init_cmd.py` | `init` — directory scan |
| `smalltalk/backup.py` | `backup` — copy originals to `.originals/` |
| `smalltalk/mine.py` | `mine` — convert files to `.st` |
| `smalltalk/status.py` | `status` — conversion progress |
| `smalltalk/wake_up.py` | `wake-up` — L1 context builder |
| `smalltalk/checker.py` | `check` — contradiction detection (flat + KG) |
| `smalltalk/kg.py` | Knowledge Graph — build, query, timeline, invalidate |
| `smalltalk/kg_viz.py` | KG visualization — generates interactive HTML via vis.js |
| `smalltalk/palace.py` | Palace navigation — `_index.st`, navigate, score |
| `smalltalk/palace_cmd.py` | `palace` CLI subcommands |
| `smalltalk/diary.py` | Agent diary at `~/.smalltalk/diaries/` |
| `smalltalk/searcher.py` | Keyword search across .st files |
| `smalltalk/parser.py` | Core regex parser for .st files |
| `smalltalk/mcp_server.py` | MCP server — 18 tools |
| `smalltalk/instructions_cmd.py` | `instructions` — serve instruction files to agents |
| `smalltalk/instructions/` | Per-command instruction files |
| `spec/grammar.md` | Canonical type reference |
| `spec/compression-guide.md` | Manual conversion guide + LLM prompt |
| `docs/icm-integration.md` | ICM + Smalltalk composition reference |
| `examples/skills/` | Compressed skill examples |
| `examples/memory/` | Memory log examples |
| `examples/agents/` | Agent definition examples (incl. content-strategist-pro) |
| `examples/knowledge-graph/` | KG examples — team, solopreneur, contradiction resolution |
| `tests/` | Pytest suite — 93 tests across parser, KG, checker, palace, wake-up |
| `.claude-plugin/` | Claude Code plugin |
| `.codex-plugin/` | Codex plugin |

---

## Requirements

- Python 3.9+
- `typer>=0.9.0`
- `httpx>=0.27.0`
- `rich>=10.11.0`
- `mcp>=1.0.0`

API key required only for `mine` — any OpenAI-compatible endpoint works, including local Ollama (free).
Reading `.st` files requires nothing beyond the agent and the file.

```bash
pip install smalltalk-cli
```

---

## Contributing

The type system is intentionally lean. To propose a new type, open an issue with:
- The use case
- What prose it replaces
- A proposed one-line example

New types are added when the use case is genuinely distinct — not when an existing type can be stretched to cover it.

---

## Theory: Why This Works

Smalltalk is not a memory tool. It is a **cognitive orientation layer**.

The difference matters. A memory tool stores information. Smalltalk changes how the model *starts* — what it knows before the first token of user input, where it goes to find more, and which tools it invokes without being told.

### The Problem With Reactive Agents

Unoriented agents are reactive by default:

1. Session starts with blank context
2. Model searches or greps files to find relevant information
3. Loads files, reads them, extracts what it thinks matters
4. Guesses which tool, skill, or agent to invoke
5. Rediscovers state that was fully resolved in a previous session
6. Burns token budget on discovery before doing any real work

This is not a capability problem. The model is capable. It's an *orientation* problem. Capability without orientation wastes itself on navigation.

### What Orientation Gives You

With Smalltalk loaded:

- The model reads `SKILL: content-strategist | automation+workflow | ...` → knows exactly what agent to invoke for content tasks, without searching
- The model reads `USE: content-strategist | when:automation-project-needs-angles` → knows *when* to invoke it
- The model reads `DECISION: deploy | railway>vercel | scale | 2026-04` → knows the current deployment decision without asking
- The model reads `WING: auth | type:topic | keywords:authentication+jwt` → knows where auth context lives before it needs it
- The model reads `LINK: project | rel:in-stage | stage-03 | valid_from:2026-04` → knows the project is actively in build phase

The model doesn't ask. It doesn't search. It already knows.

### The Cognitive Architecture

Smalltalk implements a six-layer cognitive stack:

```
Layer 0 — Identity        Always loaded. Who we are, what we're building.
Layer 1 — Index           Always loaded. The map. Where everything lives.
Layer 2 — Wake-up state   150 tokens. What's currently true right now.
Layer 3 — Navigation      On demand. Load the relevant room for this query.
Layer 4 — Knowledge Graph On demand. Entity relationships, stage, assignments.
Layer 5 — Deep reference  On demand. The full .md via REF when depth is needed.
```

Total session start cost: ~300-500 tokens (L0 + L1 + L2). That's it. Everything else loads only when needed — targeted, not flat.

### Why Typed Compression Beats Summarisation

When you summarise, an LLM decides what matters. That decision is invisible, lossy, and unrepeatable. You get a paragraph that sounds right but has no queryable structure. You can't ask it "what decisions are currently active?" or "what changed last month?"

When you compress into typed entries, you preserve:
- **The subject** — what entity does this fact belong to?
- **The type** — decision, rule, pattern, win, link?
- **The value** — what exactly was decided/broken/linked?
- **The time** — when did this become true? when did it stop?
- **The severity** — hard rule or soft preference?

This is what the AAAK dialect first demonstrated: LLMs understand typed compressed shorthand *without a decoder*. The model reads `DECISION: deploy | railway>vercel | scale | 2026-04` as fluently as a paragraph of prose — at one-tenth the token cost.

### The Compounding Advantage

| Capability | Unoriented agent | Smalltalk-oriented agent |
|---|---|---|
| Find relevant context | grep / semantic search | palace navigate |
| Choose tool/skill | infer from task description | `SKILL`+`USE` entries declare it |
| Know current state | reconstruct from history | `wake-up` in 150 tokens |
| Understand what broke | re-read logs | `PATTERN` entries |
| Know what worked | re-read conversation | `WIN` entries |
| Understand entity graph | query codebase | KG query or visualize |
| Detect contradictions | manual review | `check` — automated, zero LLM |
| Resolve contradictions | manual edit | `kg invalidate` — one command |

An oriented 70B model outperforms an unoriented 405B model on your specific domain. The difference is not intelligence — it's the absence of wasted discovery.

### No Clever Prompts Required

This is the practical consequence most users notice first.

Without Smalltalk, getting consistent output requires instructional prompting every session:
> *"Write content for this automation project. Lead with the viewer's pain point, use you/your framing, open with a curiosity gap, don't be vague, niche down to one audience, make sure every claim has proof potential..."*

With `content-strategist-pro.st` loaded at session start, the user writes:
> *"Write content for this automation project."*

The model already read the RULE, AVOID, PHASE, and USE entries. The entire methodology — the psychology, the sequencing, the anti-patterns — is pre-loaded. The user speaks naturally. The system has the playbook.

This extends to every domain the `.st` files cover. The agent already knows your deployment decision, your brand rules, your coding patterns, your preferred stack. You don't explain. You don't remind. You just work.

The knowledge is in the files. The files load at session start. The session starts oriented.

### A Living System — Not a One-Time Setup

This is the property that makes Smalltalk compound over time rather than go stale.

After every session:
- A decision that was debated gets written as `DECISION` — it's settled from here forward
- An error that was solved gets logged as `PATTERN` — it won't happen again
- A technique that worked gets captured as `WIN` — the model surfaces it next time it's relevant
- A new entity relationship gets linked via `LINK` — the KG expands

When something changes:
- `smalltalk check` detects the contradiction
- `kg invalidate` writes `ended:` to the older entry
- The old fact is preserved as history. The new fact is now the single source of truth.
- `wake-up` automatically excludes the closed entry next session — no cleanup required

The KG grows with every project. Every mistake logged means it can't be repeated. Every decision stored means it doesn't get relitigated. Every skill loaded means the methodology is already applied.

Six months in, you have a brain that knows your entire domain history — what was tried, what worked, what was decided, what changed, and why. `wake-up` surfaces only what's currently true. The model doesn't inherit the confusion of the past — only the clarity of resolved knowledge.

That is the actual goal: a system that gets more useful the longer you use it, without getting heavier.

---

## Credits

Smalltalk is a direct evolution of the **AAAK dialect** from [MemPalace](https://github.com/MemPalace/mempalace).

**MemPalace** pioneered the insight that LLMs can read structured compressed text natively — no fine-tuning, no decoder, no special API. The AAAK shorthand proved that a model given `DECISION: auth | clerk>auth0 | easier-sdk | 2026-01` understands the fact as well as a paragraph, at 90% fewer tokens. MemPalace also introduced the Palace metaphor — rooms, wings, halls — as a navigation layer for compressed agent memory.

Smalltalk v3 extends this foundation with:
- A formal, versioned grammar spec covering all agent file types
- A temporal Knowledge Graph built from `.st` files (no database)
- Contradiction detection and autonomous resolution cycles
- An MCP server (18 tools) integrating with any modern AI coding tool
- A full CLI for compression, search, navigation, and visualisation

If MemPalace is the proof of concept, Smalltalk is the production system.

---

## License

MIT

---

*Smalltalk v3.0.0 — the best context is the context that fits.*
