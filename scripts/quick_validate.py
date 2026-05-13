from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^cgpt-[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_front_matter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata


def skill_dirs() -> list[Path]:
    ignored = {".git", "scripts", "__pycache__"}
    return sorted(
        path
        for path in ROOT.iterdir()
        if path.is_dir() and path.name not in ignored and not path.name.startswith(".")
    )


def main() -> int:
    errors: list[str] = []
    checked = 0

    for skill_dir in skill_dirs():
        checked += 1
        skill_md = skill_dir / "SKILL.md"
        agent_yaml = skill_dir / "agents" / "openai.yaml"

        if not NAME_RE.match(skill_dir.name):
            errors.append(f"{skill_dir.name}: folder must be lowercase cgpt-* hyphen-case")

        if not skill_md.exists():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue

        text = skill_md.read_text(encoding="utf-8")
        metadata = parse_front_matter(text)
        if not metadata:
            errors.append(f"{skill_dir.name}: missing YAML-style front matter")
            continue

        if metadata.get("name") != skill_dir.name:
            errors.append(
                f"{skill_dir.name}: front matter name must match folder name "
                f"(found {metadata.get('name')!r})"
            )

        if not metadata.get("description"):
            errors.append(f"{skill_dir.name}: missing front matter description")

        if not agent_yaml.exists():
            errors.append(f"{skill_dir.name}: missing agents/openai.yaml")

    if checked == 0:
        errors.append("no skill folders found")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validation passed: {checked} skill folders checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
