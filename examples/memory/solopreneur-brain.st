DECISION: stack | nextjs+supabase>rails | modern+serverless+managed-db | 2025-01
DECISION: deploy | vercel>self-hosted | zero-ops+free-tier | 2025-01
DECISION: payments | stripe>paddle | developer-experience+docs | 2025-02
DECISION: email | resend>sendgrid | modern-api+vercel-native | 2025-02
PATTERN:  env-vars | broke:vercel-deploy | cause:missing-env-in-dashboard | fix:sync-local-to-vercel | reuse:y
PATTERN:  supabase-rls | broke:public-data-exposed | cause:missing-rls-policy | fix:add-select-policy | reuse:y
PATTERN:  stripe-webhook | broke:payment-not-recorded | cause:no-signature-verify | fix:verify-stripe-sig | reuse:y
WIN:      landing | single-html | fastest-to-ship+cheap | repeat:y
WIN:      auth | supabase-magic-link | no-password-ux | repeat:n
WIN:      outreach | personalised-loom | higher-reply-rate | repeat:y
CLIENT:   startup-a | pref:fast-iterations | avoid:long-docs | updated:2025-03
CLIENT:   ecom-b | pref:pixel-perfect | avoid:stock-photos | updated:2025-02
