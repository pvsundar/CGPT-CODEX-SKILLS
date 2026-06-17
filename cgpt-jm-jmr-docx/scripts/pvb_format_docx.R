#!/usr/bin/env Rscript
# ═══════════════════════════════════════════════════════════════════════════════
# pvb_format_docx.R — One-command pipeline: render + format text + format tables
# ═══════════════════════════════════════════════════════════════════════════════
#
# PURPOSE:
#   Single entry point that runs the full post-processing pipeline on a
#   Quarto/RMarkdown .docx manuscript. Optionally renders the .qmd first.
#
# USAGE:
#   # Format an already-rendered .docx:
#   Rscript pvb_format_docx.R  manuscript.docx
#
#   # Render .qmd to .docx, then format:
#   Rscript pvb_format_docx.R  manuscript.qmd
#
#   # Specify output name:
#   Rscript pvb_format_docx.R  manuscript.docx  manuscript_final.docx
#
#   # Format with Bibliography-JM style (journal format):
#   Rscript pvb_format_docx.R  manuscript.docx  --refs=Bibliography-JM
#
# PIPELINE:
#   1. If input is .qmd → quarto render to .docx
#   2. Run pvb_format_text.R   (paragraph styles, page setup, footnotes, refs)
#   3. Run pvb_format_tables_v3.R  (table borders, fonts, alignment, notes)
#
# REQUIREMENTS:
#   - pvb_format_text.R and pvb_format_tables_v3.R in the same directory
#     as this script (or on the R search path)
#   - R packages: officer, xml2
#   - quarto CLI (only if rendering from .qmd)
#
# Author: Claude (for Dr. P.V. Sundar Balakrishnan)
# ═══════════════════════════════════════════════════════════════════════════════

# ── Parse arguments ──────────────────────────────────────────────────────────

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 1) {
  cat("Usage: Rscript pvb_format_docx.R  <input.docx|input.qmd>  [output.docx]  [--refs=Bibliography|Bibliography-JM]  [--force-refs]\n")
  cat("\nOptions:\n")
  cat("  --refs=STYLE       Bibliography style: 'Bibliography' (default) or 'Bibliography-JM'\n")
  cat("  --force-refs       Force all reference paragraphs to the chosen style\n")
  cat("  --skip-text        Skip text formatting (run tables only)\n")
  cat("  --skip-tables      Skip table formatting (run text only)\n")
  cat("  --no-render        Even if input is .qmd, don't render (assume .docx exists)\n")
  quit(status = 1)
}

# Separate positional args from flags
positional <- character(0)
flags <- character(0)
for (a in args) {
  if (grepl("^--", a)) {
    flags <- c(flags, a)
  } else {
    positional <- c(positional, a)
  }
}

input_file <- positional[1]
output_file <- if (length(positional) >= 2) positional[2] else NULL

# Parse flags
refs_style   <- "Bibliography"
force_refs   <- FALSE
skip_text    <- FALSE
skip_tables  <- FALSE
no_render    <- FALSE

for (f in flags) {
  if (grepl("^--refs=", f))    refs_style  <- sub("^--refs=", "", f)
  if (f == "--force-refs")     force_refs  <- TRUE
  if (f == "--skip-text")      skip_text   <- TRUE
  if (f == "--skip-tables")    skip_tables <- TRUE
  if (f == "--no-render")      no_render   <- TRUE
}

# ── Locate companion scripts ────────────────────────────────────────────────

script_dir <- if (interactive()) {
  getwd()
} else {
  # Get directory of this script
  cmd_args <- commandArgs(trailingOnly = FALSE)
  script_arg <- cmd_args[grep("--file=", cmd_args)]
  if (length(script_arg) > 0) {
    dirname(normalizePath(sub("--file=", "", script_arg)))
  } else {
    getwd()
  }
}

text_script   <- file.path(script_dir, "pvb_format_text.R")
tables_script <- file.path(script_dir, "pvb_format_tables_v3.R")

# Validate
if (!skip_text && !file.exists(text_script)) {
  stop("Cannot find pvb_format_text.R at: ", text_script,
       "\n  Place it in the same directory as pvb_format_docx.R.")
}
if (!skip_tables && !file.exists(tables_script)) {
  stop("Cannot find pvb_format_tables_v3.R at: ", tables_script,
       "\n  Place it in the same directory as pvb_format_docx.R.")
}

# ── Step 1: Render .qmd if needed ───────────────────────────────────────────

ext <- tolower(tools::file_ext(input_file))
docx_file <- input_file

