# Skill Inventory

This index lists the Codex-owned skills currently staged in this repository.

| Skill | Purpose |
| --- | --- |
| `cgpt-academic-docx-authoring` | Create, edit, structure, and verify academic Word DOCX artifacts. |
| `cgpt-academic-proofreader` | Report-only academic proofreading for grammar, style, argument flow, citations, statistics, and Quarto readiness. |
| `cgpt-adversarial-reviewer` | Produce report-only skeptical Reviewer 2 reviews and empirical audit findings for academic work. |
| `cgpt-agent-report-persistence` | Save subagent, verifier, reviewer, synthesizer, or audit reports as durable files. |
| `cgpt-author-reviser` | Execute approved academic manuscript revisions from referee reports or revision plans. |
| `cgpt-backup` | Create timestamped backups before edits, formatting, bulk replacement, or risky automation. |
| `cgpt-canvas-flipcards` | Create self-contained HTML study flipcards and Canvas LMS embed instructions. |
| `cgpt-census-api` | Query, plan, or generate workflows for U.S. Census Bureau data. |
| `cgpt-citation-bib-audit` | Audit APA citations, BibTeX consistency, Quarto citations, and bibliography verification. |
| `cgpt-data-viz-auditor` | Audit figures, charts, maps, and plotting code for accessibility and journal readiness. |
| `cgpt-insights` | Generate self-contained HTML activity reports from local Codex session evidence. |
| `cgpt-jm-jmr-docx` | Convert, format, post-process, and verify JM/JMR and APA-style Word manuscripts. |
| `cgpt-line-endings-hygiene` | Detect and prevent CRLF/LF line-ending churn in Windows-origin work. |
| `cgpt-manuscript-recovery` | Recover academic manuscript status and produce durable recovery maps. |
| `cgpt-netlify-deploy` | Prepare, deploy, and verify Vite or React single-page apps on Netlify. |
| `cgpt-onedrive-git-safety` | Work safely with Git repositories stored under OneDrive or other synced folders. |
| `cgpt-presentation-prep` | Verify claims, numbers, figures, tables, and visual assets before research deck creation. |
| `cgpt-project-scaffold` | Plan and create conservative research or teaching project folder scaffolds. |
| `cgpt-quarto-debugger` | Diagnose and fix Quarto source problems such as YAML, citations, includes, and filters. |
| `cgpt-quarto-render-windows` | Diagnose and harden Quarto render automation on Windows. |
| `cgpt-r-debugger` | Debug, profile, and test R scripts, functions, Quarto chunks, and data pipelines. |
| `cgpt-render-check` | Validate rendered documents, decks, PDFs, HTML, Markdown, and generated reports. |
| `cgpt-reviewer-response` | Draft, revise, audit, and package academic response-to-reviewers materials. |
| `cgpt-stats-audit` | Perform report-only statistical audits of manuscripts against source data and figures. |
| `cgpt-thread-closeout` | Close out Codex threads with durable handoff notes and continuation instructions. |
| `cgpt-tool-routing-lessons` | Apply Codex-native routing lessons for filesystem, connector, sandbox, and tool choice issues. |
| `cgpt-uw-pptx-deck` | Build, rebuild, polish, audit, render, or export UW and UW Bothell PowerPoint decks. |

## Maintenance

When a skill is added, renamed, or materially changed:

1. Update this file.
2. Keep the folder name, `SKILL.md` front matter `name:`, and agent prompt aligned.
3. Run `python .\scripts\quick_validate.py`.
