from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


TODAY = "2026-06-09"
BASE = "CGPT_PVB_Master_Research_Portfolio_Dashboard_v4"

STATUS_CATEGORIES = [
    "Published / Forthcoming / Released",
    "Working Paper Completed",
    "Under Review",
    "Revise and Resubmit / In Revision",
    "Rejected / Withdrawn and Needing Resubmission",
    "Active Manuscript Development",
    "Active Data / Code / Replication Work",
    "Teaching Cases / Pedagogical Tools",
    "Software / Apps / Interactive Tools",
    "Dormant but Previously Discussed",
    "Service / Editorial / Advisory Roles",
    "Administrative / CV / Portfolio Maintenance",
]

COMPLETION_STATES = [
    "Not Started",
    "Active",
    "Partially Completed",
    "Working Paper Complete",
    "Under Review",
    "Revision in Progress",
    "Resubmission Needed",
    "Published",
    "Released",
    "Maintain",
    "Dormant",
    "Archived",
    "Blocked / Waiting",
]

PROJECT_TYPES = [
    "Peer-reviewed article",
    "Working paper",
    "Conference paper / proceedings",
    "Research note",
    "Software package",
    "Web app",
    "GPT / AI tool",
    "Teaching case",
    "Teaching tool",
    "Dataset / replication package",
    "Advisory project",
    "Editorial role",
    "Service role",
    "Administrative portfolio task",
]

PRIORITY_TIERS = [
    "P0 (this week)",
    "P1 (this month)",
    "P2 (this quarter)",
    "P3 (this year)",
    "P4 (parked)",
]

MICROTASKS = [
    "Triage reviewed",
    "Needs correction",
    "Waiting on coauthor",
    "Waiting on editor",
    "Needs outlet decision",
    "Needs files/code cleanup",
    "Ready to submit",
    "Archive-ready",
]

EXCLUDED_ITEMS = ["Being Danned", "Novel Bradshaw / Aly Lo Notes"]
URL_RE = re.compile(r"https?://[^\s)\],;]+")


