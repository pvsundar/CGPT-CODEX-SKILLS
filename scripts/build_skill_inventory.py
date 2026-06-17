from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^cgpt-[a-z0-9]+(?:-[a-z0-9]+)*$")
OUT_MD = ROOT / "CGPT-CODEX-SKILLS-MASTER-INVENTORY.md"
OUT_HTML = ROOT / "CGPT-CODEX-SKILLS-MASTER-INVENTORY.html"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_front_matter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    metadata: dict[str, str] = {}
    idx = 1
    while idx < len(lines):
        line = lines[idx]
        if line.strip() == "---":
            break
        if ":" not in line:
            idx += 1
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {">", "|"}:
            parts: list[str] = []
            idx += 1
            while idx < len(lines) and lines[idx].startswith((" ", "\t")):
                parts.append(lines[idx].strip())
                idx += 1
            metadata[key] = " ".join(part for part in parts if part)
            continue

        metadata[key] = value.strip().strip('"')
        idx += 1

    return metadata


def parse_agent_yaml(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if not stripped or stripped == "interface:" or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for child in path.rglob("*") if child.is_file())


def first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def skill_dirs() -> list[Path]:
    return sorted(
        path
        for path in ROOT.iterdir()
        if path.is_dir() and NAME_RE.match(path.name) and (path / "SKILL.md").exists()
    )


def skill_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for skill_dir in skill_dirs():
        skill_md = skill_dir / "SKILL.md"
        agent_yaml = skill_dir / "agents" / "openai.yaml"
        skill_text = read_text(skill_md)
        meta = parse_front_matter(skill_text)
        agent = parse_agent_yaml(agent_yaml)
        records.append(
            {
                "name": skill_dir.name,
                "heading": first_heading(skill_text) or skill_dir.name,
                "description": meta.get("description", ""),
                "display_name": agent.get("display_name", ""),
                "short_description": agent.get("short_description", ""),
                "default_prompt": agent.get("default_prompt", ""),
                "scripts": count_files(skill_dir / "scripts"),
                "references": count_files(skill_dir / "references"),
                "assets": count_files(skill_dir / "assets"),
                "examples": count_files(skill_dir / "examples"),
                "skill_path": str(skill_md.relative_to(ROOT)).replace("\\", "/"),
                "agent_path": str(agent_yaml.relative_to(ROOT)).replace("\\", "/")
                if agent_yaml.exists()
                else "",
            }
        )
    return records


def resource_summary(record: dict[str, object]) -> str:
    parts = []
    for key, label in (
        ("scripts", "scripts"),
        ("references", "refs"),
        ("assets", "assets"),
        ("examples", "examples"),
    ):
        count = int(record[key])
        if count:
            parts.append(f"{count} {label}")
    return ", ".join(parts) if parts else "none"


