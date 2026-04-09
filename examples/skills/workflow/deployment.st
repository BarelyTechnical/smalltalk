SKILL:   deployment | pre-deploy+deploy+verify+rollback | ci-cd | v1.0.0
USE:     deployment | when:shipping+release+production-push
PHASE:   deployment | 1 | pre-check | tests-pass+build-clean+env-vars-set
PHASE:   deployment | 2 | backup | database-backup-if-schema-change
PHASE:   deployment | 3 | deploy | staging-first+production-second
PHASE:   deployment | 4 | verify | smoke-test+monitoring-check
PHASE:   deployment | 5 | rollback | revert-if-error-rate-spikes
RULE:    deployment | staging-before-production | hard
RULE:    deployment | database-backup-before-migration | hard
RULE:    deployment | smoke-test-required | hard
RULE:    deployment | rollback-plan-before-deploy | hard
RULE:    deployment | deploy-in-low-traffic-window | soft
CHECK:   deployment | smoke-test-passes | required
CHECK:   deployment | error-rate-normal | required
CHECK:   deployment | rollback-tested | required
AVOID:   deployment | skip-staging+no-backup+no-smoke-test+deploy-during-peak
