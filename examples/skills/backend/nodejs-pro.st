SKILL:   nodejs-pro | node+express+async+streams | node.js+typescript | v1.0.0
USE:     nodejs-pro | when:backend-api+microservice+cli+event-driven
STACK:   nodejs-pro | runtime | node20 | esm+built-in-fetch+streams
STACK:   nodejs-pro | api | express+zod | routing+validation
STACK:   nodejs-pro | async | async-await+event-emitter | non-blocking
STACK:   nodejs-pro | testing | jest+supertest | unit+integration
RULE:    nodejs-pro | esm-over-commonjs | hard
RULE:    nodejs-pro | zod-for-request-validation | hard
RULE:    nodejs-pro | error-first-middleware | hard
RULE:    nodejs-pro | streams-for-large-data | soft
RULE:    nodejs-pro | no-blocking-io-on-main-thread | hard
RULE:    nodejs-pro | centralized-error-handler | hard
STEP:    nodejs-pro | setup | 1 | tsconfig-target-node20 | required
STEP:    nodejs-pro | build | 2 | define-routes-and-middleware-chain | required
STEP:    nodejs-pro | build | 3 | add-zod-validation-per-route | required
STEP:    nodejs-pro | error | 4 | global-error-handler-last | required
CHECK:   nodejs-pro | unhandled-promise-rejections-caught | required
CHECK:   nodejs-pro | no-sync-fs-in-request-path | required
AVOID:   nodejs-pro | callbacks+sync-methods+blocking-loops+global-error-swallowing
