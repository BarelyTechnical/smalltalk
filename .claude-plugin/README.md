# Smalltalk — Claude Plugin

Compress agent skill files, memory logs, and specs to .st format.
90% fewer tokens on every session start. Zero information lost.

## Install

```bash
pip install smalltalk-cli
```

## Usage in Claude Code

Once the plugin is active, use the slash command:

    /smalltalk

Or ask Claude directly:

    "Compress my skills folder to Smalltalk format"
    "Convert _brain/ to .st files"
    "Show me the Smalltalk grammar"

Claude will run `smalltalk instructions help` to load the grammar and guide you through the process.

## Manual CLI

```bash
smalltalk init <dir>      # scan what's convertible
smalltalk backup <dir>    # back up originals
smalltalk mine <dir>      # convert to .st
smalltalk status <dir>    # check conversion state
```

Set `OPENROUTER_API_KEY` or pass `--api-key` for the mine command.
