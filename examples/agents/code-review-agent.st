AGENT:   code-review-agent | automated-reviewer | analyze+comment+approve | scope:pr
TRIGGER: code-review-agent | pr-opened+pr-updated | github-event | then:review
TASK:    code-review-agent | parse-diff | pr | priority:high
TASK:    code-review-agent | check-logic-correctness | diff | priority:high
TASK:    code-review-agent | check-security | diff | priority:high
TASK:    code-review-agent | check-test-coverage | diff+tests | priority:mid
TASK:    code-review-agent | post-review-comments | github | priority:high
RULE:    code-review-agent | security-always-blocks | hard
RULE:    code-review-agent | suggest-not-demand | hard
OUTPUT:  code-review-agent | review | github-pr | comments+decision
ERROR:   code-review-agent | diff-too-large | >500-lines | state:unresolved
