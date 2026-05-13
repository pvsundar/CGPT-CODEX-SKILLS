---
name: cgpt-thread-closeout
description: Use when the user asks CGPT/Codex to close out, wrap up, end a thread, prepare a handoff, save session memory, create next-thread instructions, update status logs, archive a conversation, or make sure a project can be resumed cleanly later.
metadata:
  short-description: CGPT closeout with durable handoff notes
---

# CGPT Thread Closeout

Use this skill at the end of a meaningful work session, especially when the user wants the next Codex or Claude session to resume without rediscovery.

All new skill folders, handoffs, reports, recovery maps, backups, and similar CGPT-created artifacts should use a `CGPT` prefix unless the user explicitly asks for another naming convention. For Codex skill folder names, use lowercase `cgpt-...` so they satisfy skill naming rules.

## Core Workflow

1. Identify the active work context.
   - Primary workspace or project folder.
   - Files created, edited, exported, moved, or verified.
   - Commands, builds, tests, renders, browser checks, or validations that matter.
   - User constraints that should carry forward.

2. Verify only what is necessary.
   - Confirm important output files still exist.
   - Check timestamps/sizes for deliverables when useful.
   - For repos, check `git status --short` if code or tracked docs changed.
   - Do not do broad scans unless the user asks for a full inventory.

3. Produce durable notes when a clear project folder exists.
   - Prefer existing project-local files such as `SESSION-MEMORY.md`, `STATUS-LOG.md`, `HANDOFF.md`, or `NEXT-CODEX-TASK.md` if the project already uses them.
   - Otherwise create one compact file named `CGPT-THREAD-CLOSEOUT-YYYY-MM-DD.md` in the relevant project or reports folder.
   - Append to existing logs rather than replacing them unless the user explicitly asks for a rewrite.

4. Include a concrete next-thread launch point.
   - State the exact next task.
   - Name the starting folder and any no-touch folders.
   - Name the first files to read.
   - Include known blockers, risks, and unverified assumptions.

5. Respect boundaries.
   - Do not edit unrelated folders.
   - Do not revert user changes.
   - Do not commit, push, delete, or archive unless the user asks.
   - If the user names a sibling repo or folder to leave alone, treat that as a hard boundary.

6. If the user explicitly asks to end or archive the thread.
   - First provide the closeout and exact artifact paths.
   - Then use the archive directive if available in the current app context.

## Closeout Checklist

- Artifacts: exact paths and formats.
- Validation: commands/checks run and results.
- Git: branch, remote, and dirty/clean state when relevant.
- Memory/handoff: files updated or intentionally not updated.
- Next task: one concrete continuation prompt.
- Residual risk: anything not verified.

## Output Shape

Keep the final closeout short and operational:

```markdown
Closed out.

Done: ...
Saved: [file](</absolute/path/file.md>)
Validated: ...
Next thread should start with: ...
Residual risk: ...
```

For document/report work, include HTML/PDF/DOCX paths if they were created or updated. For manuscript recovery work, include the live manuscript, backup, recovery map, and next writing target.
