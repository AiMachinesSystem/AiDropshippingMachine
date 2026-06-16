---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: project_next_actions
status: scaffold
date: 2026-06-16
created_real: 2026-06-16
---

# Next Actions — 5 Listing Launch

## Exact next step
> Owner reviews this scaffold. To take the first live-touch step, give **`GO_AUTODS_API_READ_ONLY_TEST`** —
> a read-only AutoDS API check to confirm credentials/connectivity for store `divinit-92-us`. No writes, no import, no publish.

## Internal (no GO needed)
- [ ] Owner-side: confirm AutoDS API access exists (key obtainable from AutoDS account) — do NOT paste it in chat.
- [ ] Fill `listings/sample_5_listing_input.csv` with 5 real candidate rows (internal draft; not published).
- [ ] Review `listings/ebay_listing_schema.json` + `LISTING_VALIDATION_CHECKLIST.md`.

## Gated (each needs its GO — see GO_GATES.md)
1. `GO_AUTODS_API_READ_ONLY_TEST` — read-only API connectivity test.
2. `GO_CREATE_N8N_CREDENTIAL` — store AutoDS key in n8n credential vault (not in repo).
3. `GO_IMPORT_5_DRAFTS` — import 5 drafts into AutoDS (no publish).
4. `GO_PUBLISH_5` — publish the 5 listings (final live step).
5. `GO_ENABLE_REPRICING` / `GO_ENABLE_AUTO_ORDERING` — post-launch automation (separate, later).

## Blocked until earlier gates pass
Publishing, repricing, auto-ordering, live order processing.
