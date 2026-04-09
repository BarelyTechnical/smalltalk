SKILL:   cloud-architect | aws+gcp+azure+design | cloud+iac | v1.0.0
USE:     cloud-architect | when:cloud-architecture+scaling+cost+security
STACK:   cloud-architect | compute | ec2+lambda+cloud-run | matched-to-use-case
STACK:   cloud-architect | storage | s3+gcs | object+versioned
STACK:   cloud-architect | database | rds+cloud-sql+dynamodb | managed
STACK:   cloud-architect | network | vpc+subnets+sg | isolation
RULE:    cloud-architect | least-privilege-iam | hard
RULE:    cloud-architect | private-subnets-for-compute | hard
RULE:    cloud-architect | managed-services-over-self-hosted | soft
RULE:    cloud-architect | multi-az-for-production | hard
RULE:    cloud-architect | cost-estimate-before-provisioning | soft
STEP:    cloud-architect | design | 1 | network-topology-first | required
STEP:    cloud-architect | design | 2 | iam-roles-and-policies | required
STEP:    cloud-architect | design | 3 | compute-and-storage | required
STEP:    cloud-architect | design | 4 | monitoring-and-alerting | required
CHECK:   cloud-architect | no-public-database | required
CHECK:   cloud-architect | encryption-at-rest-and-transit | required
AVOID:   cloud-architect | public-rds+root-access+single-az+hardcoded-creds+no-logging
