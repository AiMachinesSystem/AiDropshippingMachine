---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: listing_validation_checklist
status: active
date: 2026-06-16
created_real: 2026-06-16
---

# Listing Validation Checklist (per listing, before any import/publish)

> Run on each of the 5 rows BEFORE `GO_IMPORT_5_DRAFTS`. All checks must pass (status → `validated`).
> Policy references: `02_DATA/02_CLEANED_DATA/policy_risk_table.md`, `fee_table.md`.

| # | Check | Pass condition |
|---|---|---|
| 1 | **Title** | non-empty, ≤80 chars, no prohibited/trademark terms |
| 2 | **Price** | `sale_price` > 0; sensible vs `cost` (gross spread positive — flag only, no profitability verdict here) |
| 3 | **Margin sanity** | `sale_price` covers `cost` + eBay FVF (≈13.6% + $0.30/$0.40) + shipping — flag if non-positive (informational, not a strategy call) |
| 4 | **Images** | ≥1 valid image URL; no placeholder/broken links |
| 5 | **Supplier URL** | valid `source_url`; supplier present |
| 6 | **eBay policy risk** | supplier is wholesale/owned-inventory, **NOT retail arbitrage** (no Amazon/Walmart-shipped-direct); no prohibited/restricted item; no IP/VeRO risk |
| 7 | **Duplicate SKU** | `sku` unique across the 5 rows and the store |
| 8 | **Shipping** | `shipping_policy` set; `handling_time` ≤ 2 days (eBay recommendation) |
| 9 | **Returns** | `return_policy` set (e.g. 30-day); consistent with eBay MBG |
| 10 | **AutoDS compatibility** | category/fields map to AutoDS draft payload; supplier supported by AutoDS |
| 11 | **Constants** | `marketplace=eBay.com`, `currency=USD`, `condition` ∈ enum |
| 12 | **Schema** | row validates against `ebay_listing_schema.json` (all required fields present) |

## Outcome
- All pass → `validation_status = validated` (eligible for `GO_IMPORT_5_DRAFTS`).
- Any fail → `rejected` + reason; fix before re-validating. **No publish on any unvalidated row.**
