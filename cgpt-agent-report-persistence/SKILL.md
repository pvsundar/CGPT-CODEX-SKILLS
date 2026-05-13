---
name: cgpt-agent-report-persistence
description: Save subagent, verifier, reviewer, synthesizer, or audit return text as durable files before closeout. Use when Codex delegates work to subagents, receives a verifier/proofreader/stats/reviewer report, references prior-thread output, closes a sub-session, or creates a handoff that depends on agent analysis that would otherwise live only in chat.
---

# CGPT Agent Report Persistence

Use this skill when analytic return text affects decisions, edits, or handoffs.

## Rule

If a subagent or verifier return would inform a decision later, save the full return to disk before summarizing it or closing the thread.

Chat history is not a durable audit trail. Edits plus saved report are durable; edits plus "see above" are not.

## Where To Save

Default project-local location:

```text
archive/reports/<session-or-task>_<agent-role>_YYYY-MM-DD[_HHMM].md
```

Create `archive/reports/` if it does not exist. Use `_HHMM` when more than one report from the same role is saved on the same date.

## File Header

```markdown
---
agent: <agent-role>
session: <session-or-task>
saved: <YYYY-MM-DD HH:MM local>
supervisor_invocation: <one-line prompt summary>
inputs: <files or task context>
verdict: <pass | fail | mixed | n/a>
---

# <agent-role> return - <session-or-task> - YYYY-MM-DD

<verbatim return text>
```

## Handoff Requirement

Any `HANDOFF.md`, `STATUS-LOG.md`, `SESSION-MEMORY.md`, or `NEXT-CODEX-TASK.md` that relies on the report must point to the saved path.

Use:

```text
Verifier report: archive/reports/D5-closeout_verifier_2026-05-10.md
```

Do not use:

```text
See verifier output above.
Paste from prior thread.
```

## Recovery When Missed

If the original return was lost:

1. State that the original report was not persisted.
2. Re-run the relevant verifier or audit if possible.
3. Save the new report with `_RECOVERY` in the filename.
4. Mark the handoff as reconstructed rather than original provenance.

## Rules

- Save verbatim report content before editorial summary.
- Do not trim failures or caveats from the saved report.
- Do not store decision-driving agent output only in a final chat message.
- Pair with `cgpt-thread-closeout` when ending a session.