def render_markdown(records: list[dict[str, object]]) -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# CGPT Codex Skills Master Inventory",
        "",
        f"Generated: {generated}",
        f"Skill folders inventoried: {len(records)}",
        "",
        "This inventory is generated from live `cgpt-*` skill folders, each `SKILL.md` front matter, and `agents/openai.yaml` metadata.",
        "",
        "## Summary",
        "",
        "| Skill | Agent Display | Short Description | Invocation | Resources |",
        "| --- | --- | --- | --- | --- |",
    ]

    for record in records:
        lines.append(
            "| `{name}` | {display} | {short} | `${name}` | {resources} |".format(
                name=record["name"],
                display=record["display_name"] or "",
                short=record["short_description"] or "",
                resources=resource_summary(record),
            )
        )

    lines.extend(["", "## Details", ""])
    for record in records:
        lines.extend(
            [
                f"### `{record['name']}`",
                "",
                f"- Skill file: `{record['skill_path']}`",
                f"- Agent metadata: `{record['agent_path']}`",
                f"- Agent display: {record['display_name'] or 'Not set'}",
                f"- Agent short description: {record['short_description'] or 'Not set'}",
                f"- Invocation: `${record['name']}`",
                f"- Default prompt: {record['default_prompt'] or 'Not set'}",
                f"- Resources: {resource_summary(record)}",
                f"- Trigger description: {record['description'] or 'Not set'}",
                "",
            ]
        )

    lines.extend(
        [
            "## Regeneration",
            "",
            "Run:",
            "",
            "```powershell",
            "python .\\scripts\\build_skill_inventory.py",
            "```",
            "",
            "Then validate:",
            "",
            "```powershell",
            "python .\\scripts\\quick_validate.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def render_html(records: list[dict[str, object]]) -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    rows = []
    cards = []
    for record in records:
        rows.append(
            "<tr>"
            f"<td><code>{html.escape(str(record['name']))}</code></td>"
            f"<td>{html.escape(str(record['display_name'] or ''))}</td>"
            f"<td>{html.escape(str(record['short_description'] or ''))}</td>"
            f"<td><code>${html.escape(str(record['name']))}</code></td>"
            f"<td>{html.escape(resource_summary(record))}</td>"
            "</tr>"
        )
        cards.append(
            '<section class="skill-card">'
            f"<h2>{html.escape(str(record['name']))}</h2>"
            f"<p class=\"short\">{html.escape(str(record['short_description'] or ''))}</p>"
            "<dl>"
            f"<dt>Skill file</dt><dd><code>{html.escape(str(record['skill_path']))}</code></dd>"
            f"<dt>Agent metadata</dt><dd><code>{html.escape(str(record['agent_path']))}</code></dd>"
            f"<dt>Invocation</dt><dd><code>${html.escape(str(record['name']))}</code></dd>"
            f"<dt>Default prompt</dt><dd>{html.escape(str(record['default_prompt'] or 'Not set'))}</dd>"
            f"<dt>Resources</dt><dd>{html.escape(resource_summary(record))}</dd>"
            f"<dt>Trigger description</dt><dd>{html.escape(str(record['description'] or 'Not set'))}</dd>"
            "</dl>"
            "</section>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CGPT Codex Skills Master Inventory</title>
  <style>
    :root {{
      --ink: #17202a;
      --muted: #5d6d7e;
      --line: #d8dee9;
      --panel: #ffffff;
      --bg: #f6f8fb;
      --accent: #3b6ea8;
    }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: var(--ink);
      background: var(--bg);
      line-height: 1.45;
    }}
    header {{
      padding: 32px max(24px, 6vw) 20px;
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(28px, 4vw, 44px);
      letter-spacing: 0;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 24px;
    }}
    .meta {{
      color: var(--muted);
      margin: 0;
    }}
    .table-wrap {{
      overflow-x: auto;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 900px;
    }}
    th, td {{
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      font-size: 14px;
    }}
    th {{
      background: #eef3f8;
      color: #1f3b57;
      font-size: 13px;
      text-transform: uppercase;
    }}
    code {{
      font-family: Consolas, "Liberation Mono", monospace;
      font-size: 0.95em;
    }}
    .skill-card {{
      margin-top: 16px;
      padding: 18px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .skill-card h2 {{
      margin: 0 0 6px;
      color: var(--accent);
      font-size: 22px;
    }}
    .short {{
      margin: 0 0 12px;
      color: var(--muted);
    }}
    dl {{
      display: grid;
      grid-template-columns: minmax(150px, 220px) 1fr;
      gap: 8px 16px;
      margin: 0;
    }}
    dt {{
      font-weight: 700;
      color: #2c3e50;
    }}
    dd {{
      margin: 0;
    }}
    @media (max-width: 720px) {{
      dl {{
        grid-template-columns: 1fr;
      }}
      dt {{
        margin-top: 8px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>CGPT Codex Skills Master Inventory</h1>
    <p class="meta">Generated: {html.escape(generated)} | Skill folders inventoried: {len(records)}</p>
  </header>
  <main>
    <section class="table-wrap" aria-label="Skill summary table">
      <table>
        <thead>
          <tr>
            <th>Skill</th>
            <th>Agent Display</th>
            <th>Short Description</th>
            <th>Invocation</th>
            <th>Resources</th>
          </tr>
        </thead>
        <tbody>
          {'\n          '.join(rows)}
        </tbody>
      </table>
    </section>
    {'\n    '.join(cards)}
  </main>
</body>
</html>
"""


def main() -> int:
    records = skill_records()
    OUT_MD.write_text(render_markdown(records), encoding="utf-8", newline="\n")
    OUT_HTML.write_text(render_html(records), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_HTML}")
    print(f"Inventoried {len(records)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
