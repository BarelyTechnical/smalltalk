SKILL:   postgres-pro | postgres+queries+indexing+transactions | postgresql | v1.0.0
USE:     postgres-pro | when:relational-database+complex-queries+transactions
STACK:   postgres-pro | queries | sql+cte | readable+composable
STACK:   postgres-pro | indexing | btree+partial+composite | performance
STACK:   postgres-pro | transactions | acid+isolation-levels | data-safety
STACK:   postgres-pro | json | jsonb | flexible-schema+indexed
RULE:    postgres-pro | always-use-transactions | hard
RULE:    postgres-pro | index-foreign-keys | hard
RULE:    postgres-pro | explain-analyze-before-optimize | hard
RULE:    postgres-pro | prefer-cte-over-subquery | soft
RULE:    postgres-pro | use-prepared-statements | hard
RULE:    postgres-pro | never-select-star-in-production | soft
STEP:    postgres-pro | design | 1 | normalize-to-3nf-first | required
STEP:    postgres-pro | optimize | 2 | explain-analyze-slow-queries | required
STEP:    postgres-pro | optimize | 3 | add-indexes-after-measuring | required
CHECK:   postgres-pro | no-missing-indexes-on-fk | required
CHECK:   postgres-pro | long-transactions-identified | required
AVOID:   postgres-pro | select-star+premature-indexes+text-for-enum-data+missing-fk-constraints