def norm_space(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def contains_any(text: str, terms: list[str]) -> bool:
    low = text.lower()
    return any(term.lower() in low for term in terms)


def related_links(*values: object) -> str:
    found: list[str] = []
    for url in URL_RE.findall(" ".join(str(v or "") for v in values)):
        clean = url.rstrip(".;,")
        if clean not in found:
            found.append(clean)
    return "; ".join(found)


def status_category_for(item: dict) -> str:
    tid = item.get("id", "")
    old_cat = item.get("category", "")
    software_ids = {"C08", "C09", "C10", "T01", "T02", "T03", "T04", "T05", "T06"}
    teaching_ids = {"C12", "T07", "T08", "T09", "T10", "T11", "T12", "T13", "A09"}
    data_ids = {"A02", "A07"}
    service_ids = {"S01", "S02", "S03"}
    if tid in software_ids:
        return "Software / Apps / Interactive Tools"
    if tid in teaching_ids:
        return "Teaching Cases / Pedagogical Tools"
    if tid in data_ids:
        return "Active Data / Code / Replication Work"
    if tid in service_ids:
        return "Service / Editorial / Advisory Roles"
    if tid == "D07":
        return "Working Paper Completed"
    if tid == "U01":
        return "Under Review"
    if tid in {"R01", "R02", "R03"}:
        return "Revise and Resubmit / In Revision"
    if tid in {"X01", "X02"}:
        return "Rejected / Withdrawn and Needing Resubmission"
    return {
        "Completed / Published / Released": "Published / Forthcoming / Released",
        "Under Review": "Under Review",
        "Rejected and Needing Resubmission": "Rejected / Withdrawn and Needing Resubmission",
        "In Revision (Major or Minor)": "Revise and Resubmit / In Revision",
        "Active / In Progress": "Active Manuscript Development",
        "Dormant but Previously Discussed": "Dormant but Previously Discussed",
        "Teaching Cases / Tools / Packages": "Teaching Cases / Pedagogical Tools",
        "Service / Editorial / Leadership": "Service / Editorial / Advisory Roles",
    }.get(old_cat, "Active Manuscript Development")


def project_type_for(item: dict, category: str) -> str:
    tid = item.get("id", "")
    title = item.get("title", "")
    outlet = item.get("outlet", "")
    blob = f"{title} {outlet} {item.get('notes', '')}"
    if tid in {"S01", "S02", "S03"}:
        if "Editor" in title or "Review" in title:
            return "Editorial role"
        if "Advisory" in title:
            return "Advisory project"
        return "Service role"
    if tid in {"A02", "A07"}:
        return "Dataset / replication package"
    if tid == "C08":
        return "Software package"
    if tid in {"T01", "T02"} or contains_any(blob, ["GPT", "LLM"]):
        return "GPT / AI tool"
    if tid in {"C09", "C10", "T03", "T04", "T05", "T06"} or contains_any(
        blob, ["app", "prototype", "streamlit", "shiny", "netlify", "lovable"]
    ):
        return "Web app"
    if category == "Teaching Cases / Pedagogical Tools":
        if contains_any(title, ["case", "negotiation", "TVs", "RAMKI"]):
            return "Teaching case"
        return "Teaching tool"
    if "AMTP" in title or "Proceedings" in outlet:
        return "Conference paper / proceedings"
    if category in {"Working Paper Completed", "Dormant but Previously Discussed"}:
        return "Working paper"
    if contains_any(f"{title} {outlet}", ["note", "VISPUR", "Gap Statistic Manuscript"]):
        return "Research note"
    return "Peer-reviewed article"


def completion_for(item: dict, category: str) -> str:
    tid = item.get("id", "")
    old_status = item.get("status", "")
    if tid == "R03":
        return "Revision in Progress"
    if category == "Working Paper Completed":
        return "Working Paper Complete"
    if category == "Published / Forthcoming / Released" and old_status == "Completed":
        return "Published"
    return {
        "Completed": "Published",
        "Released": "Released",
        "Maintain": "Maintain",
        "Active": "Active",
        "Partially Completed": "Partially Completed",
        "Under Review": "Under Review",
        "Major Revision": "Revision in Progress",
        "Revision in Progress": "Revision in Progress",
        "Resubmission Needed": "Resubmission Needed",
        "Dormant": "Dormant",
        "Not Started": "Not Started",
    }.get(old_status, "Active")


def priority_for(item: dict, category: str, completion: str) -> str:
    tid = item.get("id", "")
    progress = int(float(item.get("progress") or 0))
    if tid in {"U01", "R01", "R02", "R03"}:
        return "P0 (this week)"
    if tid in {"X01", "X02", "A02", "A03", "A06", "A07"}:
        return "P1 (this month)"
    if category in {"Active Manuscript Development", "Active Data / Code / Replication Work"}:
        return "P1 (this month)" if progress >= 60 else "P2 (this quarter)"
    if category in {
        "Rejected / Withdrawn and Needing Resubmission",
        "Working Paper Completed",
    }:
        return "P2 (this quarter)"
    if category in {"Teaching Cases / Pedagogical Tools", "Software / Apps / Interactive Tools"}:
        return "P3 (this year)" if completion in {"Maintain", "Partially Completed", "Active"} else "P4 (parked)"
    if category == "Service / Editorial / Advisory Roles":
        return "P3 (this year)"
    return "P4 (parked)"


def open_questions_for(item: dict) -> str:
    tid = item.get("id", "")
    questions: list[str] = []
    if tid in {"C12", "T12"}:
        questions.append("Confirm final course code: BBUS 490 vs BUS 499.")
    if tid == "D07":
        questions.append(
            "Verify whether the 2022 draft is a submission-ready working paper or should return to dormant/teaching-note status."
        )
    if tid in {"A03", "A04"}:
        questions.append("Verify whether current evidence supports Working Paper Completed or Active Manuscript Development.")
    if tid == "A10":
        questions.append("Decide whether VISPUR remains a manuscript component or separate methods paper.")
    return " ".join(questions)


def old_tasks_to_microtasks(tasks: dict | None, done: bool) -> dict[str, bool]:
    tasks = tasks or {}
    return {
        "Triage reviewed": bool(tasks.get("triage", False)),
        "Needs correction": bool(tasks.get("partial", False)),
        "Waiting on coauthor": False,
        "Waiting on editor": False,
        "Needs outlet decision": False,
        "Needs files/code cleanup": False,
        "Ready to submit": False,
        "Archive-ready": bool(tasks.get("archive", False) or done),
    }


def transform_projects(source: list[dict]) -> tuple[list[dict], list[str], list[str]]:
    projects: list[dict] = []
    correction_log: list[str] = []
    warnings: list[str] = []

    for item in source:
        title = norm_space(item.get("title"))
        if any(ex.lower() in title.lower() for ex in EXCLUDED_ITEMS):
            continue

        tid = item.get("id", "")
        category = status_category_for(item)
        completion = completion_for(item, category)
        ptype = project_type_for(item, category)
        priority = priority_for(item, category, completion)
        notes = norm_space(item.get("notes"))
        outlet = norm_space(item.get("outlet"))
        next_action = norm_space(item.get("next"))
        provenance = norm_space(item.get("prov"))
        authors = norm_space(item.get("authors"))

        if tid == "C01":
            category = "Published / Forthcoming / Released"
            completion = "Published"
            correction_log.append("C01 JBS Trifaceted set to Published / Forthcoming / Released.")
        if tid == "U01":
            category = "Under Review"
            completion = "Under Review"
            outlet = "Mathematical Social Sciences"
            if "MSS-D-26-00304" not in notes:
                notes += " Manuscript ID MSS-D-26-00304."
            if "Submitted May 20, 2026" not in notes:
                notes = "Submitted May 20, 2026. " + notes
            correction_log.append("U01 Family of Rules set to Under Review; May 20, 2026 submission date retained.")
        if tid == "C09":
            if "https://github.com/pvsundar/TRIFACET" not in notes:
                notes += " Source repository: https://github.com/pvsundar/TRIFACET."
            correction_log.append("C09 TRIFACET repository set to https://github.com/pvsundar/TRIFACET.")
        if tid == "C10":
            if "https://trifaceted.netlify.app" not in notes:
                notes += " Live deployment: https://trifaceted.netlify.app."
            correction_log.append("C10 EXEC_ED_OCTAHEDRON live deployment set to https://trifaceted.netlify.app.")
        if tid == "C12":
            notes = re.sub(
                r"First Place\s+[—-]\s+Best Document for the Strategic Business Plan",
                "First Place — Best Document for the Strategic Business Plan",
                notes,
            )
            if "First Place — Best Document for the Strategic Business Plan" not in notes:
                notes += " Award wording: First Place — Best Document for the Strategic Business Plan."
            correction_log.append("C12 ICBSC award wording preserved exactly.")
        if tid == "A01":
            if "Las Vegas, NV" not in notes:
                notes += " WBM Conference, Marketing Trends 2026 location: Las Vegas, NV."
            correction_log.append("A01 PA-HHI WBM 2026 location retained as Las Vegas, NV.")
        if tid == "R02":
            phrase = "Revision returned to co-author May 7, 2026; awaiting co-author response."
            if phrase not in notes:
                notes += " " + phrase
            correction_log.append("R02 Xiaodong/JCC status wording retained exactly.")
        if tid == "R01":
            outlet = "Target: Journal of Marketing or Journal of Marketing Research"
            correction_log.append("R01 Movies-Crime target kept as Journal of Marketing or Journal of Marketing Research.")
        if tid == "R03":
            completion = "Revision in Progress"
            notes = notes.replace("Not Started", "Revision in Progress")
            correction_log.append("R03 BIODIV-AUTO corrected from Not Started to Revision in Progress.")
        if tid == "A09":
            category = "Teaching Cases / Pedagogical Tools"
            ptype = "Teaching tool"
            if "do not include it in PA-HHI manuscript" not in notes:
                notes += " BE-HHI/NHHI/EHHI are tracked as teaching/method-note material, not folded into PA-HHI."
            correction_log.append("A09 BE-HHI/NHHI/EHHI kept as teaching/method note, separate from PA-HHI.")
        if tid in {"C12", "T12"}:
            correction_log.append(f"{tid} ICBSC course-code open question recorded: BBUS 490 vs BUS 499.")

        if category not in STATUS_CATEGORIES:
            warnings.append(f"{tid}: invalid category {category!r}; defaulted to Active Manuscript Development.")
            category = "Active Manuscript Development"
        if completion not in COMPLETION_STATES:
            warnings.append(f"{tid}: invalid completion {completion!r}; defaulted to Active.")
            completion = "Active"
        if ptype not in PROJECT_TYPES:
            warnings.append(f"{tid}: invalid project_type {ptype!r}; defaulted to Research note.")
            ptype = "Research note"

        old_category = item.get("category", "")
        history = []
        if old_category != category:
            history.append(
                {
                    "date": TODAY,
                    "from_status": old_category,
                    "to_status": category,
                    "reason": "Migrated from June 2026 edited dashboard to v4 operating-state taxonomy.",
                }
            )

        project = {
            "id": tid,
            "title": title,
            "status_category": category,
            "project_type": ptype,
            "priority_tier": priority,
            "completion_state": completion,
            "progress_percent": int(float(item.get("progress") or 0)),
            "authors_or_owner": authors,
            "outlet_or_target": outlet,
            "current_stage": f"v4: {category}; completion: {completion}. Source category/status: {old_category} / {item.get('status', '')}.",
            "next_concrete_action": next_action,
            "deadline_or_trigger": "",
            "notes": notes,
            "provenance": provenance,
            "related_files": "",
            "related_links": related_links(outlet, next_action, notes, provenance),
            "last_updated": TODAY,
            "open_questions": open_questions_for(item),
            "classification_history": history,
            "history_log": list(history),
            "done_archived": bool(item.get("done", False)),
            "microtasks": old_tasks_to_microtasks(item.get("tasks"), bool(item.get("done", False))),
            "source_snapshot": {
                "category": old_category,
                "status": item.get("status", ""),
                "progress": item.get("progress", ""),
                "tasks": item.get("tasks", {}),
            },
        }
        projects.append(project)

    cat_order = {name: idx for idx, name in enumerate(STATUS_CATEGORIES)}
    pri_order = {name: idx for idx, name in enumerate(PRIORITY_TIERS)}
    projects.sort(key=lambda p: (cat_order.get(p["status_category"], 99), pri_order.get(p["priority_tier"], 99), p["id"]))
    return projects, sorted(set(correction_log)), warnings


def state_object(projects: list[dict], corrections: list[str], source_json: Path, source_html: Path) -> dict:
    return {
        "metadata": {
            "title": "PVB Master Research Portfolio Dashboard v4 Interactive",
            "built_by": "CGPT Codex",
            "schema_version": "4.0",
            "date_built": TODAY,
            "source_json": str(source_json),
            "source_html": str(source_html),
            "naming_note": "CGPT_ prefix applied per user request; title preserves PVB_Master_Research_Portfolio_Dashboard_v4 identity.",
            "local_storage_key": "cgpt_pvb_master_research_portfolio_dashboard_v4_state",
        },
        "taxonomy": {
            "status_categories": STATUS_CATEGORIES,
            "completion_states": COMPLETION_STATES,
            "project_types": PROJECT_TYPES,
            "priority_tiers": PRIORITY_TIERS,
            "microtasks": MICROTASKS,
        },
        "projects": projects,
        "excluded_items": EXCLUDED_ITEMS,
        "correction_log": corrections,
        "legacy_value_mapping": {
            "Completed / Published / Released": "Published / Forthcoming / Released",
            "In Revision (Major or Minor)": "Revise and Resubmit / In Revision",
            "Rejected and Needing Resubmission": "Rejected / Withdrawn and Needing Resubmission",
            "Active / In Progress": "Active Manuscript Development",
            "Teaching Cases / Tools / Packages": "Teaching Cases / Pedagogical Tools",
            "Service / Editorial / Leadership": "Service / Editorial / Advisory Roles",
            "Manuscript Revision": "Revise and Resubmit / In Revision",
            "Submitted": "Under Review",
            "Completed": "Working Paper Completed",
        },
    }


HTML_TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PVB Master Research Portfolio Dashboard v4 Interactive</title>
<style>
:root{--uw-purple:#4b2e83;--uw-gold:#d4a843;--ink:#1f2933;--muted:#667085;--line:#d9dee6;--bg:#f5f6f8;--card:#fff;--soft-purple:#f2eff8;--soft-gold:#fff8dd;--red:#b42318;--shadow:0 1px 2px rgba(16,24,40,.08)}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Calibri,"Segoe UI",Arial,sans-serif;line-height:1.45}header{background:var(--uw-purple);color:white;padding:22px 28px;border-bottom:5px solid var(--uw-gold)}h1{font-size:28px;line-height:1.15;margin:0 0 6px}header p{margin:0;color:#f4eefc}.wrap{max-width:1480px;margin:0 auto;padding:18px 22px 48px}.toolbar{position:sticky;top:0;z-index:5;background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);padding:12px;margin-bottom:14px;display:grid;grid-template-columns:minmax(220px,1.4fr) repeat(5,minmax(150px,1fr));gap:10px;align-items:end}.control label,.field label{display:block;font-size:12px;font-weight:700;color:#4d5866;margin-bottom:4px;text-transform:uppercase}.control input,.control select,button,.field select{width:100%;min-height:34px;border:1px solid #c9d0da;border-radius:6px;background:#fff;color:var(--ink);padding:6px 8px;font:inherit}button{width:auto;font-weight:700;cursor:pointer;background:var(--uw-purple);color:#fff;border-color:var(--uw-purple)}button.secondary{background:#fff;color:var(--uw-purple)}button.warn{background:#fff;color:var(--red);border-color:#f0b4ad}.actions{grid-column:1/-1;display:flex;gap:8px;flex-wrap:wrap}.panel{background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);padding:14px;margin:14px 0;border-radius:6px}.panel h2,.status-section h2{font-size:20px;margin:0 0 10px}.summary-grid{display:grid;grid-template-columns:1.1fr 1.4fr 1fr;gap:14px}table{width:100%;border-collapse:collapse;font-size:14px}th,td{border-bottom:1px solid #e6eaf0;padding:7px 8px;text-align:left;vertical-align:top}th{background:#f7f7fb;color:#394150}.num{text-align:right;font-variant-numeric:tabular-nums}.total-row td{font-weight:800;background:var(--soft-gold)}.status-section{margin:18px 0}.section-head{display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:3px solid var(--uw-purple);padding:9px 2px 7px}.section-count{font-size:13px;color:#4d5866;background:#fff;border:1px solid var(--line);border-radius:999px;padding:3px 9px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:12px;margin-top:12px}.project-card{background:var(--card);border:1px solid var(--line);border-radius:6px;box-shadow:var(--shadow);padding:13px}.card-top{display:grid;grid-template-columns:30px 1fr;gap:10px}.done-wrap{padding-top:4px}.done-wrap input{width:20px;height:20px}.idline{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:5px}.pid{font-weight:800;color:var(--uw-purple)}.pill{display:inline-flex;align-items:center;min-height:22px;border-radius:999px;padding:2px 8px;font-size:12px;font-weight:700;border:1px solid var(--line);background:#f7f7fb}.pill.status{background:var(--soft-purple);color:#2f1d52}.pill.type{background:#eef6ff;color:#1849a9}.pill.priority{background:var(--soft-gold);color:#7a5200}.badge{background:#fff1f3;color:var(--red);border-color:#fecdca}.card-title{font-size:18px;font-weight:800;margin:0 0 8px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.field.wide{grid-column:1/-1}.field div[contenteditable]{width:100%;min-height:35px;border:1px solid #d6dbe4;border-radius:6px;background:#fff;padding:7px 8px}.field div[contenteditable]:focus{outline:2px solid var(--uw-gold);background:#fffdf2}.progress-row{display:flex;gap:9px;align-items:center}.progress-row input{flex:1}.progress-row output{min-width:48px;text-align:right;font-variant-numeric:tabular-nums;font-weight:700}.microtasks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:5px 10px;margin-top:10px;border-top:1px solid #e6eaf0;padding-top:9px}.microtasks label{font-size:13px;display:flex;gap:7px;align-items:center}.empty{color:var(--muted);font-style:italic;background:#fff;border:1px dashed var(--line);padding:12px;border-radius:6px}.openq{border-left:4px solid var(--uw-gold)}.history-list{font-size:14px}.muted{color:var(--muted)}.small{font-size:13px}.file-note{font-family:Consolas,"Courier New",monospace;font-size:12px;background:#f7f7fb;border:1px solid var(--line);padding:8px;border-radius:6px;overflow:auto}@media(max-width:980px){.toolbar,.summary-grid{grid-template-columns:1fr}.cards{grid-template-columns:1fr}.grid{grid-template-columns:1fr}.actions{grid-column:auto}.wrap{padding:12px}}@media print{.toolbar,.actions,button{display:none!important}body{background:#fff}.wrap{max-width:none;padding:8px}.panel,.project-card{box-shadow:none;break-inside:avoid}.cards{display:block}.project-card{margin:10px 0}header{background:#fff;color:#111;border-bottom:2px solid #111}}
</style>
</head>
<body>
<header><h1>PVB Master Research Portfolio Dashboard v4 Interactive</h1><p>CGPT build · June 9, 2026 · JSON-canonical operating dashboard with non-linear status categories</p></header>
<div class="wrap">
<section class="toolbar" aria-label="Dashboard controls">
<div class="control"><label for="searchBox">Search</label><input id="searchBox" type="search" placeholder="Search projects, notes, outlets, provenance"></div>
<div class="control"><label for="statusFilter">Status</label><select id="statusFilter"></select></div>
<div class="control"><label for="completionFilter">Completion</label><select id="completionFilter"></select></div>
<div class="control"><label for="typeFilter">Project Type</label><select id="typeFilter"></select></div>
<div class="control"><label for="priorityFilter">Priority</label><select id="priorityFilter"></select></div>
<div class="control"><label for="sortSelect">Sort</label><select id="sortSelect"><option value="priority">Priority</option><option value="title">Title</option><option value="status">Status</option><option value="progress">Progress</option><option value="last_updated">Last updated</option></select></div>
<div class="actions"><button id="exportJSONBtn" type="button">Export JSON</button><button id="importJSONBtn" type="button" class="secondary">Import JSON</button><input id="importFile" type="file" accept="application/json,.json" hidden><button id="exportHTMLBtn" type="button">Export Edited HTML</button><button id="printBtn" type="button" class="secondary">Print / PDF</button><button id="resetBtn" type="button" class="warn">Reset Local Edits</button></div>
</section>
<section class="panel"><h2>Executive Summary and Priority Queue</h2><div class="summary-grid"><div><h3>KPI Counts</h3><table><tbody id="kpiBody"></tbody></table></div><div><h3>This Week's Operating Queue</h3><table><thead><tr><th>ID</th><th>Project</th><th>Next Action</th></tr></thead><tbody id="queueBody"></tbody></table></div><div><h3>Open Questions</h3><table><thead><tr><th>ID</th><th>Question</th></tr></thead><tbody id="openQuestionsBody"></tbody></table></div></div></section>
<section id="sections"></section>
<section class="panel openq"><h2>Excluded Items / Do Not Re-add</h2><p class="muted">These remain excluded from the research portfolio unless explicitly restored.</p><ul id="excludedList"></ul></section>
<section class="panel"><h2>Classification History / Recently Changed Statuses</h2><div id="historyList" class="history-list"></div></section>
<section class="panel"><h2>Build Provenance</h2><div id="provenanceBox" class="file-note"></div></section>
</div>
<script id="state-json" type="application/json">@@STATE_JSON@@</script>
<script>
const KEY = 'cgpt_pvb_master_research_portfolio_dashboard_v4_state';
const EXPORT_HTML_NAME = 'CGPT_PVB_Master_Research_Portfolio_Dashboard_v4_INTERACTIVE_EDITED.html';
const EXPORT_JSON_NAME = 'CGPT_PVB_Master_Research_Portfolio_Dashboard_v4_STATE_EDITED.json';
const q = sel => document.querySelector(sel);
const qa = (sel, root=document) => Array.from(root.querySelectorAll(sel));
let state = null;
let saveTimer = null;
function escapeHTML(value){return String(value ?? '').replace(/[&<>"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]));}
function clone(obj){return JSON.parse(JSON.stringify(obj));}
function parseInlineState(){return JSON.parse(q('#state-json').textContent);}
function loadState(){
  let inline = parseInlineState();
  try {
    const stored = localStorage.getItem(KEY);
    if (stored) inline = JSON.parse(stored);
  } catch (err) {
    console.warn('Could not load localStorage state:', err);
  }
  return validateState(inline);
}
function writeStateScript(){q('#state-json').textContent = JSON.stringify(state, null, 2).replace(/<\//g, '<\\/');}
function saveState(){
  try {
    writeStateScript();
    localStorage.setItem(KEY, JSON.stringify(state));
    renderSummaries();
  } catch (err) {
    console.error('Save state failed:', err);
  }
}
function debounceSave(){clearTimeout(saveTimer); saveTimer = setTimeout(saveState, 250);}
function allowedFor(field){
  if (field === 'status_category') return state.taxonomy.status_categories;
  if (field === 'completion_state') return state.taxonomy.completion_states;
  if (field === 'project_type') return state.taxonomy.project_types;
  if (field === 'priority_tier') return state.taxonomy.priority_tiers;
  return [];
}
function migrateValue(value, field, project){
  const allowed = allowedFor(field);
  if (!allowed.length || allowed.includes(value)) return value;
  const mapped = state.legacy_value_mapping[value];
  if (mapped && allowed.includes(mapped)) {
    project._badges = project._badges || [];
    project._badges.push(`${field}: mapped legacy value "${value}" to "${mapped}"`);
    console.warn('Mapped legacy value', {id: project.id, field, from: value, to: mapped});
    return mapped;
  }
  project._badges = project._badges || [];
  project._badges.push(`${field}: unknown value "${value}"; defaulted to "${allowed[0]}"`);
  console.warn('Unknown controlled value', {id: project.id, field, value, fallback: allowed[0]});
  return allowed[0];
}
function validateState(input){
  const next = clone(input);
  next.projects.forEach(project => {
    project._badges = [];
    ['status_category','completion_state','project_type','priority_tier'].forEach(field => { project[field] = migrateValue(project[field], field, project); });
    project.progress_percent = Math.max(0, Math.min(100, Number(project.progress_percent || 0)));
    project.microtasks = project.microtasks || {};
    next.taxonomy.microtasks.forEach(name => { project.microtasks[name] = Boolean(project.microtasks[name]); });
    project.classification_history = project.classification_history || project.history_log || [];
    project.history_log = project.history_log || project.classification_history || [];
    if (project.id === 'R03' && project.completion_state === 'Not Started') {
      project.completion_state = 'Revision in Progress';
      project._badges.push('BIODIV-AUTO corrected from Not Started to Revision in Progress.');
      console.warn('BIODIV-AUTO cannot export as Not Started; corrected R03.');
    }
  });
  return next;
}
function optionList(values, selected){return values.map(value => `<option value="${escapeHTML(value)}" ${value === selected ? 'selected' : ''}>${escapeHTML(value)}</option>`).join('');}
function projectById(id){return state.projects.find(p => p.id === id);}
function filteredProjects(){
  const term = q('#searchBox').value.trim().toLowerCase();
  const status = q('#statusFilter').value;
  const completion = q('#completionFilter').value;
  const type = q('#typeFilter').value;
  const priority = q('#priorityFilter').value;
  const sort = q('#sortSelect').value;
  const priorityOrder = Object.fromEntries(state.taxonomy.priority_tiers.map((p,i)=>[p,i]));
  const statusOrder = Object.fromEntries(state.taxonomy.status_categories.map((p,i)=>[p,i]));
  let rows = state.projects.filter(p => {
    const blob = JSON.stringify(p).toLowerCase();
    return (!term || blob.includes(term)) && (!status || p.status_category === status) && (!completion || p.completion_state === completion) && (!type || p.project_type === type) && (!priority || p.priority_tier === priority);
  });
  rows.sort((a,b) => {
    if (sort === 'title') return a.title.localeCompare(b.title);
    if (sort === 'status') return statusOrder[a.status_category] - statusOrder[b.status_category] || a.title.localeCompare(b.title);
    if (sort === 'progress') return Number(b.progress_percent) - Number(a.progress_percent) || a.title.localeCompare(b.title);
    if (sort === 'last_updated') return String(b.last_updated).localeCompare(String(a.last_updated)) || a.title.localeCompare(b.title);
    return priorityOrder[a.priority_tier] - priorityOrder[b.priority_tier] || a.title.localeCompare(b.title);
  });
  return rows;
}
function renderFilters(){
  q('#statusFilter').innerHTML = '<option value="">All statuses</option>' + optionList(state.taxonomy.status_categories, '');
  q('#completionFilter').innerHTML = '<option value="">All completion states</option>' + optionList(state.taxonomy.completion_states, '');
  q('#typeFilter').innerHTML = '<option value="">All project types</option>' + optionList(state.taxonomy.project_types, '');
  q('#priorityFilter').innerHTML = '<option value="">All priorities</option>' + optionList(state.taxonomy.priority_tiers, '');
}
function editableField(p, field, label, wide=false){return `<div class="field ${wide ? 'wide' : ''}"><label>${escapeHTML(label)}</label><div contenteditable="true" data-id="${escapeHTML(p.id)}" data-field="${escapeHTML(field)}">${escapeHTML(p[field])}</div></div>`;}
function cardHTML(p){
  const badges = (p._badges || []).map(b => `<span class="pill badge">${escapeHTML(b)}</span>`).join('');
  const micro = state.taxonomy.microtasks.map(name => `<label><input type="checkbox" data-id="${escapeHTML(p.id)}" data-task="${escapeHTML(name)}" ${p.microtasks[name] ? 'checked' : ''}> ${escapeHTML(name)}</label>`).join('');
  return `<article class="project-card" data-id="${escapeHTML(p.id)}" data-status-category="${escapeHTML(p.status_category)}"><div class="card-top"><label class="done-wrap" title="Done / archived"><input type="checkbox" data-id="${escapeHTML(p.id)}" data-field="done_archived" ${p.done_archived ? 'checked' : ''}></label><div><div class="idline"><span class="pid">${escapeHTML(p.id)}</span><span class="pill status">${escapeHTML(p.status_category)}</span><span class="pill type">${escapeHTML(p.project_type)}</span><span class="pill priority">${escapeHTML(p.priority_tier)}</span>${badges}</div><h3 class="card-title" contenteditable="true" data-id="${escapeHTML(p.id)}" data-field="title">${escapeHTML(p.title)}</h3></div></div><div class="grid"><div class="field"><label>Status Category</label><select data-id="${escapeHTML(p.id)}" data-field="status_category">${optionList(state.taxonomy.status_categories, p.status_category)}</select></div><div class="field"><label>Completion State</label><select data-id="${escapeHTML(p.id)}" data-field="completion_state">${optionList(state.taxonomy.completion_states, p.completion_state)}</select></div><div class="field"><label>Project Type</label><select data-id="${escapeHTML(p.id)}" data-field="project_type">${optionList(state.taxonomy.project_types, p.project_type)}</select></div><div class="field"><label>Priority Tier</label><select data-id="${escapeHTML(p.id)}" data-field="priority_tier">${optionList(state.taxonomy.priority_tiers, p.priority_tier)}</select></div><div class="field wide"><label>Progress</label><div class="progress-row"><input type="range" min="0" max="100" value="${Number(p.progress_percent)}" data-id="${escapeHTML(p.id)}" data-field="progress_percent"><output>${Number(p.progress_percent)}%</output></div></div>${editableField(p,'authors_or_owner','Authors / Owner')}${editableField(p,'outlet_or_target','Outlet / Target')}${editableField(p,'current_stage','Current Stage',true)}${editableField(p,'next_concrete_action','Next Concrete Action',true)}${editableField(p,'deadline_or_trigger','Deadline / Trigger')}${editableField(p,'last_updated','Last Updated')}${editableField(p,'notes','Notes',true)}${editableField(p,'provenance','Provenance',true)}${editableField(p,'related_files','Related Files',true)}${editableField(p,'related_links','Related Links',true)}${editableField(p,'open_questions','Open Questions',true)}</div><div class="microtasks">${micro}</div></article>`;
}
function renderSections(){
  const rows = filteredProjects();
  const byCat = Object.fromEntries(state.taxonomy.status_categories.map(c => [c, []]));
  rows.forEach(p => { if (byCat[p.status_category]) byCat[p.status_category].push(p); });
  q('#sections').innerHTML = state.taxonomy.status_categories.map(cat => {
    const cards = byCat[cat];
    return `<section class="status-section" data-section="${escapeHTML(cat)}"><div class="section-head"><h2>${escapeHTML(cat)}</h2><span class="section-count">${cards.length}</span></div>${cards.length ? `<div class="cards">${cards.map(cardHTML).join('')}</div>` : '<div class="empty">No projects currently match this section and filter combination.</div>'}</section>`;
  }).join('');
  renderSummaries();
}
function renderSummaries(){
  const counts = new Map(state.taxonomy.status_categories.map(cat => [cat, 0]));
  state.projects.forEach(p => counts.set(p.status_category, (counts.get(p.status_category) || 0) + 1));
  q('#kpiBody').innerHTML = [...counts.entries()].map(([cat,n]) => `<tr><td>${escapeHTML(cat)}</td><td class="num">${n}</td></tr>`).join('') + `<tr class="total-row"><td>Total tracked items</td><td class="num">${state.projects.length}</td></tr>`;
  const priorityOrder = Object.fromEntries(state.taxonomy.priority_tiers.map((p,i)=>[p,i]));
  const queue = state.projects.filter(p => ['P0 (this week)','P1 (this month)'].includes(p.priority_tier) && !p.done_archived).sort((a,b)=>priorityOrder[a.priority_tier]-priorityOrder[b.priority_tier] || b.progress_percent-a.progress_percent).slice(0,14);
  q('#queueBody').innerHTML = queue.map(p => `<tr><td>${escapeHTML(p.id)}</td><td>${escapeHTML(p.title)}<br><span class="muted small">${escapeHTML(p.priority_tier)} · ${escapeHTML(p.status_category)}</span></td><td>${escapeHTML(p.next_concrete_action)}</td></tr>`).join('') || '<tr><td colspan="3" class="muted">No active priority items.</td></tr>';
  const open = state.projects.filter(p => String(p.open_questions || '').trim()).slice(0,20);
  q('#openQuestionsBody').innerHTML = open.map(p => `<tr><td>${escapeHTML(p.id)}</td><td>${escapeHTML(p.open_questions)}</td></tr>`).join('') || '<tr><td colspan="2" class="muted">No open questions recorded.</td></tr>';
  q('#excludedList').innerHTML = state.excluded_items.map(x => `<li>${escapeHTML(x)}</li>`).join('');
  const history = [];
  state.projects.forEach(p => (p.classification_history || []).forEach(h => history.push({project:p, h})));
  history.sort((a,b)=>String(b.h.date).localeCompare(String(a.h.date)) || a.project.id.localeCompare(b.project.id));
  q('#historyList').innerHTML = history.length ? `<table><thead><tr><th>Date</th><th>ID</th><th>From</th><th>To</th><th>Reason</th></tr></thead><tbody>${history.slice(0,60).map(row => `<tr><td>${escapeHTML(row.h.date)}</td><td>${escapeHTML(row.project.id)}</td><td>${escapeHTML(row.h.from_status)}</td><td>${escapeHTML(row.h.to_status)}</td><td>${escapeHTML(row.h.reason)}</td></tr>`).join('')}</tbody></table>` : '<p class="muted">No classification changes recorded yet.</p>';
  q('#provenanceBox').textContent = `${state.metadata.built_by} · schema ${state.metadata.schema_version}\nSource JSON: ${state.metadata.source_json}\nSource HTML: ${state.metadata.source_html}\nLocalStorage key: ${KEY}`;
}
function updateProjectFromElement(el){
  const p = projectById(el.dataset.id);
  if (!p) return;
  const field = el.dataset.field;
  if (!field) return;
  if (el.type === 'checkbox') p[field] = el.checked;
  else if (el.type === 'range') p[field] = Number(el.value);
  else if (el.tagName === 'SELECT') p[field] = el.value;
  else p[field] = el.innerText;
}
function handleInput(ev){
  const el = ev.target;
  if (el.matches('#searchBox')) { renderSections(); return; }
  if (el.matches('[data-field]')) { updateProjectFromElement(el); debounceSave(); }
}
function handleChange(ev){
  const el = ev.target;
  if (el.matches('#statusFilter,#completionFilter,#typeFilter,#priorityFilter,#sortSelect')) { renderSections(); return; }
  if (el.matches('[data-task]')) {
    const p = projectById(el.dataset.id);
    if (!p) return;
    p.microtasks[el.dataset.task] = el.checked;
    saveState();
    return;
  }
  if (el.matches('[data-field]')) {
    const p = projectById(el.dataset.id);
    if (!p) return;
    const oldStatus = p.status_category;
    updateProjectFromElement(el);
    if (el.type === 'range') {
      const out = el.parentElement.querySelector('output');
      if (out) out.textContent = el.value + '%';
    }
    if (el.dataset.field === 'status_category' && p.status_category !== oldStatus) {
      const note = prompt('Optional note for status-category change:', 'Reclassified in weekly operating dashboard.');
      const entry = {date: new Date().toISOString().slice(0,10), from_status: oldStatus, to_status: p.status_category, reason: note || 'Status category changed in dashboard.'};
      p.classification_history = p.classification_history || [];
      p.history_log = p.history_log || [];
      p.classification_history.push(entry);
      p.history_log.push(entry);
    }
    saveState();
    if (['status_category','completion_state','project_type','priority_tier','done_archived'].includes(el.dataset.field)) renderSections();
  }
}
function readDOMIntoState(){
  qa('.project-card').forEach(card => {
    qa('[data-field]', card).forEach(updateProjectFromElement);
    qa('[data-task]', card).forEach(el => {
      const p = projectById(el.dataset.id);
      if (p) p.microtasks[el.dataset.task] = el.checked;
    });
  });
}
function collect(){
  readDOMIntoState();
  state = validateState(state);
  writeStateScript();
  return state;
}
function applyStateToDOMForExport(){
  readDOMIntoState();
  state = validateState(state);
  writeStateScript();
  document.querySelectorAll('.project-card').forEach(card => {
    card.querySelectorAll('[data-field]').forEach(el => {
      if (el.type === 'checkbox') {
        if (el.checked) el.setAttribute('checked', 'checked');
        else el.removeAttribute('checked');
      } else if (el.tagName === 'SELECT') {
        el.querySelectorAll('option').forEach(opt => {
          if (opt.value === el.value) opt.setAttribute('selected', 'selected');
          else opt.removeAttribute('selected');
        });
      } else if (el.type === 'range') {
        el.setAttribute('value', el.value);
        const out = el.parentElement.querySelector('output');
        if (out) out.textContent = el.value + '%';
      } else if (el.isContentEditable) {
        el.textContent = el.innerText;
      } else if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.setAttribute('value', el.value);
        if (el.tagName === 'TEXTAREA') el.textContent = el.value;
      }
    });
    card.querySelectorAll('[data-task]').forEach(el => {
      if (el.checked) el.setAttribute('checked', 'checked');
      else el.removeAttribute('checked');
    });
  });
}
function exportHTML(){
  try {
    saveState();
    applyStateToDOMForExport();
    const cloneDoc = document.documentElement.cloneNode(true);
    const html = '<!doctype html>\n' + cloneDoc.outerHTML;
    download(EXPORT_HTML_NAME, html, 'text/html;charset=utf-8');
  } catch (err) {
    console.error('Export HTML failed:', err);
    alert('Export edited HTML failed. Open DevTools Console for details.');
  }
}
function exportJSON(){
  try {
    const json = JSON.stringify(collect(), null, 2);
    download(EXPORT_JSON_NAME, json, 'application/json;charset=utf-8');
  } catch (err) {
    console.error('Export JSON failed:', err);
    alert('Export JSON failed. Open DevTools Console for details.');
  }
}
function download(name, content, type){
  try {
    const blob = new Blob([content], { type: type || 'application/octet-stream' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name;
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 1000);
  } catch (err) {
    console.error('Download failed:', err);
    alert('Download failed. Open DevTools Console for details.');
  }
}
function importJSON(file){
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      const data = JSON.parse(ev.target.result);
      state = validateState(data);
      saveState();
      renderFilters();
      renderSections();
    } catch (err) {
      console.error('Import JSON failed:', err);
      alert('Import JSON failed. Check console for details.');
    }
  };
  reader.readAsText(file);
}
function resetLocal(){
  if (confirm('Reset local edits for this dashboard? Exported HTML/JSON files are not affected.')) {
    localStorage.removeItem(KEY);
    location.reload();
  }
}
function init(){
  state = loadState();
  renderFilters();
  renderSections();
  document.addEventListener('input', handleInput);
  document.addEventListener('change', handleChange);
  q('#exportJSONBtn').addEventListener('click', exportJSON);
  q('#exportHTMLBtn').addEventListener('click', exportHTML);
  q('#importJSONBtn').addEventListener('click', () => q('#importFile').click());
  q('#importFile').addEventListener('change', ev => { if (ev.target.files[0]) importJSON(ev.target.files[0]); ev.target.value = ''; });
  q('#resetBtn').addEventListener('click', resetLocal);
  q('#printBtn').addEventListener('click', () => window.print());
  saveState();
}
document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>
'''


def render_html(state: dict) -> str:
    state_json = json.dumps(state, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return HTML_TEMPLATE.replace("@@STATE_JSON@@", state_json)


def write_reports(state: dict, counts: Counter, corrections: list[str], warnings: list[str], out_dir: Path, source_json: Path, source_html: Path) -> dict[str, Path]:
    paths = {
        "html": out_dir / f"{BASE}_INTERACTIVE.html",
        "json": out_dir / f"{BASE}_STATE.json",
        "changelog": out_dir / f"{BASE}_CHANGELOG.md",
        "report": out_dir / f"{BASE}_CHANGES.qmd",
    }
    paths["json"].write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    paths["html"].write_text(render_html(state), encoding="utf-8", newline="\n")

    counts_lines = "\n".join(f"- {cat}: {counts.get(cat, 0)}" for cat in STATUS_CATEGORIES)
    correction_lines = "\n".join(f"- {line}" for line in corrections)
    warning_lines = "\n".join(f"- {line}" for line in warnings) if warnings else "- No invalid controlled values remained after deterministic migration."

    changelog = f"""# CGPT PVB Master Research Portfolio Dashboard v4 Changelog

Date: {TODAY}
Builder: CGPT Codex
Source JSON: `{source_json}`
Source HTML inspected: `{source_html}`

## Outputs

- `{paths['html'].name}`
- `{paths['json'].name}`
- `{paths['changelog'].name}`
- `{paths['report'].name}`

## Changes

- Built a new non-linear operating taxonomy with 12 current-state categories.
- Added Working Paper Completed and classified D07 as the test working-paper category item with an open verification question.
- Split manuscript, software/app, teaching, data/replication, service, and administrative categories.
- Hardened export/import with `applyStateToDOMForExport()` before `cloneNode()`, state JSON refresh before export, try/catch wrappers, and robust download handling.
- Preserved local autosave through an artifact-specific `localStorage` key.
- Fixed BIODIV-AUTO status mismatch by moving R03 from Not Started to Revision in Progress.
- Preserved CV errata corrections and named correction rules from the dispatch.
- Added open-questions handling for BBUS 490 vs BUS 499 and ambiguous working-paper candidates.
- Added classification-history logic so projects can move among statuses without implying a one-way pipeline.
- Used `CGPT_` filename prefix per user request.

## Category Counts

{counts_lines}

## Data Corrections Applied

{correction_lines}

## Legacy Mapping Notes

{warning_lines}
"""
    paths["changelog"].write_text(changelog, encoding="utf-8", newline="\n")

    report = f"""---
title: "CGPT PVB Master Research Portfolio Dashboard v4 Change Report"
date: "{TODAY}"
author: "CGPT Codex"
format: html
---

# Build Summary

Built a CGPT-named v4 interactive HTML dashboard from the user-edited June 2026 dashboard JSON. The new artifact treats status categories as non-linear operating states, not a publication pipeline. JSON is the canonical state; HTML is the editable interface.

# Source Files

| Role | Path |
|---|---|
| Source state JSON | `{source_json}` |
| Source edited HTML inspected | `{source_html}` |
| Dispatch / skill context | `PVB_Portfolio_Dashboard_v4_INTERACTIVE_DISPATCH.md`; `portfolio-dashboard-interactive-SKILL.md`; `interactive-html-export-hardening-SKILL.md` |

# Output Files

| Artifact | Filename |
|---|---|
| Interactive HTML | `{paths['html'].name}` |
| Canonical v4 state JSON | `{paths['json'].name}` |
| Changelog | `{paths['changelog'].name}` |
| QMD-style report | `{paths['report'].name}` |

# Taxonomy Result

| Status category | Count |
|---|---:|
"""
    for cat in STATUS_CATEGORIES:
        report += f"| {cat} | {counts.get(cat, 0)} |\n"
    report += f"""
# Data Correction Log

{correction_lines}

# Validation Checklist

| # | Check | Status |
|---:|---|---|
| 1 | `node --check` on extracted script block | Pending final validation |
| 2 | Browser file load from `file:///` | Pending final validation |
| 3 | Search, filters, and sort | Implemented; pending browser validation |
| 4 | KPI counts update after state changes | Implemented; pending browser validation |
| 5 | localStorage autosave | Implemented; pending browser validation |
| 6 | Export JSON includes every project | Implemented; pending validation |
| 7 | Import JSON updates the UI | Implemented; pending browser validation |
| 8 | Export edited HTML calls `applyStateToDOMForExport()` before `cloneNode()` | Implemented; pending script scan |
| 9 | Exported HTML preserves controls through embedded state JSON and DOM attributes | Implemented; pending browser validation |
| 10 | BIODIV-AUTO does not export as Not Started | Implemented; pending state scan |
| 11 | Working Paper Completed appears as a category | Implemented; pending state scan |
| 12 | No external dependencies | Implemented; pending source scan |
| 13 | Reclassification records history | Implemented; pending browser validation |
| 14 | Unknown status values warn and badge | Implemented; pending browser validation |

# Open Questions Preserved

- ICBSC course code remains unresolved: BBUS 490 vs BUS 499.
- D07 is placed in Working Paper Completed to exercise the new category, but the state records an open question to verify whether the 2022 draft is submission-ready or should return to dormant/teaching-note status.
- A03 and A04 remain Active Manuscript Development pending stronger evidence that either is a complete working paper.
- VISPUR scope remains unresolved: manuscript component vs separate methods paper.

# Notes For Next Update

Use the JSON export as the archive. Avoid hand-editing the HTML unless debugging interface behavior. Reclassification notes are stored in `classification_history` and mirrored to `history_log` for compatibility with the dispatch schema.
"""
    paths["report"].write_text(report, encoding="utf-8", newline="\n")
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-json", default=r"C:\Users\sundar\OneDrive - UW\Documents\GitHub\REPORTS\PVB_research_dashboard_june2026_edits.json")
    parser.add_argument("--source-html", default=r"C:\Users\sundar\OneDrive - UW\Documents\GitHub\REPORTS\PVB_research_dashboard_june2026_EDITED.html")
    parser.add_argument("--out-dir", default=r"C:\tmp\cgpt_pvb_dashboard_v4")
    args = parser.parse_args()

    source_json = Path(args.source_json)
    source_html = Path(args.source_html)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    source = json.loads(source_json.read_text(encoding="utf-8-sig"))
    projects, corrections, warnings = transform_projects(source)
    state = state_object(projects, corrections, source_json, source_html)
    counts = Counter(project["status_category"] for project in projects)
    paths = write_reports(state, counts, corrections, warnings, out_dir, source_json, source_html)

    for label, path in paths.items():
        print(f"{label}: {path} ({path.stat().st_size} bytes)")
    print(f"project_count: {len(projects)}")
    print("category_counts:", json.dumps(dict(counts), ensure_ascii=False, sort_keys=True))
    if warnings:
        print("warnings:", json.dumps(warnings, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
