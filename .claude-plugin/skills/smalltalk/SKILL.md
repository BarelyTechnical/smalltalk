---
name: smalltalk
description: Smalltalk — compress any agent file (skills, memory, agent specs) to .st format. 90% fewer tokens, zero information lost. Works with any LLM. Use when compressing skill files, memory logs, or agent definitions, or when asked about Smalltalk, .st files, or token compression.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Smalltalk

A token-efficient grammar for AI agent communication. Compress skill files, memory logs, and agent specs to `.st` format — 90% fewer tokens, zero information lost.

## Prerequisites

Ensure `smalltalk-cli` is installed:

```bash
smalltalk --version
```

If not installed:

```bash
pip install smalltalk-cli
```

## Usage

Smalltalk provides dynamic instructions via the CLI. To get instructions for any operation:

```bash
smalltalk instructions <command>
```

Where `<command>` is one of: `help`, `init`, `mine`, `backup`, `status`.

Run the appropriate instructions command, then follow the returned instructions step by step.

## Quick reference

```
smalltalk init <dir>            Scan a directory — see what's convertible
smalltalk backup <dir>          Back up all .md originals to .originals/
smalltalk mine <dir>            Convert .md files to .st format
smalltalk status <dir>          Show conversion state across a directory
smalltalk wake-up <dir>         Output L1 context for system prompt injection
smalltalk check <dir>           Detect contradictions across .st files
smalltalk diary write <id> "<entry>"   Write a session-end brain entry
smalltalk diary read <id>       Read agent diary
```

## Closing ritual (required)

After completing any task, run the closing ritual to close the PAG loop:

```bash
smalltalk instructions closing-ritual
```

This is what makes the brain grow. Without it, every session starts from the same brain.
RULE: session-end | write-decisions-patterns-wins-to-brain | hard
