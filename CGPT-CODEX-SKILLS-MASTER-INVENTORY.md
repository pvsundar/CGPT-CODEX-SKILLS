# CGPT Codex Skills Master Inventory

Generated: 2026-06-17 16:04
Skill folders inventoried: 29

This inventory is generated from live `cgpt-*` skill folders, each `SKILL.md` front matter, and `agents/openai.yaml` metadata.

## Summary

| Skill | Agent Display | Short Description | Invocation | Resources |
| --- | --- | --- | --- | --- |
| `cgpt-academic-docx-authoring` | CGPT Academic DOCX Authoring | Create and edit academic Word deliverables. | `$cgpt-academic-docx-authoring` | none |
| `cgpt-academic-proofreader` | CGPT Academic Proofreader | Produce report-only academic manuscript proofreading and readiness checks. | `$cgpt-academic-proofreader` | none |
| `cgpt-adversarial-reviewer` | CGPT Adversarial Reviewer | Simulate a skeptical Reviewer 2 for academic manuscripts. | `$cgpt-adversarial-reviewer` | none |
| `cgpt-agent-report-persistence` | CGPT Agent Report Persistence | Persist subagent reports before closeout | `$cgpt-agent-report-persistence` | 1 scripts |
| `cgpt-author-reviser` | CGPT Author Reviser | Apply approved reviewer-driven manuscript revisions. | `$cgpt-author-reviser` | none |
| `cgpt-backup` | CGPT Backup | Create timestamped backups before risky edits. | `$cgpt-backup` | 1 scripts |
| `cgpt-canvas-flipcards` | CGPT Canvas Flipcards | Create interactive HTML flipcards for Canvas. | `$cgpt-canvas-flipcards` | 6 examples |
| `cgpt-census-api` | CGPT Census API | Plan and query U.S. Census data workflows. | `$cgpt-census-api` | none |
| `cgpt-citation-bib-audit` | CGPT Citation Bib Audit | Audit APA citations, BibTeX consistency, and user-triggered deep reference verification. | `$cgpt-citation-bib-audit` | none |
| `cgpt-data-viz-auditor` | CGPT Data Viz Auditor | Audit figures, maps, labels, color, accessibility, and journal readiness. | `$cgpt-data-viz-auditor` | none |
| `cgpt-insights` | CGPT Insights | Generate local Codex or project activity insights reports. | `$cgpt-insights` | none |
| `cgpt-interactive-html-export-hardening` | CGPT Interactive HTML Hardening | Harden editable single-file HTML export/import flows. | `$cgpt-interactive-html-export-hardening` | none |
| `cgpt-jm-jmr-docx` | CGPT JM/JMR DOCX | Format Word manuscripts with the PVB/JM/JMR DOCX pipeline. | `$cgpt-jm-jmr-docx` | 3 scripts, 2 refs |
| `cgpt-line-endings-hygiene` | CGPT Line Endings Hygiene | Avoid noisy CRLF/LF diffs | `$cgpt-line-endings-hygiene` | none |
| `cgpt-manuscript-recovery` | CGPT Manuscript Recovery | Recover manuscript status and next actions | `$cgpt-manuscript-recovery` | none |
| `cgpt-netlify-deploy` | CGPT Netlify Deploy | Deploy React SPAs on Netlify safely. | `$cgpt-netlify-deploy` | none |
| `cgpt-onedrive-git-safety` | CGPT OneDrive Git Safety | Use Git safely in synced Windows repos | `$cgpt-onedrive-git-safety` | none |
| `cgpt-portfolio-dashboard-interactive` | CGPT Portfolio Dashboard Interactive | Build the editable PVB portfolio dashboard with v4 taxonomy. | `$cgpt-portfolio-dashboard-interactive` | 1 scripts |
| `cgpt-presentation-prep` | CGPT Presentation Prep | Verify manuscript facts and visual assets before deck generation. | `$cgpt-presentation-prep` | none |
| `cgpt-project-scaffold` | CGPT Project Scaffold | Plan and create research or teaching project workspaces. | `$cgpt-project-scaffold` | none |
| `cgpt-quarto-debugger` | CGPT Quarto Debugger | Fix Quarto source, YAML, citations, crossrefs, and includes. | `$cgpt-quarto-debugger` | none |
| `cgpt-quarto-render-windows` | CGPT Quarto Render Windows | Harden and verify Quarto renders on Windows. | `$cgpt-quarto-render-windows` | 1 assets |
| `cgpt-r-debugger` | CGPT R Debugger | Run reproducible R debugging, profiling, and edge-case tests. | `$cgpt-r-debugger` | none |
| `cgpt-render-check` | CGPT Render Check | Validate rendered documents, decks, PDFs, and HTML outputs. | `$cgpt-render-check` | 1 scripts |
| `cgpt-reviewer-response` | CGPT Reviewer Response | Draft and audit response-to-reviewers letters. | `$cgpt-reviewer-response` | none |
| `cgpt-stats-audit` | CGPT Stats Audit | Run report-only statistical audits against manuscript numbers and source data. | `$cgpt-stats-audit` | none |
| `cgpt-thread-closeout` | CGPT Thread Closeout | Create durable closeout and handoff artifacts. | `$cgpt-thread-closeout` | none |
| `cgpt-tool-routing-lessons` | CGPT Tool Routing Lessons | Choose safe Codex file and connector routing. | `$cgpt-tool-routing-lessons` | none |
| `cgpt-uw-pptx-deck` | CGPT UW PPTX Deck | Build and verify UW-branded PowerPoint decks. | `$cgpt-uw-pptx-deck` | none |

