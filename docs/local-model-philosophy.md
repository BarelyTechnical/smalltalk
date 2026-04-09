# The Local Model Philosophy

> *Intelligence is contextual, not absolute.*

---

## The Assumption This Challenges

The current industry position is:

```
Complex coding tasks → need big models → need cloud → need API costs → need Anthropic/OpenAI
```

Smalltalk's position is:

```
Complex coding tasks → need oriented models → orientation lives in .st files
                    → any model that reads text can be oriented
                    → local models become viable for serious work
```

That's not an incremental improvement. That's a fundamentally different cost structure for AI-assisted development.

---

## Why Small Models Fail at Complex Work

Small models struggle with complex coding tasks because they:

1. **Don't know which tool is appropriate for which situation.** They have to infer it from the task description and general training. This consumes reasoning capacity and produces wrong results.

2. **Lose track of state across multi-step reasoning.** Working memory is shallow. The model rediscovers context mid-task instead of reasoning about the actual problem.

3. **Have no domain-specific knowledge.** They generalise from training data. They don't know your architectural constraints, your team's failure patterns, or which decisions were already made and why.

4. **Burn reasoning capacity on orientation.** Before they can reason about the problem, they have to figure out what the problem is, what the codebase looks like, what constraints apply. A 70B model does this better — not because it reasons differently, but because it has more capacity to waste on orientation before the useful work begins.

**None of these failures are intelligence failures. They are context failures.**

---

## How Smalltalk Offloads Cognitive Load

Each entry type in a `.st` file offloads a specific category of cognitive work from the model's working memory to a readable file.

### Tool selection — USE and SKILL entries

```st
SKILL: seo | when:any-web-build | stack:schema+meta+robots
USE:   db-skill | when:schema-changes | then:run-migration
USE:   auth-skill | when:login+register+token | then:clerk-flow
```

The model doesn't have to reason about which tool fits this context. It reads `USE: db-skill | when:schema-changes` and already knows. That's not intelligence — it's pre-loaded routing. A 7B model reading this is as capable of correct tool selection as a 70B model reasoning from scratch.

### State tracking — DECISION and PATTERN entries

```st
DECISION: deploy    | railway>vercel | scale+cost | 2026-04
DECISION: auth      | clerk>auth0    | sdk-simplicity | 2026-02
PATTERN:  jwt       | broke:auth     | cause:missing-exp | fix:add-exp-claim | reuse:y
PATTERN:  cron-jobs | broke:prod     | cause:memory-leak | fix:restart-worker | reuse:y
```

State is not maintained through reasoning — it's read from structured facts. "What's the current deploy target?" is not a multi-step inference. It's a lookup. Small models that struggle with state accumulation across reasoning steps handle this reliably because the state is external to their working memory.

### Domain knowledge — RULE entries

```st
RULE: brand     | no-purple-gradient     | hard
RULE: api       | no-external-calls-prod | hard
RULE: deploy    | tag-release-first      | hard
RULE: data      | gdpr-consent-required  | hard | stability:permanent
```

The model doesn't need to infer your constraints from the codebase. It reads them. A small model with explicit RULE entries makes fewer domain mistakes than a large model guessing from code context.

### Failure memory — PATTERN entries

The PATTERN type is particularly powerful for small models. A PATTERN entry is documentation of a known failure mode:

```st
PATTERN: oauth-redirect | broke:auth | cause:missing-state-param | fix:add-state-to-callback | reuse:y
```

A small model reading this before debugging an auth issue doesn't have to hypothesise from scratch. The most common cause is already documented. It checks that first. This is how a junior developer with good notes outperforms a senior developer with no notes on a familiar class of problems.

---

## The Capacity Reallocation Effect

When a model is orientated before the first token of work:

- No reasoning capacity burned on "what does this codebase do?"
- No reasoning capacity burned on "which tool should I use here?"
- No reasoning capacity burned on "what decisions have already been made?"
- No reasoning capacity burned on "what failed before and why?"

That capacity goes to the actual problem.

