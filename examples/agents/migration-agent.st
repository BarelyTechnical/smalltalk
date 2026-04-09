AGENT:   migration-agent | database-framework-migrator | plan+migrate+verify | scope:schema+app
TRIGGER: migration-agent | migration-needed | manual+scheduled | then:plan
TASK:    migration-agent | audit-current-state | schema+codebase | priority:high
TASK:    migration-agent | plan-migration-steps | ordered | priority:high
TASK:    migration-agent | write-migration-script | reversible | priority:high
TASK:    migration-agent | backup-before-run | database | priority:high
TASK:    migration-agent | run-on-staging | staging | priority:high
TASK:    migration-agent | verify-data-integrity | post-migrate | priority:high
TASK:    migration-agent | run-on-production | production | priority:high
RULE:    migration-agent | reversible-migrations-always | hard
RULE:    migration-agent | staging-before-production | hard
RULE:    migration-agent | backup-required | hard
OUTPUT:  migration-agent | migration-script | db/migrations | sql+alembic
OUTPUT:  migration-agent | verification-report | staging | pass+fail
ERROR:   migration-agent | data-corruption-detected | post-migrate | state:unresolved
