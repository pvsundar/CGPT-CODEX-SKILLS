---
name: cgpt-author-reviser
description: Execute approved academic manuscript revisions from referee reports, decision letters, or user-approved revision plans. Use when the user wants Codex to apply reviewer-driven changes to manuscript files, but only after backup, triage, edit preview, and explicit approval.
---

# CGPT Author Reviser

Use this skill when the user asks Codex to apply revisions to an academic manuscript based on a saved reviewer report, decision letter, response matrix, or approved revision plan.

This is an execution skill, not a reviewer. It does not invent critique. It turns approved revision instructions into traceable edits.

## Guardrails

- Start in report/plan mode. Do not edit manuscript files until the user approves the revision plan and edit preview.
- Use `cgpt-backup` before editing active manuscript, DOCX, QMD, or response files.
- Read project guidance first when present: `MEMORY.md`, `CLAUDE.md`, `HANDOFF.md`, `SESSION-LOG.md`, master QMD include chains, and frozen-file notes.
- Do not edit frozen files, submission copies, bibliography files, data, figures, or analysis scripts unless explicitly authorized.
- Do not change numerical values, citations, models, tables, or claims unless the reviewer requested it and the user approves the exact edit.
- Keep every change traceable to a reviewer/editor item or user instruction.

## Workflow

1. Ingest the revision source.
   - Identify reviewer/editor IDs, comment numbers, requested actions, manuscript locations, and must-answer items.
   - Pair with `cgpt-reviewer-response` when response-letter strategy is needed.

2. Produce a revision plan before edits.
   - Accepted items with file targets and proposed action.
   - Deferred items requiring author choice.
   - Declined items with a reason or conflict with project rules.
   - Risks: frozen files, missing sources, unverified page/section references, or unclear active manuscript path.

3. Produce an edit preview.
   - For each accepted item, show file, location, old text when available, proposed new text, and reviewer item addressed.
   - For insertions, show exact insertion point and full proposed text.
   - Wait for explicit user approval unless the user already gave a bounded "apply all previewed edits" instruction.

4. Execute approved edits only.
   - Re-read each target file immediately before editing.
   - Use the smallest edit that implements the approved revision.
   - Preserve citations and cross-references unless the approved edit explicitly changes them.
   - Keep a revision log with file, location, reviewer item, and summary of change.

5. Verify after edits.
   - Run render/build checks when feasible.
   - Use `cgpt-render-check` for DOCX/PDF/HTML outputs.
   - Use `cgpt-citation-bib-audit` when citation keys or references changed.
   - Use `cgpt-stats-audit` when numerical claims, tables, or sample definitions changed.

## Report Format

Use this structure before edits:

```markdown
# Revision Plan

## Accepted
| ID | Issue | File(s) | Proposed action |
|---|---|---|---|

## Deferred
| ID | Question for author | Why it matters |
|---|---|---|

## Declined
| ID | Reason | Alternative |
|---|---|---|

## Edit Preview
| ID | File | Current text or location | Proposed text or action |
|---|---|---|---|
```

After edits, report:

- files changed
- reviewer items addressed
- checks run
- unresolved author decisions
- exact output or response-letter path if created

## Boundaries

If the requested revision is broad, ambiguous, or likely to change the argument materially, stop at the plan and ask for author approval.
