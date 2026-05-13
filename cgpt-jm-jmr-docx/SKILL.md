---
name: cgpt-jm-jmr-docx
description: Convert, format, post-process, and verify Word DOCX manuscripts for Journal of Marketing, Journal of Marketing Research, APA-style management/marketing submissions, and PVB academic manuscript style. Use when the user asks to convert a Word docx into JM or JMR style, format a manuscript for submission, fix APA-style tables or references, run the PVB DOCX formatter, clean a Quarto/Pandoc-rendered DOCX, style bibliography entries, or prepare a submission-ready Word file.
---

# CGPT JM/JMR DOCX

Use this skill for submission-style Word manuscripts, especially Journal of Marketing, Journal of Marketing Research, and closely related APA-style marketing/management journals.

This is a Codex-owned copy of the user's Claude/Cowork workflow. Do not edit the Claude source skill set. Use the scripts bundled in this skill unless the active project has newer project-local formatter scripts.

## What This Skill Does

- Formats body text, headings, title page/front matter, abstract, captions, footnotes, references, and page setup.
- Formats tables using journal/APA-style rules: no vertical lines, clear top/header/bottom rules, consistent font sizing, centered tables, and styled table notes.
- Supports Quarto `.qmd` to `.docx` rendering followed by post-processing.
- Supports already-rendered or user-provided `.docx` files.
- Provides a direct-creation reference for non-Quarto academic DOCX artifacts through `references/academic_defaults.js`.

## Bundled Resources

- `scripts/pvb_format_docx.R`: wrapper that renders `.qmd` when needed, then runs text and table formatting.
- `scripts/pvb_format_text.R`: paragraph styles, page setup, front matter, footnotes, and references.
- `scripts/pvb_format_tables_v3.R`: table borders, fonts, alignment, and post-table notes.
- `references/academic_defaults.js`: defaults for direct DOCX creation with Node/docx.
- `references/origin.md`: source provenance and no-touch boundary.

## Standard Workflow

1. Back up the input if it is a critical manuscript, frozen submission version, or user-supplied file.
   - Use `cgpt-backup` first when appropriate.

2. Determine the input type.
   - `.qmd`: render to DOCX, then format.
   - `.docx`: format directly.
   - `.doc`: convert to `.docx` first if tooling is available; otherwise ask the user to provide `.docx`.

3. Run the formatter from the Codex skill scripts.

```powershell
Rscript "C:\Users\sundar\.codex\skills\cgpt-jm-jmr-docx\scripts\pvb_format_docx.R" "C:\path\to\manuscript.docx" --refs=Bibliography-JM --force-refs
```

For Quarto input:

```powershell
Rscript "C:\Users\sundar\.codex\skills\cgpt-jm-jmr-docx\scripts\pvb_format_docx.R" "C:\path\to\manuscript.qmd" --refs=Bibliography-JM --force-refs
```

4. Use `--refs=Bibliography-JM` for JM/JMR-style references unless the active project specifies another bibliography style.

5. Verify output.
   - Run `cgpt-render-check` on the output DOCX.
   - Confirm the formatted file exists and is non-empty.
   - When possible, render or open the DOCX for visual QA before delivery.

## Expected Formatting

- US Letter page setup.
- Academic body text in 12pt font with manuscript spacing and first-line indentation.
- APA-style heading hierarchy.
- Abstract and front matter styled separately from body text.
- References repaired into a bibliography style with hanging indent; JM/JMR mode uses `Bibliography-JM`.
- Tables use clean academic rules, no vertical borders, centered alignment, consistent cell padding, and formatted notes.

## Dependencies

The R formatter requires:

```r
install.packages(c("officer", "xml2"), repos = "https://cloud.r-project.org")
```

Quarto is required only when the input is `.qmd`.

If dependencies are missing and installation requires network access, request approval before installing. Do not silently rewrite the workflow in another tool unless the user approves.

## Troubleshooting

| Symptom | Likely Cause | Action |
|---|---|---|
| DOCX is locked | Open in Word | Close Word and rerun |
| `officer` or `xml2` missing | R packages not installed | Ask approval to install packages |
| Tables not formatted | Table script skipped or failed | Run wrapper again or run table script directly |
| References still look like body text | Pandoc emitted refs without bibliography style | Use `--refs=Bibliography-JM --force-refs` |
| Quarto render fails | Source or YAML issue | Fix render first; do not format stale output |

## Delivery Checklist

- Backup created when needed.
- Formatter command and flags reported.
- Output path reported.
- Render/integrity check completed or limitation stated.
- Claude source skills left untouched.
