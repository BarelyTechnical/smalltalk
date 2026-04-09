# Changelog

All notable changes to Smalltalk are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [3.1.0] — 2026-04

### Added — Narrative & Positioning
- **Institutional memory framing** — README hero rewritten from compression → institutional memory
- **Managed Agents context** — README opens with the gap that platform orchestration doesn't fill
- **Contradiction Detection elevated** — section 2 in README, tool #1 in MCP table, enterprise framing added
- **Closing Loop elevated** — section 3, compounding intelligence story front and centre
- **Local Model Case** — new section in README + `docs/local-model-philosophy.md`
  - Core thesis: context is the bottleneck, not intelligence
  - "Intelligence is contextual, not absolute"
  - Table: which small model failure modes each .st entry type directly fixes
  - Two buyer conversations: enterprise (institutional memory) vs local-first (cost + air-gap)
  - Practical Ollama setup — full local pipeline with zero cloud dependency
- **Hero updated** — "Institutional memory for AI agents. Cloud or local."


### Added — Bootstrap & Automation

- **`smalltalk bootstrap <dir>`** — one-command full setup
  - Runs: backup → mine → palace init → writes CLAUDE.md to project root
  - `--dry-run` to preview without making changes
  - Skips mine if no API key (runs remaining steps)
- **`smalltalk mine --watch`** — auto-convert on file change
  - Polls directory every N seconds (default 3, configurable with `--interval`)
  - Initial pass converts any pending files immediately
  - Zero new dependencies — pure stdlib polling
- **`smalltalk install-hook <dir>`** — git post-commit auto-mine
  - Installs Python hook at `.git/hooks/post-commit`
  - After each commit, staged `.md` files are auto-converted and staged
  - Cross-platform: Python hook + bash shim, works on Windows + Linux + macOS
- **`smalltalk route <dir> "<task>"`** — task-to-skill routing
  - Scores every `.st` file against a natural language task description
  - Structural scoring: file/dir name keyword match
  - Content scoring: SKILL triggers, USE when: fields, AGENT capabilities, TRIGGER events
  - Type weights: SKILL/USE (3x), AGENT/TRIGGER (2x), RULE (1x)
  - Use at session start to know which skills to load before first message
- **MCP Tool 19:** `smalltalk_route(directory, task, top_n)` — route via MCP
- **MCP Tool 20:** `smalltalk_bootstrap_info()` — bootstrap protocol on demand
- **`examples/hooks/CLAUDE.md`** — global CLAUDE.md template
  - Copy to `~/.claude/CLAUDE.md` for automatic orientation on every project
  - Includes: wake-up, skill routing, closing ritual — the full PAG loop
- **`instructions/bootstrap.md`** — bootstrap protocol as instruction file
- **`instructions/route.md`** — routing guide as instruction file
- All new commands discoverable via `smalltalk instructions <command>`

### Changed
- `smalltalk --help` now leads with PAG description, `smalltalk bootstrap` as entry point
- MCP server updated from 18 to 20 tools

---

### Added — Closing Ritual (PAG Write Side)
- **`instructions/closing-ritual.md`** — the session-end write-back protocol
  - Defines the full PAG loop: read → do work → write back → next session smarter
  - Covers when to run, what to write, entry formats, MCP + CLI usage
  - Full sequence: identify → write → check → resolve → re-check
- **`examples/agents/session-end-ritual.st`** — closing ritual as a first-class agent definition
  - `TRIGGER: task-complete | event:session-end | then:write-brain`
  - `RULE: write-before-session-ends | hard`
  - Full TASK/OUTPUT/ERROR spec
- **`smalltalk instructions closing-ritual`** — routed in `instructions_cmd.py`
- **`RULE: session-end | write-decisions-patterns-wins-to-brain | hard`** — documented in README, SKILL.md, closing-ritual.md
- **README** — new "Closing the Loop — PAG" section
  - Names PAG (Pre-loaded Augmented Generation) explicitly
  - Describes read side vs write side, the full loop, and the compounding effect
  - Comparison table: RAG vs fine-tuning vs Smalltalk + closing ritual
