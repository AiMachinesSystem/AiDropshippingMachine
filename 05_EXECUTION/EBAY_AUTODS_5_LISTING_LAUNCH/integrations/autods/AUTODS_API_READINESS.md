---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: api_readiness_checklist
status: active
date: 2026-06-16
created_real: 2026-06-16
---

# AutoDS API Readiness Checklist

> What must be true BEFORE `GO_AUTODS_API_READ_ONLY_TEST`. No API call is made here; this is a checklist.
> API endpoint details are **NOT invented** — confirm them from official AutoDS API documentation.

| # | Item | Status | Note |
|---|---|---|---|
| 1 | AutoDS account exists | ✅ USER-PROVIDED | — |
| 2 | eBay store connected (`divinit-92-us`) | ✅ USER-PROVIDED | — |
| 3 | AutoDS API access enabled on the plan | ⬜ UNKNOWN | confirm in AutoDS account (plan may gate API) — USER INPUT NEEDED |
| 4 | API key obtainable | ⬜ UNKNOWN | from AutoDS account settings; store in `.env`/n8n, never chat/repo |
| 5 | API base URL + auth method | ⬜ TBD | `AUTODS_API_BASE_URL`; exact value + auth header = **PUBLIC RESEARCH REQUIRED** (AutoDS API docs) |
| 6 | Store ID known | ⬜ UNKNOWN | `AUTODS_STORE_ID` — from account; not in repo |
| 7 | Read-only endpoints identified | ⬜ TBD | e.g. get account / get store / list products — confirm exact paths from AutoDS API docs |
| 8 | Rate limits / pagination understood | ⬜ TBD | from AutoDS API docs |
| 9 | Secrets policy in place | ✅ | `.env` gitignored; `SECRETS_POLICY.md` |
| 10 | Read-only test scope defined | ⬜ | first call = a single read (e.g. account/store info), no writes |

## First read-only test (when GO given)
Single GET to a read-only endpoint (account or store info) using the env-managed key → log status only → confirm `divinit-92-us` is reachable. **No product/listing/order writes.** Stop and report.

## Forbidden until later gates
Any POST/PUT/PATCH/DELETE (import, list, reprice, order) — blocked. See `GO_GATES.md`.
