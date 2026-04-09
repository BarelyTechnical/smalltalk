# smalltalk diary

Specialist agent diary — append-only per-agent knowledge base.
Agents accumulate expertise across sessions and repos.

---

## Commands

    smalltalk diary write <agent-id> "<entry>"
    smalltalk diary read  <agent-id>
    smalltalk diary read  <agent-id> --last 10
    smalltalk diary list

---

## Storage

    ~/.smalltalk/diaries/<agent-id>.st

Global and cross-project. A reviewer agent that finds a JWT bug in Project A
carries that knowledge into Project B. The diary is not project-scoped.

---

## Write examples

    smalltalk diary write reviewer \
      "PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y"

    smalltalk diary write architect \
      "DECISION: cache | redis>memcached | pub-sub+data-structures | 2025-04"

    smalltalk diary write ops \
      "WIN: deploy | blue-green | zero-downtime | repeat:y"

    smalltalk diary write security \
      "PATTERN: sql-inject | broke:search | cause:raw-query | fix:parameterize | reuse:y"

---

## Read example

    smalltalk diary read reviewer

    → Diary: reviewer (last 20 entries)

      PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y  # 2026-04-08
      PATTERN: sql-inject | broke:search | cause:raw-query | fix:parameterize | reuse:y  # 2026-04-08

---

## Conventions

- agent-id is lowercase: reviewer, architect, ops, security, data, frontend
- Entries should be valid Smalltalk .st lines (TYPE: id | ...)
- PATTERN entries are the most useful — they encode solved bugs
- DECISION entries track the agent's own design choices
- WIN entries track what's worth repeating

---

## MCP equivalents

    smalltalk_diary_write(agent_id="reviewer", entry="PATTERN: ...")
    smalltalk_diary_read(agent_id="reviewer", last_n=20)

---

## Workflow

    # After every code review:
    smalltalk diary write reviewer "PATTERN: <found-bug> | ..."

    # At session start (agent reads its own history):
    smalltalk diary read reviewer --last 10
    # → agent stays sharp in its domain across sessions
