# Redistribution Review

This review records the current redistribution status of bundled scripts,
references, and repository metadata.

## Summary

- Repository-original skill instructions, README material, contribution notes,
  and validation scripts are released under the MIT License.
- Claude/Cowork skill sets are treated as source inspiration and read-only
  reference material unless a file is explicitly bundled here.
- No credentials, tokens, `.env` files, private manuscript contents, or private
  data files are intentionally included in this repository.
- Contributors should update this file whenever adding copied, adapted,
  generated, or third-party materials.

## Current Bundled Materials

| Path | Status | Notes |
| --- | --- | --- |
| `scripts/quick_validate.py` | Repository-original | Lightweight structural validator for this repository. |
| `cgpt-adversarial-reviewer/SKILL.md` | Repository-original/adapted design | Codex-owned synthesis inspired by local manuscript review workflows; no third-party text copied verbatim. |
| `cgpt-backup/scripts/make_backup.py` | Repository-original | Helper script for timestamped local backups. |
| `cgpt-render-check/scripts/render_check.py` | Repository-original | Helper script for local render-output checks. |
| `cgpt-jm-jmr-docx/scripts/pvb_format_docx.R` | Locally owned/adapted workflow material | Bundled as part of the user's JM/JMR DOCX formatting workflow. |
| `cgpt-jm-jmr-docx/scripts/pvb_format_text.R` | Locally owned/adapted workflow material | Bundled as part of the user's JM/JMR DOCX formatting workflow. |
| `cgpt-jm-jmr-docx/scripts/pvb_format_tables_v3.R` | Locally owned/adapted workflow material | Bundled as part of the user's JM/JMR DOCX formatting workflow. |
| `cgpt-jm-jmr-docx/references/academic_defaults.js` | Locally owned/adapted workflow material | Bundled reference constants for academic DOCX generation. |
| `cgpt-jm-jmr-docx/references/origin.md` | Repository-original provenance note | Documents source roots inspected and copied resources. |

## Public Release Checklist

- [x] Explicit repository license added.
- [x] README includes maintainer context and acknowledgments.
- [x] Bundled script/reference paths listed here.
- [x] No secret or environment files were found by filename scan at publication.
- [ ] Add more precise upstream license notes if any future bundled file comes
      from a third-party repository, package, article, or public example.

## Contributor Rule

Before adding a non-trivial copied or adapted file, record:

1. The source path or URL.
2. Whether the file is original, adapted, generated, or third-party.
3. The applicable license or permission basis.
4. Any restrictions on redistribution.
