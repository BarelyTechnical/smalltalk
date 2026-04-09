AGENT:   data-pipeline-agent | etl-runner | extract+transform+load+validate | scope:pipeline
TRIGGER: data-pipeline-agent | scheduled+manual | cron+event | then:run
TASK:    data-pipeline-agent | extract-from-source | database+api+file | priority:high
TASK:    data-pipeline-agent | validate-raw-data | schema | priority:high
TASK:    data-pipeline-agent | transform-data | rules | priority:high
TASK:    data-pipeline-agent | validate-transformed | quality-checks | priority:high
TASK:    data-pipeline-agent | load-to-destination | database+warehouse | priority:high
TASK:    data-pipeline-agent | send-run-report | notify | priority:mid
RULE:    data-pipeline-agent | validate-before-load | hard
RULE:    data-pipeline-agent | idempotent-run | hard
RULE:    data-pipeline-agent | log-every-stage | hard
OUTPUT:  data-pipeline-agent | data | destination | loaded
OUTPUT:  data-pipeline-agent | report | monitoring | run-summary
ERROR:   data-pipeline-agent | validation-failure | bad-data | state:unresolved
