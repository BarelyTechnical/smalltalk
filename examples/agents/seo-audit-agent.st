AGENT:   seo-audit-agent | seo-scorer | crawl+analyze+recommend | scope:website
TRIGGER: seo-audit-agent | pre-launch+monthly | manual+schedule | then:audit
TASK:    seo-audit-agent | crawl-pages | website | priority:high
TASK:    seo-audit-agent | check-title-and-meta | pages | priority:high
TASK:    seo-audit-agent | check-heading-structure | pages | priority:high
TASK:    seo-audit-agent | check-page-speed | core-web-vitals | priority:high
TASK:    seo-audit-agent | check-structured-data | schema | priority:mid
TASK:    seo-audit-agent | write-recommendations | report | priority:high
RULE:    seo-audit-agent | one-h1-per-page | hard
RULE:    seo-audit-agent | unique-title-per-page | hard
OUTPUT:  seo-audit-agent | report | seo-audit.md | markdown
OUTPUT:  seo-audit-agent | score | dashboard | numeric
ERROR:   seo-audit-agent | site-unreachable | network | state:unresolved
