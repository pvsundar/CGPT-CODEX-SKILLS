---
name: cgpt-quarto-debugger
description: Diagnose and fix Quarto source problems in `.qmd` projects, especially YAML/front matter, citations, cross-references, includes, filters, and Pandoc/engine errors. Use when Quarto renders fail, output shows unresolved references, citations do not resolve, includes are missing, or a user shares a Quarto error and asks what it means.
---

# CGPT Quarto Debugger

Use this skill for Quarto build failures caused by document source, project configuration, or scholarly apparatus. Keep it distinct from `cgpt-quarto-render-windows`, which handles Windows PATH, PATHEXT, spawned-shell, and stale-render environment hardening.

## Triage Boundary

Use this skill when symptoms point to:

- YAML/front matter syntax, nesting, duplicate keys, or wrong format options.
- Citation failures: missing bibliography, bad `.bib` path, missing keys, malformed entries, or CSL path issues.
- Cross-reference failures: unresolved `@fig-*`, `@tbl-*`, `@eq-*`, `@sec-*`, duplicate labels, wrong prefixes, or rendered `???`.
- Include/filter/project issues: missing `_quarto.yml`, `_metadata.yml`, `_variables.yml`, partials, Lua filters, custom templates, or extension paths.
- Pandoc, Typst, LaTeX, knitr, or Jupyter errors that trace back to source content or chunk code.

If `cmd`, `quarto`, R, Python, or output freshness fails only in Codex/PowerShell/scheduled tasks, switch to `cgpt-quarto-render-windows`.

## Workflow

1. Capture the exact render command, target format, error text, and expected output path.
2. Read the relevant `.qmd` plus nearby config files: `_quarto.yml`, `_metadata.yml`, include files, bibliography files, CSL files, filters, and referenced assets.
3. Classify the failure before editing: YAML, citations, crossrefs, includes, filters/templates, engine/chunk, or target-format incompatibility.
4. Make the smallest source/config fix that explains the observed failure.
5. Re-render the requested target when feasible.
6. Hand the resulting artifact to `cgpt-render-check` for final output validation.

## Fast Checks

### YAML

- Front matter starts and ends with `---`.
- Indentation uses spaces, not tabs.
- Format options are nested under the target format.
- Values with colons or special characters are quoted.
- Common keys are spelled correctly: `bibliography`, `csl`, `crossref`, `number-sections`, `reference-doc`, `include-before-body`, `include-after-body`.
- Project-level config does not conflict with document-level config.

### Citations

- `bibliography:` exists when citations appear.
- Bibliography paths resolve relative to the rendering document or project.
- Citation keys in text match `.bib` entry keys exactly, including case.
- `.bib` entries have balanced braces and valid field syntax.
- CSL files exist and are appropriate for the target style.

### Crossrefs

- Every `@fig-*`, `@tbl-*`, `@eq-*`, and `@sec-*` reference has exactly one matching label.
- Labels use the right prefix and include the leading `#` where Quarto expects it.
- Figure/table captions are present when the target format requires them for crossrefs.
- Labels are not duplicated across included files.
- Reference text does not mix underscores and hyphens by accident.

### Includes, Assets, And Filters

- Include paths, image paths, reference docs, and templates exist.
- Paths with spaces are quoted in YAML.
- Lua filters and Quarto extensions are installed or vendored into the project.
- Format-specific raw blocks are guarded with Quarto conditional content when rendering to multiple targets.

## Useful Commands

Run from the project directory when possible:

```powershell
quarto render "path\to\file.qmd" --to html --log debug
quarto render "path\to\file.qmd" --to docx --log debug
quarto check
```

For source inventory, prefer `rg`:

```powershell
rg "@(fig|tbl|eq|sec)-|#(fig|tbl|eq|sec)-" "path\to\project"
rg "@[A-Za-z0-9_:-]+" "path\to\file.qmd"
rg "bibliography:|csl:|include-|filters:|reference-doc:" "path\to\project"
```

## Rules

- Do not rewrite manuscript prose while fixing build mechanics unless the prose contains the broken reference, citation, or include.
- Do not treat a successful exit code as final validation; inspect output and run `cgpt-render-check`.
- Do not make Windows environment fixes in this skill; route those to `cgpt-quarto-render-windows`.
- Report the root cause, changed files, render command, and remaining warnings.
