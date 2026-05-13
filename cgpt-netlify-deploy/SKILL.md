---
name: cgpt-netlify-deploy
description: Prepare, deploy, and verify Vite or React single-page apps on Netlify. Use when the user asks to deploy to Netlify, fix a Netlify build, add SPA routing redirects, configure VITE environment variables, link GitHub to Netlify, or diagnose deployment failures such as vite not found, blank screen, cached deploys, or direct-route 404s.
---

# CGPT Netlify Deploy

Use this skill for Vite/React SPA deployment work. Treat deployment as a verifyable engineering workflow: inspect repo config, make minimal changes, run a local build when possible, then guide or execute Netlify steps depending on available tools and user approval.

## Pre-Deploy Checklist

1. Confirm project type and branch.
   - Inspect `package.json`, build scripts, router setup, and current Git branch.
   - Do not switch branches unless the user asks.

2. Ensure `netlify.toml` exists at repo root.

```toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"
```

3. Add required build-time public variables under `[build.environment]`.
   - Vite browser variables must be present at build time and must use `VITE_` prefixes.
   - Do not put `NODE_ENV = "production"` in `netlify.toml`; it can prevent devDependencies such as Vite from installing.
   - Public Supabase anon keys may be committed if the project already treats them as public browser config.

4. Ensure SPA redirects exist.
   - For React Router or client-side routing, create `public/_redirects` with exactly:

```text
/* /index.html 200
```

5. Build locally when feasible.
   - Run the repo's build command.
   - If dependencies are missing and network access is needed, ask for approval before installing.

## Deployment Workflow

1. Commit and push only when the user asks or deployment requires a Git-backed build.
2. Create or select the Netlify site.
3. Link the GitHub repository and production branch in Netlify.
4. Verify the deploy log shows a real build, not just cached uploaded files.
5. Open the deployed URL and test:
   - root route `/`
   - at least one direct deep link
   - browser console for build-time env errors
   - refresh/deep-link behavior for SPAs

## Failure Modes

| Symptom | Likely Cause | Fix |
|---|---|---|
| `vite: not found` | `NODE_ENV=production` caused devDependencies to be skipped | Remove `NODE_ENV`; rebuild |
| Direct route returns 404 | Missing SPA redirect | Add `public/_redirects` |
| Blank app with env error | `VITE_*` vars missing during build | Put vars in `netlify.toml [build.environment]`; trigger new build |
| Deploy says all files already uploaded | Netlify reused cached artifacts | Push a small committed change to force rebuild |
| Build command wrong | Netlify auto-detect mismatch | Set `command` and `publish` in `netlify.toml` |

## Rules

- Preserve unrelated repo changes.
- Never expose server-side secrets in browser config.
- Do not claim deployment success until the deployed URL and deep links have been checked or the limitation is reported.
- Prefer project-specific values from `.env.example`, README, or existing deployment notes; do not invent credentials.
