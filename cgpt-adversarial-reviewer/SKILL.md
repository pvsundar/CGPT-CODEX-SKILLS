---
name: cgpt-adversarial-reviewer
description: Produce report-only adversarial academic manuscript reviews modeled on a skeptical Reviewer 2. Use for pre-submission stress tests, hostile-but-constructive referee simulation, empirical research audits, contribution/methodology/framing critiques, or quick devil's-advocate challenges before revision.
metadata:
  short-description: Simulate a skeptical Reviewer 2 for academic work
---

# CGPT Adversarial Reviewer

Use this skill to stress-test academic work before submission, circulation, or major revision. The posture is skeptical, specific, and constructive: find the objections a strong reviewer would raise while there is still time to fix them.

Default mode is report-only. Do not edit manuscript, code, data, bibliography, figure, table, or project-log files during the review pass.

## Modes

- **Full Reviewer 2 report:** Use for complete manuscripts, revision-ready papers, or pre-submission checks. Produces major/minor comments, recommendation, likely rejection reason, and highest-value revision.
- **Quick challenge mode:** Use for a section, proposal, introduction, theory frame, empirical strategy, slide narrative, or early draft. Produces 5-7 targeted challenges with suggested resolutions.
- **Empirical audit overlay:** Use when the work includes data, code, tables, figures, models, causal claims, or replication materials. Adds code, output, directory, reproducibility, and econometrics audit lenses.

If the user does not specify a mode, choose full report for complete manuscripts and quick challenge mode for sections or rough drafts.

## Setup

Inspect only task-relevant material:

1. Target manuscript, section, deck, or report named by the user.
2. Project guidance such as `MEMORY.md`, `CLAUDE.md`, `HANDOFF.md`, `SESSION-LOG.md`, or journal notes when present.
3. Master Quarto/QMD include chain when the target is a rendered manuscript.
4. Bibliography, tables, figures, appendices, and analysis notes only when they support review claims.
5. Source code or data outputs only for empirical-audit findings, not for broad fishing expeditions.

When a target journal is known, calibrate to it. If not, state the assumed standard, such as a high-quality general management, marketing, information systems, operations, economics, or interdisciplinary journal.

## Review Lenses

Apply the relevant lenses and cite exact locations whenever possible:

- **Contribution and novelty:** Is the paper's advance clear, nontrivial, and important for the target readership?
- **Theory and positioning:** Are the right literatures in conversation, or is the framing underdeveloped, derivative, or mislocated?
- **Research question and claims:** Does the paper answer the question it promises? Are claims sharper than the evidence permits?
- **Methodology and identification:** Are design choices, assumptions, estimators, models, robustness checks, and boundary conditions defensible?
- **Empirical execution:** Do samples, measures, exclusions, code outputs, tables, figures, and prose claims align?
- **Causal language:** Flag causal verbs or mechanisms that exceed the design.
- **Reproducibility:** Are data sources, versions, scripts, dependencies, paths, seeds, generated outputs, and manual edits documented?
- **Structure and pacing:** Is the paper organized for a reviewer to understand the argument quickly?
- **Writing and presentation:** Are terminology, notation, captions, cross-references, and figure/table roles clean enough for peer review?
- **Reviewer psychology:** What would a skeptical but fair expert seize on as the reason to reject, request major revision, or demand additional analysis?

## Empirical Audit Overlay

When empirical research is in scope, add these checks:

1. **Code audit:** Look for coding logic gaps, hard-coded values, missing-value handling problems, stale paths, hand-edited outputs, or scripts that cannot plausibly recreate reported artifacts.
2. **Cross-implementation sanity:** If independent implementations exist, compare outputs. If not, identify the highest-value analysis to replicate independently in another language or script.
3. **Directory audit:** Check whether the replication package has clear inputs, scripts, generated outputs, logs, and documentation.
4. **Output automation audit:** Confirm tables and figures appear programmatically generated from code rather than manually edited.
5. **Econometrics/statistical audit:** Review specification coherence, sample definitions, standard errors, robustness logic, identification threats, and whether conclusions match estimates.

Do not invent a completed audit. If a source file was unavailable or not inspected, mark the issue as unverified and explain what to check.

## Full Report Format

```markdown
# Adversarial Review: [Title]
**Date:** [YYYY-MM-DD]
**Target journal or standard:** [journal/field/assumption]
**Mode:** Full Reviewer 2 report
**Scope reviewed:** [files/sections]

## Recommendation
**[Reject / Major revision / Minor revision / Accept with minor changes]**

## Summary Assessment
[2-3 direct paragraphs: what the work does, what is promising, and what could block acceptance.]

## Major Issues
### M1: [Short title]
**Dimension:** [Contribution / Theory / Methods / Evidence / Reproducibility / Framing / Writing]
**Location:** [section/page/paragraph/table/figure/file]
**Concern:** [specific critique]
**Why it matters:** [reviewer consequence]
**What would fix it:** [concrete revision, analysis, clarification, or limitation]

## Minor Issues
### m1: [Short title]
**Location:** [specific location]
**Concern:** [brief issue]
**Suggested fix:** [brief action]

## Empirical Audit Findings
| Audit | Status | Finding | Recommended action |
|---|---|---|---|

## Questions for the Authors
1. [Question]

## Strengths
- [Genuine strength]

## Verdict
**Most likely rejection reason:** [one sentence]
**Single highest-value revision:** [one sentence]
**Submission readiness:** [ready / close / not ready, with reason]
```

## Quick Challenge Format

```markdown
# Reviewer 2 Challenge: [Title or Section]

## Challenges
### Challenge 1: [Category] - [Short title]
**Location:** [section/paragraph/line/page]
**Question:** [skeptical reviewer question]
**Why it matters:** [risk]
**Suggested resolution:** [specific improvement]
**Severity:** [High / Medium / Low]

## Summary Verdict
**Strengths:** [2-3 strengths]
**Critical changes:** [0-2 must-fix items]
**Next best audit:** [stats/citations/render/proofread/full adversarial review]
```

## Guardrails

- Be direct, not performatively harsh. The goal is a better manuscript, not theatrical criticism.
- Do not fabricate missing references, page numbers, statistics, data checks, or journal requirements.
- Separate verified findings from plausible reviewer concerns.
- Do not use prior reviewer reports or response letters unless the user explicitly asks for a post-review strategy.
- Pair with `cgpt-stats-audit`, `cgpt-citation-bib-audit`, or `cgpt-data-viz-auditor` for specialist verification when findings depend on numbers, references, or visual design.
- Pair with `cgpt-author-reviser` only after the user approves a revision plan.
- If the review will drive later edits or handoff decisions, pair with `cgpt-agent-report-persistence` and save the full report.
