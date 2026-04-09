AGENT:   release-manager-agent | release-orchestrator | changelog+version+tag+deploy | scope:release
TRIGGER: release-manager-agent | release-ready | manual+pr-merge | then:release
TASK:    release-manager-agent | collect-changes | git-log+prs | priority:high
TASK:    release-manager-agent | bump-version | semver | priority:high
TASK:    release-manager-agent | write-changelog | changes | priority:high
TASK:    release-manager-agent | create-git-tag | repo | priority:high
TASK:    release-manager-agent | build-release-artifact | ci | priority:high
TASK:    release-manager-agent | deploy-to-production | cd | priority:high
TASK:    release-manager-agent | publish-release-notes | github-releases | priority:mid
RULE:    release-manager-agent | semver-always | hard
RULE:    release-manager-agent | deploy-only-tagged | hard
OUTPUT:  release-manager-agent | changelog | CHANGELOG.md | markdown
OUTPUT:  release-manager-agent | tag | repo | semver-tag
OUTPUT:  release-manager-agent | release | github | release-notes
ERROR:   release-manager-agent | tests-fail | ci | state:unresolved
