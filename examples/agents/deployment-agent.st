AGENT:   deployment-agent | deployment-runner | build+test+stage+deploy+verify | scope:app
TRIGGER: deployment-agent | merge-to-main+manual | github+cli | then:deploy
TASK:    deployment-agent | run-test-suite | ci | priority:high
TASK:    deployment-agent | build-artifact | docker+bundle | priority:high
TASK:    deployment-agent | deploy-to-staging | staging | priority:high
TASK:    deployment-agent | run-smoke-tests | staging | priority:high
TASK:    deployment-agent | deploy-to-production | production | priority:high
TASK:    deployment-agent | verify-production | smoke-test+monitoring | priority:high
TASK:    deployment-agent | rollback-if-error | production | priority:high
RULE:    deployment-agent | staging-before-prod | hard
RULE:    deployment-agent | rollback-on-error-rate-spike | hard
OUTPUT:  deployment-agent | deployed-app | production | live
OUTPUT:  deployment-agent | deploy-report | slack+logs | summary
ERROR:   deployment-agent | smoke-test-fail | production | state:unresolved
