AGENT:   documentation-agent | docs-generator | read-code+write-docs | scope:module+repo
TRIGGER: documentation-agent | new-public-api-or-outdated-docs | code-change | then:generate
TASK:    documentation-agent | scan-public-interfaces | codebase | priority:high
TASK:    documentation-agent | generate-docstrings | functions+classes | priority:high
TASK:    documentation-agent | write-readme-sections | repo | priority:mid
TASK:    documentation-agent | generate-api-reference | openapi+tsdoc | priority:mid
TASK:    documentation-agent | check-examples-run | docs | priority:high
RULE:    documentation-agent | examples-must-be-runnable | hard
RULE:    documentation-agent | explain-the-why-not-just-what | hard
OUTPUT:  documentation-agent | docstrings | codebase | inline
OUTPUT:  documentation-agent | readme | repo-root | markdown
OUTPUT:  documentation-agent | api-reference | docs/ | markdown+openapi
ERROR:   documentation-agent | ambiguous-interface | missing-types | state:unresolved
