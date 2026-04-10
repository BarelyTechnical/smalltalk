# smalltalk route

Map a task description to the most relevant .st skill/agent files.

Use this at session start to know which skills to load for the current task.
More precise than `navigate` for task-type selection.

---

## Command

    smalltalk route <dir> "<task>"
    smalltalk route <dir> "<task>" --top 3

---

## Examples

    smalltalk route skills/ "build a landing page for a plumbing business"
    → ui-designer.st       (score:9)
    → seo-expert.st        (score:7)
    → conversion-copy.st   (score:5)

    smalltalk route _brain/ "debug the authentication flow"
    → debugging-agent.st   (score:11)
    → patterns.st          (score:6)

---

## How scoring works

Route combines two signals:

    Structural    file/dir name keyword match
    Content       SKILL trigger fields, USE when: fields, AGENT capabilities

Entry type weights:

    SKILL    3x   direct skill declaration — highest signal
    USE      3x   explicit trigger condition
    AGENT    2x   agent capability declaration
    TRIGGER  2x   event-based trigger
    RULE     1x   general rules

---

## When to use route vs navigate

    route       task-type matching: "build", "debug", "review", "write"
                best for: selecting which skills/agents to activate

    navigate    domain navigation: "auth", "billing", "deploy"
                best for: finding project-specific context files

Use both at session start for full orientation:

    smalltalk route skills/ "<task>"       # which skills to load
    smalltalk navigate _brain/ "<domain>"  # which domain context to load

---

## MCP equivalent

    smalltalk_route(directory, task, top_n=5)

---

## Workflow integration

    # At session start:
    smalltalk_route("skills/", "build a landing page")
    → returns top 5 skill files

    for each file:
        smalltalk_read_file(path)  → load skill

    # Agent is now oriented for the task before the first message.