if (ext == "qmd" && !no_render) {
  message("\n", strrep("=", 70))
  message("STEP 1: Rendering ", input_file, " to DOCX")
  message(strrep("=", 70))

  # Derive expected .docx output name
  docx_file <- sub("\\.qmd$", ".docx", input_file, ignore.case = TRUE)

  # Run quarto render
  render_cmd <- sprintf('quarto render "%s" --to docx', input_file)
  message("  Running: ", render_cmd)
  status <- system(render_cmd)

  if (status != 0) {
    stop("Quarto render failed with exit code ", status)
  }
  if (!file.exists(docx_file)) {
    stop("Expected output not found: ", docx_file)
  }
  message("  Rendered: ", docx_file)
} else if (ext == "qmd" && no_render) {
  docx_file <- sub("\\.qmd$", ".docx", input_file, ignore.case = TRUE)
  if (!file.exists(docx_file)) {
    stop("--no-render specified but .docx not found: ", docx_file)
  }
  message("Skipping render (--no-render); using existing: ", docx_file)
} else if (ext != "docx") {
  stop("Input must be .docx or .qmd, got: .", ext)
}

# Determine final output path — never overwrite the original
if (is.null(output_file)) {
  base <- tools::file_path_sans_ext(docx_file)
  output_file <- paste0(base, "_pvb.docx")
}

# ── Step 2: Format text ─────────────────────────────────────────────────────

if (!skip_text) {
  message("\n", strrep("=", 70))
  message("STEP 2: Formatting text (pvb_format_text.R)")
  message(strrep("=", 70))

  # Source the script to get format_text() function
  source(text_script, local = TRUE)

  # Apply configuration overrides before running
  if (exists("REFS_STYLE", inherits = FALSE)) {
    # Already sourced; now override
  }
  # Override via environment-level assignment
  env <- environment()
  env$REFS_STYLE <- refs_style
  env$REFS_FORCE_UNIFORM <- force_refs

  # Run: input -> output (or input -> input if same)
  format_text(docx_file, output_file)
}

# ── Step 3: Format tables ───────────────────────────────────────────────────

if (!skip_tables) {
  message("\n", strrep("=", 70))
  message("STEP 3: Formatting tables (pvb_format_tables_v3.R)")
  message(strrep("=", 70))

  source(tables_script, local = TRUE)

  # If text step wrote to output_file, tables step reads from there
  tables_input <- if (!skip_text) output_file else docx_file
  if (normalizePath(tables_input, mustWork = FALSE) ==
      normalizePath(output_file, mustWork = FALSE)) {
    tmp_tables_output <- paste0(tools::file_path_sans_ext(output_file),
                                "_tables_tmp.docx")
    format_tables(tables_input, tmp_tables_output)
    if (!file.copy(tmp_tables_output, output_file, overwrite = TRUE)) {
      stop("Could not replace table-formatted output: ", output_file)
    }
    unlink(tmp_tables_output, force = TRUE)
  } else {
    format_tables(tables_input, output_file)
  }
}

# ── Step 4: Python fallback (notes + front-matter) ────────────────────────

py_script <- file.path(script_dir, "fix_docx_notes_frontmatter.py")

if (file.exists(py_script)) {
  message("\n", strrep("=", 70))
  message("STEP 4: Python fallback — notes + front-matter (fix_docx_notes_frontmatter.py)")
  message(strrep("=", 70))

  # Find Python executable
  py_exe <- Sys.which("python")
  if (nchar(py_exe) == 0) py_exe <- Sys.which("python3")
  # Fallback to known Windows path
  if (nchar(py_exe) == 0) {
    py_candidate <- "C:/Users/sundar/AppData/Local/Programs/Python/Python314/python.exe"
    if (file.exists(py_candidate)) py_exe <- py_candidate
  }

  if (nchar(py_exe) > 0) {
    # Python script writes to a _fixed file; we overwrite output_file with it
    py_cmd <- sprintf('"%s" "%s" "%s" "%s"', py_exe, py_script, output_file, output_file)
    message("  Running: ", py_cmd)
    py_status <- system(py_cmd)
    if (py_status != 0) {
      warning("Python fallback returned non-zero exit code: ", py_status,
              "\n  R formatting was applied; Python step skipped.")
    }
  } else {
    message("  Python not found — skipping fallback step.")
    message("  (R scripts already handle notes and front-matter as of v2.)")
  }
} else {
  message("\n  fix_docx_notes_frontmatter.py not found — skipping Python fallback.")
}

# ── Done ─────────────────────────────────────────────────────────────────────

message("\n", strrep("=", 70))
message("PIPELINE COMPLETE")
message("  Output: ", output_file)
message(strrep("=", 70))
