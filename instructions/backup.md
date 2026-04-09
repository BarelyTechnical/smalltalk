# Smalltalk Backup

Back up all .md originals before conversion. Always do this before mining.

## Step 1: Confirm directory

Confirm the directory the user wants to back up.
If they haven't specified one, ask.

## Step 2: Run backup

Run `smalltalk backup <dir>`.

This copies every .md file to `.originals/` inside the same directory,
preserving the full folder structure. Files already in backup are skipped.

## Step 3: Confirm output

The command will report:
- How many files were backed up
- How many were already in backup and skipped
- Location of the backup: `<dir>/.originals/`

## Step 4: Next step

Tell the user their originals are safe and they can now run:

    smalltalk mine <dir>

Note: `.originals/` is excluded from future scans — backups will never
be converted or double-backed-up.
