DECISION: platform | postgresql>mongodb | acid+relational+mature | 2024-11
DECISION: auth | jwt-stateless>sessions | scalability+microservices | 2024-11
DECISION: api | rest+openapi>graphql | team-familiarity+simplicity | 2024-12
DECISION: cache | redis>memcached | data-structures+pub-sub | 2025-01
PATTERN:  n-plus-one | broke:slow-list-endpoint | cause:orm-default-fetch | fix:select-related+prefetch | reuse:y
PATTERN:  cors-error | broke:frontend-api-call | cause:missing-origin-header | fix:configure-cors-middleware | reuse:y
PATTERN:  migration-lock | broke:deployment | cause:long-migration-on-live | fix:zero-downtime-migration | reuse:y
WIN:      platform | postgres-jsonb | flexible-schema-without-nosql | repeat:y
WIN:      auth | refresh-token-rotation | silent-re-auth+better-security | repeat:y
WIN:      deployment | staging-parity | fewer-prod-surprises | repeat:y
RULE:     team | squash-merge-only | hard
RULE:     team | pr-max-400-lines | soft
RULE:     team | migrations-reversible | hard
