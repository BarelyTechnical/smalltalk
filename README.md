<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/smalltalk-dark.svg">
    <img src="docs/smalltalk-light.svg" alt="smalltalk" width="380">
  </picture>

  <h3>The context layer for AI agents.</h3>

  <p><em>Context that loads, guides, and compounds.</em></p>

  <p>
    <a href="https://pypi.org/project/smalltalk-cli"><img src="https://img.shields.io/pypi/v/smalltalk-cli?color=4f46e5&label=pip" alt="PyPI"></a>
    <a href="https://pypi.org/project/smalltalk-cli"><img src="https://img.shields.io/pypi/pyversions/smalltalk-cli?color=4f46e5" alt="Python"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-4f46e5" alt="MIT License"></a>
    <img src="https://img.shields.io/badge/MCP%20tools-20-4f46e5" alt="20 MCP tools">
    <img src="https://img.shields.io/badge/zero%20infra-plain%20files-4f46e5" alt="zero infrastructure">
  </p>

</div>

---

Every session, your AI agent starts blank.

It doesn't know you chose Railway over Vercel and why. It doesn't know the JWT bug that wasted three days, what pattern fixed it, or that you never want purple in the brand. It figures all of that out from scratch — using your most expensive resource — while you wait.

That's not a model problem. It's a context problem. Smalltalk is the fix.

---

## The Session Cycle

Smalltalk wraps the entire session — not just the start.

```
open session   → agent loads your decisions, rules, patterns, wins
during work    → agent navigates your knowledge, routes to skills, checks for contradictions
before risky   → agent runs contradiction detection before deploy or merge
close session  → agent writes back what it learned
next session   → starts smarter than the last
```

No infrastructure. No RAG pipeline. No vector database. Plain files, git-tracked, 20 MCP tools.

---

## The Format

Your knowledge compresses into `.st` — typed, pipe-delimited, one line per fact.

```
DECISION: deploy    | railway>vercel      | scale+cost       | 2026-04
RULE:     brand     | no-purple-gradient  | hard
PATTERN:  jwt       | broke:auth          | cause:missing-exp | fix:add-exp-claim | reuse:y
SKILL:    seo       | when:any-web-build  | stack:schema+meta
WIN:      palace    | score-wing-room     | 34pct-boost       | repeat:y
LINK:     kai       | rel:works-on        | nova              | valid_from:2026-03 | stability:transient
```

Any LLM reads this natively — no fine-tuning, no decoder, no special API. A 200-line skill file becomes 20 lines. A full `_brain/` becomes ~2,000 tokens instead of 40,000.

Full grammar: [`spec/grammar.md`](spec/grammar.md)

---

## Install

```bash
pip install smalltalk-cli
```

```bash
# Register the MCP server (Claude Code)
claude mcp add smalltalk -- "python -m smalltalk.mcp_server"

# Cursor / Codex / Windsurf
# {"smalltalk": {"command": "python", "args": ["-m", "smalltalk.mcp_server"]}}
```

> **Windows / PowerShell:** quotes required — `-- "python -m smalltalk.mcp_server"`

Bootstrap your first project in one command:

```bash
smalltalk bootstrap ~/Dev/my-project/_brain --api-key YOUR_KEY

# Local Ollama — no API key, no cloud, free
smalltalk bootstrap ~/Dev/my-project/_brain \
  --base-url http://localhost:11434/v1 \
  --api-key ollama --model llama3.1
```

---

## Session Start — Orient

Before your first message, the agent loads everything that's true right now:

```bash
smalltalk wake-up _brain/
```

Output (~120 tokens):

```
# Smalltalk wake-up — 5 current entries

# permanent (core truth)
RULE: brand | never-change-without-legal-review | hard | stability:permanent

# current
DECISION: deploy  | railway>vercel | scale   | 2026-04
DECISION: auth    | clerk>auth0    | sdk      | 2026-02
PATTERN:  jwt     | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y
WIN:      palace  | score-wing-room | 34pct-boost | repeat:y
```

Entries with `ended:` — superseded decisions, closed facts — are excluded automatically. The agent reads current truth only.

---

## During Work — Navigate and Route

The agent doesn't scan files looking for context. It navigates.

```bash
# Index your _brain/ once
smalltalk palace init _brain/

# During the session — find what's relevant
smalltalk navigate _brain/ "auth decisions"
# → _brain/decisions.st     (score: high)
# → _brain/projects/auth.st (score: medium)

# Route a task to the right skill files
smalltalk route skills/ "build a landing page for a plumbing company"
# → ui-designer.st  (SKILL triggers: landing-page+demo-build, score: 9)
# → seo-expert.st   (USE when: any-web-build, score: 7)
```

The agent navigates by structure first, searches by content only when needed. 34%+ better retrieval than flat-file scanning.

---

## Before Risky Actions — Check

Every codebase accumulates contradictions. Two decisions pointing different ways. A rule flagged hard in one file, soft in another. A pattern with two different fixes for the same bug.

When an agent reads contradictory facts, it picks one arbitrarily.

Smalltalk catches this before the agent acts. Rules-based — no LLM required.

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
       Close the older entry by adding `ended:2026-04` to line 3.
```

One command resolves it:

```bash
smalltalk kg invalidate _brain/decisions.st 3
# → writes | ended:2026-04 to line 3

