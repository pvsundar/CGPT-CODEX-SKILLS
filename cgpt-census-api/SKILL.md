---
name: cgpt-census-api
description: Query, plan, or generate R/Python/API workflows for U.S. Census Bureau data such as ACS, decennial census, population estimates, County Business Patterns, FIPS codes, geographies, variables, and demographic tables. Use when the user asks for Census data or public demographic/economic statistics.
---

# CGPT Census API

Use this skill for U.S. Census Bureau data workflows: finding variables, choosing geographies, building API URLs, writing R/Python fetch code, or explaining Census results.

## Security And Currency

- Do not embed API keys in skill files, reports, scripts, or examples.
- Prefer `CENSUS_API_KEY` from the environment when a key is needed.
- If no key is available, use endpoints that work without a key for small queries or ask the user whether to provide one.
- Census datasets and vintages change. Verify available dataset years and variable names from Census metadata before relying on them for current work.
- If network access is required and unavailable, produce reproducible code and state that live verification was not run.

## Workflow

1. Clarify the question:
   - geography: nation, state, county, tract, place, metro, ZCTA
   - dataset: ACS 1-year, ACS 5-year, ACS profile/subject, decennial, PEP, CBP, Economic Census
   - vintage/year
   - variables or table IDs
   - output format: table, CSV, R, Python, URL, map-ready data
2. Verify dataset and variable availability when live access is possible.
3. Build the query using `get=`, `for=`, and `in=` predicates.
4. Include `NAME` and relevant margin-of-error variables for ACS estimates when appropriate.
5. Return tidy output code and caveats about geography, vintage, margins of error, and suppressed/missing values.

## Common Patterns

API shape:

```text
https://api.census.gov/data/{year}/{dataset}?get=NAME,{variables}&for={geography}&in={container}
```

Washington examples:

- state FIPS: `53`
- King County: `033`
- Pierce County: `053`
- Snohomish County: `061`

ACS variable suffixes:

- `E`: estimate
- `M`: margin of error
- `EA` or `MA`: annotation

## R Pattern

```r
library(httr2)
library(jsonlite)

key <- Sys.getenv("CENSUS_API_KEY")
base <- "https://api.census.gov/data/2023/acs/acs5"
query <- list(
  get = "NAME,B19013_001E,B19013_001M",
  `for` = "county:*",
  `in` = "state:53"
)
if (nzchar(key)) query$key <- key

resp <- request(base) |> req_url_query(!!!query) |> req_perform()
raw <- resp_body_json(resp, simplifyVector = TRUE)
```

## Python Pattern

```python
import os
import requests

params = {
    "get": "NAME,B19013_001E,B19013_001M",
    "for": "county:*",
    "in": "state:53",
}
key = os.getenv("CENSUS_API_KEY")
if key:
    params["key"] = key

response = requests.get("https://api.census.gov/data/2023/acs/acs5", params=params, timeout=30)
response.raise_for_status()
rows = response.json()
```

## Report Requirements

Always report:

- dataset and vintage
- geography and FIPS assumptions
- variables used and plain-English definitions
- whether live API verification ran
- limitations such as ACS margins of error, 1-year population thresholds, missing data, or vintage mismatch
