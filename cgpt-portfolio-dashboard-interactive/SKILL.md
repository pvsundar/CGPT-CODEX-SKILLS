---
name: cgpt-portfolio-dashboard-interactive
description: Build and maintain the editable PVB research portfolio dashboard with v4 operating-state taxonomy, JSON-canonical state, hardened export/import, autosave, and validation.
---

# CGPT Portfolio Dashboard Interactive

Use this skill when building or revising the editable in-browser PVB research portfolio dashboard, especially `PVB_Master_Research_Portfolio_Dashboard_v4_INTERACTIVE.html` or a `CGPT_`-prefixed derivative. This is the operating dashboard the user edits weekly. It is distinct from static portfolio synthesis reports.

Use `cgpt-interactive-html-export-hardening` alongside this skill for the export/import JavaScript.

For the June 2026 compact JSON source format, prefer the bundled script:
`scripts/build_pvb_dashboard_v4.py`. It migrates the old `category/status/authors/outlet/next/prov/tasks` schema into the v4 JSON state, applies the fixed correction rules, and emits paired HTML, JSON, changelog, and QMD-style report artifacts.

## Operating Principles

- Categories are current operating states, not a linear publication pipeline.
- A project can move between categories in any direction as evidence changes.
- JSON is canonical; HTML is the self-contained interface.
- Do not require a server, CDN, external JavaScript, or external CSS.
- Preserve user-edited source JSON as authority unless the task gives a specific correction rule.
- Record category changes in `classification_history` rather than deleting prior context.

## v4 Status Categories

Use only these `status_category` values:

1. Published / Forthcoming / Released
2. Working Paper Completed
3. Under Review
4. Revise and Resubmit / In Revision
5. Rejected / Withdrawn and Needing Resubmission
6. Active Manuscript Development
7. Active Data / Code / Replication Work
8. Teaching Cases / Pedagogical Tools
9. Software / Apps / Interactive Tools
10. Dormant but Previously Discussed
11. Service / Editorial / Advisory Roles
12. Administrative / CV / Portfolio Maintenance

## Controlled Values

`completion_state`:

- Not Started
- Active
- Partially Completed
- Working Paper Complete
- Under Review
- Revision in Progress
- Resubmission Needed
- Published
- Released
- Maintain
- Dormant
- Archived
- Blocked / Waiting

`project_type`:

- Peer-reviewed article
- Working paper
- Conference paper / proceedings
- Research note
- Software package
- Web app
- GPT / AI tool
- Teaching case
- Teaching tool
- Dataset / replication package
- Advisory project
- Editorial role
- Service role
- Administrative portfolio task

`priority_tier`:

- P0 (this week)
- P1 (this month)
- P2 (this quarter)
- P3 (this year)
- P4 (parked)

## Per-Project Schema

```json
{
  "id": "",
  "title": "",
  "status_category": "",
  "project_type": "",
  "priority_tier": "",
  "completion_state": "",
  "progress_percent": 0,
  "authors_or_owner": "",
  "outlet_or_target": "",
  "current_stage": "",
  "next_concrete_action": "",
  "deadline_or_trigger": "",
  "notes": "",
  "provenance": "",
  "related_files": "",
  "related_links": "",
  "last_updated": "YYYY-MM-DD",
  "open_questions": "",
  "classification_history": [],
  "done_archived": false,
  "microtasks": {}
}
```

Required microtasks:

- Triage reviewed
- Needs correction
- Waiting on coauthor
- Waiting on editor
- Needs outlet decision
- Needs files/code cleanup
- Ready to submit
- Archive-ready

## UI Requirements

- Search across all project fields.
- Filter independently by status category, completion state, project type, and priority tier.
- Sort by priority, title, status, progress, and last updated.
- Recompute KPI counts after every state change.
- Make text fields editable, controlled fields dropdowns, progress a slider, and done/archive a checkbox.
- Provide Import JSON, Export JSON, Export edited HTML, Reset local edits, and Print/PDF.
- Prompt for an optional classification-change note when status changes and append to `classification_history`.
- Include dashboard sections in this order: executive summary, this week's queue, the 12 status categories, open questions, excluded items, and classification history.

## Data Correction Rules

Apply these on every build unless the user explicitly supersedes them:

1. JBS Trifaceted is Published / Forthcoming / Released.
2. Family of Rules is Under Review at Mathematical Social Sciences, Manuscript ID MSS-D-26-00304.
3. Family of Rules submission date is May 20, 2026.
4. TRIFACET repository is `https://github.com/pvsundar/TRIFACET`.
5. EXEC_ED_OCTAHEDRON live deployment is `https://trifaceted.netlify.app`.
6. ICBSC award wording is exactly: "First Place — Best Document for the Strategic Business Plan."
7. ICBSC course code remains an open question: BBUS 490 vs BUS 499.
8. WBM 2026 location for PA-HHI is Las Vegas, NV.
9. Xiaodong/JCC status reads: "Revision returned to co-author May 7, 2026; awaiting co-author response."
10. Movies-Crime target remains "Journal of Marketing or Journal of Marketing Research" unless narrowed by the user.
11. BIODIV-AUTO must never export as Not Started; use Revision in Progress or Active Manuscript Development as appropriate.
12. Exclude "Being Danned" and "Novel Bradshaw / Aly Lo Notes."
13. BE-HHI/NHHI/EHHI should be treated as a teaching/method note, not folded into PA-HHI.

## Legacy Mapping

Map invalid or old values through an explicit table before rendering:

| Legacy value | v4 value |
| --- | --- |
| Completed / Published / Released | Published / Forthcoming / Released |
| In Revision (Major or Minor) | Revise and Resubmit / In Revision |
| Rejected and Needing Resubmission | Rejected / Withdrawn and Needing Resubmission |
| Active / In Progress | Active Manuscript Development |
| Teaching Cases / Tools / Packages | Teaching Cases / Pedagogical Tools |
| Service / Editorial / Leadership | Service / Editorial / Advisory Roles |
| Manuscript Revision | Revise and Resubmit / In Revision |
| Submitted | Under Review |
| Completed | Working Paper Completed, unless evidence indicates Published |

## Deliverables

When building the v4 dashboard, place paired outputs in `REPORTS` unless the user specifies another folder:

- HTML dashboard
- canonical state JSON
- changelog Markdown
- QMD-style report of changes, with YAML front matter, source files, output files, correction log, validation table, and unresolved questions

If the user asks for CGPT naming, prefix deliverables with `CGPT_`.

## Validation Checklist

Run before reporting done:

1. Extract inline script and run `node --check`.
2. Open from `file:///` in a browser when practical; console has no errors.
3. Search, all four filters, and sort work.
4. KPI counts update after status/category changes.
5. localStorage autosave persists an edit after reload.
6. Export JSON includes every project and required fields.
7. Import JSON updates the UI.
8. Export edited HTML preserves checkbox, dropdown, slider, and editable text changes.
9. Clearing localStorage does not erase exported HTML state.
10. BIODIV-AUTO does not export as Not Started.
11. Working Paper Completed appears as a category.
12. No external dependencies.
13. Reclassifying a project does not lose notes and records history.
14. Loading an unknown status warns and shows a badge.
