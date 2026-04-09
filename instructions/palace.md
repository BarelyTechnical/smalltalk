# smalltalk palace

Structure .st files into a navigable palace — wings, rooms, tunnels.
The file system IS the palace. No database required.

---

## Why this matters

Without palace structure: agent scans all .st files for every query.
With palace structure: agent reads _index.st (150 tokens), navigates directly to the right file.

Result: 34% better recall, 98% fewer tokens loaded per session.

---

## Commands

    smalltalk palace init <dir>      Scan directory, generate _index.st
    smalltalk palace index <dir>     Regenerate _index.st (after adding files)
    smalltalk palace status <dir>    Show wings, rooms, tunnels, memory stack

---

## Directory conventions

The best palace structure follows this pattern:

    _brain/
    ├── people/                ← category folder → type:person wings
    │   ├── kai.st             ← WING: kai, ROOM: kai (single-file wing)
    │   └── priya.st           ← WING: priya
    └── projects/              ← category folder → type:project wings
        ├── myapp/             ← WING: myapp (multi-room project)
        │   ├── auth.st        ← ROOM: auth
        │   ├── billing.st     ← ROOM: billing
        │   └── deploy.st      ← ROOM: deploy
        └── nova/              ← WING: nova
            └── auth.st        ← ROOM: auth (tunnel: myapp ↔ nova)

Detection rules (applied in order):
  1. Subfolder with sub-subfolders → CATEGORY folder (each sub = wing)
  2. Subfolder named people/ or projects/ with only .st files → each .st = wing
  3. Any other subfolder → WING folder (each .st = room)
  4. Root-level .st files → single-file wings (type:topic)

---

## Workflow

    # First time
    smalltalk palace init _brain/

    # Add new file
    echo "DECISION: db | postgres>mysql | scale | 2026-04" >> _brain/projects/myapp/database.st
    smalltalk palace index _brain/

    # Check what was detected
    smalltalk palace status _brain/

---

## What _index.st looks like

    # Smalltalk Palace Index
    # palace root: _brain
    # Always load first (~150 tokens). Navigate with smalltalk_navigate().

    # Memory Stack
    LAYER:  L0 | file:identity.st | load:always
    LAYER:  L1 | file:_index.st   | load:always
    LAYER:  L2 | trigger:topic    | source:navigate
    LAYER:  L3 | trigger:search   | command:smalltalk_search

    # Wings
    WING:   kai   | type:person  | keywords:kai
    WING:   myapp | type:project | keywords:myapp
    WING:   nova  | type:project | keywords:nova

    # Rooms
    ROOM:   kai      | wing:kai   | hall:DECISION+WIN | file:people/kai.st
    ROOM:   auth     | wing:myapp | hall:DECISION+PATTERN | file:projects/myapp/auth.st
    ROOM:   auth     | wing:nova  | hall:DECISION+PATTERN | file:projects/nova/auth.st

    # Tunnels
    TUNNEL: auth | wings:myapp+nova | topic:auth

---

## MCP equivalents

    smalltalk_navigate(directory="_brain/", query="auth decision")
    → ["/path/to/_brain/projects/myapp/auth.st"]

    smalltalk_list_wings(directory="_brain/")
    → kai [person], myapp [project], nova [project]

    smalltalk_list_rooms(directory="_brain/", wing="myapp")
    → auth, billing, deploy

---

## Using with local models

    smalltalk palace init _brain/
    smalltalk wake-up _brain/ > context.txt
    # Paste context.txt into system prompt
    # Agent now knows where everything is in ~150 tokens

---

## Tips

- Use descriptive folder and file names — navigate scores on names, not content
- Keep rooms focused (one topic per file, not everything in one file)
- Tunnels are auto-detected — no configuration needed
- Run 'palace index' whenever you add or rename files
