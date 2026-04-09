# ICM + Smalltalk — Future Integration Reference

> Status: Design reference only. No code changes required to either system.
> This documents how ICM and Smalltalk compose naturally as complementary layers.

---

## The Boundary (Keep This Clear)

```
ICM          →  HOW you structure and run the work
Smalltalk    →  WHAT you know and learned during that work
```

They are different tools solving different problems. They do not need to merge. The `.st` file is the bridge.

**ICM manages:** workflow stages, stage routing, what to load for each task, scaffolding outputs, stage handoffs.

**Smalltalk manages:** compressed memory, temporal knowledge, contradiction resolution, entity relationships, agent context at session start.

If this boundary is ever blurred — if Smalltalk starts managing stages, or ICM starts managing memory — both tools get worse.

---

## How They Compose (Convention, Not Code)

No new Smalltalk features are needed. No new ICM features are needed. The composition works through a convention: **ICM stage outputs get written as `.st` entries using the existing Smalltalk grammar.**

```
ICM stage runs → produces knowledge/decisions → developer writes .st entries → Smalltalk manages them
```

That's the loop. One direction. No circular dependency.

---

## Stage-by-Stage: What Gets Written as `.st`

### Stage 01 — Discovery

ICM asks: what domain? what workflow? who are the users?

Smalltalk output (written once, lives forever):

```
# _brain/identity.st
CONTEXT: project | scope | what-domain-and-what-it-solves
CONTEXT: project | audience | who-specifically
CONTEXT: project | workflow | the-core-human-process-being-automated
LINK: project | rel:assigned-to | me | valid_from:2026-04 | stability:stable
LINK: project | rel:in-stage | stage-01 | valid_from:2026-04
```

### Stage 02 — Mapping (Stage Contracts + Dependencies)

ICM formalises: what does each stage produce? what does it depend on?

Smalltalk output:

```
# _brain/stages.st
LINK: project | rel:in-stage | stage-01 | valid_from:2026-04-01 | ended:2026-04-02
LINK: project | rel:in-stage | stage-02 | valid_from:2026-04-02
DECISION: architecture | next>remix | team-familiarity | 2026-04
RULE: project | each-stage-writes-to-output-before-next | hard
```

### Stage 03 — Scaffolding

ICM generates the folder tree and files.

Smalltalk output:

```
LINK: project | rel:in-stage | stage-02 | ended:2026-04-03
LINK: project | rel:in-stage | stage-03 | valid_from:2026-04-03
COMPONENT: project | next+tailwind+supabase | does:full-stack-app | use-when:always
DECISION: deploy | railway>vercel | cost+control | 2026-04
```

### Stage 04 — Questionnaire Design

ICM builds the onboarding questionnaire for the workspace.

Smalltalk output:

```
# The questionnaire questions themselves become CONTEXT entries
CONTEXT: project | onboarding-q1 | what-is-the-core-problem-you-are-solving
CONTEXT: project | onboarding-q2 | who-is-the-primary-user
CONTEXT: project | onboarding-q3 | what-does-success-look-like-in-30-days
```

### Stage 05 — Validation

ICM verifies the workspace against MWP conventions.

Smalltalk output:

```
LINK: project | rel:in-stage | stage-03 | ended:2026-04-05
LINK: project | rel:in-stage | stage-05 | valid_from:2026-04-05
WIN: icm-setup | full-5-stage-pass | workspace-validated | repeat:y
LINK: project | rel:in-stage | complete | valid_from:2026-04-05 | stability:stable
```

---

## What Smalltalk Gives You After Each Stage

Once `.st` entries are written, the full Smalltalk toolchain works immediately:

```bash
# What stage is this project in right now?
smalltalk kg query _brain/ project

# Full stage progression timeline
smalltalk kg timeline _brain/ project

# See the full KG — entities, stages, people, dependencies
smalltalk kg visualize _brain/

# Inject only what's currently true into a new model session
smalltalk wake-up _brain/

# Check for contradictions (e.g. two active stages at once)
smalltalk check _brain/
```

The checker naturally catches the case where a project shows as active in two stages simultaneously — because two LINK entries pointing to different stages with no `ended:` is a real contradiction.

---

## ICM's CONTEXT.md → Smalltalk's LAYER entries

ICM's `CONTEXT.md` is a routing table: for task X, load files A and B, do NOT load C and D.

Smalltalk's `LAYER` entries in `_index.st` do the same thing, compressed:

```
# ICM CONTEXT.md (verbose, ~60 lines):
# "If doing discovery: load references/conventions-reference.md and
#  references/examples/script-to-animation-summary.md. Do NOT load
#  stages/02-mapping/ through stages/05-validation/."

# Smalltalk LAYER (compressed, 4 lines):
LAYER: L0 | file:identity.st             | load:always
LAYER: L1 | file:_index.st               | load:always
LAYER: L2 | trigger:stage-discovery      | source:navigate | file:stages/discovery.st
LAYER: L3 | trigger:stage-build          | source:navigate | file:stages/scaffold.st
```

`smalltalk navigate _brain/ "discovery"` loads exactly what ICM's CONTEXT.md routing would load — minus the 60-line prose file.

---

## ICM Questionnaire → Smalltalk Brain Seed

The most powerful combination: use ICM's questionnaire to seed the Smalltalk KG from day one.

When ICM's `setup/questionnaire.md` asks setup questions, write the answers directly to `.st` instead of markdown:

| ICM Questionnaire Question | Smalltalk Entry |
|---|---|
| What domain is this workspace for? | `CONTEXT: project \| scope \| <answer>` |
| Who is the primary user? | `CONTEXT: project \| audience \| <answer>` |
| What does each stage produce? | `PHASE: project \| 1 \| discovery \| <answer>` |
| What are the key constraints? | `RULE: project \| <constraint> \| hard` |
| Who is responsible? | `LINK: project \| rel:assigned-to \| <name> \| stability:stable` |

Result: the KG is populated before any work starts. `smalltalk wake-up` from session 1 already has full context.

---

## Future Possibilities (Not Current Scope)

These are potential future integrations — do NOT build these until Smalltalk is fully stable and ICM integration is validated through real use:

1. **`smalltalk icm status`** — reads ICM `stages/*/output/` folders and plots stage completion against LINK entries in `_brain/stages.st`. Detects if code is ahead of or behind the KG record.

2. **Auto-seeding from ICM outputs** — `smalltalk mine <icm-output-dir>` could detect ICM stage output files and convert them to `.st` entries using the converter. Currently `mine` handles `.md` files; ICM outputs are already markdown.

3. **ICM + Smalltalk workspace template** — a starter repo that combines both: ICM folder structure with Smalltalk `_brain/` pre-wired. The README would be 2 pages instead of 20.

None of these require changes to either system. They are wrapper scripts, not core features.

---

## Summary

| Concern | Answer |
|---|---|
| Does ICM conflict with Smalltalk? | No. Different layers, different problems. |
| Does integration require new Smalltalk features? | No. Existing grammar covers everything. |
| Where does the integration live? | In the `.st` files you write after each ICM stage. |
| Does Smalltalk need to know about ICM? | No. It just reads `.st` files. |
| Does ICM need to know about Smalltalk? | No. It just writes to `output/` folders. |
| What's the one thing to do? | After each ICM stage, write stage outcomes as `.st` entries. |

---

*This document is a design reference. Review before building any features.*
*Last updated: 2026-04*
