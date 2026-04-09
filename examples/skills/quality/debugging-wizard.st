SKILL:   debugging-wizard | debug+reproduce+trace+fix | any | v1.0.0
USE:     debugging-wizard | when:bug+error+unexpected-behaviour+production-issue
PHASE:   debugging-wizard | 1 | reproduce | create-minimal-reproducible-case
PHASE:   debugging-wizard | 2 | isolate | binary-search-the-failure-point
PHASE:   debugging-wizard | 3 | hypothesize | form-testable-hypothesis
PHASE:   debugging-wizard | 4 | verify | prove-or-disprove-hypothesis
PHASE:   debugging-wizard | 5 | fix | implement-and-verify
PHASE:   debugging-wizard | 6 | prevent | add-test-to-catch-regression
RULE:    debugging-wizard | reproduce-first-guess-never | hard
RULE:    debugging-wizard | change-one-thing-at-a-time | hard
RULE:    debugging-wizard | read-the-actual-error-message | hard
RULE:    debugging-wizard | check-recent-changes-first | soft
RULE:    debugging-wizard | add-regression-test-after-fix | hard
CHECK:   debugging-wizard | original-error-still-reproduced | required
CHECK:   debugging-wizard | fix-does-not-introduce-regression | required
AVOID:   debugging-wizard | guessing+multiple-changes+no-test+ignoring-error-message
