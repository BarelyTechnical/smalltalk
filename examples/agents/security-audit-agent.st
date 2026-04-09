AGENT:   security-audit-agent | security-scanner | scan+report+remediate | scope:codebase
TRIGGER: security-audit-agent | pre-deploy+scheduled-weekly | ci+schedule | then:scan
TASK:    security-audit-agent | run-sast-scan | semgrep+bandit | priority:high
TASK:    security-audit-agent | check-dependency-vulns | pip-audit+npm-audit | priority:high
TASK:    security-audit-agent | scan-for-secrets | gitleaks | priority:high
TASK:    security-audit-agent | review-auth-flows | codebase | priority:high
TASK:    security-audit-agent | write-security-report | findings | priority:high
RULE:    security-audit-agent | block-deploy-on-critical | hard
RULE:    security-audit-agent | secrets-always-block | hard
OUTPUT:  security-audit-agent | report | security/ | markdown
OUTPUT:  security-audit-agent | findings | ci | annotations
ERROR:   security-audit-agent | critical-vulnerability | cve | state:unresolved
