# Smalltalk — Codex Plugin

Compress agent skill files, memory logs, and specs to .st format.
90% fewer tokens on every session start. Zero information lost.

## Install

```bash
pip install smalltalk-cli
```

## Usage in Codex

Once the plugin is active, use the skills:
- `init` — scan a directory for convertible files
- `mine` — convert .md files to .st format
- `backup` — back up originals before converting
- `status` — check conversion state

## Manual CLI

```bash
smalltalk init <dir>
smalltalk backup <dir>
smalltalk mine <dir>
smalltalk status <dir>
```
