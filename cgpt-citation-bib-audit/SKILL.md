---
name: cgpt-citation-bib-audit
description: Compact Codex skill for APA citation checks, BibTeX consistency audits, Quarto citation audits, and user-triggered deep bibliography verification with source-cited results.
---

# CGPT Citation Bib Audit

Use this skill when the user asks to check citations, verify references, audit a `.bib` file, inspect Quarto citation syntax, run BibVerify, or prepare a pre-submission reference check.

## Guardrails

- Do not edit manuscript or bibliography files unless the user explicitly asks for fixes after seeing the audit.
- Do not include or request API keys. The deployed BibVerify workflow uses free scholarly APIs and a polite contact email only if the user supplies one.
- Do not run deep external verification automatically. It must be explicitly requested with terms such as "deep check", "BibVerify", "verify against databases", "pre-submission reference check", or "run full bibliography verification".
- When reporting external verification, cite the sources queried or the generated BibVerify report files. Distinguish database evidence from local format checks.
- Keep outputs compact: summary first, then tables of items needing attention.

## Local Citation Audit

For pasted text, `.qmd`, `.md`, `.docx`, or manuscript sections:

1. Extract parenthetical, narrative, and Quarto citations.
2. Check APA 7 mechanics:
   - parenthetical citations use `&`, not `and`
   - narrative citations use `and`, not `&`
   - 3 or more authors use `et al.`
   - multiple works in one parenthetical citation use semicolons
   - page references use `p.` or `pp.`
   - same-author same-year citations use suffixes such as `2020a`
3. Report line-level issues with suggested fixes.

## BibTeX Consistency Audit

When a `.bib` file is available:

1. Prefer `MANUSCRIPT-DEV-KIT/scripts/bibtex_parser.py` for parsing.
2. Compare cited keys against bibliography entries.
3. Flag:
   - cited keys missing from the `.bib`
   - unused bibliography entries
   - year mismatches
   - author/name mismatches
   - `et al.` usage inconsistent with author count
   - duplicate or ambiguous keys
4. For Quarto, check `@key`, `[@key]`, `[-@key]`, and multi-cite syntax such as `[@a; @b]`.

## Deep Verification

Use only when the user explicitly requests external verification.

Script locations:

- `MANUSCRIPT-DEV-KIT/scripts/verify_bibliography.py`
- `MANUSCRIPT-DEV-KIT/scripts/bibtex_parser.py`

Supported input:

- `.bib`
- `.docx` reference lists

Typical command pattern:

```powershell
python MANUSCRIPT-DEV-KIT/scripts/verify_bibliography.py path\to\references.bib -o path\to\verification --email user@example.edu
```

If the user did not provide an email, ask whether to use one for polite API headers or run without adding personal information. Never invent contact details.

Deep verification checks scholarly metadata against CrossRef, OpenAlex, Semantic Scholar, DataCite, PubMed, and DOI.org. It generates:

- `*_report_v2.csv`
- `*_for_R_v2.csv`
- `*_source_breakdown_v2.csv`
- `*_log_v2.txt`

Statuses to explain:

- `VERIFIED`: high-confidence match, usually supported by multiple sources
- `LIKELY_MATCH`: probable match with moderate confidence
- `PARTIAL_MATCH`: one source matches
- `LOW_CONFIDENCE`: weak match requiring manual review
- `NOT_FOUND`: no source found the item
- `ANCIENT_TEXT`: pre-1800 item skipped for modern database lookup

## Deep Verification Scope

- Spot check: verify only user-named entries by creating a temporary filtered `.bib`.
- Selected set: filter manually by user criteria such as no DOI, books, author, or year.
- Full run: verify the complete bibliography, preferably at pre-submission or after major reference changes.

The deployed script may not have native `--keys`, `--filter`, or Markdown output. If those flags are absent, create a temporary filtered `.bib` and run the existing script against that file.

## Report Format

Use this structure:

```markdown
# Citation and Bibliography Audit

## Summary
- Citations checked:
- Bibliography entries:
- Format issues:
- Missing keys:
- Unused entries:
- Deep verification: not run / run on N entries

## Must Fix
| Location | Issue | Suggested fix |
|---|---|---|

## Warnings
| Location | Issue | Why it matters |
|---|---|---|

## Deep Verification Evidence
| Entry | Status | Sources | Action |
|---|---|---|---|
```

If deep verification was not run, say so plainly and note that it requires explicit user approval because it queries external services.
