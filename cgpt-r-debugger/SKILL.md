---
name: cgpt-r-debugger
description: Reproducible R debugging, profiling, and edge-case testing for scripts, functions, Quarto analysis chunks, and data pipelines; use when the user asks to diagnose incorrect R output, slow code, brittle behavior, vectorization options, memory use, or runtime failures.
---

# CGPT R Debugger

Use this skill when the user asks to debug, profile, stress test, or optimize R code. Keep the work empirical and reproducible: run the smallest useful test harness, capture the error or timing evidence, and report the exact failure mechanism before proposing changes.

This is not broad R tutoring. Focus on concrete runtime behavior, profiling evidence, edge cases, and safe fixes.

## Guardrails

- Do not edit the user's R, QMD, data, or output files unless they explicitly ask for implementation after seeing the diagnosis.
- Prefer temporary scripts in the working directory or a project `diagnostics/` or `quality_reports/` folder only when the user permits artifacts.
- Do not install packages without approval. If a profiling package is unavailable, fall back to base R tools.
- Preserve project conventions from `CLAUDE.md`, `MEMORY.md`, `_quarto.yml`, renv files, and existing scripts.
- For analysis claims, distinguish observed runtime evidence from inferred causes.

## Workflow

1. Identify the target code path, expected output, inputs, side effects, and package/session assumptions.
2. Reproduce the issue with the smallest runnable harness:
   - source the function or script
   - load required inputs
   - set seeds and options when randomness or printing affects results
   - capture `sessionInfo()`, warnings, errors, and traceback
3. Add edge-case tests based on the code:
   - zero rows, one row, all `NA`, mixed types, duplicate keys, missing columns, factor versus character, unusual names, date/time boundaries, and larger synthetic inputs
4. Profile only after correctness is understood:
   - use `system.time()` for a baseline
   - use `Rprof()` and `summaryRprof()` for base-R profiling
   - use `bench`, `microbenchmark`, or `profvis` only when already available or approved
5. Classify the issue:
   - correctness bug
   - dependency or environment mismatch
   - data-shape assumption
   - numerical or statistical edge case
   - memory pressure
   - vectorization or algorithmic bottleneck
   - rendering or Quarto execution failure
6. Report the diagnosis with evidence and the smallest safe fix.

## R Debugging Patterns

Use base tools first:

```r
tryCatch(
  source("script.R"),
  error = function(e) {
    message("ERROR: ", conditionMessage(e))
    traceback()
  },
  warning = function(w) {
    message("WARNING: ", conditionMessage(w))
    invokeRestart("muffleWarning")
  }
)

sessionInfo()
```

For profiling:

```r
baseline <- system.time(source("script.R"))
print(baseline)

Rprof("profile.out")
source("script.R")
Rprof(NULL)
print(summaryRprof("profile.out"))
```

For edge-case checks, build a small table of test inputs and record actual versus expected behavior. Do not treat passing one happy-path run as sufficient when the requested problem concerns fragility.

## Performance Triage

Look specifically for:

- growing objects in loops with `rbind`, `cbind`, or `c(...)`
- row-wise loops over data frames where vectorized or grouped operations are clearer
- repeated file I/O inside loops
- repeated joins, filters, or model fits that can be hoisted or cached
- implicit type conversions, factor level loss, and date parsing inside tight loops
- non-deterministic order from joins, grouping, or parallel execution
- memory-heavy copies of large data frames

When recommending a refactor, show the before/after pattern only for the relevant lines and include timing evidence when possible.

## Report Format

Use this compact structure:

```markdown
# R Debugging Report

## Summary
- Target:
- Status: reproduced / not reproduced / partially reproduced
- Main cause:
- Proposed next action:

## Evidence
| Check | Result | Notes |
|---|---|---|

## Edge Cases
| Case | Expected | Actual | Status |
|---|---|---|---|

## Profiling
| Path or function | Time or share | Evidence |
|---|---:|---|

## Recommended Fixes
| Priority | Location | Fix | Rationale |
|---|---|---|---|
```

If the user asks for implementation, apply only the approved or explicitly scoped edits and rerun the reproduction harness afterward.
