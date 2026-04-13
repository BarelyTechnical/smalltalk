<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/smalltalk-dark.svg">
    <img src="docs/smalltalk-light.svg" alt="smalltalk" width="400">
  </picture>

  <h3>The intelligence layer for AI agents.</h3>

  <p><em>Structured memory that loads, guides, compounds, and never degrades.</em></p>

  <p>
    <a href="https://pypi.org/project/smalltalk-cli"><img src="https://img.shields.io/pypi/v/smalltalk-cli?color=4f46e5&label=pip" alt="PyPI"></a>
    <a href="https://pypi.org/project/smalltalk-cli"><img src="https://img.shields.io/pypi/pyversions/smalltalk-cli?color=4f46e5" alt="Python"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-4f46e5" alt="MIT License"></a>
    <img src="https://img.shields.io/badge/MCP%20tools-25-4f46e5" alt="25 MCP tools">
    <img src="https://img.shields.io/badge/zero%20infra-plain%20files-4f46e5" alt="zero infrastructure">
  </p>

</div>

---

## Why I built this

If you spend enough time working with AI agents, you hit the same wall. Halfway through a chat, the model forgets what you decided. It defaults back to its base training and ignores everything you established in the first few messages. You end up correcting the exact same mistakes over and over.

This happens on GPT-4, Claude, and every local model out there. As your context window fills up, the model loses alignment. If each response has just a 5% chance of ignoring your rules, you are completely off track before you even hit twenty messages.

I realized this isn't an intelligence problem. It's an architecture problem. The models don't have a reliable source of truth. They are just improvising from a conversational context that they are gradually forgetting. 

Smalltalk sits between your knowledge and your agent. It gives every model a structured, contradiction-free memory that persists across sessions.

Here is the loop:
1. You open a session, and the agent loads your decisions, rules, patterns, and habits.
2. During the session, the agent navigates your knowledge and routes tasks to capability files.
3. Before it does anything risky, it runs contradiction detection to make sure it's not breaking existing rules.
4. When you close the session, the agent writes back what it learned so the brain grows smarter.
5. Next time you start, the model is already caught up.

There's no vector database, no RAG pipeline, and no cloud infrastructure. It just uses plain `.st` files that are git-tracked. It gives you 25 MCP tools and works completely fine on local Ollama models.

---

## The format

I designed the format so every fact in your brain compresses to one single line. It is typed, pipe-delimited, and causal.

```
DECISION: deploy    | railway>vercel      | scale+cost        | 2026-04
RULE:     brand     | no-purple-gradient  | hard
PATTERN:  jwt       | broke:auth          | cause:missing-exp | fix:add-exp-claim | reuse:y
HABIT:    think     | trigger:new-feature | enforce:hard      | plan-before-code
MODELMAP: code      | qwen2.5-coder:14b   | ollama            | ctx:8192
BACKEND:  ollama    | api:localhost:11434 | ctx:4096          | tier:beginner
SKILL:    seo       | when:any-web-build  | stack:schema+meta
WIN:      palace    | score-wing-room     | 34pct-boost       | repeat:y
LINK:     kai       | rel:works-on        | nova              | valid_from:2026-03
```

Any LLM reads this natively. You don't need fine-tuning or special decoders. A massive 200-line skill file condenses into about 20 lines. A full brain directory goes from 40,000 tokens down to 2,000.

You can check out the full grammar in [`spec/grammar.md`](spec/grammar.md).

---

## Install

Just grab it from pip:

```bash
pip install smalltalk-cli
```

Then initialize your first project using the interactive setup wizard:

```bash
smalltalk init
```

The wizard guides you through right in your terminal. It will create the `_brain/` scaffold, detect any local backends like Ollama, let you map your models, explicitly install Git extraction hooks, and output IDE integration paths for tools like Claude Code, Cursor, and Windsurf.

If you are looking to manually configure Cursor, Windsurf, Continue, Gemini, or Claude Code, I put together a detailed mapping guide in **[docs/setup.md](docs/setup.md)**.

---

## How it works

### 1. Session start

```bash
smalltalk wake-up _brain/
```

This loads your current truth. It pulls active entries, permanent rules, and enforced habits, while ignoring superseded decisions. This gives your agent a highly compressed starting point.

### 2. During the session

Your agent navigates the knowledge structure actively rather than relying on keyword searches.

```bash
smalltalk navigate _brain/ "auth decisions"
smalltalk route skills/ "build a landing page"
```

To stop mid-session drift, Smalltalk reinjects a compact reminder into the prompt every few responses.

```bash
smalltalk reinforce _brain/
```

You can wire this automatically in your system prompt:

```
TRIGGER: every-response | event:response-complete | then:smalltalk_reinforce
```

### 3. Before risky actions

It also runs a rules-based contradiction detection. It takes milliseconds and doesn't use an LLM.

```bash
smalltalk check _brain/
```

If the agent reads conflicting facts, it normally picks one arbitrarily. Smalltalk catches this before the agent acts and helps you resolve it.

### 4. Session end

```bash
smalltalk session-end _brain/ --summary "Chose Clerk over Auth0. JWT was breaking on missing exp claim."
```

Instead of losing what you learned, the LLM extracts structured entries, writes them back to the brain, and checks for contradictions all in one command. The brain compounds automatically.

### 5. Drift detection

You can evaluate responses to catch when the model drifts from existing decisions.

```bash
smalltalk eval _brain/ -t "build hero section" -e "follow design system purple gradient" -a "used blue inline styles"
```

If it detects drift, it immediately writes a corrective PATTERN and RULE to the brain so it won't happen again.

