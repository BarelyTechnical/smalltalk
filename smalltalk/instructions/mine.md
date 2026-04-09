# Smalltalk Mine

Convert .md agent files to Smalltalk .st format using an LLM.

## Step 1: Check for API key

Check if OPENROUTER_API_KEY is set in the environment.
If not, ask the user for their key or preferred provider.

Supported providers:
- OpenRouter (default): https://openrouter.ai — set OPENROUTER_API_KEY
- Anthropic direct: --base-url https://api.anthropic.com/v1 --api-key <key>
- OpenAI direct: --base-url https://api.openai.com/v1 --api-key <key>
- Local Ollama: --base-url http://localhost:11434/v1 --api-key ollama

## Step 2: Confirm backup exists

Ask if the user has run `smalltalk backup <dir>` already.
If not, strongly recommend running it first. Originals are kept by default
but backup is best practice.

## Step 3: Run mine

Basic usage:
    smalltalk mine <dir>

With explicit key:
    smalltalk mine <dir> --api-key YOUR_KEY

Preview without writing:
    smalltalk mine <dir> --dry-run

With local Ollama:
    smalltalk mine <dir> --base-url http://localhost:11434/v1 --api-key ollama --model llama3.1

Remove originals after conversion:
    smalltalk mine <dir> --no-keep-originals

## Step 4: Review output

The command will show a spinner per file and report:
- Files converted with line reduction stats
- Files that failed (originals untouched)

## Step 5: Verify

Run `smalltalk status <dir>` to see the full conversion state with
a progress bar and per-file reduction percentages.

## What gets skipped automatically

These files are never converted — they are human-maintained:
- README.md, CHANGELOG.md, CONTRIBUTING.md, LICENSE.md
- stack.md, CONTEXT.md, GEMINI.md, CLAUDE.md

Everything else is a candidate. The tool detects file type automatically
(skill, memory, agent, design, config) and uses the appropriate Smalltalk
types for conversion.
