SKILL:   api-designer | rest+graphql+versioning+contracts | openapi+graphql | v1.0.0
USE:     api-designer | when:api-design+rest+graphql+public-interface
STACK:   api-designer | rest | openapi3 | documented+versioned
STACK:   api-designer | graphql | schema-first | typed+introspectable
STACK:   api-designer | contracts | zod+pydantic | validated
RULE:    api-designer | resources-not-actions-in-rest | hard
RULE:    api-designer | consistent-naming-conventions | hard
RULE:    api-designer | versioned-from-day-one | hard
RULE:    api-designer | document-before-implement | soft
RULE:    api-designer | error-responses-always-structured | hard
RULE:    api-designer | pagination-for-collections | hard
STEP:    api-designer | design | 1 | define-resources-and-operations | required
STEP:    api-designer | design | 2 | write-openapi-schema-first | required
STEP:    api-designer | design | 3 | define-error-response-shapes | required
STEP:    api-designer | review | 4 | consumer-review-before-build | optional
CHECK:   api-designer | all-errors-have-structured-response | required
CHECK:   api-designer | pagination-on-all-collections | required
AVOID:   api-designer | rpc-style-rest+unversioned+undocumented+inconsistent-naming
