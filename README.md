# CGPT Codex Skills

This repository is the shareable, Codex-owned collection of `cgpt-*` skills.
It is intended to keep Codex skills separate from Claude/Cowork skill sets while
making the Codex versions easy to review, improve, install, and contribute to.

## Layout

Each skill lives in its own lowercase hyphen-case folder:

```text
cgpt-example-skill/
  SKILL.md
  agents/openai.yaml
  scripts/        # optional helper scripts
  references/     # optional bundled references
  assets/         # optional reusable assets/templates
```

The repo root contains only repository metadata, validation helpers, and indexes.
Skill implementation files should stay inside their skill folder.

## Current Skill Set

See [SKILLS.md](SKILLS.md) for the current inventory.

Priority areas for this collection are:

- Academic DOCX authoring and journal-ready Word formatting.
- UW and UW Bothell slide deck creation.
- Manuscript recovery, reviewer response, stats/citation audits, and render QA.
- Codex operational utilities such as backup, closeout, Git safety, and routing.

## Validation

Run the lightweight structural validator before committing:

```powershell
python .\scripts\quick_validate.py
```

The validator checks that every skill folder has:

- A `SKILL.md` file.
- YAML-style front matter.
- A `name:` matching the folder name.
- A non-empty `description:`.
- An `agents/openai.yaml` file.

## Installation

For local Codex use, copy or sync an individual skill folder into:

```text
C:\Users\<you>\.codex\skills\
```

Keep this repository as the canonical shared source. Installed copies can drift
over time, so changes should be made here first and then installed.

## Contribution Rules

- Keep all Codex-created skills under the `cgpt-*` prefix.
- Use lowercase hyphen-case folder names.
- Keep Claude/Cowork source trees read-only references; do not vendor them here.
- Bundle runtime-critical helper scripts or references inside the relevant skill.
- Avoid secrets, credentials, private manuscript data, and user-specific paths.
- Run `python .\scripts\quick_validate.py` before opening a pull request.

## Publishing Note

This local repository is ready to connect to GitHub. Before making it public,
choose an explicit license and review bundled scripts/references for redistribution
rights.
