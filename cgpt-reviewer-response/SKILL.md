---
name: cgpt-reviewer-response
description: Draft, revise, audit, and package academic response-to-reviewers letters, editor responses, revision memos, and R&R correspondence. Use when the user shares peer-review comments, decision letters, reviewer feedback, associate editor guidance, or asks for a response matrix, rebuttal, revision strategy, cover response, or journal-facing revision correspondence.
---

# CGPT Reviewer Response

Use this skill to turn reviewer and editor feedback into a complete, professional revision response. The goal is not just diplomacy; every comment needs a traceable answer, a clear action, and a defensible record of what changed.

## Core Principles

- Every editor and reviewer comment gets a response, including praise and minor edits.
- Classify before drafting: separate major conceptual, methodological, clarification, editorial, and praise comments.
- Keep tone appreciative, concrete, and non-defensive.
- Lead with revision action, then evidence: what changed, where it changed, and why it improves the paper.
- Do not fabricate manuscript changes, citations, page numbers, analyses, tables, or reviewer text.

## Workflow

1. Ingest the material.
   - Accept pasted comments, decision letters, PDFs, DOCX files, or project notes.
   - Preserve reviewer wording when quoting comments.
   - Extract reviewer/editor ID, comment number, comment text, issue type, priority, requested action, and likely manuscript location.

2. Build the response plan.
   - Group comments by editor, AE, Reviewer 1, Reviewer 2, etc.
   - Flag must-do items that block acceptance, quick fixes, optional improvements, contradictions, and places where respectful disagreement may be warranted.
   - Ask for confirmation before drafting only when classification or revision strategy is ambiguous.

3. Draft responses.
   - Use this structure by default: acknowledgment, action taken, concrete evidence, closing sentence.
   - Include revised text excerpts when available, but keep excerpts focused.
   - For methodological comments, name the analysis, statistic, robustness check, data constraint, or decision logic.
   - For infeasible requests, explain the constraint, offer a partial accommodation, and add future-research or limitation language only when appropriate.

4. Match authorship voice.
   - Sole-authored papers use `I`, `my`, and `the revised manuscript`.
   - Co-authored papers use `we`, `our`, and `the revised manuscript`.
   - Never mix pronoun systems in a single response document except inside quoted reviewer text.

5. Apply Sundar-style revision correspondence when appropriate.
   - Use a warm but scholarly posture: gratitude, concrete revision action, stronger manuscript, open door.
   - Prefer specific acknowledgment adjectives such as thoughtful, constructive, insightful, valuable, important, helpful, or detailed.
   - Use direct action verbs: revised, clarified, streamlined, reorganized, incorporated, expanded, separated, refined, repositioned, strengthened, reframed, restructured, tightened.
   - Allow one or two genuine human asides per reviewer section when they fit the user's voice; do not manufacture them.

6. Apply JBS overlay only when the task is JBS-specific or the user asks for that voice.
   - Enforce first-person singular.
   - Use `Done.` sparingly for discrete completed fixes.
   - Avoid summary tables, action subheaders, and internal scaffolding in reviewer-facing prose.
   - Keep internal version names, file names, and handoff labels out of the response.
   - Ensure the closing includes `approbation` when the user wants the JBS signature close.

7. Audit before delivery.
   - Every numbered comment has a response.
   - Tone is respectful and non-defensive.
   - Every substantive response names a change, location, evidence, or defensible no-change rationale.
   - Page, section, table, and figure references are either verified or clearly marked for user confirmation.
   - Citation claims are verifiable and consistent with the manuscript bibliography.
   - No unresolved placeholders, internal draft labels, or unsupported claims remain.

## Output Options

- Markdown response letter for review.
- Structured response matrix when the user needs project management or broad triage.
- Journal-facing prose-only response when the target journal or overlay calls for it.
- DOCX response package by pairing this skill with `cgpt-academic-docx-authoring`, then validating with `cgpt-render-check`.
