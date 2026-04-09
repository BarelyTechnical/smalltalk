# Smalltalk Init

Guide the user through scanning a directory for convertible files.
Follow each step in order.

## Step 1: Check Python version

Run `python3 --version` (or `python --version` on Windows).
Confirm 3.9 or higher. If not found or too old, tell the user and stop.

## Step 2: Check if smalltalk-cli is installed

Run `pip show smalltalk-cli`.
If installed, report the version and skip to Step 4.

## Step 3: Install smalltalk-cli

Run `pip install smalltalk-cli`.

If this fails, try in order:
1. `pip3 install smalltalk-cli`
2. `python -m pip install smalltalk-cli`
3. If build errors occur on Linux/macOS: `sudo apt-get install build-essential python3-dev` then retry
4. If all fail, report the error and stop.

## Step 4: Ask for directory

Ask the user which directory to scan.
Offer the current working directory as the default.
Wait for their response.

## Step 5: Run init

Run `smalltalk init <dir>` where `<dir>` is the directory from Step 4.

The output will show:
- Files ready to convert (yellow)
- Files already converted (green)
- Files skipped — human-maintained (dim)

## Step 6: Show next steps

Tell the user what was found and suggest:
- Run `smalltalk backup <dir>` to back up originals before converting
- Run `smalltalk mine <dir>` to convert files to .st format
- Set OPENROUTER_API_KEY environment variable before mining
