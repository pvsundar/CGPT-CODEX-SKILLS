---
name: cgpt-quarto-render-windows
description: Diagnose and harden Quarto render automation on Windows, especially from spawned PowerShell, Codex, Desktop Commander, scheduled tasks, Cowork handoffs, or CI. Use when quarto render fails because cmd/quarto/R is not on PATH, PATHEXT is stripped, artifacts are stale despite exit code 0, output paths are wrong, rBinaryPath/checkRBinary/cmd.exe spawn errors appear, or when creating reusable Windows render scripts for `.qmd` projects.
---

# CGPT Quarto Render Windows

Use this skill for Windows `.qmd` render failures caused by spawned-shell environment drift. Keep it separate from source-content debugging: if the failure is shell inheritance, stale output, or R discovery, fix the render lane before editing manuscript prose.

## Common Diagnosis

Treat these as environment problems until evidence says otherwise:

- `cmd` not found or Quarto cannot spawn `cmd.exe`.
- `quarto` works in RStudio but not from Codex or a scheduled script.
- `$env:PATHEXT` is `.CPL` only or lacks `.EXE;.CMD`.
- R path is pinned to an older version directory.
- Render exits 0 but the output file timestamp did not advance.
- Quarto logs mention `rBinaryPath`, `checkRBinary`, or `Failed to spawn 'CMD'`.

## Immediate Diagnostics

Run in the same spawned PowerShell context that will render:

```powershell
Get-Command cmd -ErrorAction SilentlyContinue
$env:PATHEXT
Get-Command quarto -ErrorAction SilentlyContinue
$env:PATH.Substring(0, [Math]::Min(200, $env:PATH.Length))
```

If any command resolution is missing, patch the render script with the reusable preamble before changing manuscript content.

## Attempt Ceiling

Do not loop indefinitely on render failures.

- Count a failed render, non-advancing output timestamp, or silent no-op as a strike.
- Stop after three strikes and hand the user a concise render-bailout report with the attempted commands, output paths, log path, and recommended next lane.
- If the failure is deterministic `rBinaryPath`, `checkRBinary`, or `Failed to spawn 'CMD'` from a sandboxed/Cowork child process, treat strike 1 as strike 3. A fourth shell variant will not fix that layer.

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

## RStudio Handoff

Use an RStudio Terminal handoff when the render must execute R/Python chunks and the current spawned context cannot provide a reliable Windows child process environment.

Triggers:

- `.qmd` has executable chunks that are not frozen and not `eval: false`.
- The project is under a Windows OneDrive path and the current render lane is Cowork/sandboxed or otherwise failing at R discovery.
- Logs contain `rBinaryPath`, `checkRBinary`, `quarto.js`, or `Failed to spawn 'CMD'`.
- Output mtime remains older than the source after an apparent success.

Handoff protocol:

1. Stop trying new shell wrappers.
2. Write a project-local `scripts/render-[stem].ps1` only if useful for repeatability.
3. Give the user a concrete RStudio Terminal command using forward slashes in paths.
4. After the user renders, verify the output `LastWriteTime` is newer than the source and run `cgpt-render-check`.

Template:

```powershell
cd "C:/Users/sundar/OneDrive - UW/Documents/GitHub/RESEARCH/[PROJECT]/[MANUSCRIPT_FOLDER]"
quarto render [FILE].qmd --to docx
```

Replace every bracketed placeholder before handing it to the user. Do not use angle-bracket placeholders in project-facing handoff text.

## Rules

- Do not treat exit code 0 as sufficient proof of a fresh render.
- Do not hardcode one R version when multiple versions may exist.
- Do not patch prose or citations while diagnosing shell environment failures.
- Keep render logs with the generated output when the project is delivery-grade.
- Do not declare a render clean until output mtime, file size, and format-specific checks have been verified.