## Details

### `cgpt-academic-docx-authoring`

- Skill file: `cgpt-academic-docx-authoring/SKILL.md`
- Agent metadata: `cgpt-academic-docx-authoring/agents/openai.yaml`
- Agent display: CGPT Academic DOCX Authoring
- Agent short description: Create and edit academic Word deliverables.
- Invocation: `$cgpt-academic-docx-authoring`
- Default prompt: Create or revise this academic DOCX deliverable and verify the output.
- Resources: none
- Trigger description: Create, edit, structure, and verify academic Word DOCX artifacts such as manuscript drafts, cover letters, response letters, appendices, and supplementary files. Use when the user asks to author a new academic .docx, revise a Word manuscript, insert tables or figures, convert polished academic Markdown into DOCX, or prepare a journal-facing Word deliverable that is not primarily a JM/JMR formatter run.

### `cgpt-academic-proofreader`

- Skill file: `cgpt-academic-proofreader/SKILL.md`
- Agent metadata: `cgpt-academic-proofreader/agents/openai.yaml`
- Agent display: CGPT Academic Proofreader
- Agent short description: Produce report-only academic manuscript proofreading and readiness checks.
- Invocation: `$cgpt-academic-proofreader`
- Default prompt: Proofread this academic manuscript and report prioritized issues with proposed fixes, without editing source files.
- Resources: none
- Trigger description: Report-only academic manuscript proofreading for grammar, journal style, argument flow, terminology, citation mechanics, statistical reporting, and Quarto cross-reference readiness; use before sharing, submission, or after manuscript revisions.

### `cgpt-adversarial-reviewer`

- Skill file: `cgpt-adversarial-reviewer/SKILL.md`
- Agent metadata: `cgpt-adversarial-reviewer/agents/openai.yaml`
- Agent display: CGPT Adversarial Reviewer
- Agent short description: Simulate a skeptical Reviewer 2 for academic manuscripts.
- Invocation: `$cgpt-adversarial-reviewer`
- Default prompt: Run a report-only adversarial Reviewer 2 review of this academic work, with major issues, minor issues, empirical audit findings where relevant, and the highest-value revision.
- Resources: none
- Trigger description: Produce report-only adversarial academic manuscript reviews modeled on a skeptical Reviewer 2. Use for pre-submission stress tests, hostile-but-constructive referee simulation, empirical research audits, contribution/methodology/framing critiques, or quick devil's-advocate challenges before revision.

