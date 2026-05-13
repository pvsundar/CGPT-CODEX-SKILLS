---
name: cgpt-render-check
description: Validate rendered documents and presentation outputs after Quarto, Pandoc, python-pptx, document export, HTML generation, PDF export, or report build work. Use when the user asks to check, validate, QA, inspect, smoke test, or deliver a rendered DOCX, PPTX, PDF, HTML, Markdown, or generated report.
---

# CGPT Render Check

Use this skill after generating or editing a deliverable. Do not call an output clean until the relevant checks have run or you have explicitly reported why they could not run.

## Core Checks

1. File presence and size.
   - Confirm the output exists.
   - Warn if it is empty or suspiciously small.

2. Container integrity.
   - DOCX and PPTX must be valid ZIP packages.
   - PPTX should have real slide XML files and no broken slide references.
   - PDF should open with an available PDF reader library or `pdfinfo`.
   - HTML should contain normal document structure.

3. Render artifacts.
   - Search extracted text or raw HTML/Markdown for unresolved markers: `??`, `undefined`, missing figure text, raw LaTeX commands, or obvious template placeholders.
   - For HTML reports, check that expected tables/cards/sections are present when the request named them.

4. Source gotchas when applicable.
   - Quarto/Pandoc: inspect nearby `.qmd`, `.yml`, `.bib`, and asset paths when a render fails.
   - Decks: verify slide count, title text, and any project-specific font floor or brand constraints.
   - Web outputs: open the page with the Browser skill when visual layout or interaction matters.

5. Report a concise result.
   - Use PASS/WARN/FAIL.
   - Include exact file path, file type, file size, checks run, and fixes needed.

## Helper Script

Run a first-pass structural check:

```powershell
python C:\Users\sundar\.codex\skills\cgpt-render-check\scripts\render_check.py "C:\path\to\output.docx"
```

The script is intentionally conservative. It catches structural corruption and common unresolved render markers, but visual QA still requires opening or rendering the file when layout matters.
