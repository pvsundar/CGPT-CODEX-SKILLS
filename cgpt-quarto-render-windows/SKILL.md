---
name: cgpt-quarto-render-windows
description: Diagnose and harden Quarto render automation on Windows, especially from spawned PowerShell, Codex, Desktop Commander, scheduled tasks, or CI. Use when quarto render fails because cmd/quarto/R is not on PATH, PATHEXT is stripped, artifacts are stale despite exit code 0, output paths are wrong, or when creating reusable Windows render scripts for `.qmd` projects.
---

# CGPT Quarto Render Windows

Use this skill for Windows `.qmd` render failures caused by spawned-shell environment drift.

## Common Diagnosis

Treat these as environment problems until evidence says otherwise:

- `cmd` not found or Quarto cannot spawn `cmd.exe`.
- `quarto` works in RStudio but not from Codex or a scheduled script.
- `$env:PATHEXT` is `.CPL` only or lacks `.EXE;.CMD`.
- R path is pinned to an older version directory.
- Render exits 0 but the output file timestamp did not advance.

## Immediate Diagnostics

Run in the same spawned PowerShell context that will render:

```powershell
Get-Command cmd -ErrorAction SilentlyContinue
$env:PATHEXT
Get-Command quarto -ErrorAction SilentlyContinue
$env:PATH.Substring(0, [Math]::Min(200, $env:PATH.Length))
```

If any command resolution is missing, patch the render script with the reusable preamble before changing manuscript content.

## Reusable Preamble

Copy `assets/_render_preamble.ps1` into the project, usually next to render scripts or under a shared `scripts/` folder. Dot-source it at the top of every Windows render script:

```powershell
. "$PSScriptRoot\_render_preamble.ps1"
```

The preamble restores `PATHEXT`, critical Windows paths, Quarto path, latest installed R path, and `[Environment]::CurrentDirectory`.

## Render Script Pattern

1. Dot-source the preamble.
2. Capture the pre-render output `LastWriteTime`.
3. Run `quarto render` and tee stdout/stderr to a log.
4. Fail if `$LASTEXITCODE` is nonzero.
5. Fail if the expected output file does not exist or its timestamp did not advance.
6. Run `cgpt-render-check` on the output before delivery.

## Rules

- Do not treat exit code 0 as sufficient proof of a fresh render.
- Do not hardcode one R version when multiple versions may exist.
- Do not patch prose or citations while diagnosing shell environment failures.
- Keep render logs with the generated output when the project is delivery-grade.
