import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-").lower()
    return slug or "agent-report"


def read_report(args: argparse.Namespace) -> str:
    if args.input:
        return Path(args.input).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("Provide --input or pipe report text on stdin.")


def frontmatter_value(value: str) -> str:
    return value.replace("\r", " ").replace("\n", " ").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Persist agent or verifier return text as a project-local Markdown report.")
    parser.add_argument("--project", default=".", help="Project root where archive/reports should be created")
    parser.add_argument("--session", required=True, help="Short session or task label")
    parser.add_argument("--agent", required=True, help="Agent role, such as verifier, reviewer, explorer, or worker")
    parser.add_argument("--invocation", required=True, help="One-line summary of the supervisor prompt")
    parser.add_argument("--inputs", default="n/a", help="Files or task context used by the agent")
    parser.add_argument("--verdict", default="n/a", choices=["pass", "fail", "mixed", "n/a"], help="Agent verdict")
    parser.add_argument("--input", help="Path to a text or Markdown file containing the report; stdin is used if omitted")
    parser.add_argument("--timestamp", help="Override timestamp as YYYY-MM-DD_HHMM")
    args = parser.parse_args()

    report = read_report(args).strip()
    if not report:
        raise SystemExit("Report text is empty; refusing to create a placeholder report.")

    now = datetime.now()
    stamp = args.timestamp or now.strftime("%Y-%m-%d_%H%M")
    human_stamp = now.strftime("%Y-%m-%d %H:%M local")
    session_slug = slugify(args.session)
    agent_slug = slugify(args.agent)
    reports_dir = Path(args.project).resolve() / "archive" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    output = reports_dir / f"{session_slug}_{agent_slug}_{stamp}.md"

    title = f"{args.agent} return - {args.session} - {stamp}"
    content = "\n".join(
        [
            "---",
            f"agent: {frontmatter_value(args.agent)}",
            f"session: {frontmatter_value(args.session)}",
            f"saved: {human_stamp}",
            f"supervisor_invocation: {frontmatter_value(args.invocation)}",
            f"inputs: {frontmatter_value(args.inputs)}",
            f"verdict: {args.verdict}",
            "---",
            "",
            f"# {title}",
            "",
            report,
            "",
        ]
    )
    output.write_text(content, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