A 14B model reasoning about a well-scoped, fully-documented problem competes directly with a 70B model reasoning about a poorly-scoped, undocumented problem. The intelligence gap is real — but the context gap is larger, and Smalltalk eliminates the context gap.

---

## What "Competitive" Actually Means

Not competitive on all tasks. Small models still lose on:
- Novel reasoning problems with no prior art
- Massive multi-file refactors across unfamiliar codebases
- Tasks requiring broad general knowledge

Competitive on:
- Domain-specific coding with defined constraints
- Debugging known classes of problems (PATTERN entries)
- Tool-calling workflows with pre-declared routing (SKILL/USE entries)
- Code review against documented rules (RULE entries)
- Multi-step tasks where state is externalized to files (DECISION entries)

The key qualifier: **domain-specific tasks on your codebase, with a mature brain.**

A team with 6 months of accumulated PATTERN entries, DECISION logs, and RULE documentation running a local 14B model is a different thing from a team starting fresh. The brain is the advantage, not the model size.

---

## The Cost Structure Implication

If a well-maintained `_brain/` makes a local 14B model viable for serious coding work:

| | Cloud frontier model | Local model + Smalltalk |
|---|---|---|
| API cost per token | ~$15–75 / 1M tokens | $0 |
| Data sovereignty | data leaves machine | data stays local |
| Latency | ~1–5s per response | ~0.1–0.5s (on modern hardware) |
| Context limit | 200K tokens | 8–128K tokens (model-dependent) |
| Quality on oriented tasks | excellent | competitive |
| Quality on novel reasoning | excellent | inferior |
| Air-gap capable | no | yes |

For teams that:
- Are cost-sensitive at scale
- Operate in air-gapped environments (defense, healthcare, finance)
- Can't send proprietary code to external APIs
- Want zero ongoing API dependency

The local model + Smalltalk combination is not a compromise. It's a different product with different tradeoffs — tradeoffs that are preferable for a large portion of the market.

---

## The Two Buyer Conversations

### Enterprise buyer

> "When someone leaves, do they take the knowledge with them?"

The answer is currently yes — decisions live in Slack, commit messages, and tribal memory. Smalltalk makes the institutional memory explicit, machine-readable, and persistent. The agent that onboards in six months knows the same things the agent today knows.

Contradiction detection means agents can't act on stale decisions from departed engineers.

### Local-first / budget-constrained buyer

> "We can't afford frontier API costs at 100k queries a month. And we can't send our code to Anthropic's servers."

Local models are already fast enough and capable enough for most domain-specific coding tasks. The missing piece is orientation. Smalltalk provides that — and the `.st` format works identically whether the model is Claude Opus or a local Llama instance.

---

## Running Fully Local

```bash
# Bootstrap entirely locally — no cloud, no API key
smalltalk bootstrap _brain/ \
  --base-url http://localhost:11434/v1 \
  --api-key ollama \
  --model llama3.1:8b

# The .st files are model-agnostic
# Any model that reads text reads .st
smalltalk wake-up _brain/   # local model gets identical orientation to Claude
smalltalk check _brain/     # contradiction detection — zero LLM, always local

# MCP server — connect your local model via MCP
python -m smalltalk.mcp_server
```

Recommended local models (tested):
- `llama3.1:8b` — fast, reliable tool calling, good for oriented tasks
- `llama3.1:14b` — stronger reasoning, handles more complex refactors
- `qwen2.5-coder:14b` — optimized for code, strong on domain-specific tasks
- `deepseek-coder-v2:16b` — excellent on structured reasoning tasks

---

## The Core Bet

The model capability race assumes **intelligence** is the bottleneck.

Smalltalk's philosophy assumes **context** is the bottleneck.

If context is the bottleneck — and every experience with well-documented codebases suggests it is — then you don't need the biggest model. You need the best-oriented model.

That's a direct challenge to the entire "you need frontier models for serious work" narrative.

And it's a challenge that plays out at the file system level, not the API level.

---

*See also: [README.md](../README.md) — quick start and overview*
