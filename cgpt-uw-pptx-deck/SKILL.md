---
name: cgpt-uw-pptx-deck
description: Build, rebuild, polish, audit, render, or export University of Washington and UW Bothell PowerPoint decks. Use for UW-branded PPTX work, academic talks, stakeholder briefings, teaching decks, manuscript-to-deck conversions, slide visual QA, UW colors, Block W cover slides, accessibility checks, or requests to make a deck look presentation-ready.
---

# CGPT UW PPTX Deck

Use this skill to create or revise UW-styled PowerPoint decks that are grounded in source material, readable in a room, and visually stronger than a default template.

Use the Presentations plugin/skill for actual `.pptx` creation, editing, rendering, and export. If the deck is built from a manuscript or report and the numbers are not already verified, run `cgpt-presentation-prep` first.

## First Moves

1. Confirm purpose, audience, talk length, venue, source files, required output path, and whether the deliverable is PPTX only or PPTX plus PDF/images.
2. If editing an existing deck or template, inspect it before changing layouts. Preserve useful master layouts, official marks, and project-specific conventions.
3. Extract source-backed claims and numbers before designing slides. Do not estimate values from memory.
4. Choose a design mode:
   - UW Standard: formal institutional, stakeholder, teaching, dean/admin, or data-heavy decks.
   - Diagram-Forward: theory-heavy, conceptual, research-story, or teaching decks where the visual should carry the argument.
5. If the user did not choose a mode, ask only when the choice materially affects the deck. Otherwise default to UW Standard.

## UW Brand Rules

- Use official UW logo assets only. Preserve proportions, clear space, and original colors.
- Cover slides should include the talk title, then presenter name, title/affiliation, and email directly below or near the title block.
- Default identity when not otherwise specified: P. V. (Sundar) Balakrishnan; Professor, University of Washington Bothell, School of Business; sundar@uw.edu.
- Use 16:9 widescreen unless the user or venue requires another aspect ratio.
- Prefer Office-safe fonts for PPTX: Arial for headings and Calibri/Aptos for body.
- Use exact UW colors:
  - Spirit Purple `#4B2E83`
  - Husky Purple `#32006E`
  - Husky Gold/screen cream `#E8E3D3`
  - Heritage Gold `#85754D`
  - Spirit Gold `#FFC700` as decoration only
- Never use Spirit Gold as text or as a text background.
- Do not rely on color alone for meaning; pair color with labels, shape, position, or pattern.

## Slide Design Rules

- PPTX is the primary deliverable unless the user asks for another format.
- Every content slide needs one message, stated as an assertion in the title.
- Every content slide needs a dominant visual object: chart, table, diagram, image, model, equation, map, process, or callout system.
- Avoid text-only slides. If a slide is only bullets, redesign it.
- Keep body text as guideposts, not prose. A good default is at most four short fragments per slide.
- No text anywhere on a slide below 16 pt, including labels, footers, source notes, and diagram annotations.
- Do not shrink overloaded content to fit. Split the slide, shorten wording, move detail to notes, or use progressive slides.
- Reserve title space before placing objects below it. Check wrapped titles in the rendered deck.
- Use separate progressive slides for builds instead of fragile animation when the sequence matters.

## Design Modes

### UW Standard

Use for polished institutional decks.

- Lead with a warm gold-forward look and restrained Spirit Purple accents.
- Use white or Husky Gold content backgrounds with purple titles and emphasis.
- Use purple title, divider, conclusion, or reference slides when formal bookends help.
- Use cards, stat callouts, tables, comparison panels, and clean typography.
- Keep layouts dense enough for working audiences, but not crowded.

### Diagram-Forward

Use when the slide's visual structure is the argument.

- Design the diagram before writing slide text.
- Pick the relationship type first: process, comparison, hierarchy, ecosystem, branching choice, matrix, transformation, timeline, or conceptual architecture.
- Prefer asymmetric layouts such as left diagram plus right callout, or full-width diagram with compact annotations.
- Keep content-slide palettes simple: Husky Gold or white background, Spirit Purple shapes/lines/titles, black body text, Spirit Gold only as thin decoration.
- Use UW bookends for title, section, closing, and references.

## Research And Quantitative Decks

- Every number must trace to a source table, manuscript sentence, dataset output, or generated figure.
- Convert manuscript tables into slide communication objects. Show only the rows and columns needed for the slide claim.
- Highlight the coefficient, cell, point, or contrast that proves the title.
- Direct-label chart series where possible. Do not make the legend carry the core message.
- For equations and derivations, use one major equation or derivation step per slide and pair it with a plain-English gloss.
- For complex models, regression tables, or equation staging, apply quantitative-slide-design principles: progressive builds, term annotation, consistent color meaning, and no competing complex visuals on the same slide.

## Verification

Before delivery:

1. Render or visually inspect the deck with the Presentations workflow or PowerPoint-compatible tooling.
2. Check for clipped text, overlap, missing images, broken fonts, unreadable labels, and title wrapping.
3. Verify the 16 pt text floor and title-zone spacing.
4. Verify UW color use and contrast, especially text inside purple or gold panels.
5. Confirm the cover identity block and UW mark are present when UW branding is expected.
6. Confirm all factual claims and numbers against source files.
7. Export PDF or slide images when requested, then inspect the exported artifact.

## Final Report

Report the exact PPTX path, any PDF/render path, source files used, validation performed, and any caveats about data, fonts, logos, or unverified claims.
