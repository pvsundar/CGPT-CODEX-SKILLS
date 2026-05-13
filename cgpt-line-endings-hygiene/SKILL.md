---
name: cgpt-line-endings-hygiene
description: Detect and prevent CRLF/LF line-ending problems in Windows-origin repositories and manuscripts. Use before editing files created by RStudio, Word-adjacent tooling, PowerShell, bash, Cowork, or Codex; when Git shows every line changed; when `.gitattributes`, `core.autocrlf`, NUL bytes, carriage returns, or noisy diffs appear; or before line-ending normalization work.
---

# CGPT Line Endings Hygiene

Use this skill to keep substantive edits separate from line-ending churn.

## Pre-Edit Check

Before editing a text file you did not create:

```powershell
Format-Hex -Path "path\to\file" -Count 256
git ls-files --eol -- "path/to/file"
```

Or, when a simple text read is enough:

```powershell
$bytes = [System.IO.File]::ReadAllBytes("path\to\file")
"CRLF count: " + ([regex]::Matches([Text.Encoding]::UTF8.GetString($bytes), "`r`n")).Count
"LF count: " + ([regex]::Matches([Text.Encoding]::UTF8.GetString($bytes), "(?<!`r)`n")).Count
```

If the file is consistently CRLF, preserve CRLF. If it is consistently LF, preserve LF.

## Decision Rule

- Existing consistent file: match its current endings.
- Newly created file: use LF unless the file type or project policy requires CRLF.
- Mixed endings: flag it. Normalize only if the user agrees or if normalization is the explicit task.
- Whole-file diff after a small edit: stop and inspect line endings before continuing.

## Normalization Discipline

When normalization is needed in a Git repo:

1. Create or confirm `.gitattributes`.
2. Commit line-ending normalization separately from content changes.
3. Then make the substantive edit in a separate commit or separate reported change.

Minimum `.gitattributes` baseline:

```gitattributes
* text=auto eol=lf
*.ps1 text eol=crlf
*.bat text eol=crlf
*.cmd text eol=crlf
*.docx binary
*.pptx binary
*.xlsx binary
*.pdf binary
```

## Post-Edit Integrity Check

After writing:

- Confirm the diff shows only intended content changes.
- Confirm file tail and size look plausible.
- If NUL bytes, missing tail content, or unexpected byte-count changes appear, treat it as file integrity damage rather than a line-ending issue.

## Rules

- Do not hide a substantive edit inside a whole-file normalization diff.
- Do not normalize delivery manuscripts or active review files midstream unless explicitly asked.
- Do not use `git add --renormalize .` casually in a dirty worktree.
- Pair with `cgpt-onedrive-git-safety` when the repo is under OneDrive or another sync root.
