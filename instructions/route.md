# Route — Task-to-Skill Routing

Route finds the most relevant skill and agent files for a task description.
Run it at session start, before the first user message, to know exactly which
files to load.

## Why

Loading all skills at session start is expensive and imprecise. Route gives
you the top 3–5 most relevant files for the specific task at hand — exactly
what the agent needs, nothing it doesn't.

## Scoring logic

Route scores every `.st` file in the directory against task keywords:

| Signal | Weight | Examples |
|---|---|---|
| File/dir name match | 2x per keyword | `seo.st`, `skills/frontend/` |
| SKILL entry match | 3x | `SKILL: seo | when:any-web-build` |
| USE entry match | 3x | `USE: schema | when:web+seo` |
| AGENT entry match | 2x | `AGENT: frontend | web+components` |
| TRIGGER entry match | 2x | `TRIGGER: plumbing | event:demo-request` |
| RULE / CHECK match | 1x | `RULE: brand | no-purple` |

No LLM required. Zero latency.

## Commands

```bash
# Find skills for a task
smalltalk route <dir> "<task>"

# Return top 3 only
smalltalk route <dir> "<task>" --top 3

# Examples
smalltalk route skills/ "build a landing page for a plumbing company"
smalltalk route _brain/ "deploy to production"
smalltalk route _brain/ "debug the auth token refresh bug"
```

## Output

```
Route: 'build a landing page for a plumbing company' → 3 file(s)

  1. [6.0]  skills/seo-expert.st        (18 entries)  via:SKILL+USE
  2. [4.5]  skills/ui-designer.st       (24 entries)  via:SKILL
  3. [3.0]  skills/conversion-copy.st   (12 entries)  via:SKILL+AGENT

Next: smalltalk_read_file(path) on top-ranked result(s).
```

## Workflow

```
1. smalltalk_route(dir, task)         → get ranked file paths
2. smalltalk_read_file(top_path)      → load top-ranked skill
3. smalltalk_read_file(second_path)   → load second if relevant
4. Begin work with loaded context
```

## Via MCP

```
smalltalk_route(directory, task, top_n)
```

Available as tool 19 in the MCP server.

## Tips

- Use descriptive file names (`seo-expert.st` beats `skill1.st`) — the structural
  score rewards this
- Put `USE: <id> | when:<trigger-keywords>` in your skill files — these have
  the highest content weight
- Route against your `skills/` directory, not `_brain/` — skills have the right
  entry types for routing. Use `wake-up` for fact/decision context.
