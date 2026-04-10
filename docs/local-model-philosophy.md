# The Local Model Case

Why small models fail at complex tasks — and what Smalltalk does about it.

---

## The assumption

The AI industry assumes complex coding work requires frontier models. Claude 3.5, GPT-4o, Gemini Ultra. The reasoning: small models just aren't smart enough.

That assumption is wrong. Or at least, it's incomplete.

---

## What "not smart enough" actually means

When a small model fails at a complex task, the failure mode is almost always one of these:

| Failure mode | Root cause |
|---|---|
| Wrong tool selection | Model infers which tool fits which context — instead of reading it from a `USE when:` entry |
| State drift across steps | Model maintains state through reasoning — instead of reading facts from DECISION + PATTERN entries |
| Reasoning burned on orientation | Working memory used to rediscover context — instead of loading it once |
| Shallow domain knowledge | Model generalises from training — instead of reading your specific constraints |
| Repeated debugging of known issues | Model has no memory of past failures — instead of surfacing PATTERN entries upfront |

None of these are intelligence failures. They're orientation failures.

---

## The compression effect

A frontier model isn't smarter about your project. It's just better at figuring things out from scratch. Remove that need — pre-load the orientation — and the gap closes.

Smalltalk's compression format is designed for exactly this. Instead of a 2,000-line `_brain/` in prose markdown:

```
DECISION: deploy    | railway>vercel     | scale+cost         | 2026-04
PATTERN:  jwt       | broke:auth         | cause:missing-exp  | fix:add-exp-claim | reuse:y
RULE:     brand     | no-purple-gradient | hard
SKILL:    seo       | when:any-web-build | stack:schema+meta
WIN:      palace    | score-wing-room    | 34pct-boost        | repeat:y
```

~120 tokens. The agent knows your world before it starts.

---

## The number

A well-oriented local 14B model is competitive with a disoriented frontier model on your domain-specific tasks.

This isn't a claim about raw capability — a GPT-4 is smarter than llama3.1:14b in isolation. It's a claim about applied performance. On a task where the frontier model spends 30% of its context rediscovering what you already documented, and the local model starts with that context pre-loaded, the gap narrows significantly.

---

## The cost picture

| Setup | Cost per session |
|---|---|
| Frontier model (Claude/GPT-4) without Smalltalk | Pays for model time + rediscovery |
| Frontier model with Smalltalk | Pays for model time only |
| Local model (Ollama) with Smalltalk | Free — hardware only |
| Smalltalk contradiction detection | Always free — no LLM, rules-based |

The `mine` command (conversion) uses a model API once per file. After that, reading `.st` files costs nothing — any model, any session, forever.

---

## Two setups that work

**High-quality local setup:**
```bash
# Ollama with a capable coding model
ollama pull qwen2.5-coder:14b

smalltalk bootstrap _brain/ \
  --base-url http://localhost:11434/v1 \
  --api-key ollama \
  --model qwen2.5-coder:14b
```

**Air-gapped / privacy setup:**
```bash
# Convert files using any available API, once
smalltalk mine _brain/ --api-key YOUR_KEY

# After that — purely local, no external calls needed
smalltalk wake-up _brain/    # no API
smalltalk check _brain/      # no API
smalltalk navigate _brain/ "auth decisions"  # no API
```

The only command that calls an external API is `mine`. Everything else — wake-up, check, navigate, the full KG, palace, diary — runs locally.

---

## The hardware tiers

| Tier | Backend | Models that work well |
|---|---|---|
| GPU (8GB+) | Ollama | qwen2.5-coder:14b, llama3.1:8b, mistral:7b |
| GPU (16GB+) | Ollama | qwen2.5-coder:32b, llama3.3:70b (quantised) |
| CPU only | llama.cpp | Phi-3 mini, TinyLlama, BitNet variants |
| Mixed | Any | Conversion via API once, local inference forever |

Smalltalk doesn't care which backend you use. The `.st` format is model-agnostic — it's plain text that any LLM reads without modification.

---

## What this means for private codebases

Many organisations can't send code to external APIs. With Smalltalk:

1. Run `mine` once on internal infrastructure (or accept the one-time API cost for a sanitised summary)
2. Distribute `.st` files internally — they're text, small, git-trackable
3. Every session after that is fully local — no code ever leaves

The `.st` format is designed to encode **knowledge about your code** (decisions, patterns, rules) rather than the code itself. A DECISION entry is safe to send externally — it's not source code.

---

## Contradiction detection is always free

One of Smalltalk's most valuable features — catching conflicting facts before the agent acts — never touches a model at all.

```bash
smalltalk check _brain/
# → purely rules-based, deterministic, runs in milliseconds
```

For air-gapped teams, this alone is valuable: a deterministic audit that confirms your institutional knowledge is internally consistent before any agent session begins.
