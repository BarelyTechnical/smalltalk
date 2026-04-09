SKILL:   code-review | review-process+checklist+feedback | git | v1.0.0
USE:     code-review | when:reviewing-pull-requests+quality-gate
PHASE:   code-review | 1 | context | understand-why-this-change-exists
PHASE:   code-review | 2 | correctness | does-it-do-what-it-claims
PHASE:   code-review | 3 | coverage | are-edge-cases-tested
PHASE:   code-review | 4 | security | inputs+auth+secrets
PHASE:   code-review | 5 | design | will-this-age-well
RULE:    code-review | approve-behaviour-not-style | hard
RULE:    code-review | blocking-comment-must-explain-why | hard
RULE:    code-review | nitpick-label-for-non-blocking | soft
RULE:    code-review | at-least-one-full-read-before-feedback | hard
CHECK:   code-review | happy-path-tested | required
CHECK:   code-review | error-paths-tested | required
CHECK:   code-review | no-hardcoded-secrets | required
AVOID:   code-review | drive-by-comment+approving-unread+style-blocking+no-context-read
