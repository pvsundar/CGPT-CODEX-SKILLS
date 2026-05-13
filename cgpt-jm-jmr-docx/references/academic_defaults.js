/**
 * academic_defaults.js
 * Reusable constants and helpers for academic manuscript .docx creation.
 * Used by Claude Code when building standalone .docx files (cover letters,
 * response-to-reviewers, supplementary documents).
 *
 * Usage: const { AD, cell, bodyPara, heading, refPara, tableNote } = require('./academic_defaults');
 */

const { Paragraph, TextRun, TableCell, AlignmentType, HeadingLevel,
        BorderStyle, WidthType } = require('docx');

// === ACADEMIC DEFAULTS ===
const AD = {
  // Fonts
  font: "Aptos",              // Primary; Calibri as fallback
  fontFallback: "Calibri",
  // Font sizes (half-points: 24 = 12pt)
  fontSize: 24,               // 12pt body
  tableFontSize: 20,          // 10pt tables
  headingFontSize: 28,        // 14pt heading level 1
  subheadingFontSize: 24,     // 12pt heading level 2
  headerFooterSize: 20,       // 10pt running head / page number
  // Line spacing (twips: 240 = single)
  lineSpacing: 480,           // Double-spaced body
  tableLineSpacing: 240,      // Single-spaced tables
  refsLineSpacing: 276,       // 1.15 spacing for references (240 × 1.15)
  // Page geometry (DXA: 1440 = 1 inch)
  page: {
    size: { width: 12240, height: 15840 },           // US Letter
    margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }  // 1″ all sides
  },
  // Content width = page width - left margin - right margin
  contentWidth: 9360,
  // Standard indent
  firstLineIndent: 720,       // 0.5″
  hangingIndent: 720,         // 0.5″ for references
};

// === TABLE BORDERS ===
const noBorder = { style: BorderStyle.NONE, size: 0 };
const ruleBorder = { style: BorderStyle.SINGLE, size: 4, color: "000000" };

// === TABLE CELL ===
// APA-style: no vertical borders; horizontal rules only on header top/bottom and table bottom.
// opts: { bold, italics, topRule, bottomRule, width, align, size }
function cell(text, opts = {}) {
  return new TableCell({
    borders: {
      top: opts.topRule ? ruleBorder : noBorder,
      bottom: opts.bottomRule ? ruleBorder : noBorder,
      left: noBorder,
      right: noBorder,
    },
    width: { size: opts.width || 1872, type: WidthType.DXA },
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({
      alignment: opts.align || AlignmentType.CENTER,
      spacing: { line: AD.tableLineSpacing },
      children: [new TextRun({
        text,
        bold: opts.bold || false,
        italics: opts.italics || false,
        font: AD.font,
        size: opts.size || AD.tableFontSize,
      })]
    })]
  });
}

// === TABLE NOTE ===
// APA "Note." paragraph — single-spaced, 10pt, italicized prefix.
function tableNote(text) {
  return new Paragraph({
    spacing: { before: 60, line: AD.tableLineSpacing },
    children: [
      new TextRun({ text: "Note. ", italics: true, font: AD.font, size: AD.tableFontSize }),
      new TextRun({ text, font: AD.font, size: AD.tableFontSize }),
    ]
  });
}

// === BODY PARAGRAPH ===
// Double-spaced. opts: { firstLine, align, run: { bold, italics, ... } }
function bodyPara(text, opts = {}) {
  return new Paragraph({
    spacing: { line: AD.lineSpacing, after: 0 },
    indent: opts.firstLine ? { firstLine: AD.firstLineIndent } : undefined,
    alignment: opts.align || AlignmentType.LEFT,
    children: [new TextRun({
      text,
      font: AD.font,
      size: AD.fontSize,
      ...(opts.run || {}),
    })]
  });
}

// === HEADING ===
// Level 1: centered bold 14pt. Level 2: left bold 12pt.
function heading(text, level) {
  return new Paragraph({
    heading: level,
    spacing: { before: 240, after: 240 },
    alignment: level === HeadingLevel.HEADING_1 ? AlignmentType.CENTER : AlignmentType.LEFT,
    children: [new TextRun({
      text,
      bold: true,
      font: AD.font,
      size: level === HeadingLevel.HEADING_1 ? AD.headingFontSize : AD.subheadingFontSize,
    })]
  });
}

// === REFERENCE PARAGRAPH ===
// 1.15 line spacing, 0.5″ hanging indent.
function refPara(text) {
  return new Paragraph({
    spacing: { line: AD.refsLineSpacing },
    indent: { left: AD.hangingIndent, hanging: AD.hangingIndent },
    children: [new TextRun({ text, font: AD.font, size: AD.fontSize })]
  });
}

// === HEADING STYLES (for Document constructor) ===
const headingStyles = [
  {
    id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal",
    quickFormat: true,
    run: { size: AD.headingFontSize, bold: true, font: AD.font },
    paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 },
  },
  {
    id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal",
    quickFormat: true,
    run: { size: AD.subheadingFontSize, bold: true, font: AD.font },
    paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 },
  },
];

module.exports = {
  AD,
  noBorder,
  ruleBorder,
  cell,
  tableNote,
  bodyPara,
  heading,
  refPara,
  headingStyles,
};