- **`_brain/patterns/patterns.st`** — repo's own brain now compressed (eats its own cooking)
- **`_brain/_index.st`** — palace index for the repo's own brain

### Added — KG Visualizer
- **`kg_viz.py`** — zero-dependency interactive Knowledge Graph visualization
  - Generates self-contained HTML via vis.js (CDN, internet access required to render)
  - Nodes colour-coded by stability: permanent=purple/box, stable=blue, transient=cyan
  - Edges colour-coded by relationship type (works-on=amber, depends=blue, defined-as=purple, etc.)
  - Historical edges (`ended:`) rendered as dashed, 35% opacity
  - Conflict nodes highlighted: CRITICAL=red, WARNING=amber
  - Sidebar: entity list + active conflict/warning panel
  - Controls: physics/hierarchical layout toggle, historical entry toggle, entity search, reset
- **CLI:** `smalltalk kg visualize <dir>` — opens in browser or saves with `--out` + `--no-browser`
- **MCP Tool 18:** `smalltalk_kg_visualize(dir, out)` — returns path to generated HTML

### Added — Examples
- `examples/agents/content-strategist-pro.st` — full agent compressed from 250+ lines to 32 lines (~89%)
- `examples/agents/content-strategist-pro.md` — original kept as REF source

### Added — Docs
- `docs/icm-integration.md` — design reference for combining ICM workflow structure with Smalltalk memory layer

### Fixed
- Windows `cp1252` crash in `checker.py` — Unicode em-dash separator replaced with ASCII dashes
- `mcp_server.py` tool count docstring updated (17 → 18)
- `help.md` tool count updated (17 → 18)
- `pyproject.toml` description now correctly states 18 MCP tools (was 14)

---

## [3.0.0] — 2026-04

### Added — Knowledge Graph
- **LINK entry type** — temporal entity-relationship triples in `.st` format
  - `LINK: source | rel:type | target | valid_from: | ended: | stability:`
  - No database. Graph built directly from `.st` files.
- **`kg.py`** — `build_graph()`, `query_entity()`, `get_timeline()`, `invalidate_entry()`
  - `query_entity(dir, entity)` — active + historical edges, depth-2 BFS
  - `query_entity(dir, entity, as_of="2026-02")` — point-in-time historical queries
  - `get_timeline(dir, entity)` — chronological story of an entity
- **`invalidate_entry(file, line_no, ended)`** — writes `ended:YYYY-MM` to a `.st` line in place
  - Closes the contradiction→resolution cycle without manual file editing
  - Handles `ended:` update-in-place if field already exists

### Added — Contradiction Detection
- **`checker.py`** — rules-based, no LLM required
  - Detects `DECISION`, `RULE`, `PATTERN`, `WIN` flat-entry conflicts
  - **NEW:** Detects `LINK` relational overlaps — same source+rel, different targets, simultaneously active
  - Exclusive relationships (`works-on`, `assigned-to`, `defined-as`) → `CRITICAL`
  - Non-exclusive relationships (`member-of`, `contributes-to`) → skipped
  - `ended:` entries are excluded — historical facts are never flagged as contradictions
  - `stability:permanent` escalates severity to `CRITICAL`
  - Each conflict output includes: file path, line number, older/newer markers, resolution suggestion

### Added — Full Contradiction Resolution Cycle
- `smalltalk check <dir>` → detect + get file/line of older entry
- `smalltalk kg invalidate <file> <line_no>` → write `ended:` to file
- `smalltalk check <dir>` → confirm cleared
- Same cycle available via MCP: `smalltalk_check()` + `smalltalk_kg_invalidate()` + `smalltalk_check()`
- Agents can run the full autonomous cycle without human intervention

### Added — CLI `kg` Subcommand Group
- `smalltalk kg query <dir> <entity>` — entity relationships (active + historical)
- `smalltalk kg query <dir> <entity> --as-of YYYY-MM` — point-in-time query
- `smalltalk kg timeline <dir> <entity>` — chronological story
- `smalltalk kg invalidate <file> <line_no> [--ended YYYY-MM]` — resolution step

### Added — MCP Tool 17: `smalltalk_kg_invalidate`
- Closes the loop from `smalltalk_check` output to file write, over MCP
- Full docstring with worked example embedded for agent self-documentation

