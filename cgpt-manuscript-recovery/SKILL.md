---
name: cgpt-manuscript-recovery
description: Inspect an academic manuscript or revision folder after a long break and produce a durable recovery map. Use when the user asks to recover manuscript status, find the live version, identify backups/submission files/reviewer letters/Turnitin reports, resume a revision, reconstruct next actions, or create a recovery handoff before editing a manuscript.
---

# CGPT Manuscript Recovery

Use this skill to turn a messy manuscript folder into a current-state map that another Codex thread can resume from without relying on chat history.

## Workflow

1. Confirm the target folder.
   - Use the user-provided path when available.
   - If the path is ambiguous, inspect nearby folder names and choose the best match before asking.
   - Keep the pass read-only unless the user explicitly asks for backups or edits.

2. Inventory candidate artifacts.
   - Manuscripts: `.docx`, `.qmd`, `.tex`, `.md`, `.pdf`.
   - Submission package: cover letters, response letters, reviewer comments, decision letters, ScholarOne/Editorial Manager exports.
   - Evidence: Turnitin reports, figures, tables, appendices, `.bib`, data/code logs.
   - Recovery aids: `HANDOFF.md`, `MEMORY.md`, `SESSION-LOG.md`, `STATUS-LOG.md`, `NEXT-CODEX-TASK.md`, `PROJECT_STATE.json`, `archive/`, `backups/`.

3. Identify the live version.
   - Prefer explicit handoff/status notes over filenames alone.
   - If filenames conflict, compare modified times, file sizes, and nearby package files.
   - Mark confidence as high, medium, or low. Explain the evidence.

4. Detect frozen or critical files.
   - Treat submitted versions, coauthor-shared versions, reviewer letters, and files named `FINAL`, `SUBMIT`, `ACCEPTED`, `frozen`, or `backup` as no-edit until backed up.
   - If edits are requested after recovery, run `cgpt-backup` first.

5. Produce a recovery map.
   - Save it only when the user asks for a durable artifact; otherwise summarize in chat.
   - Default filename: `CGPT-<project-or-folder>-RECOVERY-MAP-YYYY-MM-DD.md` in the target folder.
   - Use exact paths and dates, not vague references to the current thread.

## Recovery Map Shape

```markdown
# CGPT Recovery Map - <Project> - YYYY-MM-DD

## Current Verdict
- Live manuscript: <path> (<confidence>; evidence)
- Current stage: <draft/revision/submission/waiting/unknown>
- Do not edit without backup: <paths>

## Key Artifacts
| Role | Path | Modified | Notes |
|---|---|---:|---|

## Evidence Read
- <path>: <what it established>

## Risks and Ambiguities
- <issue> -> <how to resolve>

## Next Codex Task
1. <specific next action>
2. <specific verification>
```

## Rules

- Do not invent project status from filenames alone.
- Do not edit manuscripts during recovery unless the user explicitly asks.
- Do not delete or rename old versions as cleanup.
- Prefer PowerShell `Get-ChildItem -LiteralPath` and `Get-Item -LiteralPath` on Windows paths.
- If Google Drive or OneDrive sync paths are involved, verify file existence with literal paths before reporting.
