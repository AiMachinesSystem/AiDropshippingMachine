---
machine: "eBay / AutoDS Dropshipping Machine"
type: cleaned_data_table
module: 02_DATA
topic: AutoDS feature / plan / supplier capabilities
status: cleaned
date: 2026-06-15
created_real: 2026-06-15
source_class: "AutoDS-official (vendor)"
analysis: none
---

# CLEANED — AutoDS Capabilities (2026-06-15)

> Data only (no "is AutoDS good?" judgement — that's Analysis). All [OBSERVED] from AutoDS-official pages,
> cached under `90_CACHE/fetches/autods.com/` (2026-06-15). Plan/channel-dependent, USD, changes over time.
> Luca's plan, EUR pricing, and current add-ons = **USER INPUT NEEDED**. Full detail: `01_RAW_DATA/autods_docs/2026-06-15_autods-features-pricing-policy-raw.md`.

## Feature capability (as stated by AutoDS)
| Capability | What AutoDS states | Plan note |
|---|---|---|
| Product import | 1-click listing (single/bulk variations), Products importer | base |
| Price & stock monitoring | scans supplier price/stock **hourly** | base |
| Repricing | automatic price optimization + charm pricing | base |
| Order fulfillment | automated/"hands-free"; auto-ordering via **Orders Processor** add-on | add-on |
| Tracking | automated tracking-number updates (24/7) | base |
| Support tooling | case management, AI copy editor, bulk changes, poor-product remover | base |

## Channels & suppliers
| Item | Value |
|---|---|
| Selling channels | eBay, Shopify, Facebook Marketplace, Wix, WooCommerce, Etsy, Amazon, TikTok Shop |
| Suppliers (sourcing) | AliExpress, Amazon, Walmart, Alibaba, CJdropshipping, Banggood, Home Depot, eBay, Costco, Wayfair, Target, vidaXL + more (33 with regional variants) |
| Italy-region suppliers | Alibaba, AliExpress, Amazon, CJ Dropshipping, Costway, DHgate, eBay-Supplier (Walmart = US-only) |
| Data flag (not analysis) | many suppliers are retailers/marketplaces → see eBay retail-arbitrage prohibition in `policy_risk_table.md` |

## Pricing (USD, Help Center billing article)
| Plan / item | Price (annual / monthly) | Cap |
|---|---|---|
| Import 200 | $19.90 / $26.90 | 200 variations |
| Starter 400 (eBay) | $29.90 / $39.90 | 400 products |
| Advanced 800–1K | $49.90–$69.90 | 800–1,000 |
| Higher (→ Master 100K) | $106–$2,787 (channel-dependent) | scales |
| Orders Processor add-on | $9.90/mo | auto-ordering |
| Trial | $0.99 (public: $1) / 3 days, per channel, non-refundable | — |

## AutoDS's eBay-policy stance (VENDOR restatement — verify vs eBay primary)
- Allowed: wholesale agreements + owned-inventory fulfillment, seller-of-record on docs.
- Prohibited: retail arbitrage (Amazon/Walmart → eBay); penalties incl. **MC011** restriction, suspension.
- Suggests wholesale/private-label suppliers (CJdropshipping, Alibaba, Wholesale2B) + "Fulfilled by AutoDS".
- [PUBLIC RESEARCH REQUIRED] confirm against eBay.it/EU primary policy for Luca's site.
