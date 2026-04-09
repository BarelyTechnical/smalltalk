# Waza Engineering Habits — Smalltalk Edition
#
# Waza's 8 habits encoded as model-agnostic SKILL + USE + RULE entries.
# Originally Claude Code slash commands. Here: portable .st entries any
# local or cloud model reads at session start.
#
# Source: github.com/tw93/Waza (MIT)
# Philosophy: github.com/ApexAutomate/smalltalk/docs/local-model-philosophy.md
#
# Load this file at session start alongside your project _brain/:
#   smalltalk wake-up .   (if placed in your _brain/)
#   or: read this file directly via smalltalk_read_file()
#
# ─────────────────────────────────────────────────────────────────────────────
# ENGINEERING HABITS
# ─────────────────────────────────────────────────────────────────────────────

# THINK — validate direction before writing any code
SKILL: think | when:new-feature+architecture+refactor+design-decision | phase:pre-code | do:plan-not-implement
USE:   think | when:user-describes-feature-or-new-task-before-writing-code
USE:   think | when:task-touches-more-than-3-components-or-8-files
USE:   think | when:adding-new-service-runtime-or-external-dependency

# Core rules from think
RULE: think | confirm-working-path-before-first-filesystem-op | hard
RULE: think | list-all-api-keys-and-deps-upfront-no-mid-task-requests | hard
RULE: think | offer-2-to-3-options-with-tradeoffs-always-include-minimal-option | hard
RULE: think | no-placeholders-in-approved-plans-every-step-concrete | hard
RULE: think | get-approval-before-proceeding-do-not-restart-from-scratch-if-rejected | hard
RULE: think | verify-mcp-servers-and-external-apis-reachable-before-designing-around-them | hard
RULE: think | more-than-3-components-exchanging-data-draw-ascii-diagram-check-for-cycles | soft
RULE: think | do-not-implement-inside-think-stop-after-approved-plan | hard

# Known failures (PATTERN entries from real gotchas in the Waza think skill)
PATTERN: wrong-path      | broke:filesystem | cause:assumed-homedir-was-project-root | fix:run-pwd-before-first-op | reuse:y
PATTERN: mid-task-creds  | broke:flow | cause:asking-for-api-key-after-3-impl-steps | fix:list-all-deps-before-starting | reuse:y
PATTERN: scratch-restart | broke:efficiency | cause:restarting-from-scratch-on-rejection | fix:ask-what-specifically-failed-re-enter-with-constraints | reuse:y
PATTERN: wrong-regional-api | broke:integration | cause:built-against-wrong-regional-vendor | fix:list-all-regional-differences-before-integration | reuse:y

# ─────────────────────────────────────────────────────────────────────────────

# HUNT — diagnose root cause before touching any code
SKILL: hunt | when:debugging+error+crash+unexpected-behavior+failing-test | phase:diagnosis | do:root-cause-first
USE:   hunt | when:bug-reported+error-appears+test-failing+behavior-unexpected
USE:   hunt | when:same-error-appears-after-a-fix

# Core rules from hunt
RULE: hunt | do-not-touch-code-until-root-cause-stated-in-one-sentence | hard
RULE: hunt | root-cause-must-name-specific-file-function-line-or-condition | hard
RULE: hunt | same-symptom-after-fix-is-hard-stop-re-read-execution-path-from-scratch | hard
RULE: hunt | after-three-failed-hypotheses-stop-and-surface-to-user | hard
RULE: hunt | never-state-env-details-from-memory-run-detection-first | hard
RULE: hunt | verify-function-exists-via-grep-before-writing-a-call-to-it | hard
RULE: hunt | fix-the-cause-not-the-symptom-if-fix-touches-more-than-5-files-pause | hard
RULE: hunt | never-restart-more-than-twice-without-new-evidence | hard

