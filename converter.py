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

Knowledge Graph:
  LINK:    source | rel:relationship-type | target | [valid_from:YYYY-MM] | [ended:YYYY-MM] | [stability:permanent|stable|transient]

  Use LINK when the file describes a relationship between two named entities:
    person → project:   LINK: kai | rel:works-on | orion | valid_from:2026-01 | stability:transient
    service → service:  LINK: auth | rel:depends | billing | stability:stable
    entity → value:     LINK: brand-color | rel:defined-as | electric-lime | stability:permanent
    person → team:      LINK: morne | rel:member-of | pixel-palace | valid_from:2026-01
    project → platform: LINK: smalltalk | rel:deployed-to | pypi | valid_from:2026-03

  Common rel: values:
    works-on, assigned-to, reports-to      — person↔project (use stability:transient)
    deployed-to, defined-as, blocks        — project↔infra (use stability:stable)
    depends, member-of, contributes-to     — service/team relationships
    related-to, shares-topic, references   — loose non-exclusive connections

  stability rules:
    permanent — core truth, only closed via contradiction (e.g. brand identity facts)
    stable    — valid until explicitly superseded (default for most links)
    transient — time-windowed, changes frequently (default for people↔project assignments)

Engineering Habits (Waza integration):
  HABIT:    id | trigger:when | enforce:hard|soft | description
            id        = habit name (think, hunt, check, design, health, write, learn, read)
            trigger   = event that activates this habit (feature-request, error, ui-task)
            enforce   = hard (always invoke) | soft (invoke when relevant)
  Example:
    HABIT: think | trigger:new-feature+architecture | enforce:hard | plan-before-code
    HABIT: hunt  | trigger:error+bug+unexpected     | enforce:hard | find-root-cause-first

Model Routing:
  MODELMAP: task-type | model | backend | ctx:tokens | tier:beginner|standard|performance|cpu-native
            task-type = category this model handles (chat, code, planning, write, analyse)
            model     = model identifier (llama3.2, qwen2.5-coder, mistral, etc.)
            backend   = inference backend (ollama, llama-cpp, ik-llama, bitnet)
            ctx       = context window this backend supports reliably
  Example:
    MODELMAP: code   | qwen2.5-coder:32b | ollama   | ctx:32000  | tier:performance
    MODELMAP: chat   | llama3.2:3b       | ollama   | ctx:4096   | tier:beginner
    MODELMAP: any    | phi-4-mini        | bitnet   | ctx:128000 | tier:cpu-native

Infrastructure Backends:
  BACKEND:  id | api:url | ctx:tokens | tier:beginner|standard|performance|cpu-native | [notes:text]
            id   = backend identifier (ollama-local, llama-cpp-server, bitnet-local)
            api  = base URL of the OpenAI-compatible API
            ctx  = reliable context window size
            tier = hardware requirement level
  Example:
    BACKEND: ollama-local  | api:http://localhost:11434/v1 | ctx:4096   | tier:beginner  | notes:context-cap-warning
    BACKEND: llama-cpp     | api:http://localhost:8080/v1  | ctx:32000  | tier:standard  | notes:full-ctx-support
    BACKEND: bitnet-local  | api:http://localhost:8081/v1  | ctx:128000 | tier:cpu-native| notes:1bit-no-gpu-needed
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
- When the file names a relationship between two entities (person↔project, service↔platform,
  service↔service), emit a LINK: entry. Use stability:transient for people assignments,
  stability:stable for architectural dependencies, stability:permanent for identity facts.
  Include valid_from:YYYY-MM only when a date is explicitly stated in the source.
- When the file describes an engineering habit (a disciplined workflow or checklist),
  emit a HABIT: entry with trigger: and enforce: fields.
- When the file maps task types to specific models or backends, emit MODELMAP: entries.
- When the file defines infrastructure backends, emit BACKEND: entries with api:, ctx:, tier:.

FILE TO CONVERT:
{content}
"""

# ── Causal intake prompt (--causal flag) ─────────────────────────────────────
CAUSAL_PROMPT = """You are an intelligence intake agent. Your task is to extract structured,
causality-aware Smalltalk .st entries from raw content (article, thread, guide, post).

Unlike standard conversion, you MUST capture:
  1. The WHY behind every rule — not just the rule itself
  2. The EVIDENCE — how many sources, what context (e.g. evidence:47-sites-tested)
  3. The CONTRADICTION — if this conflicts with an existing brain entry, flag it
  4. The CONFIDENCE — evidence:cited (primary source) | evidence:anecdotal | evidence:inferred

{grammar}

OUTPUT FORMAT rules:
- One .st entry per line, no prose, no markdown
- Append `| evidence:TYPE` to RULE, DECISION, and PATTERN entries
- Append `| source:short-description` when a clear source is present
- If content contradicts a fact you can infer the reader may already hold, prepend: # CONFLICT:
- Use `reuse:y` on PATTERN entries that describe general failure modes worth encoding

Examples of causal entries:
  RULE: seo | depth-before-breadth | hard | evidence:cited | source:ahrefs-cluster-study
  PATTERN: llm-context | broke:alignment | cause:no-structured-summary | fix:pag-wake-up | reuse:y | evidence:anecdotal
  DECISION: deploy | railway>vercel | cost+scale | evidence:inferred | source:twitter-thread
  # CONFLICT: RULE: seo | volume-first (check brain — this contradicts cluster-first approach)

CONTENT TO ANALYSE:
{content}
"""


FILE_TYPE_HINTS = {
    "skill": ["when to use", "use when", "quick start", "best practices", "core stack", "## reference"],
    "memory": ["date:", "project:", "problem:", "cause:", "fix:", "what worked", "preferences",
               "rejections", "works on", "works with", "assigned to", "member of", "depends on",
               "relationship"],
    "agent": ["pipeline", "trigger", "task:", "output:", "agent", "workflow", "poll", "deploy",
              "integrates with", "connects to", "depends on", "reports to"],
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
    if any(x in filename_lower for x in ["decision", "pattern", "win", "client", "brain",
                                          "habit", "waza", "backend", "modelmap"]):
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


def convert_file_causal(path: Path, api_key: str, model: str, base_url: str) -> str:
    """Causal intake mode — extracts evidence chains and causality, not just structure."""
    content = path.read_text(encoding="utf-8")

    prompt = CAUSAL_PROMPT.format(
        grammar=GRAMMAR_SUMMARY,
        content=content,
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": model,
        "max_tokens": 3000,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = httpx.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers=headers,
        json=payload,
        timeout=90.0,
    )
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"].strip()


def convert_text_causal(text: str, api_key: str, model: str, base_url: str) -> str:
    """Causal intake from raw text (article, thread, post) — no file needed."""
    prompt = CAUSAL_PROMPT.format(
        grammar=GRAMMAR_SUMMARY,
        content=text,
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": model,
        "max_tokens": 3000,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = httpx.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers=headers,
        json=payload,
        timeout=90.0,
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
