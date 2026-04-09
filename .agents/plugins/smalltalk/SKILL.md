---
name: smalltalk
description: Smalltalk — compress any agent file (skills, memory, agent specs) to .st format. 90% fewer tokens, zero information lost. Works with any LLM. Use when compressing skill files, memory logs, or agent definitions, or when asked about Smalltalk, .st files, or token compression.
---

# Smalltalk

A token-efficient grammar for AI agent communication.

## Prerequisites

```bash
pip install smalltalk-cli
smalltalk --version
```

## Usage

```bash
smalltalk instructions <command>
```

Commands: `help`, `init`, `mine`, `backup`, `status`

## Quick reference

```
smalltalk init <dir>       Scan a directory — see what's convertible
smalltalk backup <dir>     Back up all .md originals to .originals/
smalltalk mine <dir>       Convert .md files to .st format
smalltalk status <dir>     Show conversion state
```
