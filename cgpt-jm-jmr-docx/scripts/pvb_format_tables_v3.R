#!/usr/bin/env Rscript
# ═══════════════════════════════════════════════════════════════════════════════
# pvb_format_tables_v3.R — Post-processor for Quarto/RMarkdown DOCX output
# ═══════════════════════════════════════════════════════════════════════════════
#
# PURPOSE:
#   Reformats EVERY table in a rendered .docx file to match the PVB academic
#   manuscript style (pvb-template_TABLES_v3.docx specifications).
#
# USAGE:
#   Rscript pvb_format_tables_v3.R  input.docx  [output.docx]
#
#   If output.docx is omitted, overwrites input.docx in place.
#
# WORKFLOW:
#   1. quarto render manuscript.qmd --to docx
#   2. Rscript pvb_format_tables_v3.R manuscript.docx manuscript_formatted.docx
#
# WHAT IT DOES:
#   Tables (cell-level borders — reliable across all renderers):
#     ✓ Thick top rule on header row (sz=12, 1.5pt black)
#     ✓ Thick bottom rule on last row (sz=12, 1.5pt black)
#     ✓ Thin horizontal rules between ALL rows (sz=4, 0.5pt)
#     ✓ NO vertical rules (left, right, insideV suppressed)
#     ✓ NO shading/banding (transparent background)
#     ✓ Calibri 11pt body text; header row bold + centered
#     ✓ First column left-aligned; remaining columns centered
#     ✓ Cell padding: top/bottom 60 twips, left/right 100 twips
#     ✓ Centered on page; original column widths preserved (no tblW/tblLayout override)
#
#   Table notes (paragraphs AFTER each table starting with Note/Notes):
#     ✓ 10pt Calibri italic
#     ✓ Left alignment
#     ✓ 1.15x line spacing, 40tw before (gap from table), 200tw after (10pt breathing room)
#
# DOES NOT TOUCH:
#   - Cell content (text, numbers, significance stars)
#   - Row/column count or table captions
#   - Anything outside <w:tbl> and post-table note paragraphs
#
# REQUIREMENTS:
#   install.packages(c("officer", "xml2"))
#
# CHANGELOG:
#   v1 (2026-02-23): Cell-level borders, font/size/bold, shading removal.
#   v2 (ChatGPT):    Attempted tblBorders approach — caused no-border bug
#                     because tcBorders=none overrides tblBorders.
#   v3 (2026-02-23): v1 borders (proven) + post-table note formatting (10pt
#                     italic justified) + STRIP_BODY_BOLD toggle.
#   v3.1 (2026-02-24): Fixed xml_children(body) bug — docx_body_xml() returns
#                     <w:document> root, so xml_children() returned [<w:body>]
#                     instead of paragraphs/tables.  Note detection loop
#                     silently matched nothing.  Now descends into <w:body>.
#
# Author: Claude (for Dr. P.V. Sundar Balakrishnan)
# ═══════════════════════════════════════════════════════════════════════════════

library(officer)
library(xml2)

# ── Configuration (matches pvb-template_TABLES_v3.docx) ──────────────────────
FONT_NAME          <- "Calibri"
FONT_SIZE_HP       <- 22L       # 11pt in half-points
FONT_SIZE_NOTE_HP  <- 20L       # 10pt for table notes
BORDER_THICK_SZ    <- 12L       # 1.5pt in eighth-points (Word's border sz)
BORDER_THIN_SZ     <- 4L        # 0.5pt
CELL_PAD_TB        <- 60L       # top/bottom cell padding in twips
CELL_PAD_LR        <- 100L      # left/right cell padding in twips

# ── Behavior toggles ─────────────────────────────────────────────────────────
STRIP_BODY_BOLD    <- TRUE      # TRUE: enforce body cells non-bold
                                # FALSE: preserves any intentional bold in body

