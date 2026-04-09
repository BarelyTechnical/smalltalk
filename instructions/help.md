# Smalltalk

Token-efficient grammar for AI agent communication.
Compress skill files, memory logs, and agent specs to .st format — 90% fewer tokens, zero information lost.

---

## CLI Commands

    smalltalk init <dir>              Scan a directory — see what's convertible
    smalltalk backup <dir>            Back up all .md originals to .originals/
    smalltalk mine <dir>              Convert .md files to .st format
    smalltalk status <dir>            Show conversion state across a directory
    smalltalk wake-up <dir>           Output compressed L1 context for system prompt injection
    smalltalk check <dir>             Detect contradictions across .st files

    smalltalk kg query <dir> <entity>           Entity relationships (active + historical)
    smalltalk kg query <dir> <entity> --as-of   Point-in-time query  (YYYY-MM)
    smalltalk kg timeline <dir> <entity>         Chronological story of an entity
    smalltalk kg invalidate <file> <line>        Write ended: to resolve a contradiction
    smalltalk kg invalidate <file> <line> --ended YYYY-MM
    smalltalk kg visualize <dir>               Open interactive KG graph in browser
    smalltalk kg visualize <dir> --out out.html --no-browser   Save HTML without opening

    smalltalk palace init <dir>       Generate _index.st from directory structure
    smalltalk palace index <dir>      Refresh _index.st after adding files
    smalltalk palace status <dir>     Show wings, rooms, tunnels

    smalltalk diary write <id> "<entry>"  Write specialist agent diary entry
    smalltalk diary read <id>             Read agent diary

    smalltalk instructions help             Print this file
    smalltalk instructions mine             Step-by-step mine guide
    smalltalk instructions kg              Knowledge Graph guide (LINK, temporal, invalidate)
    smalltalk instructions palace          Palace navigation guide
    smalltalk instructions check           Contradiction detection guide
    smalltalk instructions closing-ritual  The session-end write-back protocol (PAG close loop)

---

## MCP Server (18 tools)

    python -m smalltalk.mcp_server

    smalltalk_status(dir)                  Overview — file count, entry count, types
    smalltalk_get_spec()                   Full grammar type reference
    smalltalk_list_files(dir)              List all .st files with entry counts
    smalltalk_read_file(path)              Read a .st file
    smalltalk_search(dir, query)           Keyword search across .st files
    smalltalk_wake_up(dir)                 Extract L1 context for system prompt
    smalltalk_check(dir)                   Contradiction detection
    smalltalk_palace_init(dir)             Generate _index.st
    smalltalk_palace_index(dir)            Refresh _index.st
    smalltalk_navigate(dir, query)         Load relevant rooms for a query
    smalltalk_list_wings(dir)              List all palace wings
    smalltalk_list_rooms(dir, wing)        List rooms in a wing
    smalltalk_kg_query(dir, entity)        Entity relationships
    smalltalk_kg_timeline(dir, entity)     Chronological story of an entity
    smalltalk_kg_invalidate(file, line)    Write ended: to resolve a contradiction
    smalltalk_kg_visualize(dir)            Generate interactive KG HTML (returns file path)
    smalltalk_diary_write(id, entry)       Write agent diary entry
    smalltalk_diary_read(id)              Read agent diary

---

## The Grammar

Syntax: TYPE: identifier | field | field | field

Separators:
  |   field boundary
  +   multiple values in one field    next+vite+remix
  :   key-value within a field        broke:vite-build
  >   choice over alternative         cloudflare>vercel

Values: lowercase-hyphenated, no spaces inside field values.
One line per entry. Append — never overwrite.

### Universal Types

    RULE:     id | rule-description | hard|soft
    REF:      id | path/to/file.st  | covers:topic
    NOTE:     id | observation
    CONFIG:   id | key | value
    CONTEXT:  id | scope | value
    DECISION: id | choice>rejected | reason | date
    PATTERN:  id | broke:what | cause:why | fix:what | reuse:y/n

### Memory Types

    WIN:       id | technique | outcome | repeat:y/n
    CLIENT:    id | pref:what | avoid:what | updated:date
    COMPONENT: id | stack | does:what | use-when
    PROMPT:    id | task-type | approach | why-worked | reuse:y/n

