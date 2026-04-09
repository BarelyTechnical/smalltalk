SKILL:   microservices-architect | services+communication+saga+observability | docker+k8s | v1.0.0
USE:     microservices-architect | when:distributed-system+scaling+team-autonomy
STACK:   microservices-architect | communication | rest+grpc+events | sync+async
STACK:   microservices-architect | messaging | kafka+rabbitmq | async-decoupled
STACK:   microservices-architect | observability | opentelemetry | traces+metrics+logs
STACK:   microservices-architect | data | per-service-db | bounded-context
RULE:    microservices-architect | one-database-per-service | hard
RULE:    microservices-architect | api-gateway-for-entry | hard
RULE:    microservices-architect | async-for-cross-service-writes | hard
RULE:    microservices-architect | distributed-tracing-required | hard
RULE:    microservices-architect | design-for-failure | hard
CHECK:   microservices-architect | circuit-breakers-configured | required
CHECK:   microservices-architect | trace-ids-propagated | required
AVOID:   microservices-architect | shared-database+synchronous-chain+no-observability+micro-too-small