# ── OOXML namespace map ──────────────────────────────────────────────────────
NS <- c(w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main")

# ══════════════════════════════════════════════════════════════════════════════
# XML HELPERS
# ══════════════════════════════════════════════════════════════════════════════

remove_if_exists <- function(parent, xpath) {
  node <- xml_find_first(parent, xpath, ns = NS)
  if (!inherits(node, "xml_missing")) xml_remove(node)
}

upsert_child <- function(parent, xpath, new_xml_str) {
  remove_if_exists(parent, xpath)
  xml_add_child(parent, read_xml(new_xml_str))
}

# ── Border helpers (cell-level — reliable approach) ──────────────────────────

make_tcBorders <- function(top_sz, bottom_sz) {
  sprintf(paste0(
    '<w:tcBorders xmlns:w="%s">',
    '<w:top w:val="single" w:sz="%d" w:space="0" w:color="000000"/>',
    '<w:bottom w:val="single" w:sz="%d" w:space="0" w:color="000000"/>',
    '<w:start w:val="none" w:sz="0" w:space="0" w:color="auto"/>',
    '<w:end w:val="none" w:sz="0" w:space="0" w:color="auto"/>',
    '<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>',
    '</w:tcBorders>'
  ), NS["w"], top_sz, bottom_sz)
}

make_tcMar <- function() {
  sprintf(paste0(
    '<w:tcMar xmlns:w="%s">',
    '<w:top w:w="%d" w:type="dxa"/>',
    '<w:bottom w:w="%d" w:type="dxa"/>',
    '<w:start w:w="%d" w:type="dxa"/>',
    '<w:end w:w="%d" w:type="dxa"/>',
    '</w:tcMar>'
  ), NS["w"], CELL_PAD_TB, CELL_PAD_TB, CELL_PAD_LR, CELL_PAD_LR)
}


# ══════════════════════════════════════════════════════════════════════════════
# FORMAT ONE TABLE
# ══════════════════════════════════════════════════════════════════════════════

format_one_table <- function(tbl) {

  # ── 1. Table-level properties ──────────────────────────────────────────────
  tblPr <- xml_find_first(tbl, "w:tblPr", ns = NS)
  if (inherits(tblPr, "xml_missing")) {
    xml_add_child(tbl, read_xml(sprintf('<w:tblPr xmlns:w="%s"/>', NS["w"])),
                  .where = 0)
    tblPr <- xml_find_first(tbl, "w:tblPr", ns = NS)
  }

  # Do NOT override tblW or tblLayout — forcing fixed/100% width redistributes
  # column widths and squashes narrow columns (e.g. N column).  Let each table
  # keep its original column widths; only borders, fonts, and shading are ours to set.

  # Center table on page
  upsert_child(tblPr, "w:jc",
    sprintf('<w:jc w:val="center" xmlns:w="%s"/>', NS["w"]))

  # Remove inherited styling that could override our cell-level borders
  remove_if_exists(tblPr, "w:tblBorders")
  remove_if_exists(tblPr, "w:tblCellMar")
  remove_if_exists(tblPr, "w:tblStyle")
  remove_if_exists(tblPr, "w:tblLook")

  # ── 2. Process rows ───────────────────────────────────────────────────────
  rows <- xml_find_all(tbl, "w:tr", ns = NS)
  n_rows <- length(rows)

  for (r_idx in seq_along(rows)) {
    tr <- rows[[r_idx]]

    # Detect header (Word's <w:tblHeader/> or first row)
    trPr <- xml_find_first(tr, "w:trPr", ns = NS)
    is_header <- (r_idx == 1)
    if (!inherits(trPr, "xml_missing")) {
      hdr_node <- xml_find_first(trPr, "w:tblHeader", ns = NS)
      if (!inherits(hdr_node, "xml_missing")) is_header <- TRUE
    }

    is_last_row <- (r_idx == n_rows)

    # ── 3. Process cells ─────────────────────────────────────────────────────
    cells <- xml_find_all(tr, "w:tc", ns = NS)

    for (c_idx in seq_along(cells)) {
      tc <- cells[[c_idx]]

      # Ensure tcPr
      tcPr <- xml_find_first(tc, "w:tcPr", ns = NS)
      if (inherits(tcPr, "xml_missing")) {
        xml_add_child(tc, read_xml(sprintf('<w:tcPr xmlns:w="%s"/>', NS["w"])),
                      .where = 0)
        tcPr <- xml_find_first(tc, "w:tcPr", ns = NS)
      }

      # Cell borders (cell-level: the approach that works)
      if (is_header) {
        upsert_child(tcPr, "w:tcBorders",
                     make_tcBorders(BORDER_THICK_SZ, BORDER_THIN_SZ))
      } else if (is_last_row) {
        upsert_child(tcPr, "w:tcBorders",
                     make_tcBorders(BORDER_THIN_SZ, BORDER_THICK_SZ))
      } else {
        upsert_child(tcPr, "w:tcBorders",
                     make_tcBorders(BORDER_THIN_SZ, BORDER_THIN_SZ))
      }

      # Cell margins
      upsert_child(tcPr, "w:tcMar", make_tcMar())

      # Remove shading
      remove_if_exists(tcPr, "w:shd")

      # ── Format paragraphs in cell ────────────────────────────────────────
      paragraphs <- xml_find_all(tc, "w:p", ns = NS)
      for (p in paragraphs) {
        format_cell_paragraph(p, is_header, c_idx)
      }
    }
  }
}


# ══════════════════════════════════════════════════════════════════════════════
# FORMAT PARAGRAPH INSIDE A TABLE CELL
# ══════════════════════════════════════════════════════════════════════════════

format_cell_paragraph <- function(p, is_header, col_idx) {

  pPr <- xml_find_first(p, "w:pPr", ns = NS)
  if (inherits(pPr, "xml_missing")) {
    xml_add_child(p, read_xml(sprintf('<w:pPr xmlns:w="%s"/>', NS["w"])),
                  .where = 0)
    pPr <- xml_find_first(p, "w:pPr", ns = NS)
  }

  # Alignment: header → center; col 1 → left; others → center
  align_val <- if (is_header) "center"
               else if (col_idx == 1) "left"
               else "center"
  upsert_child(pPr, "w:jc",
    sprintf('<w:jc w:val="%s" xmlns:w="%s"/>', align_val, NS["w"]))

  # Single line spacing, no extra space
  upsert_child(pPr, "w:spacing",
    sprintf('<w:spacing w:line="240" w:lineRule="auto" w:before="0" w:after="0" xmlns:w="%s"/>',
            NS["w"]))

  # Paragraph-level rPr (default font for the paragraph)
  pPr_rPr <- xml_find_first(pPr, "w:rPr", ns = NS)
  if (inherits(pPr_rPr, "xml_missing")) {
    xml_add_child(pPr, read_xml(sprintf('<w:rPr xmlns:w="%s"/>', NS["w"])))
    pPr_rPr <- xml_find_first(pPr, "w:rPr", ns = NS)
  }
  set_font_props(pPr_rPr, FONT_SIZE_HP)

  # Format each run
  runs <- xml_find_all(p, "w:r", ns = NS)
  for (r in runs) {
    rPr <- xml_find_first(r, "w:rPr", ns = NS)
    if (inherits(rPr, "xml_missing")) {
      xml_add_child(r, read_xml(sprintf('<w:rPr xmlns:w="%s"/>', NS["w"])),
                    .where = 0)
      rPr <- xml_find_first(r, "w:rPr", ns = NS)
    }

    set_font_props(rPr, FONT_SIZE_HP)

    # Bold: header ON; body conditional
    if (is_header) {
      upsert_child(rPr, "w:b",  sprintf('<w:b xmlns:w="%s"/>',  NS["w"]))
      upsert_child(rPr, "w:bCs", sprintf('<w:bCs xmlns:w="%s"/>', NS["w"]))
    } else if (STRIP_BODY_BOLD) {
      remove_if_exists(rPr, "w:b")
      remove_if_exists(rPr, "w:bCs")
    }

    # Clean up
    remove_if_exists(rPr, "w:color")
    remove_if_exists(rPr, "w:highlight")
    remove_if_exists(rPr, "w:shd")
  }
}


# ══════════════════════════════════════════════════════════════════════════════
# FORMAT A POST-TABLE NOTE PARAGRAPH
# ══════════════════════════════════════════════════════════════════════════════
# Notes appear as body paragraphs immediately after </w:tbl>, starting with
# "Note:", "Notes:", "Notes.", or "Model selection note:".
# Format: 10pt Calibri italic, justified, single spacing.

format_note_paragraph <- function(p) {

  pPr <- xml_find_first(p, "w:pPr", ns = NS)
  if (inherits(pPr, "xml_missing")) {
    xml_add_child(p, read_xml(sprintf('<w:pPr xmlns:w="%s"/>', NS["w"])),
                  .where = 0)
    pPr <- xml_find_first(p, "w:pPr", ns = NS)
  }

  # Left alignment
  upsert_child(pPr, "w:jc",
    sprintf('<w:jc w:val="left" xmlns:w="%s"/>', NS["w"]))

  # 1.15x line spacing; small space before (40tw gap from table), 200tw after
  # (10pt breathing room before next body paragraph begins)
  upsert_child(pPr, "w:spacing",
    sprintf('<w:spacing w:line="276" w:lineRule="auto" w:before="40" w:after="200" xmlns:w="%s"/>',
            NS["w"]))

  # Paragraph-level rPr
  pPr_rPr <- xml_find_first(pPr, "w:rPr", ns = NS)
  if (inherits(pPr_rPr, "xml_missing")) {
    xml_add_child(pPr, read_xml(sprintf('<w:rPr xmlns:w="%s"/>', NS["w"])))
    pPr_rPr <- xml_find_first(pPr, "w:rPr", ns = NS)
  }
  set_font_props(pPr_rPr, FONT_SIZE_NOTE_HP)
  # Italic at paragraph level
  upsert_child(pPr_rPr, "w:i",  sprintf('<w:i xmlns:w="%s"/>',  NS["w"]))
  upsert_child(pPr_rPr, "w:iCs", sprintf('<w:iCs xmlns:w="%s"/>', NS["w"]))

  # Format each run: 10pt italic
  runs <- xml_find_all(p, "w:r", ns = NS)
  for (r in runs) {
    rPr <- xml_find_first(r, "w:rPr", ns = NS)
    if (inherits(rPr, "xml_missing")) {
      xml_add_child(r, read_xml(sprintf('<w:rPr xmlns:w="%s"/>', NS["w"])),
                    .where = 0)
      rPr <- xml_find_first(r, "w:rPr", ns = NS)
    }

    set_font_props(rPr, FONT_SIZE_NOTE_HP)

    # Italic
    upsert_child(rPr, "w:i",  sprintf('<w:i xmlns:w="%s"/>',  NS["w"]))
    upsert_child(rPr, "w:iCs", sprintf('<w:iCs xmlns:w="%s"/>', NS["w"]))

    # Remove bold (notes should not be bold)
    remove_if_exists(rPr, "w:b")
    remove_if_exists(rPr, "w:bCs")

    # Clean
    remove_if_exists(rPr, "w:color")
    remove_if_exists(rPr, "w:highlight")
    remove_if_exists(rPr, "w:shd")
  }
}


# ══════════════════════════════════════════════════════════════════════════════
# SHARED: set font name and size on an rPr element
# ══════════════════════════════════════════════════════════════════════════════

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


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: extract text from a paragraph node
# ══════════════════════════════════════════════════════════════════════════════

get_para_text <- function(p) {
  texts <- xml_find_all(p, ".//w:t", ns = NS)
  paste0(xml_text(texts), collapse = "")
}

# ══════════════════════════════════════════════════════════════════════════════
# HELPER: detect if a paragraph is a table note
# ══════════════════════════════════════════════════════════════════════════════

is_table_note <- function(p) {
  txt <- trimws(tolower(get_para_text(p)))
  if (nchar(txt) == 0) return(FALSE)
  # Match: "note:", "notes:", "notes.", "model selection note:"
  grepl("^notes?[:.\\s]", txt) || grepl("^model selection note", txt)
}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN: format_tables()
# ══════════════════════════════════════════════════════════════════════════════

format_tables <- function(input_docx, output_docx = input_docx) {

  message("Reading: ", input_docx)
  doc <- read_docx(input_docx)

  body <- docx_body_xml(doc)

  # ── Pass 1: Format all tables ──────────────────────────────────────────────
  tables <- xml_find_all(body, ".//w:tbl", ns = NS)
  n_tables <- length(tables)
  message(sprintf("Found %d tables.", n_tables))

  for (t_idx in seq_along(tables)) {
    format_one_table(tables[[t_idx]])
    if (t_idx %% 10 == 0)
      message(sprintf("  ...formatted %d/%d tables", t_idx, n_tables))
  }

  # ── Pass 2: Format post-table note paragraphs ─────────────────────────────
  # Walk top-level children of <w:body>; after each <w:tbl>, check if the
  # next sibling paragraph starts with "Note"/"Notes".
  #
  # NOTE: docx_body_xml(doc) returns the <w:document> root, whose only child
  # is <w:body>.  We must descend into <w:body> to iterate over paragraphs
  # and tables.  Using xml_children() directly on the document root returns
  # [<w:body>] — a single element — so the tbl-detection loop would silently

  # match nothing.  (Bug fixed 2026-02-24.)
  w_body <- xml_find_first(body, "w:body", ns = NS)
  body_children <- xml_children(w_body)
  n_children <- length(body_children)
  notes_formatted <- 0L

  for (i in seq_along(body_children)) {
    node <- body_children[[i]]
    node_tag <- xml_name(node)

    if (node_tag == "tbl" && i < n_children) {
      # Check next sibling(s) — sometimes a note spans 2 paragraphs
      for (offset in 1:2) {
        j <- i + offset
        if (j > n_children) break

        next_node <- body_children[[j]]
        if (xml_name(next_node) != "p") break

        if (is_table_note(next_node)) {
          format_note_paragraph(next_node)
          notes_formatted <- notes_formatted + 1L
        } else {
          break   # stop looking once we hit a non-note paragraph
        }
      }
    }
  }

  message(sprintf("Formatted %d post-table note paragraphs.", notes_formatted))

  # ── Write output ───────────────────────────────────────────────────────────
  message(sprintf("Writing: %s  (%d tables, %d notes)",
                  output_docx, n_tables, notes_formatted))
  print(doc, target = output_docx)
  message("Done.")
  invisible(output_docx)
}


# ══════════════════════════════════════════════════════════════════════════════
# CLI entry point
# ══════════════════════════════════════════════════════════════════════════════
# Only run CLI when this script is invoked directly (not source()'d by wrapper)
.this_script_is_main <- function() {
  if (interactive()) return(FALSE)
  cmd_args <- commandArgs(trailingOnly = FALSE)
  file_arg <- cmd_args[grep("^--file=", cmd_args)]
  if (length(file_arg) == 0) return(FALSE)
  script_path <- normalizePath(sub("^--file=", "", file_arg), mustWork = FALSE)
  grepl("pvb_format_tables", basename(script_path), fixed = TRUE)
}

if (.this_script_is_main()) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) < 1) {
    cat("Usage: Rscript pvb_format_tables_v3.R  input.docx  [output.docx]\n")
    quit(status = 1)
  }
  input  <- args[1]
  output <- if (length(args) >= 2) args[2] else args[1]
  format_tables(input, output)
}
