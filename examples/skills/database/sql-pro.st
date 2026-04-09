SKILL:   sql-pro | sql+joins+aggregation+window-functions | sql | v1.0.0
USE:     sql-pro | when:data-query+reporting+analytics+any-relational-db
STACK:   sql-pro | read | select+join+where+group-by | base-queries
STACK:   sql-pro | advanced | window-functions+cte | analytics+ranking
STACK:   sql-pro | write | insert+update+delete+upsert | data-modification
RULE:    sql-pro | cte-over-subquery | soft
RULE:    sql-pro | explicit-join-conditions | hard
RULE:    sql-pro | filter-early-with-where | hard
RULE:    sql-pro | window-function-over-self-join | soft
RULE:    sql-pro | no-correlated-subquery-in-select | hard
STEP:    sql-pro | query | 1 | start-with-from-and-joins | required
STEP:    sql-pro | query | 2 | filter-with-where-before-aggregate | required
STEP:    sql-pro | query | 3 | use-having-for-post-aggregate-filter | required
STEP:    sql-pro | review | 4 | read-explain-plan | required
CHECK:   sql-pro | every-join-has-explicit-condition | required
CHECK:   sql-pro | aggregates-not-in-where | required
AVOID:   sql-pro | implicit-joins+correlated-subquery+select-star+function-on-indexed-column
