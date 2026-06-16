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
> **Docs discovery (2026-06-16): the AutoDS API is application-gated + PAID** (one-time activation fee + ongoing
> subscription, **no free trial**; credentials issued only post-approval; **no read-only scope**). So
> `GO_AUTODS_API_READ_ONLY_TEST` via the official API **cannot proceed without first applying/qualifying/paying**.
> **Owner decision required:** **(A)** apply for the AutoDS API at `autods.com/api` (paid) → unlocks the API path;
> **or (B)** skip the API for now and use the **UI-based read-only intake** (guided review / screenshots) to gather
> the same store data with zero cost. Until decided, no live API step. See `integrations/autods/AUTODS_API_READINESS.md` ⛔.

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
