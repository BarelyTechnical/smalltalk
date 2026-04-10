# Smalltalk — global session orientation
# Copy this to ~/.claude/CLAUDE.md to orient every Claude Code session automatically

## Session Start (always run first)

1. Call `smalltalk_wake_up` on the _brain/ directory of the current project
2. Read the output — note all active DECISION, RULE, and PATTERN entries
3. Call `smalltalk_navigate` to locate relevant files for the current task
4. Do not ask for context that is already loaded

## During Work

- Use `smalltalk_navigate(dir, task)` before `smalltalk_search(dir, query)`
- Use `smalltalk_route(dir, task)` to identify which skill files to load
- Use `smalltalk_kg_query(dir, entity)` to understand relationships
- Run `smalltalk_check(dir)` before any deploy, merge, or production push

## Session End (required — hard rule)

Run the closing ritual. This is not optional.

1. Identify: decisions made, patterns found, wins, errors encountered
2. Write each as a Smalltalk entry via `smalltalk_diary_write(agent_id, entry)`
3. Run `smalltalk_check(_brain/)` — resolve any contradictions found
4. One entry minimum. Two minutes maximum.

Full protocol: `smalltalk instructions closing-ritual`

## Embedded rules

RULE: session-end | write-decisions-patterns-wins-to-brain | hard
RULE: session-start | run-wake-up-before-asking-for-context | hard
TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write
TRIGGER: session-open | event:session-start | then:smalltalk_wake_up
