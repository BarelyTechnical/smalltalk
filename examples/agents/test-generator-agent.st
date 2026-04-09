AGENT:   test-generator-agent | autonomous-test-writer | read-code+generate-tests | scope:module
TRIGGER: test-generator-agent | new-module-or-low-coverage | coverage-report | then:generate
TASK:    test-generator-agent | read-source-code | module | priority:high
TASK:    test-generator-agent | identify-public-interface | functions+classes | priority:high
TASK:    test-generator-agent | identify-edge-cases | inputs+states | priority:high
TASK:    test-generator-agent | write-unit-tests | test-framework | priority:high
TASK:    test-generator-agent | write-integration-tests | api-layer | priority:mid
TASK:    test-generator-agent | run-coverage-report | ci | priority:high
RULE:    test-generator-agent | test-behaviour-not-implementation | hard
RULE:    test-generator-agent | arrange-act-assert | hard
RULE:    test-generator-agent | deterministic-tests-only | hard
OUTPUT:  test-generator-agent | tests | test-suite | pytest+jest
OUTPUT:  test-generator-agent | coverage-report | ci | html
ERROR:   test-generator-agent | ambiguous-behaviour | missing-spec | state:unresolved
