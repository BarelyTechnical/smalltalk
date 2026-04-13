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

## The Problem

If you spend enough time working with AI agents, you hit the same wall: **Context Drift**.

Halfway through a complex session, the model forgets the architectural decisions you made earlier. It defaults back to its base training, ignores your design system, and completely drops the nuance you established in the first few messages. 

This happens on GPT-4, Claude, and every local model out there. As your context window fills up, the model loses alignment. If each response has just a 5% chance of ignoring your rules, your project is completely off track before you even hit twenty messages. You end up correcting the exact same mistakes over and over.

The standard solution is RAG or a Vector Database. But RAG is probabilistic and blurry. It fetches "similar" texts, not deterministic rules. AI agents don't need semantic similarity to fix context drift—they need a strict, contradiction-free source of truth injected directly into their context window.

## The Solution

Smalltalk sits between your knowledge and your agent. It gives every model a structured, contradiction-free memory that persists across sessions and is aggressively maintained *per-response*.

It achieves this through:
1. **The Invisible Proxy**: Intercepts `POST /v1/chat/completions` IDE traffic. It dynamically appends the compiled brain rules to the bottom of the system block. Because the injection is highly compressed (e.g., 40k tokens → 2k tokens), it cleanly rides alongside your IDE's hidden prompts without blowing out the model's context window.
2. **Git-Driven Harvesting**: Asynchronous git hooks analyze your commits to extract decisions and habits without manual entry.
3. **Active Orchestration**: Local agents get their context actively supervised, automatically summarizing and flushing tokens before models silently truncate memory.
4. **Deterministic Validation**: Non-LLM contradiction loops act as a strict firewall for your memory graph. The proxy cannot force the model to output perfect code, but when the AI attempts to log a decision or learn a new rule, Smalltalk's deterministic checks prevent conflicting facts from entering the `.st` files. Drift happens in the chat, but it can never infect the long-term memory.

There is no vector database, no RAG pipeline, and no cloud infrastructure. It uses deeply compressed, pipe-delimited `.st` files that are git-tracked. It gives you 25 MCP tools and works completely offline with local Ollama models.

---

## The Format

Smalltalk is built on the AAAK grammar (from MemPalace). Every fact, rule, or architectural decision compresses into one single typed, pipe-delimited line. 

Instead of a 4,000 token markdown document that says:
> *"When building the frontend, ensure that we use Vercel for deployment. The brand guidelines dictate that we strictly avoid using purple gradients... If you are handling authentication and encounter a JWT auth break, it's usually because of the missing expiration claim. Fix it by adding the exp claim back. Always reuse the auth utility..."*

It becomes a 24 token `.st` block:
```st
DECISION: deploy    | railway>vercel      | scale+cost        | 2026-04
RULE:     brand     | no-purple-gradient  | hard
PATTERN:  jwt       | broke:auth          | cause:missing-exp | fix:add-exp-claim | reuse:y
HABIT:    think     | trigger:new-feature | enforce:hard      | plan-before-code
MODELMAP: code      | qwen2.5-coder:14b   | ollama            | ctx:8192
BACKEND:  ollama    | api:localhost:11434 | ctx:4096          | tier:beginner
SKILL:    seo       | when:any-web-build  | stack:schema+meta
```

Because it's syntactically rigid, any LLM reads this natively. A 200-line documentation file condenses into about 20 lines. A massive project brain goes from 40,000 tokens down to 2,000, leaving plenty of room for actual execution context. (Full grammar in [`spec/grammar.md`](spec/grammar.md)).

---

## Installation

Just grab it from pip:

```bash
pip install smalltalk-cli
```

Then initialize your first project using the interactive setup wizard:

```bash
smalltalk init
```

The wizard guides you through your terminal. It creates the `_brain/` scaffold, detects local backends (like Ollama), lets you map your models, explicitly installs Git extraction hooks, and outputs IDE integration paths for Claude Code, Cursor, and Windsurf. (See **[docs/setup.md](docs/setup.md)** for detailed manual config).

---

## Architecture: How it operates

Smalltalk isn't just a CLI you run once at the start of a project. It has three operating modes depending on how you write code.

### 1. The Invisible Proxy (v4.1)
*For persistent IDE sessions (Cursor, Windsurf, Cline)*

This is the primary way experienced developers use Smalltalk. You run the proxy server locally:

```bash
smalltalk serve _brain/
```

Then, point your IDE's OpenAI Base URL to `http://localhost:8765/v1`. 

Smalltalk acts as a transparent, passive interceptor. Every time you hit enter in your IDE, the proxy catches the outbound `POST /v1/chat/completions` request. It resolves the brain, aggressively injects your highly compressed `.st` rules into the system block, and forwards the prompt. 

![Smalltalk Proxy Architecture In Action](docs/demo.gif)
*Demo: Watch the proxy silently compile and prepend the brain on every generated response.*

By reinforcing the context on **every single request**, the model is forcefully realigned before generating its next token. *(Note: This server also acts as a native REST API for integrations with automation platforms like n8n or EvoNexus).*

### 2. Active Orchestration
*For constrained local AI execution (4B to 14B models)*

Local models silently hit context limits and aggressively truncate memory mid-task, destroying execution context. Smalltalk's Orchestrator wraps around the local LLM. When the context fills up, Smalltalk forcibly extracts a hand-off summary, logs a `DECISION` entry, and systematically resets the context window. The model never realizes its memory wiped.

```bash
smalltalk orchestrate _brain "build a login system" --task-type code
smalltalk orchestrate _brain "build a login system" --resume
```

### 3. MCP Server
*For explicit tool calling*

If your agent supports Context Protocols (like Claude Desktop), Smalltalk exposes its entire knowledge graph and verification logic as 25 distinct tools.

```bash
python -m smalltalk.mcp_server
```

---

## The Knowledge Loop: How the brain grows

If Smalltalk enforces the rules, how do the rules get there? The system continuously harvests new intelligence safely.

### 1. Async Git Hooks
You don't need to manually log what you learned. Install the git hook:

```bash
smalltalk install-hook _brain/
```

Every time you `git commit`, an asynchronous background LLM worker spawns. It silently reviews your diff, identifies architectural jumps and solved bugs, converts them into `.st` formats, and commits them to `_brain/diary.st`. It takes zero setup and never blocks your terminal.

### 2. Causal Intake (Mining)
Point Smalltalk at documentation, Reddit threads, or external guides to build your agents' baseline. It doesn't just copy the text; it extracts the causative rules (the *why* and the *evidence*).

```bash
smalltalk mine _brain/ --api-key YOUR_KEY --causal
```

### 3. Manual Session Closures (CLI Loop)
For standalone CLI usage, you can cleanly close a session to trigger an immediate extraction into the graph:

```bash
smalltalk session-end _brain/ --summary "Chose Clerk over Auth0. JWT broke on missing exp."
```

---

## Safety: Contradiction & Drift Detection

Before your agent takes a risky action, or if you suspect it's wandering off path, Smalltalk has tools to reign it in deterministically:

- **Check**: Validates the current memory graph for conflicting facts. This logic is local, takes milliseconds, and does not require an LLM. (`smalltalk check _brain/`)
- **Eval**: Evaluates a specific agent response against expected rules. If it detects a violation, it writes a corrective `PATTERN` so it never happens again.
- **Reinforce**: For CLI scripting loops, you can forcibly drop a compressed reminder into the chat pipeline to halt drift.

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
