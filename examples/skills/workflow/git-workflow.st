SKILL:   git-workflow | branching+commits+pr+merge | git+github | v1.0.0
USE:     git-workflow | when:version-control+collaboration+code-review
STACK:   git-workflow | branching | trunk-based+feature-branches | short-lived
STACK:   git-workflow | commits | conventional-commits | feat+fix+chore+docs
STACK:   git-workflow | review | pull-requests | reviewed-before-merge
RULE:    git-workflow | atomic-commits | hard
RULE:    git-workflow | descriptive-commit-messages | hard
RULE:    git-workflow | branch-short-lived-max-2-days | soft
RULE:    git-workflow | squash-merge-to-main | soft
RULE:    git-workflow | no-force-push-main | hard
RULE:    git-workflow | conventional-commit-format | hard
STEP:    git-workflow | branch | 1 | branch-from-main | required
STEP:    git-workflow | commit | 2 | atomic-commits-per-change | required
STEP:    git-workflow | pr | 3 | small-pr-reviewable-in-30min | required
STEP:    git-workflow | merge | 4 | squash-and-delete-branch | required
CHECK:   git-workflow | tests-pass-before-merge | required
CHECK:   git-workflow | no-secrets-in-history | required
AVOID:   git-workflow | large-prs+force-push-shared+vague-messages+long-lived-branches
