SKILL:   devops-engineer | ci-cd+docker+pipelines+deployment | docker+github-actions | v1.0.0
USE:     devops-engineer | when:ci-cd+deployment+containerization+automation
STACK:   devops-engineer | containers | docker+docker-compose | build+run
STACK:   devops-engineer | ci-cd | github-actions | test+lint+build+deploy
STACK:   devops-engineer | secrets | env+vault | never-hardcoded
STACK:   devops-engineer | monitoring | healthchecks+alerts | production-aware
RULE:    devops-engineer | everything-in-a-container | hard
RULE:    devops-engineer | secrets-never-in-code | hard
RULE:    devops-engineer | test-before-deploy | hard
RULE:    devops-engineer | idempotent-deployments | hard
RULE:    devops-engineer | rollback-plan-before-deploy | hard
STEP:    devops-engineer | ci | 1 | lint-and-test-on-pr | required
STEP:    devops-engineer | ci | 2 | build-and-push-image-on-merge | required
STEP:    devops-engineer | cd | 3 | deploy-to-staging-then-prod | required
STEP:    devops-engineer | verify | 4 | smoke-test-after-deploy | required
CHECK:   devops-engineer | no-secrets-in-image | required
CHECK:   devops-engineer | rollback-tested | required
AVOID:   devops-engineer | hardcoded-secrets+manual-deploy+skip-staging+no-healthcheck
