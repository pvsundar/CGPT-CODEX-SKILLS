---
name: cgpt-interactive-html-export-hardening
description: Harden self-contained editable HTML artifacts so export/import, localStorage, controls, and re-opened HTML round trips preserve user edits without JavaScript parse failures.
---

# CGPT Interactive HTML Export Hardening

Use this skill before building or repairing any single-file HTML artifact that lets the user edit in-browser and export JSON or a re-openable HTML file. Typical targets are dashboards, trackers, forms, configurators, and teaching tools.

## Core Rules

1. Treat JSON as canonical state and HTML as the interface. Provide both Export JSON and Import JSON.
2. Never put a raw newline inside a single-quoted or double-quoted JavaScript string. Use `\n` or template literals.
3. Call `applyStateToDOMForExport()` before `cloneNode()` or `outerHTML`.
4. Mirror runtime properties into attributes before serialization:
   - checkboxes: set/remove `checked`
   - selects: set `selected` on the chosen option only
   - ranges: set `value` and update adjacent output text
   - text inputs/textareas: set `value`, and set textarea text content
   - contenteditable nodes: write `innerText` back to `textContent`
5. Wrap export and download functions in `try/catch`; log with `console.error` and alert the user on failure.
6. Validate controlled dropdown values on load. If a stored value is not in the option set, map it through a legacy-value table, log a warning, and show a visible badge.
7. Autosave on `input` and `change` with a short debounce. Reset local edits by clearing the artifact-specific localStorage key only.
8. Clearing localStorage must not erase state already preserved in exported HTML.

## Required Pattern

```js
function applyStateToDOMForExport(){
  document.querySelectorAll('[data-field], [data-task]').forEach(el => {
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
      const out = el.parentElement && el.parentElement.querySelector('output');
      if (out) out.textContent = el.value + '%';
    } else if (el.isContentEditable) {
      el.textContent = el.innerText;
    } else if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      el.setAttribute('value', el.value);
      if (el.tagName === 'TEXTAREA') el.textContent = el.value;
    }
  });
}

function exportHTML(){
  try {
    saveState();
    applyStateToDOMForExport();
    const clone = document.documentElement.cloneNode(true);
    const html = '<!doctype html>\n' + clone.outerHTML;
    download('artifact_EDITED.html', html, 'text/html;charset=utf-8');
  } catch (err) {
    console.error('Export HTML failed:', err);
    alert('Export edited HTML failed. Open DevTools Console for details.');
  }
}

function exportJSON(){
  try {
    const json = JSON.stringify(collect(), null, 2);
    download('artifact_STATE.json', json, 'application/json;charset=utf-8');
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
```

## Validation

Before reporting done:

- Extract the inline script block and run `node --check`.
- Open the HTML from `file:///` when practical and check the console.
- Change a checkbox, select, range, and editable text field; export HTML; reopen in a fresh browser context; confirm all four changes persist.
- Export JSON, edit one field, import it, and verify the UI updates.
- Clear localStorage and reopen the exported HTML; preserved exported state should remain visible.
- Test an invalid dropdown value; the page should warn, map, and badge the affected card or control.
