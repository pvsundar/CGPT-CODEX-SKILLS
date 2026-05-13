# Contributing

This repo is for Codex-native `cgpt-*` skills.

## Add or Revise a Skill

1. Create or edit one skill folder at the repo root.
2. Keep the folder name lowercase hyphen-case and prefixed with `cgpt-`.
3. Put the main instructions in `SKILL.md`.
4. Put Codex agent metadata in `agents/openai.yaml`.
5. Keep helper scripts, templates, references, or assets inside the same skill folder.
6. Update `SKILLS.md`.
7. Run:

```powershell
python .\scripts\quick_validate.py
```

## Quality Bar

- The skill should have a clear trigger condition.
- The workflow should be specific enough for Codex to execute without guessing.
- Extra files should be loaded only when needed.
- Bundled scripts should be reusable and not depend on private local paths.
- Do not include credentials, private data, or manuscript contents unless explicitly intended for public release.

## Pull Requests

Good pull requests should include:

- A short description of the skill change.
- Any new or changed helper scripts.
- The validator result.
- Notes about dependencies, licensing, or redistribution concerns.

## Boundaries

Claude/Cowork skill sets may be used as reference material when allowed, but this
repo should contain Codex-owned skill implementations only.