---

## The compounding effect

Every session that closes properly leaves the brain smarter than before. Mistakes get encoded. Wins get encoded. Drift gets caught and corrected. The brain never degrades because contradictions are resolved explicitly and stale facts are closed out.

In your first session, the agent re-explains your stack and your decisions. By session fifty, the agent operates like a senior engineer who has worked in your codebase for years.

---

## Active Orchestration (Local Models)

I built an active Orchestrator engine into v4.0 for a specific reason. Local 4B and 7B models silently hit context limits and aggressively truncate memory mid-task. The orchestrator wraps around the LLM, breaks tasks down, and actively manages token budgets. When the context fills up, Smalltalk forcibly extracts a hand-off summary, logs a DECISION entry, and systematically resets the context. The model never realizes its memory wiped. It allows you to run infinite-length execution on constrained hardware.

```bash
smalltalk orchestrate _brain "build a login system" --task-type code
smalltalk orchestrate _brain "build a login system" --resume
```

Give a 7B or 14B model a properly structured brain and orchestration, and the gap with frontier models closes rapidly.

Contradiction detection never requires a model. It is always local and always free.

---

## Invisible Proxy Architecture (v4.1)

Smalltalk acts as a completely passive, invisible proxy layer that sits exactly between your IDE and your local LLM backend.

Point your IDE to Smalltalk's proxy server, and every outbound prompt is intercepted natively. The brain is resolved, context is injected silently, and the request is transparently forwarded to your model.

```bash
smalltalk serve _brain/
```

In your IDE Settings, just change your OpenAI Base URL to `http://localhost:8765/v1`.
You don't need MCP triggers or strict configurations at all. Every interaction natively pulls your historical domain knowledge automatically.

---

## Git-Driven Knowledge Extraction

You can skip manually running `smalltalk mine` if you want to. Smalltalk acts natively within version control to asynchronously harvest intelligence.

```bash
smalltalk install-hook _brain/
```

Every time you run `git commit`, an asynchronous background LLM worker spawns. It silently reviews your diff, identifies solved bugs or architectural jumps, parses them into `.st` formats, and commits them to your `diary.st`. It doesn't block your terminal response time.

---

## Causal intake

You can convert articles, Reddit threads, research papers, and documentation into structured brain entries. It captures the rules along with the evidence and reasoning behind them.

```bash
smalltalk mine _brain/ --api-key YOUR_KEY
smalltalk mine _brain/ --api-key YOUR_KEY --causal
```

---

## REST API Server

Smalltalk ships with a full standard-library REST API for seamless integration with automation platforms like n8n and EvoNexus, or custom frontend environments without MCP support.

```bash
smalltalk serve _brain/ --port 8765
```

---

## MCP server

```bash
python -m smalltalk.mcp_server
```

It comes with 25 tools spanning orientation, navigation, drift prevention, contradiction checking, knowledge graph queries, and infrastructure scanning.

---

## CLI reference

```bash
# Setup
smalltalk init                               # interactive setup wizard (v4.1)
smalltalk bootstrap <dir> --api-key <key>    # fast headless setup and markdown conversion

# Session cycle
smalltalk wake-up <dir>                      # start orientation
smalltalk navigate <dir> "<query>"           # find relevant files
smalltalk route <dir> "<task>"               # match task to skills
smalltalk reinforce <dir>                    # prevent drift
smalltalk check <dir>                        # contradiction check
smalltalk eval <dir> -t "<task>" -e "<expected>" -a "<actual>"
smalltalk session-end <dir> -s "<summary>"   # automated closing ritual
smalltalk diary write <id> "<entry>"         # manual diary write
smalltalk diary read <id>                    # review logs

# Causal intake
smalltalk mine <dir> --api-key <key>         # convert .md to .st
smalltalk mine <dir> --api-key <key> --causal
smalltalk mine <dir> --watch                 # auto-convert on save

# Knowledge graph
smalltalk kg query <dir> <entity>
smalltalk kg timeline <dir> <entity>
smalltalk kg invalidate <file> <line>
smalltalk kg visualize <dir>

# Palace navigation
smalltalk palace init <dir>
smalltalk palace index <dir>

# Orchestration & Server
smalltalk orchestrate <dir> "<task>"
smalltalk orchestrate <dir> "<task>" --resume
smalltalk serve <dir> --port 8765

# Hardware
smalltalk detect-backends
smalltalk detect-backends --brain <dir>

# Utilities
smalltalk scan <dir>         # see what .md files are convertible
smalltalk status <dir>       # conversion progress
smalltalk install-hook <dir> # auto-convert on git commit
```

Setup options for Claude Code, Cursor, Windsurf, Codex, and Antigravity are in [docs/setup.md](docs/setup.md).

---

## Requirements

- Python 3.9+
- `typer`, `httpx`, `rich`, `mcp` (these install automatically)
- API key only needed for `mine` and `session-end`.

All detection, navigation, and contradiction checking is strictly local and free.

---

## Credits

**[MemPalace](https://github.com/MemPalace/mempalace)** — I evolved Smalltalk from the AAAK dialect introduced by MemPalace, which proved that LLMs read structured compressed text natively. MemPalace introduced the Palace metaphor for agent memory navigation.

**[Waza](https://github.com/tw93/Waza)** by [@tw93](https://github.com/tw93) — 8 engineering habits from over five hundred real sessions. `examples/waza-habits.st` brings these habits to any model on any platform. MIT licensed.

---

## License

MIT

---

*Smalltalk v4.0.0*
