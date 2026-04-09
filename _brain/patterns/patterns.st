# Smalltalk _brain — compressed patterns
# Generated from: _brain/patterns/powershell-claude-cli.md
# Format: Smalltalk .st grammar

PATTERN: powershell-claude-mcp | broke:mcp-add-command | cause:powershell-parses-dashes-as-params | fix:wrap-command-in-quotes | reuse:y
NOTE:    powershell-claude-mcp | incorrect: claude mcp add smalltalk -- python -m smalltalk.mcp_server
NOTE:    powershell-claude-mcp | correct: claude mcp add smalltalk -- "python -m smalltalk.mcp_server"

# 2026-04-09 — Audit + closing ritual session
DECISION: smalltalk-pag-framing | pag>rag | orientation-not-retrieval | 2026-04
PATTERN:  pag-loop-open | broke:brain-not-growing | cause:no-write-back-trigger | fix:closing-ritual-instruction+session-end-agent | reuse:y
WIN:      smalltalk-closing-ritual | session-end-write-back-protocol | brain-compounds-per-session | repeat:y
WIN:      repo-self-compression | compressed-own-brain-patterns | eats-own-cooking | repeat:y
NOTE:     smalltalk-audit | claude_chat2-claims-all-verified | read-side-solid-write-side-was-gap-now-closed

# 2026-04-09 — PAG positioning + automation session
DECISION: readme-framing | pag-first>cognitive-layer | rag-comparison-as-hook | 2026-04
WIN:      pag-tagline | rag-finds-answer-pag-already-knows | strong-positioning | repeat:y
DECISION: auto-mine | watch-mode+git-hook>manual-mine | removes-friction | 2026-04
DECISION: bootstrap-cmd | one-command-setup>multi-step-manual | onboarding-speed | 2026-04
PATTERN:  git-onedrive-hang | broke:git-status-remote | cause:onedrive-file-locks | fix:run-in-own-terminal | reuse:y
PATTERN:  git-wrong-dir | broke:push-rejected | cause:ran-from-parent-not-repo-root | fix:cd-to-smalltalk-subfolder | reuse:y
WIN:      routing-no-deps | stdlib-polling-watch+python-hook | zero-new-dependencies | repeat:y
WIN:      getting-started-doc | separated-from-setup-md | zero-to-oriented-in-10min | repeat:y
DECISION: global-claude-hook | examples-hooks-CLAUDE.md>per-project | auto-orientation-all-projects | 2026-04
NOTE:     mcp-tools | grew-18-to-20 | smalltalk-route+smalltalk-bootstrap-info
NOTE:     repo-structure | git-was-at-parent-level | actual-code-in-smalltalk-subfolder | watch-for-future-sessions
