# Smalltalk Status

Check the conversion state of a directory.

## Usage

    smalltalk status <dir>

## Output

The command shows:

1. A progress bar — percentage of convertible files that have .st versions
2. Converted files — with original line count, compressed line count, and % reduction
3. Pending files — convertible .md files that don't yet have a .st version
4. Skipped files — human-maintained files that are never converted

## Reading the output

A file showing "180→20 lines (89% reduction)" means:
- The original .md was 180 lines
- The .st version is 20 lines
- Token cost for agents loading this file dropped by ~89%

## If there are pending files

Run `smalltalk mine <dir>` to convert them.
Make sure OPENROUTER_API_KEY is set or pass --api-key.

## If all files show as converted

Your directory is fully compressed.
Agents loading .st files from this directory are running at maximum efficiency.
