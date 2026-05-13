---
name: cgpt-backup
description: Create timestamped backup copies of important files or folders before editing, formatting, bulk replacement, risky automation, or user-requested backup work. Use when the user says backup, create a checkpoint, copy before editing, preserve the current version, or when a MEMORY/HANDOFF note marks a file as frozen or critical.
---

# CGPT Backup

Use this skill before changing anything that needs a recoverable checkpoint: manuscripts, submission packages, decks, reports, data files, app configs, or entire project folders.

## Workflow

1. Identify the exact source path.
   - Prefer `-LiteralPath` on Windows.
   - If the user did not name a path, inspect the active project context and ask only if multiple targets are plausible.

2. Choose the backup location.
   - Default: same parent folder as the original.
   - File pattern: `<stem>_backup_YYYY-MM-DD<ext>`.
   - Directory pattern: `<name>_backup_YYYY-MM-DD`.
   - If that name exists, append `_2`, `_3`, etc.

3. Create the backup.
   - Use `scripts/make_backup.py` when available.
   - Otherwise use native PowerShell copy commands end to end.
   - Do not use Git as a substitute for a requested backup.

4. Verify before continuing.
   - Confirm the destination exists.
   - Confirm file size matches for a single file.
   - For directories, confirm recursive file count and total bytes are nonzero.

5. Report the result.
   - Include the original path, backup path, size, and whether verification passed.

## Rules

- Never edit the backup after creating it.
- Never delete old backups unless the user explicitly asks.
- Do not overwrite an existing backup.
- When backing up before edits, finish the backup first, then make the requested edits.
- If the source is inside a Git repo, do not treat a dirty worktree as a blocker; just report it if relevant.

## Helper Script

Run from PowerShell:

```powershell
python C:\Users\sundar\.codex\skills\cgpt-backup\scripts\make_backup.py --source "C:\path\to\file-or-folder"
```

Optional destination parent:

```powershell
python C:\Users\sundar\.codex\skills\cgpt-backup\scripts\make_backup.py --source "C:\path\to\file.docx" --dest-dir "C:\path\to\backups"
```