### `cgpt-agent-report-persistence`

- Skill file: `cgpt-agent-report-persistence/SKILL.md`
- Agent metadata: `cgpt-agent-report-persistence/agents/openai.yaml`
- Agent display: CGPT Agent Report Persistence
- Agent short description: Persist subagent reports before closeout
- Invocation: `$cgpt-agent-report-persistence`
- Default prompt: Use $cgpt-agent-report-persistence to save the verifier return before closing this thread.
- Resources: 1 scripts
- Trigger description: Save subagent, verifier, reviewer, synthesizer, or audit return text as durable files before closeout. Use when Codex delegates work to subagents, receives a verifier/proofreader/stats/reviewer report, references prior-thread output, closes a sub-session, or creates a handoff that depends on agent analysis that would otherwise live only in chat.

### `cgpt-author-reviser`

- Skill file: `cgpt-author-reviser/SKILL.md`
- Agent metadata: `cgpt-author-reviser/agents/openai.yaml`
- Agent display: CGPT Author Reviser
- Agent short description: Apply approved reviewer-driven manuscript revisions.
- Invocation: `$cgpt-author-reviser`
- Default prompt: Build a revision plan and edit preview from this reviewer feedback before applying manuscript changes.
- Resources: none
- Trigger description: Execute approved academic manuscript revisions from referee reports, decision letters, or user-approved revision plans. Use when the user wants Codex to apply reviewer-driven changes to manuscript files, but only after backup, triage, edit preview, and explicit approval.

### `cgpt-backup`

- Skill file: `cgpt-backup/SKILL.md`
- Agent metadata: `cgpt-backup/agents/openai.yaml`
- Agent display: CGPT Backup
- Agent short description: Create timestamped backups before risky edits.
- Invocation: `$cgpt-backup`
- Default prompt: Back up the specified file or folder before continuing.
- Resources: 1 scripts
- Trigger description: Create timestamped backup copies of important files or folders before editing, formatting, bulk replacement, risky automation, or user-requested backup work. Use when the user says backup, create a checkpoint, copy before editing, preserve the current version, or when a MEMORY/HANDOFF note marks a file as frozen or critical.

### `cgpt-canvas-flipcards`

- Skill file: `cgpt-canvas-flipcards/SKILL.md`
- Agent metadata: `cgpt-canvas-flipcards/agents/openai.yaml`
- Agent display: CGPT Canvas Flipcards
- Agent short description: Create interactive HTML flipcards for Canvas.
- Invocation: `$cgpt-canvas-flipcards`
- Default prompt: Create a self-contained flipcard HTML study tool and Canvas embed instructions for this topic.
- Resources: 6 examples
- Trigger description: Create self-contained HTML study flipcards and Canvas LMS embed instructions for teaching modules. Use when the user asks for flip cards, study cards, interactive HTML review tools, Canvas iframe embeds, or troubleshooting Canvas pages that strip JavaScript.

### `cgpt-census-api`

- Skill file: `cgpt-census-api/SKILL.md`
- Agent metadata: `cgpt-census-api/agents/openai.yaml`
- Agent display: CGPT Census API
- Agent short description: Plan and query U.S. Census data workflows.
- Invocation: `$cgpt-census-api`
- Default prompt: Build a Census data query or reproducible R/Python workflow for this geography and variable set.
- Resources: none
- Trigger description: Query, plan, or generate R/Python/API workflows for U.S. Census Bureau data such as ACS, decennial census, population estimates, County Business Patterns, FIPS codes, geographies, variables, and demographic tables. Use when the user asks for Census data or public demographic/economic statistics.

### `cgpt-citation-bib-audit`

- Skill file: `cgpt-citation-bib-audit/SKILL.md`
- Agent metadata: `cgpt-citation-bib-audit/agents/openai.yaml`
- Agent display: CGPT Citation Bib Audit
- Agent short description: Audit APA citations, BibTeX consistency, and user-triggered deep reference verification.
- Invocation: `$cgpt-citation-bib-audit`
- Default prompt: Audit this manuscript's citations and bibliography, then report issues without editing source files.
- Resources: none
- Trigger description: Compact Codex skill for APA citation checks, BibTeX consistency audits, Quarto citation audits, and user-triggered deep bibliography verification with source-cited results.

