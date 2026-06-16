---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: project_status
status: scaffold
date: 2026-06-16
created_real: 2026-06-16
---

# Current Status — 5 Listing Launch

| Item | Status |
|---|---|
| AutoDS account | **USER-PROVIDED CONTEXT — exists** |
| eBay store connected | **USER-PROVIDED CONTEXT — `divinit-92-us` (eBay.com / US / USD)** |
| AutoDS API status | **documented but GATED** (2026-06-16 docs discovery): public OpenAPI at `gw-docs.autods.com`, base `https://gw.autods.com`, Bearer JWT; access = **application + paid activation fee + subscription, no free trial, no read-only scope** → `GO_AUTODS_API_READ_ONLY_TEST` blocked without applying |
| n8n status | **not connected** (blueprint only; not installed/credentialed) |
| Integration scaffold | **created (internal)** — schemas/blueprints/checklists/templates only |
| Secrets | no `.env` values stored; `.env.example` = names only |
| Publishing | **not authorized** (`GO_PUBLISH_5` not given) |
| Live writes (import/repricing/auto-order) | **not authorized** |

## Phase
Internal execution-planning (scaffold built). No live action performed. Awaiting owner GO for the first live-touch step (AutoDS read-only API test).
