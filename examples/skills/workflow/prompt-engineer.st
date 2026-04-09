SKILL:   prompt-engineer | prompting+chain-of-thought+few-shot+eval | llm | v1.0.0
USE:     prompt-engineer | when:llm-integration+prompt-design+ai-feature
STACK:   prompt-engineer | patterns | zero-shot+few-shot+chain-of-thought | per-task
STACK:   prompt-engineer | structure | system+user+assistant | roles
STACK:   prompt-engineer | eval | automated+human | measure-output-quality
RULE:    prompt-engineer | specific-over-vague | hard
RULE:    prompt-engineer | chain-of-thought-for-reasoning | hard
RULE:    prompt-engineer | few-shot-for-format | hard
RULE:    prompt-engineer | test-prompt-before-production | hard
RULE:    prompt-engineer | version-prompts-like-code | hard
RULE:    prompt-engineer | system-prompt-for-persona-and-constraints | hard
STEP:    prompt-engineer | design | 1 | define-task-and-expected-output | required
STEP:    prompt-engineer | design | 2 | write-system-prompt | required
STEP:    prompt-engineer | design | 3 | add-few-shot-examples | optional
STEP:    prompt-engineer | validate | 4 | test-edge-cases | required
CHECK:   prompt-engineer | output-format-consistent | required
CHECK:   prompt-engineer | edge-cases-handled | required
AVOID:   prompt-engineer | vague-instructions+no-examples+untested+unversioned+no-eval
