# smalltalk bootstrap

One-command project setup. Gets a directory fully oriented as a Smalltalk palace.

---

## Command

    smalltalk bootstrap <dir>
    smalltalk bootstrap <dir> --api-key <key>
    smalltalk bootstrap <dir> --dry-run

---

## What it runs

    Step 1  backup         Copy all .md files to .originals/
    Step 2  mine           Convert .md to .st format (skipped if no API key)
    Step 3  palace init    Generate _index.st
    Step 4  config         Write CLAUDE.md to project root

Each step is equivalent to running the individual command manually.

---

## Arguments

    --api-key    API key for the mine step (OpenRouter by default)
                 Set OPENROUTER_API_KEY env var to avoid passing it each time
    --model      LLM model for conversion (default: anthropic/claude-haiku-4-5)
    --base-url   OpenAI-compatible endpoint (default: OpenRouter)
    --dry-run    Preview what would happen without making any changes

---

## After bootstrap

    smalltalk wake-up <dir>     Verify context — see what the agent loads
    smalltalk check <dir>       Verify clean — no contradictions
    smalltalk status <dir>      Show conversion progress

---

## MCP equivalent

    smalltalk_bootstrap_info()   Returns the bootstrap protocol and next steps.

---

## Closing the loop

Bootstrap sets up the read side. To close the PAG loop, add to CLAUDE.md:

    RULE: session-end | write-decisions-patterns-wins-to-brain | hard
    TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write

Then: smalltalk instructions closing-ritual

---

## Manual equivalent (if you prefer step by step)

    smalltalk init <dir>          1. See what's convertible
    smalltalk backup <dir>        2. Back up originals
    smalltalk mine <dir>          3. Convert to .st
    smalltalk palace init <dir>   4. Generate _index.st
    smalltalk install-hook <dir>  5. Auto-convert on git commit (optional)
