---
name: cgpt-canvas-flipcards
description: Create self-contained HTML study flipcards and Canvas LMS embed instructions for teaching modules. Use when the user asks for flip cards, study cards, interactive HTML review tools, Canvas iframe embeds, or troubleshooting Canvas pages that strip JavaScript.
---

# CGPT Canvas Flipcards

Use this skill to build standalone HTML flipcard study tools and package them for Canvas. The output should work as a local HTML file and as a Canvas file-download iframe.

## Canvas Constraint

Canvas may strip `<script>` tags from Rich Content Editor pages and file previews. Do not tell the user to paste the full interactive HTML into a Canvas page body. Instead:

- upload the `.html` file to Canvas Files
- use the `/download` URL in an iframe
- provide a direct full-screen download link as fallback

## Workflow

1. Gather topic, course, audience, number of cards, source material, and whether Canvas embed code is needed.
2. Create a self-contained HTML file with no CDN dependencies.
3. Use 8-15 cards for a normal session unless the user requests otherwise.
4. Each card should have:
   - category
   - term
   - hint
   - definition
   - example
5. Include category filters, shuffle, reset, progress, and print-friendly CSS when feasible.
6. Verify the HTML file exists, contains normal document structure, and has no external dependencies unless explicitly allowed.

## Card Quality

- Keep hints short and non-revealing.
- Definitions should be precise and student-facing.
- Examples should be concrete and domain-relevant.
- Avoid long prose cards; split dense concepts.
- Use accessible colors, keyboard-focus styles, and responsive layout.

## Canvas Embed Pattern

After the user uploads the file and provides the Canvas file ID:

```html
<iframe src="/courses/{COURSE_ID}/files/{FILE_ID}/download"
        width="100%"
        height="850"
        style="border:1px solid #ccc; border-radius:8px;"
        allowfullscreen>
</iframe>

<p><a href="/courses/{COURSE_ID}/files/{FILE_ID}/download" target="_blank">
Open full-screen in a new tab
</a></p>
```

Do not hardcode a course ID unless the user provides or confirms it.

## File Naming

Use lowercase names:

```text
study-flipcards-{topic-slug}.html
```

For BUS490, use:

```text
bus490-{topic-slug}.html
```

## Verification

Before delivery:

- confirm the HTML file exists and is non-empty
- inspect for `<html>`, `<style>`, and `<script>`
- check that all cards have term, hint, definition, and example
- open with Browser when visual/interactivity verification is requested or practical
- provide exact local path and Canvas embed snippet

## Bundled Example

This repository includes a tested showcase example at:

```text
cgpt-canvas-flipcards/examples/study-flipcards-github-repos-for-scholars.html
```

Use the paired Markdown and HTML notes in the same folder when demonstrating
what the skill produces and how the artifact can be shared.