smalltalk check _brain/
# → OK  No active contradictions detected.
```

Autonomous agents running via MCP execute this full cycle — detect, invalidate, confirm — without human intervention.

---

## Session End — The Closing Ritual

At session end, the agent writes back what it learned. This is what makes Smalltalk compound.

```bash
smalltalk diary write reviewer "DECISION: auth | clerk>auth0 | sdk-simplicity | 2026-04"
smalltalk diary write reviewer "PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y"
smalltalk diary write reviewer "WIN: clerk-setup | one-sdk-all-platforms | repeat:y"
smalltalk check _brain/
```

Add this to your `CLAUDE.md` or system prompt to wire it automatically:

```
RULE: session-end | write-decisions-patterns-wins-to-brain | hard
TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write
```

The `examples/hooks/CLAUDE.md` template wires this across every project globally.

Without the ritual: every session starts from the same brain.  
With it: every session compounds. The agent that opens this project next month already knows what you learned today.

Full protocol: `smalltalk instructions closing-ritual`

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

---

## Local Models

The industry assumes complex work needs frontier models. That assumption has one root cause: unoriented models burn intelligence figuring out your world from scratch. Give a 7B or 14B model the right context upfront, and the gap closes.

```bash
# Everything local — zero API cost
smalltalk bootstrap _brain/ \
  --base-url http://localhost:11434/v1 \
  --api-key ollama --model llama3.1

# Contradiction detection never needs a model — always local
smalltalk check _brain/
```

A well-oriented local 14B model competes with a disoriented frontier model on your domain.

---

## MCP Server — 20 Tools

```bash
python -m smalltalk.mcp_server
```

| Tool | When the agent uses it |
|---|---|
| `smalltalk_wake_up` | Session start — load orientation |
| `smalltalk_navigate` | Mid-session — find relevant files by domain |
| `smalltalk_route` | Mid-session — match task to skill files |
| `smalltalk_check` | Before deploy/merge — catch contradictions |
| `smalltalk_kg_invalidate` | Resolve a contradiction — writes `ended:` |
| `smalltalk_diary_write` | Session end — closing ritual |
| `smalltalk_diary_read` | Load accumulated agent expertise |
| `smalltalk_kg_query` | Entity relationships — current or historical |
| `smalltalk_kg_timeline` | Chronological story of an entity |
| `smalltalk_kg_visualize` | Interactive graph as HTML |
| `smalltalk_search` | Keyword search across .st files |
| `smalltalk_palace_init` | Index a directory for navigation |
| `smalltalk_list_wings` | List palace wings |
| `smalltalk_list_rooms` | List rooms in a wing |
| `smalltalk_status` | File count, entry count, type breakdown |
| `smalltalk_get_spec` | Full grammar reference |
| `smalltalk_list_files` | All .st files with entry counts |
| `smalltalk_read_file` | Read a .st file |
| `smalltalk_palace_index` | Refresh index after adding files |
| `smalltalk_bootstrap_info` | Bootstrap protocol for new projects |

---

## Waza + Smalltalk

[Waza](https://github.com/tw93/Waza) packages 8 engineering habits — think, hunt, check, design, health, write, learn, read — as Claude Code slash commands, built from 500+ hours across 7 real projects.

The problem: those habits only work in Claude Code. A local Ollama model, Cursor, or Gemini CLI can't use them.

`examples/waza-habits.st` encodes all 8 habits as model-agnostic `.st` entries — 99 entries including routing triggers, RULE enforcement, and real failure PATTERNs from Waza's gotcha tables. Any model reads this at session start and operates with the same discipline.

```bash
cp examples/waza-habits.st ~/Dev/my-project/_brain/
smalltalk wake-up _brain/   # habits load alongside project context
```

Smalltalk gives the model what to know. Waza gives it how to think.

---

## CLI Reference

```bash
# Bootstrap (one command)
smalltalk bootstrap <dir> --api-key <key>
smalltalk bootstrap <dir> --base-url http://localhost:11434/v1 --api-key ollama

# The session cycle
smalltalk wake-up <dir>                 # start: load orientation
smalltalk navigate <dir> "<query>"      # during: find relevant files
smalltalk route <dir> "<task>"          # during: match task to skills
smalltalk check <dir>                   # before risky: contradiction check
smalltalk diary write <id> "<entry>"    # end: closing ritual
smalltalk diary read <id>               # end: review what was logged

# Knowledge graph
smalltalk kg query <dir> <entity>
smalltalk kg timeline <dir> <entity>
smalltalk kg invalidate <file> <line>
smalltalk kg visualize <dir>

# Palace navigation
smalltalk palace init <dir>
smalltalk palace index <dir>

# Conversion
smalltalk init <dir>         # scan — see what's convertible
smalltalk mine <dir>         # convert .md to .st
smalltalk mine <dir> --watch # auto-convert on save
smalltalk status <dir>       # conversion progress

# Git hook
smalltalk install-hook <dir>
```

Per-tool setup (Claude Code, Cursor, Codex, Windsurf, Antigravity): [docs/setup.md](docs/setup.md)

---

## Requirements

- Python 3.9+
- `typer`, `httpx`, `rich`, `mcp` — installed automatically via pip
- API key only needed for `mine` (conversion). Reading `.st` files costs nothing.

---

## Credits

**[MemPalace](https://github.com/MemPalace/mempalace)** — Smalltalk is a direct evolution of the AAAK dialect from MemPalace, which established that LLMs read structured compressed text natively — no fine-tuning, no decoder, no special API. MemPalace also introduced the Palace metaphor for compressed agent memory navigation.

**[Waza](https://github.com/tw93/Waza)** by [@tw93](https://github.com/tw93) — 8 engineering habits from 500+ real sessions. The `examples/waza-habits.st` encoding brings these habits to any model, any platform. MIT licensed.

---

## License

MIT

---

*Smalltalk v3.1.0 — context that loads, guides, and compounds.*
