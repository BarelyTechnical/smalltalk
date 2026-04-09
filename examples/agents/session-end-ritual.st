AGENT:   session-end-ritual | brain-updater | write-decisions+patterns+wins+errors | scope:global
TRIGGER: session-end-ritual | task-complete | event:session-end | then:write-brain
RULE:    session-end-ritual | write-before-session-ends | hard
RULE:    session-end-ritual | one-line-per-item-aaak-format-only | hard
RULE:    session-end-ritual | check-contradictions-after-writing | hard
TASK:    session-end-ritual | identify-decisions-made | session-context | priority:high
TASK:    session-end-ritual | identify-patterns-found | bugs+fixes+workarounds | priority:high
TASK:    session-end-ritual | identify-wins | techniques+outcomes | priority:mid
TASK:    session-end-ritual | identify-errors | unresolved-failures | priority:mid
TASK:    session-end-ritual | write-entries-via-diary-write | smalltalk-mcp | priority:high
TASK:    session-end-ritual | run-contradiction-check | _brain | priority:mid
TASK:    session-end-ritual | resolve-contradictions-if-found | kg-invalidate | priority:high
OUTPUT:  session-end-ritual | decision-entries | diary/<agent-id>.st | aaak-lines
OUTPUT:  session-end-ritual | pattern-entries | diary/<agent-id>.st | aaak-lines
OUTPUT:  session-end-ritual | win-entries | diary/<agent-id>.st | aaak-lines
OUTPUT:  session-end-ritual | check-result | stdout | contradiction-report
ERROR:   session-end-ritual | nothing-to-write | no-decisions-made | state:recovered
NOTE:    session-end-ritual | even-null-sessions | write-at-least-a-status-win | always
