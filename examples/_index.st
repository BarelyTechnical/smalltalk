# Smalltalk Palace Index
# palace root: examples
# Always load first (~150 tokens). Navigate with smalltalk_navigate().

# Memory Stack
LAYER:  L0 | file:identity.st | load:always
LAYER:  L1 | file:_index.st   | load:always
LAYER:  L2 | trigger:topic    | source:navigate
LAYER:  L3 | trigger:search   | command:smalltalk_search

# Wings
WING:   agents | type:topic | keywords:agents
WING:   memory | type:topic | keywords:memory
WING:   architecture | type:topic | keywords:architecture
WING:   backend | type:topic | keywords:backend
WING:   database | type:topic | keywords:database
WING:   frontend | type:topic | keywords:frontend
WING:   infrastructure | type:topic | keywords:infrastructure
WING:   quality | type:topic | keywords:quality
WING:   workflow | type:topic | keywords:workflow

# Rooms
ROOM:   api-testing-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/api-testing-agent.st
ROOM:   code-review-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/code-review-agent.st
ROOM:   data-pipeline-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/data-pipeline-agent.st
ROOM:   debugging-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/debugging-agent.st
ROOM:   deployment-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/deployment-agent.st
ROOM:   documentation-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/documentation-agent.st
ROOM:   migration-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/migration-agent.st
ROOM:   onboarding-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+TASK+TRIGGER | file:agents/onboarding-agent.st
ROOM:   performance-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/performance-agent.st
ROOM:   pr-review-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/pr-review-agent.st
ROOM:   refactor-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/refactor-agent.st
ROOM:   release-manager-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/release-manager-agent.st
ROOM:   security-audit-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/security-audit-agent.st
ROOM:   seo-audit-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/seo-audit-agent.st
ROOM:   test-generator-agent | wing:agents | hall:AGENT+ERROR+OUTPUT+RULE+TASK+TRIGGER | file:agents/test-generator-agent.st
ROOM:   brain-entries | wing:memory | hall:CLIENT+COMPONENT+DECISION+PATTERN+PROMPT+WIN | file:memory/brain-entries.st
ROOM:   dev-team-brain | wing:memory | hall:DECISION+PATTERN+RULE+WIN | file:memory/dev-team-brain.st
ROOM:   product-team-brain | wing:memory | hall:DECISION+PATTERN+PROMPT+WIN | file:memory/product-team-brain.st
ROOM:   solopreneur-brain | wing:memory | hall:CLIENT+DECISION+PATTERN+WIN | file:memory/solopreneur-brain.st
ROOM:   api-designer | wing:architecture | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/architecture/api-designer.st
ROOM:   architecture-designer | wing:architecture | hall:AVOID+CHECK+PHASE+RULE+SKILL+USE | file:skills/architecture/architecture-designer.st
ROOM:   microservices-architect | wing:architecture | hall:AVOID+CHECK+RULE+SKILL+STACK+USE | file:skills/architecture/microservices-architect.st
ROOM:   rag-architect | wing:architecture | hall:AVOID+CHECK+PHASE+RULE+SKILL+STACK+USE | file:skills/architecture/rag-architect.st
ROOM:   django-expert | wing:backend | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/backend/django-expert.st
ROOM:   fastapi-expert | wing:backend | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/backend/fastapi-expert.st
ROOM:   golang-pro | wing:backend | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/backend/golang-pro.st
ROOM:   nodejs-pro | wing:backend | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/backend/nodejs-pro.st
ROOM:   python-pro | wing:backend | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/backend/python-pro.st
ROOM:   database-optimizer | wing:database | hall:AVOID+CHECK+PHASE+RULE+SKILL+STACK+USE | file:skills/database/database-optimizer.st
ROOM:   postgres-pro | wing:database | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/database/postgres-pro.st
ROOM:   sql-pro | wing:database | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/database/sql-pro.st
ROOM:   nextjs-developer | wing:frontend | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/frontend/nextjs-developer.st
ROOM:   react-expert | wing:frontend | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/frontend/react-expert.st
ROOM:   tailwind-expert | wing:frontend | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/frontend/tailwind-expert.st
ROOM:   typescript-pro | wing:frontend | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/frontend/typescript-pro.st
ROOM:   vue-expert | wing:frontend | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/frontend/vue-expert.st
ROOM:   cloud-architect | wing:infrastructure | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/infrastructure/cloud-architect.st
ROOM:   devops-engineer | wing:infrastructure | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/infrastructure/devops-engineer.st
ROOM:   kubernetes-specialist | wing:infrastructure | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/infrastructure/kubernetes-specialist.st
ROOM:   terraform-engineer | wing:infrastructure | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/infrastructure/terraform-engineer.st
ROOM:   code-reviewer | wing:quality | hall:AVOID+CHECK+PHASE+RULE+SKILL+USE | file:skills/quality/code-reviewer.st
ROOM:   debugging-wizard | wing:quality | hall:AVOID+CHECK+PHASE+RULE+SKILL+USE | file:skills/quality/debugging-wizard.st
ROOM:   security-reviewer | wing:quality | hall:AVOID+CHECK+PHASE+RULE+SKILL+STACK+USE | file:skills/quality/security-reviewer.st
ROOM:   test-master | wing:quality | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/quality/test-master.st
ROOM:   code-review | wing:workflow | hall:AVOID+CHECK+PHASE+RULE+SKILL+USE | file:skills/workflow/code-review.st
ROOM:   deployment | wing:workflow | hall:AVOID+CHECK+PHASE+RULE+SKILL+USE | file:skills/workflow/deployment.st
ROOM:   git-workflow | wing:workflow | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/workflow/git-workflow.st
ROOM:   prompt-engineer | wing:workflow | hall:AVOID+CHECK+RULE+SKILL+STACK+STEP+USE | file:skills/workflow/prompt-engineer.st
ROOM:   systematic-debugging | wing:workflow | hall:AVOID+CHECK+PHASE+RULE+SKILL+USE | file:skills/workflow/systematic-debugging.st
