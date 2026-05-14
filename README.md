# CGPT Codex Skills

This repository is the shareable, Codex-owned collection of `cgpt-*` skills.
It is intended to keep Codex skills separate from Claude/Cowork skill sets while
making the Codex versions easy to review, improve, install, and contribute to.

## Creator and Maintainer

Created and maintained by **P. V. (Sundar) Balakrishnan**.

This collection grew out of practical academic, teaching, manuscript, document,
presentation, and software-delivery workflows. The goal is to keep useful Codex
skills in a public, versioned, contributor-friendly repository rather than as
one-off local files.

## Acknowledgments

Thanks to the many people who have shared Claude skills, agent workflows,
prompting patterns, and practical automation examples. Those shared materials
helped clarify what a reusable skill should include: clear triggers, scoped
instructions, bundled helper scripts when needed, and enough validation guidance
for another agent or contributor to improve the work.

This repository contains Codex-owned implementations. Claude/Cowork sources are
treated as references unless a file is explicitly bundled here with attribution
or local ownership notes.

## Try a Concrete Example

To see what a skill can produce, open the rendered flipcards demo:

- [Open the GitHub Repositories for Scholars flipcards as a web page](https://htmlpreview.github.io/?https://github.com/pvsundar/CGPT-CODEX-SKILLS/blob/main/cgpt-canvas-flipcards/examples/study-flipcards-github-repos-for-scholars.html)
- [View the source file on GitHub](https://github.com/pvsundar/CGPT-CODEX-SKILLS/blob/main/cgpt-canvas-flipcards/examples/study-flipcards-github-repos-for-scholars.html)
- [Read the sharing note](cgpt-canvas-flipcards/examples/github-repos-for-scholars-sharing-note.md)

GitHub's normal file view shows HTML as code. The rendered link above uses a
static preview service so nontechnical readers can experience the same file as
an interactive web page.

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
- Manuscript recovery, adversarial review, reviewer response, stats/citation audits, and render QA.
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

## License and Redistribution

Repository-original material is released under the MIT License; see
[LICENSE](LICENSE).

Bundled scripts and references are tracked in
[REDISTRIBUTION-REVIEW.md](REDISTRIBUTION-REVIEW.md). Contributors should update
that review whenever they add copied, adapted, generated, or third-party
materials.
