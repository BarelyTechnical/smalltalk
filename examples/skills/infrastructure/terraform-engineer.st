SKILL:   terraform-engineer | iac+terraform+modules+state | terraform+aws+gcp | v1.0.0
USE:     terraform-engineer | when:infrastructure-as-code+cloud-provisioning
STACK:   terraform-engineer | iac | terraform | hcl+providers+state
STACK:   terraform-engineer | state | s3+dynamodb | remote+lock
STACK:   terraform-engineer | modules | local+registry | reusable-infra
RULE:    terraform-engineer | remote-state-always | hard
RULE:    terraform-engineer | plan-before-apply | hard
RULE:    terraform-engineer | modules-for-reusable-patterns | hard
RULE:    terraform-engineer | no-hardcoded-values-use-variables | hard
RULE:    terraform-engineer | tag-all-resources | soft
STEP:    terraform-engineer | init | 1 | configure-remote-backend | required
STEP:    terraform-engineer | plan | 2 | terraform-plan-review-output | required
STEP:    terraform-engineer | apply | 3 | terraform-apply-with-approval | required
STEP:    terraform-engineer | verify | 4 | confirm-state-and-resources | required
CHECK:   terraform-engineer | plan-output-reviewed-before-apply | required
CHECK:   terraform-engineer | state-backed-and-locked | required
AVOID:   terraform-engineer | local-state+hardcoded-creds+apply-without-plan+no-modules