# Known failures from hunt
PATTERN: hypothesis-skipped  | broke:debugging | cause:trying-one-thing-without-a-hypothesis | fix:write-hypothesis-first-then-instrument | reuse:y
PATTERN: symptom-patch        | broke:stability | cause:patching-symptom-not-cause | fix:trace-execution-path-backward-before-touching-code | reuse:y
PATTERN: nonexistent-function | broke:compile | cause:calling-function-that-does-not-exist | fix:grep-codebase-before-writing-any-call | reuse:y
PATTERN: restart-loop         | broke:time | cause:restarting-8-times-without-reading-error | fix:read-last-error-verbatim-before-restarting | reuse:y
PATTERN: multi-stage-bug      | broke:pipeline | cause:diagnosed-orchestrator-not-downstream-stage | fix:test-each-stage-in-isolation | reuse:y

# ─────────────────────────────────────────────────────────────────────────────

# CHECK — review before merging or shipping
SKILL: check | when:pre-merge+pre-deploy+post-implementation | phase:verification | do:diff-review
USE:   check | when:implementation-task-complete
USE:   check | when:before-committing-non-trivial-diff
USE:   check | when:diff-touches-auth+payments+data-mutation

# Core rules from check
RULE: check | get-full-diff-first-classify-depth-before-reviewing | hard
RULE: check | quick-under-100-lines-standard-100-to-500-deep-500-plus-or-auth-payment-data | hard
RULE: check | check-scope-drift-before-reading-code | hard
RULE: check | hard-stops-must-be-fixed-before-merging | hard
RULE: check | do-not-claim-done-until-verification-command-runs-and-passes | hard
RULE: check | if-thinking-should-work-now-run-tests-first | hard
RULE: check | bug-fixes-require-regression-test-before-done | hard
RULE: check | confirm-github-issue-pr-number-via-gh-cli-never-from-memory | hard
RULE: check | pr-comments-1-to-2-sentences-natural-not-a-report | soft

# Known failures from check
PATTERN: no-artifacts-on-release | broke:release | cause:declared-done-before-uploading-artifacts | fix:verify-every-artifact-exists-and-uploaded | reuse:y
PATTERN: trivial-fix-broke-things | broke:stability | cause:skipped-tests-on-one-liner | fix:run-tests-regardless-of-fix-size | reuse:y
PATTERN: wrong-issue-number | broke:comms | cause:commented-on-wrong-issue-from-memory | fix:run-gh-issue-view-N-before-acting | reuse:y
PATTERN: deploy-missing-env | broke:deploy | cause:deployed-without-checking-env-vars | fix:run-env-check-before-deploying | reuse:y

# ─────────────────────────────────────────────────────────────────────────────

# DESIGN — build UI with a committed point of view
SKILL: design | when:ui+ux+visual+component+page+interface | phase:pre-implementation | do:aesthetic-direction-first
USE:   design | when:building-any-ui-component-page-or-visual-interface
USE:   design | when:user-requests-frontend+visual+layout+animation

# Core rules from design
RULE: design | lock-direction-before-writing-code-audience-aesthetic-anchor-constraints | hard
RULE: design | no-inter-roboto-system-ui-as-primary-display-typeface | hard
RULE: design | one-color-owns-page-one-or-two-accents | hard
RULE: design | default-to-cardless-sections-remove-borders-if-understanding-not-hurt | soft
RULE: design | no-flat-white-or-flat-black-backgrounds-by-default | soft
RULE: design | honor-prefers-reduced-motion-visible-focus-states-alt-text | hard
RULE: design | visual-thesis-content-plan-interaction-thesis-before-first-component | hard
RULE: design | open-result-in-browser-and-check-at-375px-before-handoff | hard

# Known failures from design
PATTERN: invisible-font    | broke:identity | cause:used-inter-as-display-font | fix:pick-typeface-with-personality | reuse:y
PATTERN: template-feel     | broke:design | cause:identical-cards-with-identical-padding | fix:if-swapping-content-needs-no-layout-change-redo-it | reuse:y
PATTERN: unchecked-browser | broke:qa | cause:claimed-correct-without-opening-browser | fix:always-open-browser-verify-at-full-width-and-375px | reuse:y
PATTERN: same-look-every-project | broke:variety | cause:defaulting-to-same-pattern | fix:vary-light-dark-serif-sans-dense-spacious | reuse:y

