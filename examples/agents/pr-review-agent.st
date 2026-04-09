AGENT:   pr-review-agent | pull-request-reviewer | read-diff+review+comment | scope:pr
TRIGGER: pr-review-agent | pr-opened-or-updated | github-event | then:review
TASK:    pr-review-agent | read-pr-description | github-pr | priority:high
TASK:    pr-review-agent | review-diff-for-correctness | code-diff | priority:high
TASK:    pr-review-agent | check-security-issues | code-diff | priority:high
TASK:    pr-review-agent | check-test-coverage | diff+tests | priority:mid
TASK:    pr-review-agent | write-review-comments | github-api | priority:high
TASK:    pr-review-agent | request-changes-or-approve | github-api | priority:high
RULE:    pr-review-agent | block-on-security-always | hard
RULE:    pr-review-agent | suggest-not-demand | hard
RULE:    pr-review-agent | specific-line-comments | hard
OUTPUT:  pr-review-agent | review | github-pr | approved+changes-requested
OUTPUT:  pr-review-agent | comments | github-pr | inline-comments
ERROR:   pr-review-agent | pr-too-large | >500-lines | state:unresolved
