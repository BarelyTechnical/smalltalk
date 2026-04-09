SKILL:   security-reviewer | owasp+injection+auth+secrets | security | v1.0.0
USE:     security-reviewer | when:security-audit+auth-review+before-deploy
STACK:   security-reviewer | analysis | owasp-top-10 | standard-risk-set
STACK:   security-reviewer | scanning | bandit+semgrep | sast
STACK:   security-reviewer | secrets | gitleaks+trufflehog | secret-detection
PHASE:   security-reviewer | 1 | inputs | validate-all-inputs-at-boundary
PHASE:   security-reviewer | 2 | auth | check-authn+authz+session
PHASE:   security-reviewer | 3 | secrets | scan-for-hardcoded-secrets
PHASE:   security-reviewer | 4 | deps | check-dependency-vulns
RULE:    security-reviewer | never-trust-user-input | hard
RULE:    security-reviewer | parameterized-queries-always | hard
RULE:    security-reviewer | secrets-in-env-only | hard
RULE:    security-reviewer | least-privilege-principle | hard
CHECK:   security-reviewer | sql-injection-impossible | required
CHECK:   security-reviewer | auth-on-all-protected-routes | required
CHECK:   security-reviewer | no-secrets-in-git | required
AVOID:   security-reviewer | eval+raw-sql+client-side-auth+hardcoded-keys+md5-passwords
