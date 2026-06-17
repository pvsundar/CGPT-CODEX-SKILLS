---
name: cgpt-onedrive-git-safety
description: Work safely with Git repositories stored under OneDrive, Google Drive, Dropbox, iCloud Drive, or other synced Windows folders. Use before git status/add/commit/diff/reset/checkout in synced repos, when handling dirty worktrees, no-touch sibling repos, line-ending phantoms, stuck index.lock files, or closeout claims about tests/builds on synced filesystems.
---

# CGPT OneDrive Git Safety

Use this skill when a repo is inside a cloud-synced folder or when a Git closeout claim must be reliable.

## First Checks

1. Confirm the exact working directory with `Get-Location`.
2. Detect synced path indicators: `OneDrive -`, `OneDrive\`, `Google Drive`, `Dropbox`, `iCloud Drive`, `Box`.
3. Run Git from Windows-native PowerShell in this Codex environment. Treat bash-side Git reports from synced folders as advisory only.
4. If the user names a sibling folder or repo as no-touch, write down that boundary and do not inspect or modify it unless asked.
5. If Windows-native Git and another shell disagree, trust the Windows-native report for synced paths.

## Dirty Worktree Discipline

- Never run `git reset --hard`, `git checkout -- <file>`, or equivalent destructive cleanup unless the user explicitly asks.
- Do not revert changes you did not make.
- If unrelated dirty files exist, ignore them and scope Git operations to the files relevant to the task.
- Before staging, review `git status --short` and the relevant diffs from the Windows-native shell.

## Synced Filesystem Risks

- Stale status can over-report line-ending changes or under-report staged/deleted files.
- `.git/index.lock` can appear stuck because a prior shell or sync process held a handle.
- File content can differ between runtime, working tree, and committed blob if sync interfered.

If any Git state looks contradictory, pause Git mutations and re-check from a fresh Windows-native PowerShell session after the sync layer settles.

## Verification Before Closeout Claims

Before saying "tests pass", "build is clean", or "committed state is verified":

1. Run the relevant tests/builds.
2. Verify the files in the committed or staged state when a commit is involved:
   - `git show HEAD:<path>` for committed files.
   - `git diff --cached -- <path>` for staged files.
3. For high-stakes delivery, verify from a clean worktree or temporary worktree rather than only the live edited folder.

If full verification is not feasible, qualify the claim precisely.

On a synced filesystem, a runtime green check is not the same as a committed-state green check. When the claim is about `HEAD`, inspect the relevant `HEAD` blobs or run the pipeline from a temporary worktree/archive of that commit before calling it verified.

## Line Endings

- If Git reports whole-file diffs after a tiny edit, suspect CRLF/LF normalization.
- Use `cgpt-line-endings-hygiene` before rewriting Windows-origin files.
- Do not combine line-ending normalization with substantive edits unless the user explicitly asks.

## Report Back

When Git safety affected the work, report:

- The exact repo path used.
- Whether the path is synced.
- Which files were intentionally touched.
- Any dirty files left untouched.
- The verification command(s) actually run.
