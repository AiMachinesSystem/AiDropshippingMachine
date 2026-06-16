---
machine: "eBay / AutoDS Dropshipping Machine"
type: source_discovery_plan
module: 02_DATA
status: plan_only
date: 2026-06-15
collection_status: not_started
---

# Source Discovery Plan — eBay / AutoDS Dropshipping Machine

## Stop Rule

This is a source plan only.

Do not collect data.
Do not browse.
Do not access eBay, AutoDS, suppliers, payment accounts, or any live platform.
Stop before collection unless owner approves Data Collection.

## Source Plan

| Source | Source Type | Why It Matters | Expected Data | Access Status | Public / Private | Confidence | Limitations | If Collection Is Approved | Archive Destination |
|---|---|---|---|---|---|---|---|---|---|
| eBay Seller Hub | Account dashboard | Core owned account, listing, performance, account health, messages, order data | Account status, limits, listings, sales, orders, cancellations, defects, late shipment, tracking, returns, feedback | Not approved | Private | High if owner-provided/exported | Requires owner login/access; account-specific | Collect screenshots/exports only or read-only with approval | 02_DATA/01_RAW_DATA/eBay_seller_hub/ |
| eBay Seller Hub Account Health / Performance | Account dashboard | Detect suspension, defect, cancellation, late shipment, tracking and service risk | Account health status, performance metrics, seller level, warnings | Not approved | Private | High if owner-provided/exported | Current eBay metric definitions require verification | Archive owner-provided screenshots/exports | 02_DATA/01_RAW_DATA/account_health/ |
| AutoDS Dashboard | Automation dashboard | Understand store connection, automation, product imports, suppliers, repricing, orders, tracking | Product list, automation settings, supplier setup, repricing rules, order status, tracking sync, errors | Not approved | Private | High if owner-provided/exported | Requires owner access; settings can change | Archive screenshots/exports; no settings changes | 02_DATA/01_RAW_DATA/autods/ |
| Supplier Platforms | Supplier websites/accounts | Validate price, stock, shipping, tracking, return terms, handling time, product restrictions | Supplier cost, inventory, ship-from, delivery estimates, return terms, tracking availability | Not approved | Public/private depending supplier | Medium until verified | Prices/stock change; terms vary; access may be required | Collect candidate supplier facts and terms | 02_DATA/01_RAW_DATA/suppliers/ |
| eBay Search Results | Marketplace public search | Identify competing listings, price bands, title patterns, shipping/return positioning, visible demand signals | Listing titles, prices, shipping, returns, seller signals, sold/availability if visible | Not approved | Public | Medium | Public data cannot prove profit or conversion; search personalization risk | Collect search snapshots for approved keywords/categories | 02_DATA/01_RAW_DATA/ebay_search/ |
| Competitor Listings | Marketplace public listing pages | Understand direct listing structure, images, item specifics, policies, trust signals | Title, photos, item specifics, price, shipping, returns, seller feedback, visible sales signals if available | Not approved | Public | Medium | Competitor economics unknown; sold data may be partial | Capture approved competitor listing facts | 02_DATA/01_RAW_DATA/competitor_listings/ |
| Terapeak / Product Research Tools | Research tool | If available, supports demand, sold price, seasonality, competition review | Sold trends, average sold price, sell-through indicators, keyword/category signals | Not approved / Availability unknown | Private/tool-gated | Medium if available | Tool access unknown; data definitions require verification | Collect exported research records only if owner has access | 02_DATA/01_RAW_DATA/product_research_tools/ |
| AutoDS Product Research Tools | Platform tool | Candidate SKU discovery and supplier mapping | Product ideas, supplier links, estimated demand, costs, imports | Not approved | Private | Medium if available | Tool estimates may be proprietary/incomplete | Capture candidate product facts only | 02_DATA/01_RAW_DATA/autods_product_research/ |
| Fee Calculators | Public or platform calculator | Estimate eBay fees, payment fees, final value fees, optional costs, breakeven | Fee estimates by category/price/shipping | Not approved | Public/tool | Medium | Current fee rules require verification; category-dependent | Collect calculator outputs and assumptions | 02_DATA/02_CLEANED_DATA/fee_table.md |
| eBay Policy Pages | Public policy source | Validate dropshipping rules, listing rules, tracking, shipping, returns, seller performance requirements | Current eBay policy language and requirements | Not approved | Public | High if current official source | Must verify current pages; no memory assumptions | Collect policy excerpts and source dates | 02_DATA/01_RAW_DATA/policies/ |
| AutoDS Help / Documentation | Public/private documentation | Validate features, automation behavior, supported suppliers, order/tracking rules | Feature documentation, settings behavior, limitations | Not approved | Public/private | Medium | Tool features may change; plan-specific | Collect official docs and owner plan context | 02_DATA/01_RAW_DATA/autods_docs/ |
| Customer Feedback / Review Sources | eBay feedback, listing reviews, competitor feedback | Detect objections, product quality issues, shipping complaints, trust concerns | Feedback comments, ratings, complaint themes | Not approved | Public/private | Medium | Public feedback may be biased; own messages may contain PII | Collect non-PII public themes or redacted own feedback | 02_DATA/01_RAW_DATA/reviews_feedback/ |
| Shipping / Tracking Sources | Supplier shipping pages, carrier/tracking info, AutoDS tracking behavior, eBay shipping policy | Control delivery promise and tracking upload risk | Handling time, ship-from, carrier, tracking availability, delivery estimate | Not approved | Public/private | Medium | Varies by supplier/SKU/location | Collect shipping fields for candidate SKUs | 02_DATA/02_CLEANED_DATA/shipping_table.md |
| Return / Refund Sources | eBay return settings, supplier returns, owner policies | Prevent mismatch between supplier terms and eBay buyer expectations | Return windows, refund rules, restocking, labels, costs | Not approved | Public/private | Medium | Policy mismatch risk; requires current verification | Build return/refund comparison table | 02_DATA/02_CLEANED_DATA/returns_refunds_table.md |

## Collection Scope If Approved Later

1. Start with owner-provided screenshots/exports.
2. Capture raw data first.
3. Create cleaned tables second.
4. Log missing data.
5. Log data quality limits.
6. Stop before analysis unless owner authorizes Analysis.
