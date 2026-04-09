DECISION: metrics | north-star:weekly-active-users | aligned-to-retention | 2025-01
DECISION: a-b-testing | statsig>launchdarkly | pricing+sdk | 2025-02
DECISION: analytics | posthog>mixpanel | self-host-option+cheaper | 2025-01
PATTERN:  feature-flag | broke:all-users-got-beta | cause:flag-default-true | fix:explicit-default-false | reuse:y
PATTERN:  onboarding-drop | broke:d7-retention | cause:no-aha-moment | fix:guide-to-first-value | reuse:y
WIN:      experiment | tooltip-vs-modal | tooltip-18pct-higher-completion | repeat:y
WIN:      launch | waitlist-with-referral | 3x-organic-growth | repeat:y
WIN:      retention | weekly-digest-email | plus-12pct-d30 | repeat:y
PROMPT:   user-interview | jobs-to-be-done | what-were-you-doing-when | why-worked:reveals-motivation | reuse:y
PROMPT:   feature-spec | outcome-not-output | define-success-metric-first | why-worked:prevents-overbuilding | reuse:y
