---
name: cgpt-tool-routing-lessons
description: Apply Codex-native routing lessons for filesystem sandbox boundaries, connector scopes, local workspace paths, escalation, and tool choice. Use when file access fails, paths are outside the workspace, connectors may be needed, writes require approval, or a task crosses local/cloud/profile directories.
---

# CGPT Tool Routing Lessons

Use this skill when a task involves uncertain file reach, sandbox boundaries, connector-backed files, cloud-synced folders, or paths outside the current writable workspace.

This is a Codex-native adaptation of prior tool-routing lessons. Do not copy Cowork/Desktop Commander mechanics into Codex sessions.

## Routing Rules

1. Workspace files.
   - Read with normal shell commands, preferring `rg`, `Get-Content`, and targeted `Get-ChildItem`.
   - Edit with `apply_patch` for manual file edits.
   - Use repo-local validation before claiming success.

2. Writable roots.
   - Confirm whether the target path is inside the current writable roots before editing.
   - If it is outside, request approval with `sandbox_permissions: require_escalated`.
   - Do not work around approvals by writing elsewhere and asking the user to copy.

3. Connector files.
   - If a user explicitly references Google Drive, Gmail, GitHub, or similar app context, prefer the relevant connector/plugin when available.
   - If connector access is unavailable but a synced local tree exists, use the local synced path and state that route.

4. User profile or app config paths.
   - Treat `%APPDATA%`, `%LOCALAPPDATA%`, `.codex`, `.claude`, program folders, and system paths as outside normal workspace scope.
   - Reads may be allowed; writes usually require escalation or explicit user authorization.

5. Network or dependency operations.
   - If a required command fails due to network, sandbox, or registry/index access, rerun with escalation and a clear justification.
   - Do not silently skip dependency installation if it is required for the requested verification.

## Failure Signatures

| Symptom | Likely cause | Action |
|---|---|---|
| Access denied in a profile or temp path | sandbox or filesystem ACL | switch to workspace path or request escalation |
| File exists in Explorer but command cannot see it | wrong drive, sync state, allowlist, or path quoting | verify exact path with `Get-Item -LiteralPath` |
| Git sees huge whole-file diffs | line endings or encoding churn | use `cgpt-line-endings-hygiene` |
| A connector file cannot be read locally | not synced or connector required | use the app connector or ask for path/export |
| Dev/test command cannot download packages | restricted network | rerun with escalation if needed |

## Reporting

When routing mattered, report:

- which path was used
- whether it was workspace, synced local, connector, or profile/config
- whether escalation was required
- any path or access limitation that remains

## Boundaries

- Do not edit memory or profile-level configuration unless the user explicitly asks and the target is verified.
- Do not assume a path from a previous tool environment is valid in Codex.
- Do not use destructive filesystem commands without explicit request and path verification.
