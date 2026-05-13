---
name: cgpt-academic-proofreader
description: Report-only academic manuscript proofreading for grammar, journal style, argument flow, terminology, citation mechanics, statistical reporting, and Quarto cross-reference readiness; use before sharing, submission, or after manuscript revisions.
---

# CGPT Academic Proofreader

Use this skill when the user asks for proofreading, copyediting review, pre-submission language checks, journal-readiness review, or a manuscript quality report. The default mode is report-only: identify issues and propose fixes, but do not edit manuscript files.

## Default Behavior

- Report only unless the user explicitly asks to apply approved fixes.
- Do not edit `.qmd`, `.md`, `.docx`, `.bib`, figures, tables, or project logs during the review pass.
- Write a report only when the user asks for a file-based review or the project already uses `quality_reports/`.
- Prioritize peer-review risks over cosmetic wording.
- Coordinate with `cgpt-stats-audit` for numerical verification and `cgpt-citation-bib-audit` for deep bibliography checks. Do not duplicate full stats or external citation audits unless requested.

## Setup

Before reviewing, inspect only the relevant project guidance:

- target manuscript or section
- `CLAUDE.md`, `MEMORY.md`, `SESSION-LOG.md`, or project notes if present
- `.bib` files when citation mechanics or key resolution are in scope
- `_quarto.yml` or master QMD include chains when cross-references or rendered structure matter

If exact line numbers are available, include them. If reviewing DOCX or rendered text without stable lines, use section, paragraph, heading, or page context.

## Review Checklist

Check every requested manuscript for:

- grammar, agreement, articles, tense, sentence boundaries, and informal contractions
- journal tone, excessive hedging, weak openings, and unclear topic sentences
- causal language in observational work, including verbs such as "causes," "drives," "impacts," and "mediates" when not warranted
- author-first literature summaries that should be claim-first
- paragraph structure: claim, evidence, synthesis, implication or transition
- terminology, symbols, acronym definitions, variable names, and sample labels
- statistical reporting completeness at the prose level, including sample sizes, estimators, uncertainty, p-values, effect sizes, and confidence intervals where applicable
- citation mechanics, including unresolved `@key` patterns, inconsistent narrative versus parenthetical syntax, and likely missing support for factual claims
- Quarto references such as `@fig-`, `@tbl-`, `@eq-`, and `@sec-`
- captions, table and figure callouts, heading hierarchy, abstract presence, and obvious completeness gaps

Treat unresolved citations, unsupported factual claims, causal overreach, missing sample definitions, and broken cross-references as high-priority risks.

## Severity

- Critical: likely to block rendering, submission, or citation integrity.
- High: likely reviewer or editor concern, including causal overclaiming, unsupported claims, missing sample definitions, major argument gaps, or unresolved references.
- Medium: clarity, consistency, style, or reporting issues that weaken the manuscript.
- Low: local grammar, phrasing, punctuation, or polish.

## Report Format

Use this structure for a full review:

```markdown
# Academic Proofreading Report
**Date:**
**Document:**
**Mode:** Report only

## Summary
- Critical:
- High:
- Medium:
- Low:
- Overall readiness:

## Must Fix Before Sharing or Submission
| Location | Severity | Issue | Proposed fix |
|---|---|---|---|

## Detailed Issues
| Location | Category | Severity | Current text | Proposed text | Rationale |
|---|---|---|---|---|---|

## Cross-Checks
| Check | Result | Notes |
|---|---|---|

## Overall Assessment
- Strengths:
- Priority fixes:
- Recommended next audit:
```

For a narrow proofread, keep the same severity logic but report only the requested sections or issue categories.

## Applying Fixes

Only apply changes after explicit approval or when the user directly asks for edits. Then:

1. Apply only approved fixes.
2. Keep edits scoped to manuscript text, not data or analysis logic.
3. Re-read the affected passages.
4. If Quarto, DOCX, citations, or cross-references may be affected, recommend or run the appropriate render/check skill when in scope.

If approval is ambiguous, stop at the report.
