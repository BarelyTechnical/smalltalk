SKILL:   code-reviewer | review+feedback+standards | git | v1.0.0
USE:     code-reviewer | when:pull-request+code-review+quality-check
PHASE:   code-reviewer | 1 | understand | read-pr-description-and-linked-issue
PHASE:   code-reviewer | 2 | logic | verify-correctness-and-edge-cases
PHASE:   code-reviewer | 3 | quality | check-naming+structure+duplication
PHASE:   code-reviewer | 4 | security | check-inputs+auth+secrets+injection
PHASE:   code-reviewer | 5 | feedback | write-constructive-specific-comments
RULE:    code-reviewer | suggest-not-demand | hard
RULE:    code-reviewer | block-on-correctness-not-style | hard
RULE:    code-reviewer | comment-on-why-not-just-what | hard
RULE:    code-reviewer | security-issues-always-block | hard
CHECK:   code-reviewer | no-authn-bypass | required
CHECK:   code-reviewer | no-secrets-in-code | required
CHECK:   code-reviewer | edge-cases-covered | required
CHECK:   code-reviewer | error-paths-handled | required
AVOID:   code-reviewer | nit-picking-style+blocking-on-preference+vague-comments+approve-without-reading
