#!/usr/bin/env Rscript
# ═══════════════════════════════════════════════════════════════════════════════
# pvb_format_text.R — Post-processor for Quarto/RMarkdown DOCX output
# ═══════════════════════════════════════════════════════════════════════════════
#
# PURPOSE:
#   Reformats all NON-TABLE paragraphs in a rendered .docx file to match the
#   PVB academic manuscript style (pvb-template-short.docx specifications).
#   Companion script to pvb_format_tables_v3.R, which handles tables only.
#
# USAGE:
#   Rscript pvb_format_text.R  input.docx  [output.docx]
#
#   If output.docx is omitted, overwrites input.docx in place.
#
# RECOMMENDED WORKFLOW:
#   1. quarto render manuscript.qmd --to docx
#   2. Rscript pvb_format_text.R   manuscript.docx  manuscript_styled.docx
#   3. Rscript pvb_format_tables_v3.R  manuscript_styled.docx  manuscript_final.docx
#
#   Or combine in a single pipeline (both scripts can overwrite in place):
#   1. quarto render manuscript.qmd --to docx
#   2. Rscript pvb_format_text.R   manuscript.docx
#   3. Rscript pvb_format_tables_v3.R  manuscript.docx
#
# WHAT IT DOES:
#   For every non-table paragraph, enforces the template specifications:
#
#   Title:          centered, bold, 14pt, no indent, 240tw after
#   Subtitle:       centered, 12pt, no indent, 80tw after
#   Author:         centered, 12pt, no indent, 80tw after
#   Date:           centered, 12pt, no indent, 240tw after
#   AbstractTitle:  centered, bold, 12pt, no indent, 240tw before
#   Abstract:       justified, 11pt, 0.5" L/R indent, no first-line indent
#   Heading 1:      centered, bold, 12pt, no indent, 120tw before/after
#   Heading 2:      left, bold, 12pt, no indent, 200tw before, 80tw after
#   Heading 3:      left, italic, 12pt, no indent, 200tw before, 80tw after
#   Heading 4:      left, bold+italic, 12pt, no indent, 160tw before, 80tw after
#   FirstParagraph: left, 12pt, 1.5× spacing, no first-line indent
#   BodyText:       left, 12pt, 1.5× spacing, 0.5" first-line indent
#   Normal:         left, 12pt, 1.5× spacing, 0.5" first-line indent
#   Bibliography:   justified, 11pt, 1.15× spacing, 0.5" hanging indent
#   Bibliography-JM:justified, 12pt, 1.15× spacing, 450tw hanging indent
#   Caption:        left, bold, 11pt, single spacing, no indent
#   TableCaption:   same as Caption + keepNext
#   PVBTableNote:   left, 10pt, italic, 1.15× spacing, 200tw after (breathing room before next body para)
#   Compact:        justified, 11pt, single spacing, 100tw L/R indent
#   FootnoteText:   justified, 10pt, single spacing
#
#   References section repair (Pass 5):
#     ✓ Detects "References" heading (last H1 with that text)
#     ✓ Walks all paragraphs until next H1 or end of body
#     ✓ Fixes orphaned references (Normal/BodyText → Bibliography style)
#     ✓ Configurable: REFS_STYLE selects Bibliography vs Bibliography-JM
#     ✓ Configurable: REFS_FORCE_UNIFORM can restyle ALL refs uniformly
#
#   Front-matter repair (Pass 6):
#     ✓ Detects Author/Date paragraphs before first heading
#     ✓ Quarto does not assign Author/Date pStyle; they arrive as Normal
#     ✓ Applies Author style (centered, 12pt) to short non-sentence lines
#
#   Page setup (sectPr):
#     ✓ Letter size (8.5" × 11")
#     ✓ Margins: top/bottom 1", left 0.875", right 0.9375"
#
# DOES NOT TOUCH:
#   - Anything inside <w:tbl> elements (tables handled by pvb_format_tables_v3.R)
#   - Images, drawings, or embedded objects
#   - Content of runs (text, significance stars, etc.)
#   - Existing bold/italic on inline runs UNLESS the style requires clearing it
#
# REQUIREMENTS:
#   install.packages(c("officer", "xml2"))
#
# CHANGELOG:
#   v1 (2026-02-23): Initial release — paragraph-level formatting enforcement,
#                     page setup, and run-level font/size/bold/italic cleanup.
#   v2 (2026-02-24): Bug fixes and enhancements:
#                     ✓ Fixed xml_children(body) bug in adjust_h2_after_h1(),
#                       repair_references_section(), and format_page_setup().
#                       docx_body_xml() returns <w:document> root, so
#                       xml_children() returned [<w:body>] instead of the
#                       actual paragraphs/tables.  All three functions now
#                       descend into <w:body> correctly.
#                     ✓ Added Subtitle to STYLE_SPECS (centered, 12pt).
#                     ✓ Added Pass 6: repair_front_matter() — detects Author
#                       and Date paragraphs that Quarto renders without pStyle
#                       and applies centered Author formatting.
#
# Author: Claude (for Dr. P.V. Sundar Balakrishnan)
# ═══════════════════════════════════════════════════════════════════════════════

