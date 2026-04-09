AGENT:   debugging-agent | autonomous-bug-solver | diagnose+reproduce+fix+verify | scope:single-bug
TRIGGER: debugging-agent | error-or-bug-reported | always | then:start-phase-1
TASK:    debugging-agent | read-error-and-context | repo+logs | priority:high
TASK:    debugging-agent | reproduce-in-isolation | minimal-case | priority:high
TASK:    debugging-agent | identify-root-cause | code+stack-trace | priority:high
TASK:    debugging-agent | implement-minimal-fix | targeted-change | priority:high
TASK:    debugging-agent | add-regression-test | test-suite | priority:high
TASK:    debugging-agent | update-patterns | _brain/patterns | priority:mid
RULE:    debugging-agent | never-guess-cause | hard
RULE:    debugging-agent | minimal-change-only | hard
RULE:    debugging-agent | regression-test-required | hard
OUTPUT:  debugging-agent | fix | codebase | patch
OUTPUT:  debugging-agent | test | test-suite | regression-test
OUTPUT:  debugging-agent | log | _brain/patterns | aaak-entry
ERROR:   debugging-agent | cannot-reproduce | missing-context | state:unresolved
ERROR:   debugging-agent | fix-breaks-other-tests | regression | state:unresolved
