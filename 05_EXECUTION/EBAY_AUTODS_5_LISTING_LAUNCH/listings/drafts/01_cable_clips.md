---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: listing_draft
sku: DIVU-CBL-001
status: draft
validation_status: draft
date: 2026-06-16
created_real: 2026-06-16
---

# Draft 1 — Self-Adhesive Cable Clips (20-pack)

> DRAFT for review. No publish. Numbers labeled `[OBSERVED]/[ESTIMATE]/[UNKNOWN]`; cached evidence in `90_CACHE/fetches/products/`.

| Field | Value |
|---|---|
| sku | DIVU-CBL-001 |
| title | Self Adhesive Cable Clips 20pcs Cord Organizer Wire Holder Desk Wall Management (76 ch) |
| category | Computer Cable Ties & Organizers · **category_id 67858** [OBSERVED browse node — confirm leaf in Sell flow] |
| sale_price | $12.99 (test band $9.99–$14.99) |
| supplier | AliExpress (AutoDS-supported wholesale) · `aliexpress.us/item/3256808520144344` |
| cost | $1.15 [OBSERVED — aliexpress cable-clip pack] |
| est_fee | $2.17 [ESTIMATE = 12.99×0.136 + 0.40, eBay US FVF] |
| est_shipping | $0.00 (free per supplier — VERIFY landed) |
| **est_margin** | **~$9.67 (74.4%) [ESTIMATE]** |
| shipping_policy | <set in AutoDS — economy, handling ≤2d> |
| return_policy | 30-day returns |
| handling_time | 2 days |
| quantity | per AutoDS stock |
| condition | New |
| marketplace / currency | eBay.com / USD |

## Description (copy-paste ready)
Keep your cables tidy and within reach with this 20-piece self-adhesive cable clip set.

What you get:
- 20 reusable cable clips with strong adhesive backing
- Holds charging cables, USB cords, earphone wires, mouse/keyboard cables, and more
- No tools or drilling needed: peel, press, and stick to desk, wall, car, or nightstand
- Slots suit thin to medium cords; group several clips for multiple cables

How to use: 1) Clean and dry the surface. 2) Peel off the adhesive backing. 3) Press firmly 10–20 seconds. 4) Snap your cable into the slot.

Specifications: 20 clips · ABS plastic with adhesive backing · color as shown (assorted) · self-adhesive (no screws).

Note: For best hold, apply to smooth, clean, dust-free surfaces and let the adhesive set before loading cables. Ships from our supply partner; please allow standard handling and delivery time.

## Item specifics
- Type: Self-Adhesive Cable Clips / Cord Holder · Quantity: 20 · Material: ABS + adhesive · Mounting: Self-adhesive (no tools) · Compatible: charging/USB/earphone/mouse cables · Use: desk/wall/car · Color: assorted · Brand: Unbranded/Generic

## Evidence
- Demand: 61,056 active listings in category 67858 + one listing visibly 132 sold [OBSERVED lower-bound] (cache: `2026-06-16_ebay-category-67858.txt`, `..._ebay-cable-clips-demand.txt`).
- Supplier: $1.15 16–20pc pack [OBSERVED] (cache: `2026-06-16_aliexpress-adhesive-cable-clips.txt`).

## Brand / policy check
LOW. Generic commodity, no brand/logo. Reworded supplier "3M" reference out (verifier fix). Use plain/own photos — never reuse a seller's branded images.

## Verification gaps (confirm before `GO_IMPORT_5_DRAFTS`)
True sell-through (Terapeak) [UNKNOWN] · exact AliExpress SKU + live price + US shipping/ETA · leaf category in Sell flow · high competition ($2.70–$4.56 cheap cluster) → validate price.
