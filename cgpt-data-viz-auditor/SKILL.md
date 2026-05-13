---
name: cgpt-data-viz-auditor
description: Audit statistical figures, charts, maps, and plotting code for accessibility, labels, color, export quality, and academic journal readiness. Use when reviewing ggplot2, matplotlib, rendered figures, manuscript graphics, maps, or multi-figure submissions before delivery or journal submission.
---

# CGPT Data Viz Auditor

Use this skill to review figures that already exist as code or rendered artifacts. The goal is a concrete audit with specific fixes, not a general design critique.

## Scope

Audit:

- ggplot2, matplotlib, seaborn, base R, and static exported figures.
- Manuscript figures, tables-as-figures, multi-panel plots, diagrams, and maps.
- Accessibility and color reliability, including color vision deficiency and contrast.
- Journal readiness for marketing, management, social science, and policy-style submissions.
- UW-branded charts when the project calls for UW styling.

Do not use this skill to invent new statistical analyses. If the final artifact is DOCX, PPTX, PDF, HTML, or a rendered report, hand off final structural/output validation to `cgpt-render-check`.

## Audit Workflow

1. Identify target venue, medium, and final size when known: journal, slide, report, web, single-column, double-column, print, or screen.
2. Inspect the source code and/or rendered image.
3. Check labels, accessibility, color, layout, journal/export requirements, and figure numbering/captions.
4. Provide PASS/WARN/FAIL with prioritized issues and exact code or artifact fixes.
5. If code was changed, render the figure again when feasible.
6. Run or recommend `cgpt-render-check` on the final containing artifact.

## Core Checklist

### Labels And Text

- Axis titles are present and include units or scale transformations.
- Tick labels are readable at final size and do not overlap.
- Legends have descriptive titles and human-readable entries.
- Panel labels are consistent and referenced correctly in the caption.
- Captions belong in the manuscript or report unless the target format requires embedded text.
- Minimum print readability: 8 pt for minor labels, 10 pt or larger for axis titles and legends.

### Color And Accessibility

- Palette is colorblind-safe; prefer viridis, Okabe-Ito, or vetted Brewer palettes.
- Color is not the only encoding for categories; add shape, linetype, direct labels, pattern, or faceting.
- Data marks, labels, and map boundaries have sufficient contrast against the background.
- Avoid rainbow/jet palettes, red-green-only comparisons, and default hue scales for many groups.
- For UW work, follow `uw-accessibility`: exact UW colors, Spirit Gold decorative only, and no color-only meaning.

### Layout And Interpretation

- Plot has a clear visual hierarchy and enough margins; labels are not clipped.
- Aspect ratio is appropriate for the venue.
- Gridlines are lighter than data marks.
- Multi-panel figures use consistent scales, labels, themes, and legend treatment unless differences are intentional.
- Direct labels are preferred when they reduce legend lookup.
- The figure supports one clear takeaway; remove decoration that competes with data.

### Journal And Export Standards

- Export is at least 300 DPI for print; use 600 DPI for line art when required.
- Vector PDF/SVG/EPS is preferred for line charts and diagrams when accepted.
- Raster PNG/TIFF dimensions match target column width and file-size limits.
- Fonts are embedded or standard enough for the submission pipeline.
- Figure numbering, captions, and in-text references match the manuscript.
- Do not rely on low-resolution screenshots for submission graphics.

### Maps And Spatial Figures

- Include a legend, scale bar or clear scale context, projection/CRS when relevant, and data source note.
- Choropleth bins are meaningful, labeled, and not misleading.
- Missing data is explicitly encoded and labeled.
- Avoid map projections or color ramps that distort the intended comparison.
- Boundary lines, labels, and overlays remain legible at final size.

## Common Fixes

For ggplot2:

```r
scale_color_viridis_d(option = "D")
scale_fill_viridis_d(option = "D")
labs(x = "Year", y = "Revenue (USD millions)", color = "Segment")
theme_minimal(base_size = 11) +
  theme(panel.grid.minor = element_blank(),
        legend.position = "bottom")
ggsave("figure-1.tiff", width = 7, height = 5, dpi = 300, compression = "lzw")
```

For matplotlib:

```python
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
})
fig.savefig("figure-1.pdf", bbox_inches="tight")
fig.savefig("figure-1.png", dpi=300, bbox_inches="tight")
```

## Report Format

Use a compact result:

```text
Status: PASS/WARN/FAIL
Figure(s): path or identifier
Critical issues: count and short list
Recommended fixes: exact changes
Verification: rendered/inspected, plus final cgpt-render-check status or handoff
```

## Rules

- Ground findings in visible evidence or source code.
- Separate accessibility failures from style preferences.
- Do not silently change the statistical meaning of a plot.
- When a chart is embedded in a larger deliverable, finish with `cgpt-render-check` on that deliverable.