### `cgpt-data-viz-auditor`

- Skill file: `cgpt-data-viz-auditor/SKILL.md`
- Agent metadata: `cgpt-data-viz-auditor/agents/openai.yaml`
- Agent display: CGPT Data Viz Auditor
- Agent short description: Audit figures, maps, labels, color, accessibility, and journal readiness.
- Invocation: `$cgpt-data-viz-auditor`
- Default prompt: Use $cgpt-data-viz-auditor to audit this figure or plotting code and identify concrete fixes.
- Resources: none
- Trigger description: Audit statistical figures, charts, maps, and plotting code for accessibility, labels, color, export quality, and academic journal readiness. Use when reviewing ggplot2, matplotlib, rendered figures, manuscript graphics, maps, or multi-figure submissions before delivery or journal submission.

### `cgpt-insights`

- Skill file: `cgpt-insights/SKILL.md`
- Agent metadata: `cgpt-insights/agents/openai.yaml`
- Agent display: CGPT Insights
- Agent short description: Generate local Codex or project activity insights reports.
- Invocation: `$cgpt-insights`
- Default prompt: Create an insights report for recent local project activity.
- Resources: none
- Trigger description: Generate self-contained HTML activity reports from local Codex session evidence, project SESSION-LOG/HANDOFF/TASKS files, GitHub-root reports, or Claude/Cowork skill inventories. Use when the user asks for insights, usage report, activity report, weekly review, project status dashboard, what have I been working on, coding activity trends, or a polished REPORTS HTML summary.

### `cgpt-interactive-html-export-hardening`

- Skill file: `cgpt-interactive-html-export-hardening/SKILL.md`
- Agent metadata: `cgpt-interactive-html-export-hardening/agents/openai.yaml`
- Agent display: CGPT Interactive HTML Hardening
- Agent short description: Harden editable single-file HTML export/import flows.
- Invocation: `$cgpt-interactive-html-export-hardening`
- Default prompt: Harden this interactive HTML artifact so JSON and exported HTML preserve user edits.
- Resources: none
- Trigger description: Harden self-contained editable HTML artifacts so export/import, localStorage, controls, and re-opened HTML round trips preserve user edits without JavaScript parse failures.

### `cgpt-jm-jmr-docx`

- Skill file: `cgpt-jm-jmr-docx/SKILL.md`
- Agent metadata: `cgpt-jm-jmr-docx/agents/openai.yaml`
- Agent display: CGPT JM/JMR DOCX
- Agent short description: Format Word manuscripts with the PVB/JM/JMR DOCX pipeline.
- Invocation: `$cgpt-jm-jmr-docx`
- Default prompt: Run the current PVB/JM/JMR DOCX formatting pipeline and verify the output.
- Resources: 3 scripts, 2 refs
- Trigger description: Convert, format, post-process, and verify Word DOCX manuscripts for Journal of Marketing, Journal of Marketing Research, APA-style management/marketing submissions, and PVB academic manuscript style. Use when the user asks to convert a Word docx into JM or JMR style, format a manuscript for submission, fix APA-style tables or references, run the PVB DOCX formatter, clean a Quarto/Pandoc-rendered DOCX, style bibliography entries, or prepare a submission-ready Word file.

### `cgpt-line-endings-hygiene`

- Skill file: `cgpt-line-endings-hygiene/SKILL.md`
- Agent metadata: `cgpt-line-endings-hygiene/agents/openai.yaml`
- Agent display: CGPT Line Endings Hygiene
- Agent short description: Avoid noisy CRLF/LF diffs
- Invocation: `$cgpt-line-endings-hygiene`
- Default prompt: Use $cgpt-line-endings-hygiene before editing this Windows-origin file.
- Resources: none
- Trigger description: Detect and prevent CRLF/LF line-ending problems in Windows-origin repositories and manuscripts. Use before editing files created by RStudio, Word-adjacent tooling, PowerShell, bash, Cowork, or Codex; when Git shows every line changed; when `.gitattributes`, `core.autocrlf`, NUL bytes, carriage returns, or noisy diffs appear; or before line-ending normalization work.

