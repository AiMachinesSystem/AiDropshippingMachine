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
| AutoDS account | **CONNECTED (read-only) — `Divinit-92-Us` id 3713044** (verified live via Playwright 2026-06-16) |
| eBay store | **`divinit-92-us` (eBay.com / US / USD)** — **214 active listings, 11 drafts (+4 untracked), 23 lifetime orders, $62 profit/7d** [OBSERVED 2026-06-16] |
| AutoDS subscription | **TRIAL — expires 2026-06-18** (orders_processor add-on trial too); decision needed (renew vs lapse) |
| AutoDS read-only access | **OPERATIONAL via Playwright** — saved `storage_state.json` (gitignored); scripts: smoke_test / login / read_autods_status / read_products_counts / read_drafts_count / read_marketplace |
| AutoDS REST API | **GATED** — public OpenAPI (`gw-docs.autods.com`, Bearer JWT) but access = application + paid activation + subscription, **no key issued** → `GO_AUTODS_API_READ_ONLY_TEST` still blocked (Playwright path used instead) |
| Auto-ordering | toggled ON but **NON-FUNCTIONAL** (0 buyer accounts, $0 wallet) — do not enable half-configured |
| Health flags | 1 draft VeRO keyword ('alcohol'); some listings OOS/On-Hold/supplier-title-changed (full tally pending) |
| n8n status | **not connected** (blueprint only) |
| Secrets | real `.env` + `autods_credentials.env` + `storage_state.json` present **locally, gitignored** (never committed) |
| Publishing / live writes (import/reprice/auto-order) | **not authorized** (`GO_IMPORT_5_DRAFTS` / `GO_PUBLISH_5` / `GO_ENABLE_REPRICING` / `GO_ENABLE_AUTO_ORDERING` all CLOSED) |

## Phase
Read-only intelligence complete: AutoDS account read, capability audit, deep product research, and an autonomous strategic decision (`04_STRATEGY/STRATEGIC_DECISION_2026-06-16.md`) all produced 2026-06-16 with **zero live writes**. Immediate owner decision: **renew AutoDS trial before 2026-06-18**. Next live-touch steps (fix VeRO/OOS, import test SKUs) remain behind their GO gates.