# ─────────────────────────────────────────────────────────────────────────────

# HEALTH — audit Claude Code config stack when agent misbehaves
SKILL: health | when:agent-ignoring-instructions+inconsistent-behavior+hooks-misfiring+mcp-audit | phase:maintenance | do:six-layer-audit
USE:   health | when:claude-ignores-instructions-or-behaves-inconsistently
USE:   health | when:hooks-malfunction-or-mcp-servers-need-auditing
USE:   health | when:toolchain+claude-md+mcp-config needs review

# Core rules from health
RULE: health | audit-six-layers-in-order-claudemd-rules-skills-hooks-subagents-verifiers | hard
RULE: health | never-auto-apply-fixes-without-confirmation | hard
RULE: health | classify-tier-simple-standard-complex-apply-only-that-tiers-requirements | hard
RULE: health | mcp-live-check-call-each-server-before-analysis | hard

# ─────────────────────────────────────────────────────────────────────────────

# WRITE — strip AI writing patterns from prose
SKILL: write | when:explicit-prose-writing+editing+polishing | phase:content | do:ai-pattern-removal
USE:   write | when:user-explicitly-asks-to-write-edit-or-polish-prose
USE:   write | when:output-sounds-ai-generated-and-needs-humanising

# Core rules from write
RULE: write | detect-text-language-before-applying-rules | hard
RULE: write | preserve-every-sentence-unless-told-to-cut | hard
RULE: write | no-silent-restructuring | hard
RULE: write | match-naming-conventions-of-existing-files-before-creating-new | hard

# ─────────────────────────────────────────────────────────────────────────────

# LEARN — research to published output, six phases
SKILL: learn | when:deep-research+unfamiliar-domain+article-prep | phase:research | do:six-phase-workflow
USE:   learn | when:diving-deep-into-unfamiliar-domain-or-preparing-research-article
USE:   learn | when:turning-collected-sources-into-publishable-output

# Core rules from learn
RULE: learn | choose-mode-deep-research-quick-reference-write-to-learn | hard
RULE: learn | primary-sources-only-not-summaries-not-explainers | hard
RULE: learn | if-section-has-no-sources-it-does-not-belong | hard
RULE: learn | when-two-sources-contradict-note-both-and-evidence-do-not-pick-silently | hard
RULE: learn | do-not-start-writing-phase-until-outline-is-solid | hard

# ─────────────────────────────────────────────────────────────────────────────

# READ — fetch URL or PDF as clean Markdown
SKILL: read | when:url+pdf+web-page-to-read | phase:research | do:fetch-as-markdown
USE:   read | when:given-any-url-web-link-or-pdf-to-read
USE:   read | when:user-shares-link-for-context

# Core rules from read
RULE: read | after-saving-stop-do-not-analyze-unless-asked | hard
RULE: read | if-content-truncated-say-so-and-offer-to-continue | soft

# ─────────────────────────────────────────────────────────────────────────────
# CROSS-HABIT ANTI-PATTERNS
# These failures apply across all habits — pulled from real sessions.
# ─────────────────────────────────────────────────────────────────────────────

AVOID: random-walk-debugging | trying-things-without-a-written-hypothesis
AVOID: credential-requests-mid-task | list-all-deps-before-starting
AVOID: claiming-done-without-verification | run-tests-before-declaring-done
AVOID: restarting-from-scratch-on-rejection | ask-what-specifically-failed
AVOID: skipping-browser-check-for-ui | always-open-browser-verify-at-375px
AVOID: silent-source-silently-reconciling-contradictions | note-both-positions
AVOID: default-typography | inter-roboto-system-ui-communicate-nothing