### Knowledge Graph Types

    LINK:   source | rel:relationship | target | [valid_from:YYYY-MM] | [ended:YYYY-MM] | [stability:x]
    TUNNEL: wing-id | connects:wing-id | via:shared-topic

Common rel: values — works-on, depends, defined-as, member-of, reports-to, assigned-to,
             deployed-to, blocks, contributes-to, references, replaced-by, caused-by

Temporal fields (valid on ANY entry type):
    valid_from:YYYY-MM     When this fact became true
    ended:YYYY-MM          When this fact stopped being true  (set by contradiction resolution only)
    stability:permanent    Core truth — always load, never auto-expire
    stability:stable       Valid until explicitly ended  (default)
    stability:transient    Expected to change — use for assignments, sprints, status

### Skill Types

    SKILL:   id | triggers | stack | version
    USE:     id | when:context
    PHASE:   id | number | name | what-happens
    STEP:    id | phase | number | action | required|optional
    STACK:   id | layer | tool | why
    CHECK:   id | verification-item | required|optional
    AVOID:   id | antipatterns+separated
    SCRIPT:  id | path/to/script | what-it-does

### Agent Types

    AGENT:   id | role | capabilities | scope
    TASK:    id | action | target | priority:high|mid|low
    TRIGGER: id | event | condition | then:action
    OUTPUT:  id | type | destination | format
    ERROR:   id | broke:what | cause:why | state:recovered|unresolved

### Palace Types

    WING:   id | type:project|person|topic | keywords:kw1+kw2+kw3
    ROOM:   id | wing:wing-id | hall:TYPE1+TYPE2 | file:relative/path.st
    TUNNEL: id | wings:wing-a+wing-b | topic
    LAYER:  id | file:path|trigger:event | load:always|source:x|command:x

---

## Contradiction Resolution — Full Cycle

The checker detects. The invalidate command resolves. You confirm.

    Step 1:  smalltalk check <dir>
             → [WARNING] DECISION: deploy | diverging-choices
               decisions.st:7  DECISION: deploy | vercel>railway | cost | 2026-01  << older

    Step 2:  smalltalk kg invalidate decisions.st 7
             → Before: DECISION: deploy | vercel>railway | cost | 2026-01
             → After:  DECISION: deploy | vercel>railway | cost | 2026-01 | ended:2026-04

    Step 3:  smalltalk check <dir>
             → OK  No active contradictions detected.

Agents can run this cycle autonomously via MCP:
    smalltalk_check() → find file + line_no → smalltalk_kg_invalidate() → smalltalk_check()

Key rule: ended: is NEVER set by a clock. Only set by contradiction resolution.
Historical entries (ended: <= today) are excluded from check, wake-up, and navigate.

---

## What Gets Compressed

    Skill definitions (SKILL.md, .cursorrules, routing files)  → compress to .st
    Memory logs (_brain/decisions/, patterns/, wins/, etc.)    → compress to .st
    Agent specs and pipeline definitions                        → compress to .st
    Design systems and style guides                            → compress to .st
    Config and environment mapping                             → compress to .st
    Human-maintained context (stack.md, CONTEXT.md)           → keep as .md
    Reference docs loaded on demand                            → keep as .md, link via REF
    READMEs and documentation                                  → keep as .md
    Code files, MCP servers, API schemas                       → never compress (ops layer)

Rule: if an agent loads it on every session start → compress it.
If an agent loads it only when a specific topic comes up → keep .md, link via REF.
If it must be syntactically exact (code, schemas, configs) → never compress.

---

## Loading .st Files

Add to your CLAUDE.md, GEMINI.md, or system prompt:

    Read .st files before .md files. .st is Smalltalk compressed format —
    load as session context. Load .md references only when a specific topic
    requires deep detail.

---

## Getting Started

    1. smalltalk instructions init      — set up and convert your first directory
    2. smalltalk instructions mine      — convert files to .st
    3. smalltalk instructions status    — check conversion state
    4. smalltalk instructions wake-up   — inject context into local models
    5. smalltalk instructions check     — detect contradictions
    6. smalltalk instructions kg        — knowledge graph, LINK entries, invalidate
    7. smalltalk instructions palace    — palace navigation and _index.st
    8. smalltalk instructions diary     — specialist agent knowledge base
