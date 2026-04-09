# Smalltalk — Global Session Protocol

## Session Start (always — every session, every project)

1. Check if the project has a `_brain/` or `_index.st` — if yes:
   - Run `smalltalk_wake_up` on `_brain/` — load DECISION, RULE, PATTERN, WIN context
   - Run `smalltalk_diary_read` for the active agent id — load accumulated expertise
2. Check if a task has been given — if yes:
   - Run `smalltalk_route` on the skills directory for the task description
   - Load the top-scored skill files via `smalltalk_read_file`
3. Note what was loaded. Do not re-ask for context that is already in scope.

## During Work

- Use `smalltalk_navigate` to find relevant files before `smalltalk_search`
- Use `smalltalk_route` when selecting which skill or agent to activate
- Use `smalltalk_kg_query` to understand entity relationships
- Use `smalltalk_check` before any deployment or production push

## Session End (hard rule — not optional)

RULE: session-end | write-decisions-patterns-wins-to-brain | hard
TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write

Run the closing ritual before the session ends:
1. Identify decisions made, patterns found, wins, errors this session
2. Write each as a Smalltalk entry via `smalltalk_diary_write(agent_id, entry)`
3. Run `smalltalk_check` on `_brain/`
4. Resolve any contradictions found via `smalltalk_kg_invalidate`

Entry formats:
    DECISION: <subject> | <choice>><rejected> | <reason> | <YYYY-MM>
    PATTERN:  <subject> | broke:<what> | cause:<why> | fix:<what> | reuse:y/n
    WIN:      <subject> | <technique> | <outcome> | repeat:y/n
    ERROR:    <subject> | broke:<what> | cause:<why> | state:recovered|unresolved

Full protocol: `smalltalk instructions closing-ritual`

## If a project has no Smalltalk setup yet

Run: `smalltalk_bootstrap_info()` — returns exact setup commands.
Or: `smalltalk bootstrap <dir>` — one-command full setup.

## Grammar reference

Run: `smalltalk_get_spec()` for the full type reference.
Run: `smalltalk instructions <command>` for step-by-step guides.