library(officer)
library(xml2)

# ── OOXML namespace map ────────────────────────────────────────────────────────
NS <- c(w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main")

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION — extracted from pvb-template-short.docx
# ═══════════════════════════════════════════════════════════════════════════════

FONT_NAME <- "Calibri"

# Font sizes in half-points (Word convention: 12pt = 24hp, 11pt = 22hp, etc.)
SZ_12PT <- 24L
SZ_14PT <- 28L
SZ_11PT <- 22L
SZ_10PT <- 20L
SZ_9PT  <- 18L

# Line spacing (lineRule="auto"): 240 = single, 276 = 1.15×, 360 = 1.5×
LINE_SINGLE <- 240L
LINE_115    <- 276L
LINE_150    <- 360L

# Indentation in twips (1440tw = 1 inch; 720tw = 0.5 inch)
INDENT_HALF_INCH <- 720L

# ═══════════════════════════════════════════════════════════════════════════════
# BEHAVIOR TOGGLES
# ═══════════════════════════════════════════════════════════════════════════════

# Which bibliography spec to apply when fixing orphaned reference paragraphs
# (ones that lost their style during pandoc rendering and appear as Normal/
# BodyText/FirstParagraph inside the References section).
#
# Options:
#   "Bibliography"     — pandoc default: 11pt, 0.5" hanging, 120tw after
#   "Bibliography-JM"  — journal style:  12pt, 450tw hanging, no space after
#
REFS_STYLE <- "Bibliography"

# Force ALL paragraphs in the References section to REFS_STYLE, even those
# already tagged with a valid bibliography style.
# TRUE  = uniform style (recommended when switching to Bibliography-JM)
# FALSE = only fix paragraphs that lack a bibliography style (default)
REFS_FORCE_UNIFORM <- FALSE

# ═══════════════════════════════════════════════════════════════════════════════
# STYLE DEFINITIONS
# Each entry defines the expected formatting for a given Word style.
# Fields:
#   jc        = paragraph alignment ("both", "center", "left", "right")
#   line      = line spacing value (auto rule)
#   before    = space before in twips
#   after     = space after in twips
#   firstLine = first-line indent in twips (0 = none)
#   indLeft   = left indent in twips
#   indRight  = right indent in twips
#   hanging   = hanging indent in twips (overrides firstLine)
#   keepNext  = logical, keep with next paragraph
#   sz        = font size in half-points
#   bold      = TRUE/FALSE/NA (NA = don't touch)
#   italic    = TRUE/FALSE/NA (NA = don't touch)
# ═══════════════════════════════════════════════════════════════════════════════

STYLE_SPECS <- list(

  Title = list(
    jc = "center", line = LINE_115, before = 0L, after = 240L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = TRUE,
    sz = SZ_14PT, bold = TRUE, italic = FALSE
  ),

  Subtitle = list(
    jc = "center", line = LINE_115, before = 0L, after = 80L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = TRUE,
    sz = SZ_12PT, bold = FALSE, italic = FALSE
  ),

  Author = list(
    jc = "center", line = LINE_115, before = 0L, after = 80L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = TRUE,
    sz = SZ_12PT, bold = FALSE, italic = FALSE
  ),

  Date = list(
    jc = "center", line = LINE_115, before = 0L, after = 240L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = TRUE,
    sz = SZ_12PT, bold = FALSE, italic = FALSE
  ),

  AbstractTitle = list(
    jc = "center", line = LINE_115, before = 240L, after = 0L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = TRUE,
    sz = SZ_12PT, bold = TRUE, italic = FALSE
  ),

  Abstract = list(
    jc = "both", line = LINE_150, before = 80L, after = 240L,
    firstLine = 0L, indLeft = INDENT_HALF_INCH, indRight = INDENT_HALF_INCH,
    keepNext = FALSE,
    sz = SZ_11PT, bold = FALSE, italic = FALSE
  ),

  Heading1 = list(
    jc = "center", line = LINE_115, before = 120L, after = 120L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = TRUE,
    sz = SZ_12PT, bold = TRUE, italic = FALSE
  ),

  Heading2 = list(
    jc = "left", line = LINE_115, before = 200L, after = 80L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = TRUE,
    sz = SZ_12PT, bold = TRUE, italic = FALSE
  ),

  Heading3 = list(
    jc = "left", line = LINE_SINGLE, before = 200L, after = 80L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = TRUE,
    sz = SZ_12PT, bold = FALSE, italic = TRUE
  ),

  Heading4 = list(
    jc = "left", line = LINE_SINGLE, before = 160L, after = 80L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = TRUE,
    sz = SZ_12PT, bold = TRUE, italic = TRUE
  ),

  FirstParagraph = list(
    jc = "left", line = LINE_150, before = 0L, after = 0L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = FALSE,
    sz = SZ_12PT, bold = FALSE, italic = NA   # NA = preserve inline bold/italic
  ),

  BodyText = list(
    jc = "left", line = LINE_150, before = 0L, after = 0L,
    firstLine = INDENT_HALF_INCH, indLeft = 0L, indRight = 0L, keepNext = FALSE,
    sz = SZ_12PT, bold = FALSE, italic = NA
  ),

  Normal = list(
    jc = "left", line = LINE_150, before = 0L, after = 0L,
    firstLine = INDENT_HALF_INCH, indLeft = 0L, indRight = 0L, keepNext = FALSE,
    sz = SZ_12PT, bold = FALSE, italic = NA
  ),

  Bibliography = list(
    jc = "both", line = LINE_115, before = 0L, after = 120L,
    firstLine = 0L, indLeft = INDENT_HALF_INCH, indRight = 0L,
    hanging = INDENT_HALF_INCH, keepNext = FALSE,
    sz = SZ_11PT, bold = FALSE, italic = NA
  ),

  `Bibliography-JM` = list(
    jc = "both", line = LINE_115, before = 0L, after = 0L,
    firstLine = 0L, indLeft = 450L, indRight = 0L,
    hanging = 450L, keepNext = FALSE,
    sz = SZ_12PT, bold = FALSE, italic = NA
  ),

  Caption = list(
    jc = "left", line = LINE_SINGLE, before = 200L, after = 60L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = FALSE,
    sz = SZ_11PT, bold = TRUE, italic = FALSE
  ),

  TableCaption = list(
    jc = "left", line = LINE_SINGLE, before = 200L, after = 60L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = TRUE,
    sz = SZ_11PT, bold = TRUE, italic = FALSE
  ),

  ImageCaption = list(
    jc = "left", line = LINE_SINGLE, before = 200L, after = 60L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = FALSE,
    sz = SZ_11PT, bold = TRUE, italic = FALSE
  ),

  PVBTableNote = list(
    jc = "left", line = LINE_115, before = 60L, after = 200L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = FALSE,
    sz = SZ_10PT, bold = FALSE, italic = TRUE
  ),

  Compact = list(
    jc = "both", line = LINE_SINGLE, before = 60L, after = 0L,
    firstLine = 0L, indLeft = 100L, indRight = 100L, keepNext = FALSE,
    sz = SZ_11PT, bold = FALSE, italic = NA
  ),

  FootnoteText = list(
    jc = "both", line = LINE_SINGLE, before = 0L, after = 0L,
    firstLine = 0L, indLeft = 0L, indRight = 0L, keepNext = FALSE,
    sz = SZ_10PT, bold = FALSE, italic = NA
  ),

  Strong1 = list(
    jc = "both", line = LINE_150, before = 0L, after = 0L,
    firstLine = INDENT_HALF_INCH, indLeft = 0L, indRight = 0L, keepNext = FALSE,
    sz = SZ_12PT, bold = TRUE, italic = FALSE
  )
)


# ═══════════════════════════════════════════════════════════════════════════════
# XML HELPERS (shared pattern with pvb_format_tables_v3.R)
# ═══════════════════════════════════════════════════════════════════════════════

remove_if_exists <- function(parent, xpath) {
  node <- xml_find_first(parent, xpath, ns = NS)
  if (!inherits(node, "xml_missing")) xml_remove(node)
}

upsert_child <- function(parent, xpath, new_xml_str) {
  remove_if_exists(parent, xpath)
  xml_add_child(parent, read_xml(new_xml_str))
}

#' Set font name and size on an rPr element
set_font_props <- function(rPr, size_hp) {
  # w:eastAsia is explicit to prevent Word's theme font (Aptos in Office 365/2024)
  # from bleeding into the East Asian slot when only ascii/hAnsi/cs are set.
  upsert_child(rPr, "w:rFonts",
    sprintf('<w:rFonts w:ascii="%s" w:hAnsi="%s" w:cs="%s" w:eastAsia="%s" xmlns:w="%s"/>',
            FONT_NAME, FONT_NAME, FONT_NAME, FONT_NAME, NS["w"]))
  upsert_child(rPr, "w:sz",
    sprintf('<w:sz w:val="%d" xmlns:w="%s"/>', size_hp, NS["w"]))
  upsert_child(rPr, "w:szCs",
    sprintf('<w:szCs w:val="%d" xmlns:w="%s"/>', size_hp, NS["w"]))
}

#' Get the style ID from a paragraph's <w:pStyle> element
get_style_id <- function(p) {
  pPr <- xml_find_first(p, "w:pPr", ns = NS)
  if (inherits(pPr, "xml_missing")) return("Normal")
  pStyle <- xml_find_first(pPr, "w:pStyle", ns = NS)
  if (inherits(pStyle, "xml_missing")) return("Normal")
  xml_attr(pStyle, "val")
}

#' Ensure a pPr element exists on a paragraph
ensure_pPr <- function(p) {
  pPr <- xml_find_first(p, "w:pPr", ns = NS)
  if (inherits(pPr, "xml_missing")) {
    xml_add_child(p, read_xml(sprintf('<w:pPr xmlns:w="%s"/>', NS["w"])),
                  .where = 0)
    pPr <- xml_find_first(p, "w:pPr", ns = NS)
  }
  pPr
}

#' Ensure an rPr element exists on a run or inside pPr
ensure_rPr <- function(parent, where = 0) {
  rPr <- xml_find_first(parent, "w:rPr", ns = NS)
  if (inherits(rPr, "xml_missing")) {
    xml_add_child(parent, read_xml(sprintf('<w:rPr xmlns:w="%s"/>', NS["w"])),
                  .where = where)
    rPr <- xml_find_first(parent, "w:rPr", ns = NS)
  }
  rPr
}


# ═══════════════════════════════════════════════════════════════════════════════
# FORMAT ONE PARAGRAPH (the main workhorse)
# ═══════════════════════════════════════════════════════════════════════════════

format_paragraph <- function(p, spec) {

  pPr <- ensure_pPr(p)

  # ── 1. Paragraph alignment ──────────────────────────────────────────────────
  upsert_child(pPr, "w:jc",
    sprintf('<w:jc w:val="%s" xmlns:w="%s"/>', spec$jc, NS["w"]))

  # ── 2. Spacing ──────────────────────────────────────────────────────────────
  upsert_child(pPr, "w:spacing",
    sprintf(paste0(
      '<w:spacing w:line="%d" w:lineRule="auto"',
      ' w:before="%d" w:after="%d" xmlns:w="%s"/>'
    ), spec$line, spec$before, spec$after, NS["w"]))

  # ── 3. Indentation ─────────────────────────────────────────────────────────
  if (!is.null(spec$hanging) && spec$hanging > 0) {
    # Hanging indent (bibliography style)
    upsert_child(pPr, "w:ind",
      sprintf('<w:ind w:left="%d" w:right="%d" w:hanging="%d" xmlns:w="%s"/>',
              spec$indLeft, spec$indRight, spec$hanging, NS["w"]))
  } else {
    upsert_child(pPr, "w:ind",
      sprintf('<w:ind w:left="%d" w:right="%d" w:firstLine="%d" xmlns:w="%s"/>',
              spec$indLeft, spec$indRight, spec$firstLine, NS["w"]))
  }

  # ── 4. Keep with next ──────────────────────────────────────────────────────
  if (isTRUE(spec$keepNext)) {
    kn <- xml_find_first(pPr, "w:keepNext", ns = NS)
    if (inherits(kn, "xml_missing")) {
      xml_add_child(pPr, read_xml(sprintf('<w:keepNext xmlns:w="%s"/>', NS["w"])))
    }
  } else {
    remove_if_exists(pPr, "w:keepNext")
  }

  # ── 5. Paragraph-level rPr (default run properties) ────────────────────────
  pPr_rPr <- ensure_rPr(pPr)
  set_font_props(pPr_rPr, spec$sz)

  # Set bold at paragraph default level
  if (isTRUE(spec$bold)) {
    upsert_child(pPr_rPr, "w:b",  sprintf('<w:b xmlns:w="%s"/>',  NS["w"]))
    upsert_child(pPr_rPr, "w:bCs", sprintf('<w:bCs xmlns:w="%s"/>', NS["w"]))
  } else if (identical(spec$bold, FALSE)) {
    remove_if_exists(pPr_rPr, "w:b")
    remove_if_exists(pPr_rPr, "w:bCs")
  }

  # Set italic at paragraph default level
  if (isTRUE(spec$italic)) {
    upsert_child(pPr_rPr, "w:i",  sprintf('<w:i xmlns:w="%s"/>',  NS["w"]))
    upsert_child(pPr_rPr, "w:iCs", sprintf('<w:iCs xmlns:w="%s"/>', NS["w"]))
  } else if (identical(spec$italic, FALSE)) {
    remove_if_exists(pPr_rPr, "w:i")
    remove_if_exists(pPr_rPr, "w:iCs")
  }

  # Force black text at paragraph level
  upsert_child(pPr_rPr, "w:color",
    sprintf('<w:color w:val="000000" xmlns:w="%s"/>', NS["w"]))

  # ── 6. Format individual runs ──────────────────────────────────────────────
  runs <- xml_find_all(p, "w:r", ns = NS)
  for (r in runs) {
    rPr <- ensure_rPr(r)

    # Font and size
    set_font_props(rPr, spec$sz)

    # Bold: enforce for heading styles, strip for non-bold styles, preserve for NA
    if (isTRUE(spec$bold)) {
      upsert_child(rPr, "w:b",  sprintf('<w:b xmlns:w="%s"/>',  NS["w"]))
      upsert_child(rPr, "w:bCs", sprintf('<w:bCs xmlns:w="%s"/>', NS["w"]))
    } else if (identical(spec$bold, FALSE)) {
      remove_if_exists(rPr, "w:b")
      remove_if_exists(rPr, "w:bCs")
    }
    # bold = NA → don't touch (preserves intentional inline bold)

    # Italic: same logic
    if (isTRUE(spec$italic)) {
      upsert_child(rPr, "w:i",  sprintf('<w:i xmlns:w="%s"/>',  NS["w"]))
      upsert_child(rPr, "w:iCs", sprintf('<w:iCs xmlns:w="%s"/>', NS["w"]))
    } else if (identical(spec$italic, FALSE)) {
      remove_if_exists(rPr, "w:i")
      remove_if_exists(rPr, "w:iCs")
    }
    # italic = NA → don't touch (preserves intentional inline italic)

    # Clean up unwanted formatting
    remove_if_exists(rPr, "w:highlight")
    remove_if_exists(rPr, "w:shd")

    # Force black text color (remove any colored overrides from pandoc)
    # BUT preserve hyperlink coloring — check if parent style is Hyperlink
    rStyle <- xml_find_first(rPr, "w:rStyle", ns = NS)
    is_hyperlink <- FALSE
    if (!inherits(rStyle, "xml_missing")) {
      rs_val <- xml_attr(rStyle, "val")
      if (!is.na(rs_val) && rs_val == "Hyperlink") is_hyperlink <- TRUE
    }
    if (!is_hyperlink) {
      upsert_child(rPr, "w:color",
        sprintf('<w:color w:val="000000" xmlns:w="%s"/>', NS["w"]))
    }
  }
}


# ═══════════════════════════════════════════════════════════════════════════════
# FORMAT HEADING 2 AFTER HEADING 1 — suppress extra space-before
# ═══════════════════════════════════════════════════════════════════════════════
# When H2 immediately follows H1, we reduce H2's space-before to 0
# to match the template's visual spacing convention.

adjust_h2_after_h1 <- function(body) {
  # docx_body_xml() returns <w:document>; descend into <w:body> for children.
  # (Bug fixed 2026-02-24: xml_children(body) returned [<w:body>], not paras.)
  w_body <- xml_find_first(body, "w:body", ns = NS)
  children <- xml_children(w_body)
  prev_style <- ""

  for (i in seq_along(children)) {
    node <- children[[i]]
    if (xml_name(node) != "p") {
      prev_style <- ""
      next
    }

    style_id <- get_style_id(node)

    if (style_id == "Heading2" && prev_style == "Heading1") {
      pPr <- xml_find_first(node, "w:pPr", ns = NS)
      if (!inherits(pPr, "xml_missing")) {
        sp <- xml_find_first(pPr, "w:spacing", ns = NS)
        if (!inherits(sp, "xml_missing")) {
          xml_set_attr(sp, "w:before", "0")
        }
      }
    }

    # Similarly: H3 after H2, H4 after H3
    if (style_id == "Heading3" && prev_style == "Heading2") {
      pPr <- xml_find_first(node, "w:pPr", ns = NS)
      if (!inherits(pPr, "xml_missing")) {
        sp <- xml_find_first(pPr, "w:spacing", ns = NS)
        if (!inherits(sp, "xml_missing")) {
          xml_set_attr(sp, "w:before", "0")
        }
      }
    }

    if (style_id == "Heading4" && prev_style == "Heading3") {
      pPr <- xml_find_first(node, "w:pPr", ns = NS)
      if (!inherits(pPr, "xml_missing")) {
        sp <- xml_find_first(pPr, "w:spacing", ns = NS)
        if (!inherits(sp, "xml_missing")) {
          xml_set_attr(sp, "w:before", "0")
        }
      }
    }

    prev_style <- style_id
  }
}


# ═══════════════════════════════════════════════════════════════════════════════
# FORMAT PAGE SETUP (sectPr)
# ═══════════════════════════════════════════════════════════════════════════════

format_page_setup <- function(body) {
  # sectPr lives inside <w:body>, not as a direct child of <w:document>.
  # Use descendant search to find it reliably.  (Bug fixed 2026-02-24.)
  sectPr <- xml_find_first(body, ".//w:sectPr", ns = NS)
  if (inherits(sectPr, "xml_missing")) return(invisible(NULL))

  # Page size: Letter (12240 × 15840 twips = 8.5" × 11")
  upsert_child(sectPr, "w:pgSz",
    sprintf('<w:pgSz w:w="12240" w:h="15840" xmlns:w="%s"/>', NS["w"]))

  # Margins: top=1440 (1"), right=1350 (0.9375"), bottom=1440, left=1260 (0.875")
  # header/footer=720 (0.5")
  upsert_child(sectPr, "w:pgMar",
    sprintf(paste0(
      '<w:pgMar w:top="1440" w:right="1350" w:bottom="1440" w:left="1260"',
      ' w:header="720" w:footer="720" w:gutter="0" xmlns:w="%s"/>'
    ), NS["w"]))

  message("  Page setup enforced: Letter, margins 1\"/0.875\"/1\"/0.9375\"")
}


# ═══════════════════════════════════════════════════════════════════════════════
# FORMAT FOOTNOTES
# ═══════════════════════════════════════════════════════════════════════════════

format_footnotes <- function(doc) {
  # Access the footnotes XML part
  fn_xml <- tryCatch({
    # officer stores footnotes in a separate XML part
    pkg <- doc$package_dir
    fn_path <- file.path(pkg, "word", "footnotes.xml")
    if (file.exists(fn_path)) read_xml(fn_path) else NULL
  }, error = function(e) NULL)

  if (is.null(fn_xml)) {
    message("  No footnotes found.")
    return(invisible(NULL))
  }

  fn_ns <- xml_ns(fn_xml)
  fn_paras <- xml_find_all(fn_xml, ".//w:p", ns = NS)
  n_fn <- length(fn_paras)

  if (n_fn == 0) {
    message("  No footnote paragraphs found.")
    return(invisible(NULL))
  }

  fn_spec <- STYLE_SPECS$FootnoteText

  for (p in fn_paras) {
    style_id <- get_style_id(p)
    # Only format actual footnote text (skip separator footnotes)
    if (style_id %in% c("FootnoteText", "Normal", "")) {
      pPr <- ensure_pPr(p)

      # Spacing: single, no extra space
      upsert_child(pPr, "w:spacing",
        sprintf('<w:spacing w:line="240" w:lineRule="auto" w:before="0" w:after="0" xmlns:w="%s"/>',
                NS["w"]))

      # No indent
      upsert_child(pPr, "w:ind",
        sprintf('<w:ind w:firstLine="0" xmlns:w="%s"/>', NS["w"]))

      # Font at paragraph level
      pPr_rPr <- ensure_rPr(pPr)
      set_font_props(pPr_rPr, SZ_10PT)

      # Format each run (skip footnote reference superscripts)
      runs <- xml_find_all(p, "w:r", ns = NS)
      for (r in runs) {
        rPr <- ensure_rPr(r)
        # Check if this run is a footnote reference (superscript)
        va <- xml_find_first(rPr, "w:vertAlign", ns = NS)
        if (!inherits(va, "xml_missing") && xml_attr(va, "val") == "superscript") {
          # Just set font, don't change size (superscript has its own)
          upsert_child(rPr, "w:rFonts",
            sprintf('<w:rFonts w:ascii="%s" w:hAnsi="%s" w:cs="%s" xmlns:w="%s"/>',
                    FONT_NAME, FONT_NAME, FONT_NAME, NS["w"]))
          next
        }
        set_font_props(rPr, SZ_10PT)
      }
    }
  }

  # Write back
  fn_path <- file.path(doc$package_dir, "word", "footnotes.xml")
  write_xml(fn_xml, fn_path)
  message(sprintf("  Formatted %d footnote paragraphs.", n_fn))
}


# ═══════════════════════════════════════════════════════════════════════════════
# REPAIR REFERENCES SECTION
# ═══════════════════════════════════════════════════════════════════════════════
# Pandoc/Quarto citeproc sometimes renders reference paragraphs as Normal or
# BodyText instead of Bibliography. This pass:
#   1. Finds the "References" heading (H1)
#   2. Walks all paragraphs after it (until next H1 or end of body)
#   3. Applies the chosen REFS_STYLE to orphaned or all paragraphs
#
# Also handles the pStyle tag: sets it to REFS_STYLE so the paragraph
# is properly tagged in Word's style inspector.

BIB_STYLES <- c("Bibliography", "Bibliography-JM")

get_para_text <- function(p) {
  texts <- xml_find_all(p, ".//w:t", ns = NS)
  paste0(xml_text(texts), collapse = "")
}

repair_references_section <- function(body) {

  # docx_body_xml() returns <w:document>; descend into <w:body> for children.
  # (Bug fixed 2026-02-24: xml_children(body) returned [<w:body>], not paras.)
  w_body <- xml_find_first(body, "w:body", ns = NS)
  children <- xml_children(w_body)
  n <- length(children)

  # Find the last "References" heading (H1) — use last because some templates

  # have two References sections (demo vs. actual)
  refs_start <- 0L
  for (i in seq_along(children)) {
    node <- children[[i]]
    if (xml_name(node) != "p") next
    style_id <- get_style_id(node)
    if (style_id == "Heading1") {
      txt <- trimws(get_para_text(node))
      if (grepl("^references$", txt, ignore.case = TRUE)) {
        refs_start <- i
      }
    }
  }

  if (refs_start == 0L) {
    message("  No 'References' heading found — skipping references repair.")
    return(invisible(0L))
  }

  # Walk paragraphs after the References heading
  target_spec <- STYLE_SPECS[[REFS_STYLE]]
  if (is.null(target_spec)) {
    message(sprintf("  WARNING: REFS_STYLE '%s' not found in STYLE_SPECS!", REFS_STYLE))
    return(invisible(0L))
  }

  repaired <- 0L

  for (j in (refs_start + 1L):n) {
    node <- children[[j]]
    tag <- xml_name(node)

    # Stop at tables, section breaks, or another H1 (e.g. Appendix)
    if (tag == "tbl") next
    if (tag == "sectPr") break
    if (tag != "p") next

    style_id <- get_style_id(node)

    # Stop if we hit another H1 (e.g. "Appendix" section)
    if (style_id == "Heading1") break

    # Skip empty paragraphs
    txt <- trimws(get_para_text(node))
    if (nchar(txt) == 0) next

    # Decide whether to reformat this paragraph
    needs_fix <- FALSE

    if (REFS_FORCE_UNIFORM) {
      # Force all to target style
      needs_fix <- TRUE
    } else {
      # Only fix if NOT already a valid bibliography style
      if (!(style_id %in% BIB_STYLES)) {
        needs_fix <- TRUE
      }
    }

    if (needs_fix) {
      # Update the pStyle tag to REFS_STYLE
      pPr <- ensure_pPr(node)
      upsert_child(pPr, "w:pStyle",
        sprintf('<w:pStyle w:val="%s" xmlns:w="%s"/>', REFS_STYLE, NS["w"]))

      # Apply the formatting spec
      format_paragraph(node, target_spec)
      repaired <- repaired + 1L
    }
  }

  message(sprintf("  References section: %d paragraphs repaired to '%s' style.",
                  repaired, REFS_STYLE))
  invisible(repaired)
}


# ═══════════════════════════════════════════════════════════════════════════════
# REPAIR FRONT-MATTER (Author / Date paragraphs)
# ═══════════════════════════════════════════════════════════════════════════════
# Quarto/Pandoc does not assign Author or Date pStyle tags to front-matter
# paragraphs.  They arrive as Normal/unstyled, which means format_paragraph()
# treats them as body text (justified, 0.5" first-line indent).  This pass
# finds paragraphs between Title/Subtitle and the first Heading, then applies
# Author formatting to short non-sentence lines (names, dates).
#
# Heuristics for "likely author/date":
#   - Appears before first Heading
#   - Not styled as Title, Subtitle, Abstract, AbstractTitle, or Heading*
#   - Text is short (< 60 chars) and does NOT end with a period (not a sentence)
#   - Text does NOT start with "*" (acknowledgment footnote)
#
# Added 2026-02-24.

repair_front_matter <- function(body) {

  w_body <- xml_find_first(body, "w:body", ns = NS)
  children <- xml_children(w_body)
  n <- length(children)

  # Styles that belong in the front matter and should be left alone
  front_styles <- c("Title", "Subtitle", "Abstract", "AbstractTitle")

  author_spec <- STYLE_SPECS[["Author"]]
  repaired <- 0L

  for (i in seq_along(children)) {
    node <- children[[i]]
    if (xml_name(node) != "p") next

    style_id <- get_style_id(node)

    # Stop at first heading — end of front matter
    if (grepl("^Heading", style_id)) break

    # Skip paragraphs that already have a recognized front-matter style
    if (style_id %in% front_styles) next

    # Skip paragraphs that already have Author or Date style
    if (style_id %in% c("Author", "Date")) next

    txt <- trimws(get_para_text(node))
    if (nchar(txt) == 0) next

    # Heuristic: short, non-sentence, non-acknowledgment text → Author/Date
    if (nchar(txt) < 60 && !grepl("\\.$", txt) && !grepl("^\\*", txt)) {
      # Apply Author formatting (centered, 12pt, no indent)
      pPr <- ensure_pPr(node)
      upsert_child(pPr, "w:pStyle",
        sprintf('<w:pStyle w:val="Author" xmlns:w="%s"/>', NS["w"]))
      format_paragraph(node, author_spec)
      repaired <- repaired + 1L
    }
  }

  message(sprintf("  Front matter: %d paragraphs repaired to Author style.",
                  repaired))
  invisible(repaired)
}


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN: format_text()
# ═══════════════════════════════════════════════════════════════════════════════

format_text <- function(input_docx, output_docx = input_docx) {

  message("Reading: ", input_docx)
  doc <- read_docx(input_docx)
  body <- docx_body_xml(doc)

  # ── Pass 1: Format all non-table paragraphs ────────────────────────────────
  # Get ONLY top-level paragraphs (not inside tables)
  paragraphs <- xml_find_all(body, "w:body/w:p", ns = NS)
  n_paras <- length(paragraphs)
  message(sprintf("Found %d top-level paragraphs.", n_paras))

  style_counts <- list()
  skipped <- 0L

  for (i in seq_along(paragraphs)) {
    p <- paragraphs[[i]]
    style_id <- get_style_id(p)

    # Look up spec
    spec <- STYLE_SPECS[[style_id]]

    if (is.null(spec)) {
      # Unknown style — skip, don't damage it
      skipped <- skipped + 1L
      next
    }

    format_paragraph(p, spec)

    # Track counts
    style_counts[[style_id]] <- (style_counts[[style_id]] %||% 0L) + 1L

    if (i %% 50 == 0)
      message(sprintf("  ...formatted %d/%d paragraphs", i, n_paras))
  }

  # ── Pass 2: Heading adjacency adjustments ──────────────────────────────────
  adjust_h2_after_h1(body)
  message("  Applied heading adjacency spacing adjustments.")

  # ── Pass 3: Page setup ─────────────────────────────────────────────────────
  format_page_setup(body)

  # ── Pass 4: Footnotes ──────────────────────────────────────────────────────
  format_footnotes(doc)

  # ── Pass 5: References section repair ──────────────────────────────────────
  # Fix any reference paragraphs that pandoc/citeproc rendered with the wrong
  # style (Normal, BodyText, FirstParagraph) inside the References section.
  repair_references_section(body)

  # ── Pass 6: Front-matter Author/Date detection ──────────────────────────
  # Quarto does not assign Author or Date pStyle to front-matter paragraphs.
  # They arrive as Normal (justified, indented) instead of centered.  This
  # pass walks paragraphs between Title/Subtitle and the first Heading1,
  # detects likely author names and dates, and applies Author/Date formatting.
  # (Added 2026-02-24.)
  repair_front_matter(body)

  # ── Summary ────────────────────────────────────────────────────────────────
  message("\n  Style breakdown:")
  for (nm in sort(names(style_counts))) {
    message(sprintf("    %-20s %d", nm, style_counts[[nm]]))
  }
  if (skipped > 0)
    message(sprintf("    %-20s %d (unrecognized — left untouched)", "SKIPPED", skipped))

  # ── Write output ───────────────────────────────────────────────────────────
  message(sprintf("\nWriting: %s  (%d paragraphs formatted)",
                  output_docx, n_paras - skipped))
  print(doc, target = output_docx)
  message("Done.")
  invisible(output_docx)
}


# ═══════════════════════════════════════════════════════════════════════════════
# CLI entry point
# ═══════════════════════════════════════════════════════════════════════════════
# Only run CLI when this script is invoked directly (not source()'d by wrapper)
.this_script_is_main <- function() {
  if (interactive()) return(FALSE)
  cmd_args <- commandArgs(trailingOnly = FALSE)
  file_arg <- cmd_args[grep("^--file=", cmd_args)]
  if (length(file_arg) == 0) return(FALSE)
  script_path <- normalizePath(sub("^--file=", "", file_arg), mustWork = FALSE)
  grepl("pvb_format_text", basename(script_path), fixed = TRUE)
}

if (.this_script_is_main()) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) < 1) {
    cat("Usage: Rscript pvb_format_text.R  input.docx  [output.docx]\n")
    quit(status = 1)
  }
  input  <- args[1]
  output <- if (length(args) >= 2) args[2] else args[1]
  format_text(input, output)
}
