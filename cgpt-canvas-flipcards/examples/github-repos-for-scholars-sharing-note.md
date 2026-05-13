# Sharing Note: GitHub Repositories for Scholars Flipcards

This example demonstrates the `cgpt-canvas-flipcards` skill with a practical
teaching context: scholars learning what a GitHub repository is, why it is
useful, and how public versioned sharing can support transparent research.

## Included Artifact

- `study-flipcards-github-repos-for-scholars.html`

The HTML file is self-contained. It has no CDN dependencies, includes embedded
CSS and JavaScript, and can be opened locally, hosted from a static site, or
uploaded to Canvas Files.

## Teaching Use

The deck covers 10 cards across three categories:

- Core Concepts: repository, commit, README.
- Scholarly Value: transparency, reproducibility, citation and credit.
- Good Practice: license, do not share secrets, small clear files, release.

The goal is not to turn scholars into software engineers. The goal is to make
repository sharing legible as a scholarly communication practice: a place where
research materials, teaching examples, code, and documentation can be reviewed,
reused, cited, and improved.

## Canvas Embed Pattern

After uploading the HTML file to Canvas Files, use the Canvas file download URL
inside an iframe:

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

Replace `{COURSE_ID}` and `{FILE_ID}` with the real Canvas values after upload.

## Verification Notes

This example should be checked before sharing by confirming:

- the file exists and is non-empty;
- it contains `<html>`, `<style>`, and `<script>`;
- all cards include category, term, hint, definition, and example;
- category filters, shuffle, reset, print, and card flipping work in a browser.
