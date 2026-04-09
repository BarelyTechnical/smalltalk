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
