---
name: cgpt-project-scaffold
description: Plan and create conservative research or teaching project folder scaffolds with tracking files, handoffs, and template-based starter structure. Use when the user asks to start a new manuscript project, teaching module, course folder, or project workspace.
---

# CGPT Project Scaffold

Use this skill to set up a new research or teaching workspace. Default to a proposal first; create folders and files only after the user approves the scaffold or clearly asks to execute it.

## Modes

- Research manuscript project: paper, revision, dataset, journal submission, manuscript workspace.
- Teaching project: course, module, slides, handouts, instructor notes, student materials, interactive tools.
- Active manuscript workspace: shallow working area for current QMD, rendered files, and submission artifacts.

## Guardrails

- Do not create folders or move files until the user approves the proposed layout unless the request explicitly says to create it now.
- Use `cgpt-onedrive-git-safety` when working inside synced Git folders.
- Keep new structures shallow and named clearly. Avoid burying active manuscript files multiple levels down.
- Do not register projects in Claude/Cowork-specific config. This is a Codex skill; create Codex-readable handoff/status files instead.
- Do not run `git init`, commit, push, or move existing files unless explicitly requested.
- If creating Markdown proposals or handoffs for the user, also create HTML copies under `REPORTS/CODEX` when the user needs readable reports.

## Research Scaffold

Recommended structure:

```text
<PROJECT>/
├── MEMORY.md
├── HANDOFF.md
├── SESSION-LOG.md
├── DECISIONS.md
├── quality_reports/
├── manuscript/
├── rendered/
├── data/
├── scripts/
└── references/
```

Use templates from `MANUSCRIPT-DEV-KIT/templates/` when available. Fill only known fields; leave explicit placeholders for missing information.

## Teaching Scaffold

For a course:

```text
<COURSE>/
├── HANDOFF.md
├── SESSION-LOG.md
├── COURSE-MATERIALS/
├── SLIDES/
├── HANDOUTS/
├── INSTRUCTOR-NOTES/
├── INTERACTIVE/
├── DATA/
├── SCRIPTS/
└── MEDIA/
```

For a topic module:

```text
<TOPIC>/
├── HANDOFF.md
├── SESSION-LOG.md
├── slides/
├── handouts/
├── instructor-notes/
├── interactive/
└── media/
```

## Workflow

1. Gather project name, type, title, purpose, target journal/course, collaborators, and immediate deliverables.
2. Propose the scaffold with exact paths.
3. Identify any source files to copy, not move.
4. Ask for approval when the request is not explicitly execution-oriented.
5. Create folders and starter files.
6. Verify file existence and report exact paths.

## Output

Report:

- created paths
- skipped optional fields
- next concrete task
- any source files copied
- any assumptions about naming, target journal, course, or folder depth