### `cgpt-manuscript-recovery`

- Skill file: `cgpt-manuscript-recovery/SKILL.md`
- Agent metadata: `cgpt-manuscript-recovery/agents/openai.yaml`
- Agent display: CGPT Manuscript Recovery
- Agent short description: Recover manuscript status and next actions
- Invocation: `$cgpt-manuscript-recovery`
- Default prompt: Use $cgpt-manuscript-recovery to inspect this manuscript folder and produce a recovery map.
- Resources: none
- Trigger description: Inspect an academic manuscript or revision folder after a long break and produce a durable recovery map. Use when the user asks to recover manuscript status, find the live version, identify backups/submission files/reviewer letters/Turnitin reports, resume a revision, reconstruct next actions, or create a recovery handoff before editing a manuscript.

### `cgpt-netlify-deploy`

- Skill file: `cgpt-netlify-deploy/SKILL.md`
- Agent metadata: `cgpt-netlify-deploy/agents/openai.yaml`
- Agent display: CGPT Netlify Deploy
- Agent short description: Deploy React SPAs on Netlify safely.
- Invocation: `$cgpt-netlify-deploy`
- Default prompt: Prepare and verify this app for Netlify deployment.
- Resources: none
- Trigger description: Prepare, deploy, and verify Vite or React single-page apps on Netlify. Use when the user asks to deploy to Netlify, fix a Netlify build, add SPA routing redirects, configure VITE environment variables, link GitHub to Netlify, or diagnose deployment failures such as vite not found, blank screen, cached deploys, or direct-route 404s.

### `cgpt-onedrive-git-safety`

- Skill file: `cgpt-onedrive-git-safety/SKILL.md`
- Agent metadata: `cgpt-onedrive-git-safety/agents/openai.yaml`
- Agent display: CGPT OneDrive Git Safety
- Agent short description: Use Git safely in synced Windows repos
- Invocation: `$cgpt-onedrive-git-safety`
- Default prompt: Use $cgpt-onedrive-git-safety before changing Git state in this OneDrive repository.
- Resources: none
- Trigger description: Work safely with Git repositories stored under OneDrive, Google Drive, Dropbox, iCloud Drive, or other synced Windows folders. Use before git status/add/commit/diff/reset/checkout in synced repos, when handling dirty worktrees, no-touch sibling repos, line-ending phantoms, stuck index.lock files, or closeout claims about tests/builds on synced filesystems.

### `cgpt-portfolio-dashboard-interactive`

- Skill file: `cgpt-portfolio-dashboard-interactive/SKILL.md`
- Agent metadata: `cgpt-portfolio-dashboard-interactive/agents/openai.yaml`
- Agent display: CGPT Portfolio Dashboard Interactive
- Agent short description: Build the editable PVB portfolio dashboard with v4 taxonomy.
- Invocation: `$cgpt-portfolio-dashboard-interactive`
- Default prompt: Build or revise the interactive PVB portfolio dashboard with JSON-canonical state and hardened export.
- Resources: 1 scripts
- Trigger description: Build and maintain the editable PVB research portfolio dashboard with v4 operating-state taxonomy, JSON-canonical state, hardened export/import, autosave, and validation.

### `cgpt-presentation-prep`

- Skill file: `cgpt-presentation-prep/SKILL.md`
- Agent metadata: `cgpt-presentation-prep/agents/openai.yaml`
- Agent display: CGPT Presentation Prep
- Agent short description: Verify manuscript facts and visual assets before deck generation.
- Invocation: `$cgpt-presentation-prep`
- Default prompt: Extract and verify the source-backed facts, numbers, and visuals needed before building this presentation.
- Resources: none
- Trigger description: Extract and verify ground-truth claims, numbers, figures, tables, and visual assets before building a research presentation. Use before manuscript-to-deck work, academic talks, slide-number checks, presentation prep, source verification, figure audits, and requests to confirm that slide values match the paper or report.

