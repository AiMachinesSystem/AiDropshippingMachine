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
