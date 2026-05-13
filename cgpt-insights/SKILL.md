---
name: cgpt-insights
description: Generate self-contained HTML activity reports from local Codex session evidence, project SESSION-LOG/HANDOFF/TASKS files, GitHub-root reports, or Claude/Cowork skill inventories. Use when the user asks for insights, usage report, activity report, weekly review, project status dashboard, what have I been working on, coding activity trends, or a polished REPORTS HTML summary.
---

# CGPT Insights

Use this skill to produce a grounded, self-contained report about recent work. The report should be evidence-backed, visually polished, and saved under the active workspace's `REPORTS` folder when one exists.

## Default Output

- HTML: `REPORTS/CGPT-INSIGHTS-YYYY-MM-DD.html` or a more specific `CGPT-<TOPIC>-REPORT-YYYY-MM-DD.html`.
- Chat summary: short bullets with the biggest findings and exact report path.

## Data Sources

Prefer local evidence in this order:

1. User-named files or folders.
2. Current repo files: `SESSION-LOG.md`, `HANDOFF.md`, `TASKS.md`, `STATUS-LOG.md`, `NEXT-CODEX-TASK.md`, `MEMORY.md`, `PROJECT_STATE.json`.
3. Git history and `git status` if the user asks for code/project activity.
4. `C:\Users\sundar\.codex\sessions` only when the task is specifically about Codex usage history and the files are readable.
5. Claude/Cowork sources under `CLAUDE-SKILLS-AGENTS-MEMORY` when the user asks to compare or port those workflows.

Do not fabricate tool counts, time spent, or quality scores. If a metric is unavailable, omit it or label it as unavailable.

## Report Structure

1. Header with title, date, scope, and data sources.
2. At-a-glance cards with only supported metrics.
3. Project or artifact table sorted by importance or recency.
4. What changed or what was produced.
5. Friction points and blockers.
6. Recommendations with concrete next actions.
7. Appendix with source files inspected.

## Visual Rules

- Make a self-contained HTML file with inline CSS.
- Use restrained UW styling where appropriate: purple `#4B2E83`, gold `#B7A57A`, neutral grays, and clear status colors.
- Use tables for inventories and cards for summary metrics.
- Do not rely on external CSS, fonts, scripts, or web assets.

## Workflow

1. Clarify scope only if the report target is ambiguous.
2. Inventory candidate data sources quickly before reading deeply.
3. Extract facts with file paths and dates.
4. Build the HTML report.
5. Verify the file exists and is non-empty.
6. If layout matters, open it with the Browser skill or otherwise report that visual QA was not run.

## Boundaries

- Keep the run read-only over source logs unless the user asks to update them.
- Save only the requested report artifact and avoid editing project files incidentally.
- If using memory-derived context, say so in the final answer and cite memory according to current Codex instructions.