### `cgpt-project-scaffold`

- Skill file: `cgpt-project-scaffold/SKILL.md`
- Agent metadata: `cgpt-project-scaffold/agents/openai.yaml`
- Agent display: CGPT Project Scaffold
- Agent short description: Plan and create research or teaching project workspaces.
- Invocation: `$cgpt-project-scaffold`
- Default prompt: Propose a conservative project scaffold first, then create it only after approval.
- Resources: none
- Trigger description: Plan and create conservative research or teaching project folder scaffolds with tracking files, handoffs, and template-based starter structure. Use when the user asks to start a new manuscript project, teaching module, course folder, or project workspace.

### `cgpt-quarto-debugger`

- Skill file: `cgpt-quarto-debugger/SKILL.md`
- Agent metadata: `cgpt-quarto-debugger/agents/openai.yaml`
- Agent display: CGPT Quarto Debugger
- Agent short description: Fix Quarto source, YAML, citations, crossrefs, and includes.
- Invocation: `$cgpt-quarto-debugger`
- Default prompt: Use $cgpt-quarto-debugger to diagnose this Quarto source/render failure and verify the fix.
- Resources: none
- Trigger description: Diagnose and fix Quarto source problems in `.qmd` projects, especially YAML/front matter, citations, cross-references, includes, filters, and Pandoc/engine errors. Use when Quarto renders fail, output shows unresolved references, citations do not resolve, includes are missing, or a user shares a Quarto error and asks what it means.

### `cgpt-quarto-render-windows`

- Skill file: `cgpt-quarto-render-windows/SKILL.md`
- Agent metadata: `cgpt-quarto-render-windows/agents/openai.yaml`
- Agent display: CGPT Quarto Render Windows
- Agent short description: Harden and verify Quarto renders on Windows.
- Invocation: `$cgpt-quarto-render-windows`
- Default prompt: Use $cgpt-quarto-render-windows to diagnose this Windows Quarto render, stop after deterministic failures, and verify output freshness.
- Resources: 1 assets
- Trigger description: Diagnose and harden Quarto render automation on Windows, especially from spawned PowerShell, Codex, Desktop Commander, scheduled tasks, Cowork handoffs, or CI. Use when quarto render fails because cmd/quarto/R is not on PATH, PATHEXT is stripped, artifacts are stale despite exit code 0, output paths are wrong, rBinaryPath/checkRBinary/cmd.exe spawn errors appear, or when creating reusable Windows render scripts for `.qmd` projects.

### `cgpt-r-debugger`

- Skill file: `cgpt-r-debugger/SKILL.md`
- Agent metadata: `cgpt-r-debugger/agents/openai.yaml`
- Agent display: CGPT R Debugger
- Agent short description: Run reproducible R debugging, profiling, and edge-case tests.
- Invocation: `$cgpt-r-debugger`
- Default prompt: Debug this R code with a reproducible harness, profile bottlenecks if needed, and report the evidence before editing files.
- Resources: none
- Trigger description: Reproducible R debugging, profiling, and edge-case testing for scripts, functions, Quarto analysis chunks, and data pipelines; use when the user asks to diagnose incorrect R output, slow code, brittle behavior, vectorization options, memory use, or runtime failures.

### `cgpt-render-check`

- Skill file: `cgpt-render-check/SKILL.md`
- Agent metadata: `cgpt-render-check/agents/openai.yaml`
- Agent display: CGPT Render Check
- Agent short description: Validate rendered documents, decks, PDFs, and HTML outputs.
- Invocation: `$cgpt-render-check`
- Default prompt: Validate this rendered output and report pass, warning, and failure checks.
- Resources: 1 scripts
- Trigger description: Validate rendered documents and presentation outputs after Quarto, Pandoc, python-pptx, document export, HTML generation, PDF export, or report build work. Use when the user asks to check, validate, QA, inspect, smoke test, or deliver a rendered DOCX, PPTX, PDF, HTML, Markdown, or generated report.

