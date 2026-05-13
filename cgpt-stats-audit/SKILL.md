---
name: cgpt-stats-audit
description: Compact Codex skill for report-only statistical audits of manuscripts against source data, extracted numerals, sample labels, figures, and cross-references.
---

# CGPT Stats Audit

Use this skill when the user asks for a stats audit, statistical verification, manuscript number check, pre-submission stats gate, or consistency check between a manuscript and source data.

## Default Behavior

- Report only by default. Do not edit manuscripts, supplements, data, figures, or project state.
- Write audit artifacts only when the user asks for a file-based audit or when the project already uses `quality_reports/`.
- Do not declare a manuscript "submission-ready" unless the statistical audit passes and any existing render/citation checks also pass.
- If the user asks for fixes, first report the exact mismatches and ask which files to edit unless the requested edit scope is already explicit.

## Pipeline

Run in this order:

1. Compute ground truth from source data.
2. Extract all manuscript numerals.
3. Match extracted values against ground truth and lint supporting evidence.

Do not skip a phase unless the user asks for a narrow spot check.

## Phase 1: Compute Ground Truth

Inputs:

- source data paths from `MEMORY.md`, `CLAUDE.md`, `PROJECT_STATE.json`, or user instructions
- CSV/XLSX data files in project data or results directories

Expected artifact:

- `quality_reports/ground_truth.json`

Rules:

- Compute values from source data, not from manuscript prose.
- Include explicit sample labels in keys when possible, for example `sample=restricted_N57`.
- Mark uncomputable values as `UNVERIFIABLE` with a note explaining what data is missing.
- Preserve or create a reproducible script when doing a full audit, commonly `quality_reports/stats_audit_compute.py`.

## Phase 2: Extract Numerals

Inputs:

- manuscript `.qmd`, `.md`, `.docx`, supplement, tables, captions, footnotes, and appendices

Expected artifact:

- `quality_reports/extracted_numbers.csv`

Extract every numeral and classify it as one of:

- `structural`
- `N`
- `rank`
- `correlation`
- `p_value`
- `test_statistic`
- `coefficient`
- `R_squared`
- `percentage`
- `descriptive`
- `unknown`

Capture document, section, line number if available, sentence or table-row context, raw value, normalized value, type, and sample label.

## Phase 3: Match and Lint

Expected artifact:

- `quality_reports/audit_report.md`

Checks:

- strict deterministic rounding against ground truth
- sample-label consistency
- impossible values such as correlations outside `[-1, 1]`, p-values outside `[0, 1]`, negative SDs, rank values greater than sample size, or invalid HHI/Gini ranges
- stale figures by comparing figure timestamps to source data timestamps when possible
- banned terms and project-specific conventions from `CLAUDE.md`
- stale sample or tier references from `MEMORY.md`
- broken Quarto references such as missing `@tbl-`, `@fig-`, `@sec-`, or `@eq-` targets

## PASS Criteria

Report `PASS` only when all must-fix categories are zero:

- critical mismatches
- sample label issues
- impossible values
- stale figures
- banned word or convention violations that the project treats as blockers
- stale tier or sample references
- cross-reference failures

Orphan numbers and unmatched ground-truth keys are warnings unless project instructions make them blockers.

## Report Format

Use this structure for a full audit:

```markdown
# Stats Audit Report
**Date:**
**Manuscript:**
**Ground truth:**
**Extracted numerals:**

## Critical Mismatches
| Location | Manuscript value | Expected | Ground-truth key | Issue |
|---|---:|---:|---|---|

## Sample Label Issues
| Location | Value | Matched key | Issue |
|---|---:|---|---|

## Impossible Values
| Location | Value | Type | Rule violated |
|---|---:|---|---|

## Stale Figures
| Figure | Figure date | Source data date | Issue |
|---|---|---|---|

## Convention and Cross-Reference Checks
| Location | Pattern | Issue |
|---|---|---|

## Orphan Numbers
| Location | Value | Type | Context |
|---|---:|---|---|

## Unmatched Ground Truth
| Key | Value | Note |
|---|---:|---|

## Summary
- Critical mismatches:
- Sample label issues:
- Impossible values:
- Stale figures:
- Convention violations:
- Cross-reference failures:
- Orphan numbers:
- Unmatched ground-truth keys:

## Verdict
**Audit status:** PASS / FAIL
```

For a spot check, keep the same severity logic but report only the requested values.

## Source Material

This Codex skill is a compact workflow derived from the local manuscript development kit:

- `MANUSCRIPT-DEV-KIT/protocols/stats-audit-protocol.md`
- `MANUSCRIPT-DEV-KIT/agents/stats-calculator.md`
- `MANUSCRIPT-DEV-KIT/agents/stats-extractor.md`
- `MANUSCRIPT-DEV-KIT/agents/stats-matcher.md`
