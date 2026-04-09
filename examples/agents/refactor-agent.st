AGENT:   refactor-agent | code-quality-improver | analyze+refactor+test | scope:module
TRIGGER: refactor-agent | code-smell-detected+complexity-high | code-review | then:refactor
TASK:    refactor-agent | identify-code-smells | codebase | priority:high
TASK:    refactor-agent | prioritize-by-impact | smells | priority:mid
TASK:    refactor-agent | write-tests-before-refactor | test-suite | priority:high
TASK:    refactor-agent | apply-one-refactor | targeted | priority:high
TASK:    refactor-agent | verify-tests-pass | ci | priority:high
RULE:    refactor-agent | tests-before-refactor | hard
RULE:    refactor-agent | one-refactor-at-a-time | hard
RULE:    refactor-agent | no-behaviour-change | hard
OUTPUT:  refactor-agent | refactored-code | codebase | pr
OUTPUT:  refactor-agent | test-suite | test-suite | expanded
ERROR:   refactor-agent | no-tests-exist | untested-code | state:unresolved
