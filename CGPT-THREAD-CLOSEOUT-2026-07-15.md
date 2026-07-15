# CGPT Codex Skills Closeout - 2026-07-15

## Scope

Closed out the DOCX formatter bibliography-alignment maintenance pass from:

`C:\Users\sundar\OneDrive - UW\Documents\GitHub\CLAUDE-SKILLS-AGENTS-MEMORY\CGPT-CODEX-SKILLS`

The immediate bug was that `pvb_format_text.R` used Word alignment `jc = "both"` for bibliography styles, which makes references fully justified after Quarto/Pandoc DOCX rendering. The permanent active-setting fix is `jc = "left"` for both `Bibliography` and `Bibliography-JM`.

## Updated Active Formatter Locations

Canonical Codex repo source:

- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\CLAUDE-SKILLS-AGENTS-MEMORY\CGPT-CODEX-SKILLS\cgpt-jm-jmr-docx\scripts\pvb_format_text.R`

Installed Codex skill and reusable kits:

- `C:\Users\sundar\.codex\skills\cgpt-jm-jmr-docx\scripts\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\CLAUDE-SKILLS-AGENTS-MEMORY\analysis-kit\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\CLAUDE-SKILLS-AGENTS-MEMORY\MANUSCRIPT-DEV-KIT\scripts\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\CLAUDE-SKILLS-AGENTS-MEMORY\manuscript-kit\pvb_format_text.R`

Active project/tool copies:

- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\RESEARCH\BIODIV-AUTO-MANUSCRIPT\tools\docx-formatting\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\RESEARCH\DEPT-RANKINGS-GS-CITATIONS\PAPER-v7-JMR\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\RESEARCH\DEPT-RANKINGS-GS-CITATIONS\PAPER-v8-USNEWS-JMR\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\RESEARCH\MOVIES-CRIME-GITHUB\DOCX-FORMATTER\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\RESEARCH\MOVIES-CRIME-GITHUB\RESPONSES-TO-JOSH-ANALYSES\CC-SKILL-FORMAT-WORDDOCX\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\RESEARCH\PURRNIMA-MBR\manuscript-kit\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\RESEARCH\XIAODONG-JCC - 2026\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\TOOLS\FORMATTING-CODE\pvb_format_text.R`

## Memory Updated

Added:

- `C:\Users\sundar\.codex\memories\extensions\ad_hoc\notes\2026-07-15-docx-bibliography-left-align-formatter.md`

Carry-forward rule:

- Keep `STYLE_SPECS$Bibliography$jc` and `STYLE_SPECS[["Bibliography-JM"]]$jc` as `"left"`.
- Do not reintroduce `"both"` for reference styles unless a specific journal deliverable explicitly requires fully justified references.

## Validation

Validated on 2026-07-15:

- Full GitHub-tree search for `pvb_format_text.R`.
- Active copies scanned for bibliography-style `jc = "both"`; all active copies returned `BIB_LEFT`.
- Active copies parsed with:
  - `C:\Users\sundar\AppData\Local\Programs\R\R-4.5.2\bin\x64\Rscript.exe`
- Current repo was clean and synced before this closeout file was created:
  - Branch: `main`
  - HEAD: `1149be8`
  - `origin/main`: `1149be8`

R startup emitted locale warnings for `C.UTF-8`, but parse exit status was 0 for all active copies.

## Intentionally Not Updated

Historical archive/frozen copies still show the old justified reference style and were not edited:

- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\_ARCHIVE\FORMATTING-CODE-preupdate-2026-07-02\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\CLAUDE-SKILLS-AGENTS-MEMORY\archive\pvb-scripts-presync-20260615\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\RESEARCH\DEPT-RANKINGS-GS-CITATIONS\ZARCHIVE-FROZEN-MANUSCRIPTS\PAPER-v4-JMR\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\RESEARCH\DEPT-RANKINGS-GS-CITATIONS\ZARCHIVE-FROZEN-MANUSCRIPTS\PAPER-v5-3TIERS-JMR\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\RESEARCH\DEPT-RANKINGS-GS-CITATIONS\ZARCHIVE-FROZEN-MANUSCRIPTS\PAPER-v5-JMR\pvb_format_text.R`
- `C:\Users\sundar\OneDrive - UW\Documents\GitHub\RESEARCH\DEPT-RANKINGS-GS-CITATIONS\ZARCHIVE-FROZEN-MANUSCRIPTS\PAPER-v6-3TIERS-JMR\pvb_format_text.R`

## Residual Risk

- No live DOCX render was run in this pass; validation was static alignment scan plus R parse.
- Several active project copies were updated outside the `CGPT-CODEX-SKILLS` git repo. Their owning repos, if any, may need separate commits if those projects require clean git state.
- Archive/frozen copies retain the old behavior by design.

## Next Thread Launch Point

Start in:

`C:\Users\sundar\OneDrive - UW\Documents\GitHub\CLAUDE-SKILLS-AGENTS-MEMORY\CGPT-CODEX-SKILLS`

Read first:

1. `CGPT-THREAD-CLOSEOUT-2026-07-15.md`
2. `C:\Users\sundar\.codex\memories\extensions\ad_hoc\notes\2026-07-15-docx-bibliography-left-align-formatter.md`
3. `cgpt-jm-jmr-docx\scripts\pvb_format_text.R`

If the issue appears again, first check whether the render is using an archive/frozen formatter copy or a project-local formatter copy outside the active list above.
