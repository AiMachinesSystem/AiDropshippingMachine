---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: store_mapping
status: active
date: 2026-06-16
created_real: 2026-06-16
label: USER-PROVIDED CONTEXT
---

# AutoDS Store Mapping

| Field | Value | Source |
|---|---|---|
| AutoDS store name | `divinit-92-us` | USER-PROVIDED CONTEXT |
| Marketplace | eBay.com | USER-PROVIDED CONTEXT |
| Country | US | USER-PROVIDED CONTEXT |
| Currency | USD | USER-PROVIDED CONTEXT |
| Connection status | **connected** (per user-provided context) | USER-PROVIDED CONTEXT |
| AutoDS Store ID | `<unknown>` → `AUTODS_STORE_ID` (from owner's account; not in repo) | USER INPUT NEEDED |

## Notes
- The Store ID is read from `.env` / n8n credential, never hard-coded here.
- Seller context: US-registered seller → US buyers (see `02_DATA/owner_context.md`); US-domestic.
- This mapping is the canonical reference for the workflow's store target; do not list to any other store.

## Connection type: API vs non-API (MIP) — confirm for `divinit-92-us`
> `divinit-92-us` connection type is **UNKNOWN — USER INPUT NEEDED** (which one is set in AutoDS).
> Verified distinction (source: help.autods.com, 2026-06-16; cache `90_CACHE/fetches/autods.com/2026-06-16_ebay-api-vs-nonapi-mip.txt`):

| Aspect | **API store** | **Non-API (MIP)** |
|---|---|---|
| Connect via | eBay API permissions (grant AutoDS 3rd-party app mgmt) | AutoDS Chrome extension + eBay MIP token |
| Extra cost | none beyond plan | **+$9.97/month** per account |
| Automation | full price/stock/orders/tracking, minutes | via eBay File Exchange, ~5–10 min |
| Orders sync | automatic | only when extension active, last 7 days |
| Message center / dynamic policies | yes | no |
| Requirements | none special | computer **on 24/7**, Chrome, stable internet, **same IP** for eBay+MIP |

- **Account-impact note [VERIFIED]:** the standard API connection grants AutoDS **full third-party management** of the eBay account (not a read-only scope). No documented read-only connection mode.

