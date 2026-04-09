SKILL:   fastapi-expert | fastapi+pydantic+async+openapi | python+fastapi | v1.0.0
USE:     fastapi-expert | when:rest-api+python-backend+async+openapi-docs
STACK:   fastapi-expert | framework | fastapi | async+auto-openapi
STACK:   fastapi-expert | validation | pydantic-v2 | request+response+settings
STACK:   fastapi-expert | auth | oauth2+jwt | bearer-token+scopes
STACK:   fastapi-expert | db | sqlalchemy-async+alembic | orm+migrations
STACK:   fastapi-expert | testing | httpx+pytest-asyncio | async-test-client
RULE:    fastapi-expert | response-model-always | hard
RULE:    fastapi-expert | dependency-injection-for-db-and-auth | hard
RULE:    fastapi-expert | async-endpoints-for-io | hard
RULE:    fastapi-expert | pydantic-settings-for-config | hard
RULE:    fastapi-expert | router-prefix-and-tags | hard
RULE:    fastapi-expert | http-exceptions-not-bare-raise | hard
STEP:    fastapi-expert | setup | 1 | create-app-router-structure | required
STEP:    fastapi-expert | build | 2 | define-pydantic-schemas-first | required
STEP:    fastapi-expert | build | 3 | implement-dependency-chain | required
STEP:    fastapi-expert | build | 4 | add-response-models-to-all-routes | required
CHECK:   fastapi-expert | openapi-docs-generate-clean | required
CHECK:   fastapi-expert | all-routes-have-response-model | required
AVOID:   fastapi-expert | sync-endpoints+dict-returns+global-state+unversioned-routes
