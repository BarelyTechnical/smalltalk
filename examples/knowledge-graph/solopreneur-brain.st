# Smalltalk v3.0.0 — KG example: solopreneur brain
# Single-person setup — track projects, tools, and decisions over time.

# ── Active projects ───────────────────────────────────────────────────────────

LINK: me | rel:works-on     | pixel-palace  | valid_from:2025-10 | stability:transient
LINK: me | rel:works-on     | smalltalk     | valid_from:2026-01 | stability:transient
LINK: me | rel:based-in     | johannesburg  | stability:permanent

# ── Clients ──────────────────────────────────────────────────────────────────

LINK: enn-driving-school | rel:client-of   | me  | valid_from:2026-03 | stability:stable
LINK: enn-driving-school | rel:deployed-to | cloudflare-pages | valid_from:2026-03 | stability:stable

# ── Tool decisions ────────────────────────────────────────────────────────────

DECISION: hosting    | cloudflare-pages>vercel  | free-tier+pixel-palace-demos | 2026-02 | stability:stable
DECISION: ai-default | anthropic>openai          | claude-code-integration       | 2026-01 | stability:stable
DECISION: stack      | nextjs>remix              | ecosystem-size+vercel-support | 2025-11 | stability:stable
DECISION: database   | supabase>planetscale      | postgres+auth+storage-bundle  | 2025-10 | stability:stable

# ── Previously considered, now closed ────────────────────────────────────────

LINK: me | rel:works-on | openclaw | valid_from:2026-02 | ended:2026-04 | stability:transient

# ── Permanent rules ───────────────────────────────────────────────────────────

RULE: outreach | no-cold-pitch-without-demo-ready | hard | stability:permanent
RULE: pricing  | never-discount-below-cost        | hard | stability:permanent

# ── Recurring patterns ─────────────────────────────────────────────────────────

PATTERN: deploy | broke:cloudflare-build-fail | cause:missing-env-var | fix:check-dashboard-env | reuse:y
PATTERN: mine   | broke:converter-hallucination | cause:too-little-context | fix:add-file-type-hint | reuse:y

WIN: palace-navigate | score-wing-then-room | 34pct-retrieval-boost | repeat:y
WIN: dry-run-first   | preview-before-write | caught-bugs-before-prod | repeat:y
