---
name: cgpt-academic-docx-authoring
description: Create, edit, structure, and verify academic Word DOCX artifacts such as manuscript drafts, cover letters, response letters, appendices, and supplementary files. Use when the user asks to author a new academic .docx, revise a Word manuscript, insert tables or figures, convert polished academic Markdown into DOCX, or prepare a journal-facing Word deliverable that is not primarily a JM/JMR formatter run.
---

# CGPT Academic DOCX Authoring

Use this skill for academic Word authoring and editing where the main work is document construction, content organization, tables, figures, comments, or revision-ready prose. For JM/JMR or PVB formatter runs, use `cgpt-jm-jmr-docx`. For final integrity checks, use `cgpt-render-check`.

## Scope

- Create new academic DOCX files from source notes, Markdown, Quarto output, or user instructions.
- Edit existing DOCX manuscripts, cover letters, response letters, appendices, and supplementary materials.
- Build journal-style tables, figure callouts, captions, headings, references sections, and front matter.
- Preserve reviewer-facing or journal-facing polish: consistent voice, clean headings, no unresolved placeholders, no broken file references.

## Workflow

1. Identify the deliverable.
   - Confirm whether the output is a manuscript, cover letter, response letter, appendix, supplement, or internal memo.
   - Confirm journal/style constraints when they are named. If unspecified, use conservative APA-style academic defaults.

2. Protect important inputs.
   - If editing a critical manuscript, submission version, or user-supplied DOCX, use `cgpt-backup` before changing it.
   - Do not treat Git history as a substitute for a requested backup.

3. Choose the authoring path.
   - Existing `.docx`: edit the file directly with a DOCX-aware workflow and preserve existing structure when possible.
   - Markdown or text source: convert or build into DOCX, then inspect the generated structure.
   - Quarto manuscript: render to DOCX first; if the job is submission formatting, hand off to `cgpt-jm-jmr-docx`.
   - Response-to-reviewers prose: use `cgpt-reviewer-response` for content strategy, then this skill for the DOCX artifact.

4. Apply academic document defaults.
   - Use US Letter unless the journal specifies otherwise.
   - Use 12pt body text, readable academic font defaults, one-inch margins, and consistent heading hierarchy.
   - Keep tables journal-clean: no vertical rules, clear top/header/bottom rules, compact table font, and explicit table notes.
   - Keep figure captions and callouts traceable to the manuscript text.

5. Verify before delivery.
   - Use `cgpt-render-check` for structural validation.
   - Confirm file existence, nonzero size, valid DOCX package, expected major sections, expected table/figure count where relevant, and no unresolved markers such as `TODO`, `??`, `undefined`, or placeholder bracket text.
   - When layout matters, render/open the DOCX for visual QA and report any limitation if that is not possible.

## Editing Rules

- Preserve the user's wording where the request is formatting or structure only.
- Do not invent citations, journal requirements, author affiliations, reviewer comments, page numbers, table numbers, or results.
- Use tracked changes or comments only when the user asks for them or when the workflow clearly requires reviewable edits.
- Keep internal filenames, draft labels, and tool handoff notes out of journal-facing text.
- Report the exact output path, validation result, and any unresolved assumptions.

## Handoff

Use the adjacent CGPT skills rather than duplicating their jobs:

- `cgpt-backup` before risky or user-requested backups.
- `cgpt-jm-jmr-docx` for JM/JMR or PVB manuscript post-processing.
- `cgpt-reviewer-response` for response-letter strategy and voice.
- `cgpt-render-check` before calling the DOCX deliverable ready.
