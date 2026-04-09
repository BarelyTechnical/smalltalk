# smalltalk closing-ritual

The session-end write-back protocol.

Every Smalltalk-oriented agent MUST run the closing ritual when work is complete.
This is what closes the PAG loop — the brain grows every session, automatically.

---

## The Loop

Without closing ritual:
    Session start → read .st files → do work → session ends → brain unchanged
    Next session starts from the same brain. It doesn't grow.

With closing ritual:
    Session start → read .st files → do work →
    closing ritual → write DECISION / PATTERN / WIN / ERROR entries →
    next session starts smarter than the last.

---

## When to Run

Run the closing ritual when:
- A task is complete
- A decision was made
- A bug was found and fixed
- A technique worked (worth repeating)
- A technique failed (worth avoiding)
- Any session ends where something was learned

---

## What to Write

Ask yourself these four questions at session end:

    1. Did I make a decision that should persist?
       → Write a DECISION: entry
    
    2. Did something break and get fixed?
       → Write a PATTERN: entry
    
    3. Did a technique produce a clearly good outcome?
       → Write a WIN: entry
    
    4. Did something fail that I couldn't resolve?
       → Write an ERROR: entry to the relevant agent diary

---

## Entry Formats

    DECISION: <subject> | <choice>><rejected> | <reason> | <YYYY-MM>
    PATTERN:  <subject> | broke:<what> | cause:<why> | fix:<what> | reuse:y/n
    WIN:      <subject> | <technique> | <outcome> | repeat:y/n
    ERROR:    <subject> | broke:<what> | cause:<why> | state:recovered|unresolved

One line per entry. Lowercase-hyphenated values. No prose.

---

## How to Write

### Via CLI

    smalltalk diary write <agent-id> "DECISION: deploy | railway>vercel | cost+dx | 2026-04"
    smalltalk diary write <agent-id> "PATTERN: jwt | broke:auth | cause:missing-exp | fix:add-exp-claim | reuse:y"
    smalltalk diary write <agent-id> "WIN: palette-navigate | score-wing-then-room | 34pct-boost | repeat:y"

### Via MCP (recommended for agents)

    smalltalk_diary_write(
        agent_id="reviewer",
        entry="PATTERN: n-plus-one | broke:slow-list | cause:orm-lazy | fix:select-related | reuse:y"
    )

---

## Run Contradiction Check After Writing

After adding entries, check for new contradictions before the session ends:

    smalltalk check <dir>          # CLI
    smalltalk_check("<dir>")       # MCP

If contradictions are found, resolve them:

    smalltalk kg invalidate <file> <line_no>   # close the older entry

---

## Full Closing Ritual Sequence

    # 1. Identify what was learned this session
    #    (decisions, patterns, wins, errors)

    # 2. Write entries
    smalltalk_diary_write(agent_id, "DECISION: ...")
    smalltalk_diary_write(agent_id, "PATTERN: ...")
    smalltalk_diary_write(agent_id, "WIN: ...")

    # 3. Check for contradictions
    smalltalk_check(directory)

    # 4. Resolve any contradictions flagged
    #    smalltalk_kg_invalidate(file, line_no)

    # 5. Re-check to confirm clean
    #    smalltalk_check(directory)

---

## Rule

    RULE: session-end | write-decisions-patterns-wins-to-brain | hard
    TRIGGER: task-complete | event:session-end | then:smalltalk_diary_write

This is not optional. A Smalltalk-oriented agent that doesn't close the loop
is an agent that can't compound. Every build, every decision, every failure
that doesn't get written back is lost forever.

The read side is free. The write side is the investment.

---

## MCP Quick Reference

    smalltalk_diary_write(agent_id, entry)   — write one entry
    smalltalk_diary_read(agent_id)           — verify entries were written
    smalltalk_check(directory)               — check for new contradictions
    smalltalk_kg_invalidate(file, line_no)   — resolve a contradiction

---

## Example: Full Developer Session Closing Ritual

Session: Built OAuth flow for a new project.

    smalltalk_diary_write("architect", "DECISION: auth | clerk>auth0 | sdk-simplicity+react-native | 2026-04")
    smalltalk_diary_write("reviewer", "PATTERN: jwt | broke:silent-fail | cause:missing-exp | fix:add-exp-claim | reuse:y")
    smalltalk_diary_write("architect", "WIN: clerk-setup | one-sdk-all-platforms | zero-custom-middleware | repeat:y")
    smalltalk_check("_brain/")

Next session: the architect agent already knows Clerk won, why, and that the JWT exp fix is reusable.
No context files needed. No reminders. Already known.
