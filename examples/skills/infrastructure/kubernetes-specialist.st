SKILL:   kubernetes-specialist | k8s+pods+services+deployments | kubernetes | v1.0.0
USE:     kubernetes-specialist | when:container-orchestration+scaling+production-workloads
STACK:   kubernetes-specialist | workloads | deployment+statefulset | managed-pods
STACK:   kubernetes-specialist | networking | service+ingress | routing
STACK:   kubernetes-specialist | config | configmap+secret | separated-config
STACK:   kubernetes-specialist | scaling | hpa+vpa | auto-scale
RULE:    kubernetes-specialist | requests-and-limits-always | hard
RULE:    kubernetes-specialist | liveness-and-readiness-probes | hard
RULE:    kubernetes-specialist | secrets-not-configmaps-for-sensitive | hard
RULE:    kubernetes-specialist | namespace-isolation | hard
RULE:    kubernetes-specialist | rolling-updates-not-recreate | soft
STEP:    kubernetes-specialist | deploy | 1 | write-deployment-manifest | required
STEP:    kubernetes-specialist | deploy | 2 | define-service-and-ingress | required
STEP:    kubernetes-specialist | deploy | 3 | configure-probes-and-limits | required
STEP:    kubernetes-specialist | verify | 4 | kubectl-rollout-status | required
CHECK:   kubernetes-specialist | all-pods-have-resource-limits | required
CHECK:   kubernetes-specialist | probes-configured | required
AVOID:   kubernetes-specialist | no-limits+privileged-containers+hostnetwork+recreate-strategy
