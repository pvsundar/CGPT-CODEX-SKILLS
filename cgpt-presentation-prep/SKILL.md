---
name: cgpt-presentation-prep
description: Extract and verify ground-truth claims, numbers, figures, tables, and visual assets before building a research presentation. Use before manuscript-to-deck work, academic talks, slide-number checks, presentation prep, source verification, figure audits, and requests to confirm that slide values match the paper or report.
---

# CGPT Presentation Prep

Use this skill before generating slides from a manuscript, paper, report, or research workspace when facts, values, figures, or claims need to be verified. The goal is to make the deck build source-grounded before any PPTX design starts.

This skill prepares the evidence. Use `cgpt-uw-pptx-deck` or the Presentations plugin after the user confirms the extracted facts and visual plan.

## Core Rule

Every number or factual claim intended for a slide must trace to a specific source location. Do not estimate, calculate, infer, or fill placeholders with guesses unless the user explicitly asks for analysis beyond source extraction.

## Intake

1. Identify the source set:
   - user-named manuscript, report, deck, spreadsheet, script output, or folder
   - project `MEMORY.md`, `README`, `SESSION-LOG`, task files, or handoff notes when present and relevant
   - modular `.qmd`/`.md` sections included by a master manuscript
   - appendices, tables, figures, and replication outputs
2. Determine whether this is extraction mode or verification mode:
   - Extraction mode: build a new ground-truth table from sources.
   - Verification mode: check existing slide numbers, notes, or memory tables against sources.
3. Ask for missing source files only if they are necessary and cannot be found locally.

## Ground-Truth Extraction

Read the relevant source material before proposing slides. Extract only facts useful for presentation planning:

- research question, setting, contribution claims, and headline findings
- sample sizes, units, time periods, exclusions, and data sources
- key tables and the few values a presenter would highlight
- key figures, captions, source paths, and whether the files exist
- core formulas, model terms, properties, proofs, or worked examples
- caveats, limitations, and audience-sensitive qualifications

Use this compact table when possible:

| Item | Value or claim | Source location | Exact source text or evidence | Slide use | Caveat |
|---|---|---|---|---|---|

If a needed value is absent, write `NOT FOUND IN SOURCE` rather than filling it in.

## Figure And Visual Asset Audit

For each existing figure or candidate visual:

- record file path, format, dimensions if available, and whether it exists
- judge whether it will survive 16:9 projection
- flag tiny labels, dense legends, bad aspect ratios, low resolution, or inaccessible colors
- recommend whether to reuse, crop, regenerate, redraw as a diagram, or replace with a placeholder

For new visuals, classify them before creating anything:

- Category A: can be generated from verified source values or from conceptual structure.
- Category B: requires running code, accessing external data, or calculating values not present in the source.

Ask the user to confirm the extraction and the Category A/B split before substantial generation or deck building.

## Talk Planning Output

After extraction, propose a slide-ready evidence map, not a full deck unless requested:

- talk type and likely duration if known
- 3-5 core audience takeaways
- preliminary section arc
- candidate slides with each slide's source-backed claim
- visuals available now and visuals requiring more data/code
- risks: unverified numbers, missing files, dense figures, or values that need replication scripts

## Boundaries

- Do not edit project memory, manuscript files, or source data unless the user explicitly asks.
- Do not start deck generation until the user confirms the extracted values or clearly waives confirmation.
- Do not claim a figure exists without checking the path when local files are available.
- Keep quotations short and only as much as needed to anchor the extracted fact.

## Handoff

When the prep pass is complete, report:

- number of values or claims confirmed
- number of values not found or needing follow-up
- figure and asset readiness
- exact source files inspected
- whether the project is ready for `cgpt-uw-pptx-deck` or another deck-build workflow
