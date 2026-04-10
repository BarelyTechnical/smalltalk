# Waza Engineering Habits — compressed for any model, any platform
# Source: github.com/tw93/Waza — 8 habits from 500+ hours, 7 projects, 300+ sessions
# Encoded by Smalltalk as model-agnostic .st entries
# Load in _brain/ — habits auto-load with wake-up

# ══════════════════════════════════════════════════════════
# HABITS — the 8 disciplines
# ══════════════════════════════════════════════════════════

SKILL: think | when:before-new-feature+architecture-decision+complex-task | stack:analysis+planning | version:1
USE: think | when:feature-design+architecture+tech-decision+system-design
RULE: think | analyse-problem-and-plan-before-writing-code | hard
STEP: think | phase:1 | number:1 | restate-goal-in-own-words | required
STEP: think | phase:1 | number:2 | identify-constraints-and-assumptions | required
STEP: think | phase:1 | number:3 | sketch-approach-before-implementing | required
STEP: think | phase:1 | number:4 | flag-risks-and-open-questions | required
AVOID: think | jumping-to-code+skipping-analysis+assuming-requirements

SKILL: hunt | when:debugging+error+unexpected-behaviour+regression | stack:root-cause-analysis | version:1
USE: hunt | when:bug+error+test-failure+unexpected+crash+regression
RULE: hunt | find-root-cause-before-touching-code | hard
STEP: hunt | phase:1 | number:1 | reproduce-the-error-first | required
STEP: hunt | phase:1 | number:2 | read-error-message-completely | required
STEP: hunt | phase:1 | number:3 | trace-to-root-cause-not-symptom | required
STEP: hunt | phase:1 | number:4 | fix-root-cause-not-symptom | required
STEP: hunt | phase:1 | number:5 | verify-fix-did-not-break-anything | required
AVOID: hunt | guessing+patching-symptoms+fixing-without-reproducing
PATTERN: hunt | broke:wrong-layer | cause:fixing-symptom-not-root | fix:trace-up-call-stack-to-origin | reuse:y

SKILL: check | when:implementation-complete+before-merge+before-deploy | stack:code-review+testing | version:1
USE: check | when:after-implementing+before-pr+before-deploy+before-commit
RULE: check | review-before-merging | hard
STEP: check | phase:1 | number:1 | does-it-handle-edge-cases | required
STEP: check | phase:1 | number:2 | are-there-tests | required
STEP: check | phase:1 | number:3 | is-error-handling-present | required
STEP: check | phase:1 | number:4 | does-it-match-the-spec | required
STEP: check | phase:1 | number:5 | run-smalltalk-check-on-brain | required
AVOID: check | shipping-without-review+assuming-it-works+skipping-edge-cases

SKILL: design | when:building-ui+component+page+layout+visual | stack:ui+ux+css | version:1
USE: design | when:any-ui+component+landing-page+dashboard+form+modal
RULE: design | follow-design-system-before-writing-css | hard
STEP: design | phase:1 | number:1 | check-existing-components-first | required
STEP: design | phase:1 | number:2 | follow-brand-and-spacing-rules | required
STEP: design | phase:1 | number:3 | mobile-first | required
STEP: design | phase:1 | number:4 | check-contrast-and-accessibility | required
AVOID: design | inline-styles+reinventing-components+ignoring-brand

SKILL: health | when:agent-ignoring-instructions+hooks-misfiring+loop-detected | stack:diagnostics | version:1
USE: health | when:agent-not-following-rules+mcp-broken+session-state-wrong+drift-detected
RULE: health | diagnose-before-resetting | hard
STEP: health | phase:1 | number:1 | run-smalltalk-check | required
STEP: health | phase:1 | number:2 | read-active-rules-from-brain | required
STEP: health | phase:1 | number:3 | identify-what-rule-was-violated | required
STEP: health | phase:1 | number:4 | restate-active-rules-to-agent | required
AVOID: health | resetting-without-diagnosing+adding-more-rules

SKILL: write | when:asked-to-write-prose+documentation+copy+content | stack:writing | version:1
USE: write | when:README+docs+blog+copy+email+social+content
RULE: write | human-first-person-conversational-no-em-dashes | hard
RULE: write | no-ai-formatting-tells-no-bold-bullets-no-passive | hard
STEP: write | phase:1 | number:1 | identify-audience-and-goal | required
STEP: write | phase:1 | number:2 | write-as-a-real-person-not-an-ai | required
STEP: write | phase:1 | number:3 | cut-anything-that-doesnt-add-value | required
AVOID: write | em-dashes+bold-bullet-leads+passive-voice+ai-patterns