### `cgpt-reviewer-response`

- Skill file: `cgpt-reviewer-response/SKILL.md`
- Agent metadata: `cgpt-reviewer-response/agents/openai.yaml`
- Agent display: CGPT Reviewer Response
- Agent short description: Draft and audit response-to-reviewers letters.
- Invocation: `$cgpt-reviewer-response`
- Default prompt: Draft a response-to-reviewers letter from these comments and revision notes.
- Resources: none
- Trigger description: Draft, revise, audit, and package academic response-to-reviewers letters, editor responses, revision memos, and R&R correspondence. Use when the user shares peer-review comments, decision letters, reviewer feedback, associate editor guidance, or asks for a response matrix, rebuttal, revision strategy, cover response, or journal-facing revision correspondence.

### `cgpt-stats-audit`

- Skill file: `cgpt-stats-audit/SKILL.md`
- Agent metadata: `cgpt-stats-audit/agents/openai.yaml`
- Agent display: CGPT Stats Audit
- Agent short description: Run report-only statistical audits against manuscript numbers and source data.
- Invocation: `$cgpt-stats-audit`
- Default prompt: Audit this manuscript's reported statistics against source data and report mismatches without editing manuscripts.
- Resources: none
- Trigger description: Compact Codex skill for report-only statistical audits of manuscripts against source data, extracted numerals, sample labels, figures, and cross-references.

### `cgpt-thread-closeout`

- Skill file: `cgpt-thread-closeout/SKILL.md`
- Agent metadata: `cgpt-thread-closeout/agents/openai.yaml`
- Agent display: CGPT Thread Closeout
- Agent short description: Create durable closeout and handoff artifacts.
- Invocation: `$cgpt-thread-closeout`
- Default prompt: Close out this thread with status, handoff, and next-task notes.
- Resources: none
- Trigger description: Use when the user asks CGPT/Codex to close out, wrap up, end a thread, prepare a handoff, save session memory, create next-thread instructions, update status logs, archive a conversation, or make sure a project can be resumed cleanly later.

### `cgpt-tool-routing-lessons`

- Skill file: `cgpt-tool-routing-lessons/SKILL.md`
- Agent metadata: `cgpt-tool-routing-lessons/agents/openai.yaml`
- Agent display: CGPT Tool Routing Lessons
- Agent short description: Choose safe Codex file and connector routing.
- Invocation: `$cgpt-tool-routing-lessons`
- Default prompt: Diagnose the safest Codex tool route for this path, connector, or sandbox-boundary task.
- Resources: none
- Trigger description: Apply Codex-native routing lessons for filesystem sandbox boundaries, connector scopes, local workspace paths, escalation, and tool choice. Use when file access fails, paths are outside the workspace, connectors may be needed, writes require approval, or a task crosses local/cloud/profile directories.

### `cgpt-uw-pptx-deck`

- Skill file: `cgpt-uw-pptx-deck/SKILL.md`
- Agent metadata: `cgpt-uw-pptx-deck/agents/openai.yaml`
- Agent display: CGPT UW PPTX Deck
- Agent short description: Build and verify UW-branded PowerPoint decks.
- Invocation: `$cgpt-uw-pptx-deck`
- Default prompt: Create or polish this UW PowerPoint deck and verify branding, readability, and source-backed claims.
- Resources: none
- Trigger description: Build, rebuild, polish, audit, render, or export University of Washington and UW Bothell PowerPoint decks. Use for UW-branded PPTX work, academic talks, stakeholder briefings, teaching decks, manuscript-to-deck conversions, slide visual QA, UW colors, Block W cover slides, accessibility checks, or requests to make a deck look presentation-ready.

## Regeneration

Run:

```powershell
python .\scripts\build_skill_inventory.py
```

Then validate:

```powershell
python .\scripts\quick_validate.py
```
