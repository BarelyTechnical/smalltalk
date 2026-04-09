AGENT:   api-testing-agent | api-qa | generate-tests+run+report | scope:api
TRIGGER: api-testing-agent | api-change+pre-deploy | ci+pr | then:test
TASK:    api-testing-agent | read-openapi-schema | spec | priority:high
TASK:    api-testing-agent | generate-test-cases | endpoints | priority:high
TASK:    api-testing-agent | test-happy-paths | endpoints | priority:high
TASK:    api-testing-agent | test-error-cases | endpoints | priority:high
TASK:    api-testing-agent | test-auth-boundaries | endpoints | priority:high
TASK:    api-testing-agent | report-results | ci | priority:high
RULE:    api-testing-agent | test-auth-on-every-protected-endpoint | hard
RULE:    api-testing-agent | test-error-responses | hard
OUTPUT:  api-testing-agent | test-suite | tests/ | http-files+pytest
OUTPUT:  api-testing-agent | report | ci | pass-fail-summary
ERROR:   api-testing-agent | no-openapi-spec | missing-schema | state:unresolved
