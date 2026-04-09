AGENT:   performance-agent | performance-optimizer | profile+identify+fix+verify | scope:app
TRIGGER: performance-agent | slow-endpoint+high-latency+cpu-spike | monitoring | then:profile
TASK:    performance-agent | identify-slow-path | profiler+apm | priority:high
TASK:    performance-agent | profile-detailed | targeted | priority:high
TASK:    performance-agent | identify-bottleneck | flame-graph | priority:high
TASK:    performance-agent | implement-targeted-fix | code | priority:high
TASK:    performance-agent | measure-improvement | load-test | priority:high
RULE:    performance-agent | measure-first-optimize-second | hard
RULE:    performance-agent | one-change-at-a-time | hard
OUTPUT:  performance-agent | fix | codebase | pr
OUTPUT:  performance-agent | report | perf/ | before-after-metrics
ERROR:   performance-agent | no-profiler-data | environment | state:unresolved