SKILL: learn | when:unfamiliar-domain+new-tech+deep-dive-needed | stack:research | version:1
USE: learn | when:new-library+framework+concept+domain+approaching-unknown
RULE: learn | understand-before-using | hard
STEP: learn | phase:1 | number:1 | read-official-docs-first | required
STEP: learn | phase:1 | number:2 | find-one-working-example | required
STEP: learn | phase:1 | number:3 | write-own-minimal-example | required
STEP: learn | phase:1 | number:4 | log-key-patterns-to-brain | required
AVOID: learn | cargo-culting+copying-without-understanding

SKILL: read | when:given-url+pdf+doc+article | stack:extraction | version:1
USE: read | when:url+pdf+document+article+specification+guide
RULE: read | extract-structured-insights-before-responding | hard
STEP: read | phase:1 | number:1 | read-fully-before-summarising | required
STEP: read | phase:1 | number:2 | extract-decisions-patterns-rules | required
STEP: read | phase:1 | number:3 | flag-contradictions-with-brain | required
STEP: read | phase:1 | number:4 | write-key-insights-to-diary | required
AVOID: read | skimming+responding-before-reading+losing-insights

# ══════════════════════════════════════════════════════════
# ROUTING — when to invoke which habit
# ══════════════════════════════════════════════════════════

TRIGGER: think-trigger | event:feature-request+architecture-question | then:think
TRIGGER: hunt-trigger | event:error+bug+unexpected | then:hunt
TRIGGER: check-trigger | event:implementation-done+pre-merge | then:check
TRIGGER: design-trigger | event:ui-task+component-task | then:design
TRIGGER: health-trigger | event:agent-drift+rule-ignored+mcp-broken | then:health
TRIGGER: write-trigger | event:prose-requested+doc-requested | then:write
TRIGGER: learn-trigger | event:unfamiliar-domain | then:learn
TRIGGER: read-trigger | event:url-provided+document-provided | then:read

# ══════════════════════════════════════════════════════════
# PATTERNS — real failure entries from Waza's gotcha tables
# ══════════════════════════════════════════════════════════

PATTERN: think | broke:architecture | cause:skipped-think-went-straight-to-code | fix:stop-delete-replan | reuse:y
PATTERN: hunt | broke:debugging | cause:fixed-symptom-not-root | fix:trace-up-stack-to-actual-origin | reuse:y
PATTERN: hunt | broke:test | cause:reproduced-in-wrong-env | fix:reproduce-in-prod-config | reuse:y
PATTERN: check | broke:edge-case | cause:not-checked-before-merge | fix:write-edge-case-test | reuse:y
PATTERN: design | broke:mobile | cause:desktop-first | fix:start-mobile-then-scale-up | reuse:y
PATTERN: health | broke:instructions | cause:context-window-overflow | fix:restart-with-smalltalk-wake-up | reuse:y
PATTERN: write | broke:tone | cause:ai-formatting-leaked-through | fix:rewrite-from-first-person | reuse:y
PATTERN: learn | broke:integration | cause:used-api-without-reading-docs | fix:read-official-docs-then-retry | reuse:y
PATTERN: read | broke:context | cause:skimmed-then-responded | fix:read-fully-then-extract | reuse:y

# ══════════════════════════════════════════════════════════
# HARD RULES — enforced across all habits
# ══════════════════════════════════════════════════════════

RULE: no-code-before-think | always-plan-before-implementing | hard
RULE: no-fix-before-hunt | always-find-root-cause-first | hard
RULE: no-ship-before-check | always-review-before-merge | hard
RULE: no-ai-write | write-like-a-human-first-person | hard

# ══════════════════════════════════════════════════════════
# WINS — proven habits worth repeating (from Waza's sessions)
# ══════════════════════════════════════════════════════════

WIN: think | plan-before-code | fewer-rewrites | repeat:y
WIN: hunt | reproduce-first | root-cause-accuracy | repeat:y
WIN: check | edge-case-before-merge | zero-regressions | repeat:y
WIN: design | mobile-first | no-responsive-rework | repeat:y
WIN: health | restart-with-wake-up | restores-orientation | repeat:y
