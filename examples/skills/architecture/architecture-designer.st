SKILL:   architecture-designer | system-design+patterns+trade-offs | any | v1.0.0
USE:     architecture-designer | when:new-system+major-refactor+scaling-problem
PHASE:   architecture-designer | 1 | requirements | gather-functional+non-functional
PHASE:   architecture-designer | 2 | constraints | identify-budget+team+time+scale
PHASE:   architecture-designer | 3 | design | choose-patterns+draw-components
PHASE:   architecture-designer | 4 | trade-offs | evaluate-complexity+cost+risk
PHASE:   architecture-designer | 5 | document | write-adr-per-decision
RULE:    architecture-designer | document-decisions-with-reasoning | hard
RULE:    architecture-designer | start-simple-evolve-later | hard
RULE:    architecture-designer | design-for-the-team-you-have | hard
RULE:    architecture-designer | prefer-boring-tech | soft
RULE:    architecture-designer | failure-modes-must-be-designed | hard
CHECK:   architecture-designer | single-points-of-failure-identified | required
CHECK:   architecture-designer | scaling-path-understood | required
AVOID:   architecture-designer | premature-optimization+over-engineering+distributed-for-small-scale
