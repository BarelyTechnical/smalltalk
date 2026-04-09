import httpx
from pathlib import Path

GRAMMAR_SUMMARY = """
Smalltalk is a typed, pipe-delimited, one-line-per-entry grammar for AI agent files.

SYNTAX: TYPE: identifier | field | field | field

SEPARATORS:
  |   field boundary
  +   multiple values in one field  (next+vite+remix)
  :   key-value within a field      (broke:vite-build)
  >   choice over alternative       (cloudflare>vercel)

VALUES: lowercase-hyphenated, no spaces inside field values

TYPES:

Universal:
  RULE:     id | rule-description | hard|soft
  REF:      id | path/to/file.st  | covers:topic
  NOTE:     id | observation
  CONFIG:   id | key | value
  CONTEXT:  id | scope | value
  DECISION: id | choice>rejected | reason | date
  PATTERN:  id | broke:what | cause:why | fix:what | reuse:y/n

Memory:
  WIN:       id | technique | outcome | repeat:y/n
  CLIENT:    id | pref:what | avoid:what | updated:date
  COMPONENT: id | stack | does:what | use-when
  PROMPT:    id | task-type | approach | why-worked | reuse:y/n

Skills:
  SKILL:   id | triggers | stack | version
  USE:     id | when:context
  PHASE:   id | number | name | what-happens
  STEP:    id | phase | number | action | required|optional
  STACK:   id | layer | tool | why
  CHECK:   id | verification-item | required|optional
  AVOID:   id | antipatterns+separated
  SCRIPT:  id | path/to/script | what-it-does
  STYLE:   id | style-name | description
  FONT:    id | preference | weights | style | usage
  COLOR:   id | system | key:value | key:value

Agents:
  AGENT:   id | role | capabilities | scope
  TASK:    id | action | target | priority:high|mid|low
  TRIGGER: id | event | condition | then:action
  OUTPUT:  id | type | destination | format
  ERROR:   id | broke:what | cause:why | state:recovered|unresolved
"""

CONVERSION_PROMPT = """You are converting a markdown agent file to Smalltalk .st compressed format.

{grammar}

FILE TYPE DETECTED: {file_type}

RULES:
- Output Smalltalk .st entries ONLY — no markdown, no prose, no explanation, no code fences
- One line per entry
- Extract every rule, step, reference, and fact — drop scaffolding prose only
- Sub-file references (mentions of other .md files) become REF: entries pointing to .st versions
- Values must be lowercase-hyphenated, no spaces inside field values
- Keep entries as short as possible while remaining unambiguous

FILE TO CONVERT:
{content}
"""

FILE_TYPE_HINTS = {
    "skill": ["when to use", "use when", "quick start", "best practices", "core stack", "## reference"],
    "memory": ["date:", "project:", "problem:", "cause:", "fix:", "what worked", "preferences", "rejections"],
    "agent": ["pipeline", "trigger", "task:", "output:", "agent", "workflow", "poll", "deploy"],
    "config": ["config", "environment", "settings", "key:", "value:"],
    "design": ["philosophy", "visual", "composition", "color", "typography", "palette", "style"],
}

SKIP_NAMES = {
    "readme.md", "changelog.md", "contributing.md", "license.md",
    "stack.md", "context.md", "gemini.md", "claude.md", "agents.md",
}


def detect_file_type(content: str, filename: str) -> str:
    content_lower = content.lower()
    filename_lower = filename.lower()

    scores = {ft: 0 for ft in FILE_TYPE_HINTS}
    for ft, hints in FILE_TYPE_HINTS.items():
        for hint in hints:
            if hint in content_lower or hint in filename_lower:
                scores[ft] += 1

    if any(x in filename_lower for x in ["skill", "cursorrules", "rules", "routing"]):
        scores["skill"] += 3
    if any(x in filename_lower for x in ["agent", "pipeline", "bot", "worker"]):
        scores["agent"] += 3
    if any(x in filename_lower for x in ["design", "canvas", "brand", "style", "theme"]):
        scores["design"] += 3
    if any(x in filename_lower for x in ["decision", "pattern", "win", "client", "brain"]):
        scores["memory"] += 3

    return max(scores, key=scores.get)


def convert_file(path: Path, api_key: str, model: str, base_url: str) -> str:
    content = path.read_text(encoding="utf-8")
    file_type = detect_file_type(content, path.name)

    prompt = CONVERSION_PROMPT.format(
        grammar=GRAMMAR_SUMMARY,
        file_type=file_type,
        content=content,
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": model,
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = httpx.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers=headers,
        json=payload,
        timeout=60.0,
    )
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"].strip()


def is_convertible(path: Path) -> bool:
    if path.name.lower() in SKIP_NAMES:
        return False
    content = path.read_text(encoding="utf-8", errors="ignore")
    lines = [l for l in content.splitlines() if l.strip()]
    if len(lines) < 5:
        return False
    return True
