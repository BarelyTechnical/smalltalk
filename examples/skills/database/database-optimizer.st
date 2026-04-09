SKILL:   database-optimizer | indexing+explain+n-plus-one+caching | sql+postgresql | v1.0.0
USE:     database-optimizer | when:slow-queries+high-db-load+optimization
STACK:   database-optimizer | analysis | EXPLAIN ANALYZE | query-plan
STACK:   database-optimizer | indexing | btree+partial+covering | targeted
STACK:   database-optimizer | caching | query-cache+materialized-view | computed
PHASE:   database-optimizer | 1 | measure | run-explain-analyze-first
PHASE:   database-optimizer | 2 | identify | seq-scan+nested-loop+high-rows
PHASE:   database-optimizer | 3 | index | add-targeted-indexes
PHASE:   database-optimizer | 4 | verify | re-run-explain-and-compare
RULE:    database-optimizer | measure-before-optimize | hard
RULE:    database-optimizer | index-for-selectivity-not-guessing | hard
RULE:    database-optimizer | avoid-function-on-indexed-column | hard
RULE:    database-optimizer | batch-writes-over-row-by-row | hard
CHECK:   database-optimizer | n-plus-one-queries-eliminated | required
CHECK:   database-optimizer | slow-query-log-reviewed | required
AVOID:   database-optimizer | premature-indexing+select-star+orm-default-fetch+text-pattern-without-index
