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

> **Access note (2026-06-16):** the AutoDS API is application-gated + paid (no free trial); the JWT credential
> is issued only after approval + activation fee. See `AUTODS_API_READINESS.md` ⛔ BLOCKER. Endpoints below are
> VERIFIED from the public OpenAPI spec but **cannot be called until access is granted**.

## Configuration (from env / n8n credential — never hard-coded)
- `AUTODS_API_BASE_URL` = `https://gw.autods.com` [VERIFIED — gw-docs.autods.com/openapi.json, 2026-06-16]
- `AUTODS_API_KEY` (bearer JWT) · `AUTODS_STORE_ID` · `AUTODS_STORE_NAME=divinit-92-us`
- Public spec/Swagger: `https://gw-docs.autods.com/openapi.json` (AutoDS Gateway, OpenAPI 3.0.3, v1.0.11).

## Auth
- **Bearer JWT** — header `Authorization: Bearer <JWT>` (`autods_auth` = http/bearer/JWT) [VERIFIED]. POST bodies `application/json`.
- JWT issued **only after AutoDS API-feature approval + activation fee** [REQUIRES ACCOUNT ACCESS]; from env/credential vault; never logged or in repo/chat.

## Methods — PHASE 1: READ-ONLY ONLY (the only methods allowed until later GO)
| Method | Purpose | HTTP | Endpoint | Gate |
|---|---|---|---|---|
| `getUserDetails()` | account/user details (best first-test) | GET | `/auto-order-v3/users/external/user-details` [VERIFIED] | `GO_AUTODS_API_READ_ONLY_TEST` |
| `getCurrentUser()` | current user | GET | `/v1/users/current` [VERIFIED] | `GO_AUTODS_API_READ_ONLY_TEST` |
| `getSupportedSuppliers()` | supported suppliers | GET | `/auto-order-v3/suppliers/external/supported` [VERIFIED] | `GO_AUTODS_API_READ_ONLY_TEST` |
| `getProduct(productId)` | a product (read) | GET | `/api/products/{product_id}` [VERIFIED] | `GO_AUTODS_API_READ_ONLY_TEST` |

> No public "list stores" endpoint — stores appear only as a `{store_ids}` path param on write endpoints [VERIFIED].

## Methods — PHASE 2+: WRITE (NOT in scope; each behind its own GO)
`createDraft()` (`GO_IMPORT_5_DRAFTS`) · `publishListing()` (`GO_PUBLISH_5`) · `setRepricing()` (`GO_ENABLE_REPRICING`) · `enableAutoOrder()` (`GO_ENABLE_AUTO_ORDERING`). **Do not implement until the gate is open.**

## Cross-cutting
- **Retry:** ≤2 on transient errors; no retry loops.
- **Rate limits:** respect AutoDS limits (TBD from docs); backoff on 429.
- **Logging:** status codes + ids only; **never log the key or PII**.
- **Idempotency / safety:** Phase-1 client must be physically incapable of writes (no write methods compiled in).
- **Errors:** surface clearly; on auth failure, STOP (do not guess credentials).
