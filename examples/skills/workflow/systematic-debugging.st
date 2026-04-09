SKILL:   systematic-debugging | reproduce+isolate+fix+verify | any | v1.0.0
USE:     systematic-debugging | when:bug+error+unexpected+regression
PHASE:   systematic-debugging | 1 | read | read-full-error-message-and-stack-trace
PHASE:   systematic-debugging | 2 | reproduce | confirm-error-reproducible
PHASE:   systematic-debugging | 3 | isolate | narrow-scope-to-smallest-failing-case
PHASE:   systematic-debugging | 4 | hypothesize | form-one-testable-hypothesis
PHASE:   systematic-debugging | 5 | fix | apply-minimal-change
PHASE:   systematic-debugging | 6 | verify | confirm-fix+no-regression
RULE:    systematic-debugging | never-guess | hard
RULE:    systematic-debugging | one-change-at-a-time | hard
RULE:    systematic-debugging | check-patterns-before-digging | hard
RULE:    systematic-debugging | add-regression-test-after-fix | hard
CHECK:   systematic-debugging | original-error-confirmed | required
CHECK:   systematic-debugging | fix-logged-to-patterns | required
AVOID:   systematic-debugging | multiple-changes+no-reproduction+assuming-cause+no-test-after