### Added — Temporal Validity Improvements
- `_is_valid_date()` — validates YYYY-MM format before string comparison
  - Prevents silent wrong comparisons from malformed dates (`soon`, `TBD`, etc.)
- `is_currently_valid()` now validates date format before comparing
- `_extract_date()` fallback uses stable `file:name:line` composite (not just line number)
  - Prevents cross-file ordering from being wrong when entries have no date

### Added — Palace Fix
- Category folder detection now uses `rglob` instead of `glob`
  - Nested structures like `projects/myapp/auth/auth.st` now indexed correctly

### Added — Tests
- `tests/test_parser.py` (14 tests)
- `tests/test_kg.py` (30 tests)
- `tests/test_checker.py` (32 tests)
- `tests/test_wake_up.py` (7 tests)
- `tests/test_palace.py` (7 tests)

### Added — Examples
- `examples/knowledge-graph/team-brain.st` — team KG with entity relationships, temporal entries
- `examples/knowledge-graph/solopreneur-brain.st` — single-person setup
- `examples/knowledge-graph/contradiction-resolution.st` — worked before/after example

### Fixed
- `requirements.txt` missing `mcp>=1.0.0`
- `.gitignore` missing `.pytest_cache/`, `_brain/`, `*.db`
- `README.md` footer version mismatch (was v1.0.0, now v3.0.0)
- `mcp_server.py` tool count docstring (was "12 tools", now "17 tools")

---

## [2.0.0] — 2026-01

### Added — Palace Navigation
- Wing / room / tunnel structure for `.st` file organization
- `_index.st` auto-generated from directory structure
- `smalltalk palace init <dir>` — scan and generate `_index.st`
- `smalltalk palace index <dir>` — refresh after adding files
- `smalltalk palace status <dir>` — show structure
- `navigate(dir, query)` — keyword + hall scoring, returns top-3 relevant rooms
- MCP tools: `smalltalk_palace_init`, `smalltalk_palace_index`, `smalltalk_navigate`,
  `smalltalk_list_wings`, `smalltalk_list_rooms`

### Added — Wake-Up Context
- `smalltalk wake-up <dir>` — extract L1 context (~150 tokens)
- Loads: all active DECISION, hard RULE, all active PATTERN, repeat:y WIN
- Excludes: ended entries, future valid_from entries
- Permanent entries appear first

### Added — Diary System
- Per-agent append-only knowledge at `~/.smalltalk/diaries/<agent-id>.st`
- Cross-project — accumulates expertise globally, not per-repo
- `smalltalk diary write <agent-id> <entry>` — append
- `smalltalk diary read <agent-id>` — read all entries
- MCP tools: `smalltalk_diary_write`, `smalltalk_diary_read`

### Added — MCP Server
- FastMCP-based server exposing Smalltalk to Claude Code, Cursor, Codex, and any MCP client
- Initial 12 tools: status, spec, list files, read file, search, palace ops, wake-up, check

---

## [1.0.0] — 2025-11

### Added — Grammar + CLI
- Typed, pipe-delimited `.st` format — `TYPE: identifier | field | field`
- Entry types: RULE, DECISION, PATTERN, WIN, CLIENT, COMPONENT, PROMPT, NOTE,
  CONFIG, CONTEXT, REF, SKILL, USE, PHASE, STEP, STACK, CHECK, AVOID, AGENT,
  TASK, TRIGGER, OUTPUT, ERROR
- `smalltalk init <dir>` — scan for convertible files
- `smalltalk backup <dir>` — copy originals to `.originals/`
- `smalltalk mine <dir>` — LLM-assisted `.md → .st` conversion
- `smalltalk status <dir>` — conversion progress
- `smalltalk instructions <command>` — serve instruction files to agents
- Works with any OpenAI-compatible endpoint (OpenRouter, Anthropic, Ollama)
- Claude Code plugin (`.claude-plugin/`) + Codex plugin (`.codex-plugin/`)
- ~90% token reduction. Zero information lost. Zero dependencies for reading.

---

*Smalltalk v3.0.0 — the best context is the context that fits.*
