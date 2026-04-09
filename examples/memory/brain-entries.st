DECISION: my-app | postgres>sqlite | concurrent-writes+dataset-exceeds-10gb | 2026-01-15
DECISION: my-app | cloudflare-pages>vercel | free-tier+github-native+no-build-config | 2026-02-03
DECISION: my-app | openrouter>direct-anthropic | per-token-pricing+model-flexibility | 2026-02-20
DECISION: my-app | tailwind>css-modules | utility-first-faster-iteration+no-context-switching | 2026-03-01

PATTERN:  my-app | broke:vite-build-missing-pages | cause:hardcoded-rollup-input | fix:fast-glob-dynamic-discovery | reuse:y
PATTERN:  my-app | broke:supabase-auth-redirect | cause:missing-callback-route | fix:add-auth-callback-handler | reuse:y
PATTERN:  my-app | broke:env-var-undefined-prod | cause:vercel-env-not-set | fix:add-to-vercel-dashboard | reuse:y
PATTERN:  my-app | broke:n8n-webhook-timeout | cause:long-running-sync-operation | fix:switch-to-async+respond-202 | reuse:y

WIN:      my-app | schema-first-design | no-migration-surprises+clear-api-contract | repeat:y
WIN:      my-app | dry-run-before-destructive-ops | caught-3-bugs-before-they-hit-prod | repeat:y
WIN:      my-app | single-conversion-action-per-page | higher-cta-clickthrough | repeat:y

CLIENT:   acme-corp | pref:dark-theme+bold-typography+professional | avoid:stock-photos+generic-icons | updated:2026-03-10
CLIENT:   studio-x | pref:minimal+whitespace+feminine | avoid:heavy-gradients+dark-palette | updated:2026-02-28

COMPONENT: data-table | react+tanstack-table+tailwind | sortable-filterable-paginated-table | use-when:list-view-with-actions
COMPONENT: scroll-counter | vanilla-js+intersection-observer | animates-numbers-on-scroll-enter | use-when:stats-section
COMPONENT: toast-notify | react+sonner | ephemeral-feedback-messages | use-when:form-submit+api-response

PROMPT:   code-review | ask-for-three-failure-modes-before-approving | surfaces-edge-cases-llm-misses | reuse:y
PROMPT:   cold-outreach | specific-pain-point-first+no-direct-ask-in-first-message | higher-reply-rate | reuse:y
PROMPT:   debugging | paste-full-error+ask-for-cause-before-fix | avoids-symptom-only-fixes | reuse:y
