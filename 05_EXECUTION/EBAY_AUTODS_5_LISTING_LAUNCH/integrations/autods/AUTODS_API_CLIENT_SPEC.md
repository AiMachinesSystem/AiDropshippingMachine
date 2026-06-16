---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: api_client_spec
status: draft_spec
date: 2026-06-16
created_real: 2026-06-16
---

# AutoDS API Client Spec (read-only first)

> Language-agnostic specification for a future AutoDS client. **Spec only — no client built, no calls made.**
> Concrete endpoints/auth = **confirm from official AutoDS API docs** (not invented here).

## Configuration (from env / n8n credential — never hard-coded)
- `AUTODS_API_BASE_URL` · `AUTODS_API_KEY` · `AUTODS_STORE_ID` · `AUTODS_STORE_NAME=divinit-92-us`

## Auth
- Token/key in an `Authorization` header (exact scheme TBD from AutoDS docs). Key sourced from env/credential vault; never logged.

## Methods — PHASE 1: READ-ONLY ONLY (the only methods allowed until later GO)
| Method | Purpose | HTTP | Endpoint | Gate |
|---|---|---|---|---|
| `getAccount()` | account/plan info | GET | `<TBD — AutoDS docs>` | `GO_AUTODS_API_READ_ONLY_TEST` |
| `getStore(storeId)` | store status for `divinit-92-us` | GET | `<TBD>` | `GO_AUTODS_API_READ_ONLY_TEST` |
| `listProducts(storeId)` | existing products (read) | GET | `<TBD>` | `GO_AUTODS_API_READ_ONLY_TEST` |

## Methods — PHASE 2+: WRITE (NOT in scope; each behind its own GO)
`createDraft()` (`GO_IMPORT_5_DRAFTS`) · `publishListing()` (`GO_PUBLISH_5`) · `setRepricing()` (`GO_ENABLE_REPRICING`) · `enableAutoOrder()` (`GO_ENABLE_AUTO_ORDERING`). **Do not implement until the gate is open.**

## Cross-cutting
- **Retry:** ≤2 on transient errors; no retry loops.
- **Rate limits:** respect AutoDS limits (TBD from docs); backoff on 429.
- **Logging:** status codes + ids only; **never log the key or PII**.
- **Idempotency / safety:** Phase-1 client must be physically incapable of writes (no write methods compiled in).
- **Errors:** surface clearly; on auth failure, STOP (do not guess credentials).
