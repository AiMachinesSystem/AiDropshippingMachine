---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: api_readiness_checklist
status: active
date: 2026-06-16
created_real: 2026-06-16
docs_discovery: 2026-06-16
---

# AutoDS API Readiness Checklist

> Updated 2026-06-16 with **public docs discovery** (no API call, no login). Evidence labels:
> VERIFIED (official AutoDS page/spec) · PUBLIC SOURCE · UNKNOWN · REQUIRES ACCOUNT ACCESS.
> Source cache: `90_CACHE/fetches/autods.com/2026-06-16_*` (OpenAPI spec + help.autods.com).

| # | Item | Status | Note |
|---|---|---|---|
| 1 | AutoDS account exists | ✅ USER-PROVIDED | — |
| 2 | eBay store connected (`divinit-92-us`) | ✅ USER-PROVIDED | connection **TYPE (API vs non-API/MIP) UNKNOWN** — USER INPUT NEEDED |
| 3 | AutoDS API access enabled | ❌ **GATED** | API is **application-gated + paid**: apply at autods.com/api, qualify, pay one-time activation fee + ongoing subscription, **no free trial** [VERIFIED] |
| 4 | API token (bearer JWT) obtainable | ⬜ REQUIRES ACCOUNT ACCESS | issued only AFTER approval + payment; no public token-issuance endpoint [VERIFIED] |
| 5 | API base URL + auth method | ✅ VERIFIED | base `https://gw.autods.com`; auth = **Bearer JWT** (`Authorization: Bearer <JWT>`) |
| 6 | Store ID known | ⬜ UNKNOWN | `AUTODS_STORE_ID` from account; **no public "list stores" endpoint** (store = `{store_ids}` path param) |
| 7 | Read-only endpoint identified | ✅ VERIFIED | first-test candidate `GET /auto-order-v3/users/external/user-details`; also `/v1/users/current` |
| 8 | Rate limits / scopes | ⬜ REQUIRES ACCOUNT ACCESS | not public; released post-approval |
| 9 | Secrets policy in place | ✅ | `.env` gitignored; `SECRETS_POLICY.md` |
| 10 | Read-only test scope possible? | ⚠️ | endpoint known, BUT **no documented read-only scope**; standard eBay connection = FULL management grant [VERIFIED] |

## Verified from public docs (2026-06-16)
> Source: `https://gw-docs.autods.com/openapi.json` (AutoDS Gateway, OpenAPI 3.0.3, v1.0.11, 90 paths) + `help.autods.com`. Cache: `90_CACHE/fetches/autods.com/2026-06-16_gw-docs-openapi.txt`, `…_api-feature-access-requirements.txt`.
- **Base URL:** `https://gw.autods.com` [VERIFIED]. Public Swagger/spec at `gw-docs.autods.com/openapi.json`. (No `developers.autods.com`.)
- **Auth:** Bearer **JWT** (`autods_auth` = http/bearer/JWT). Header `Authorization: Bearer <JWT>`; POST bodies `application/json` [VERIFIED].
- **Read-only first-test endpoint:** `GET /auto-order-v3/users/external/user-details` ("Get User Details") [VERIFIED]. Other reads: `/v1/users/current`, `/auto-order-v3/suppliers/external/supported`.
- **Product/order endpoints** exist (`/api/products/…`, `/auto-order/order/…`); **stores** only via `{store_ids}` path param — no list-stores endpoint [VERIFIED].

## ⛔ BLOCKER — `GO_AUTODS_API_READ_ONLY_TEST` is NOT ready
1. AutoDS API access is **application-gated, PAID** (one-time activation fee + ongoing subscription, **no free trial**); full docs + credentials released **only after approval + payment** [VERIFIED — help.autods.com]. (Third-party snippets cite a ~$5,000 activation fee — **unverified** [PUBLIC SOURCE].)
2. Requires **intermediate/advanced technical knowledge or a dev team** [VERIFIED].
3. **No documented read-only scope / read-only connection mode**; the standard AutoDS↔eBay connection grants AutoDS **FULL third-party management permissions** over the eBay account [VERIFIED].
→ A near-term read-only API test via the official AutoDS API **cannot proceed without first applying, qualifying, and paying**. **Owner decision required** (apply for paid API vs use the UI-based read-only intake instead).

## Forbidden until later gates
Any POST/PUT/PATCH/DELETE (import, list, reprice, order) — blocked. See `GO_GATES.md`. No API call is made from this repo.
