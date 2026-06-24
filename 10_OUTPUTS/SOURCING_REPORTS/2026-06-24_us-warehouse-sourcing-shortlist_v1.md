---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: us_warehouse_sourcing_shortlist
status: complete (internal sourcing/ranking/evidence — no live action; publish/import GO-gated)
date: 2026-06-24
created_real: 2026-06-24
owner_go: "Luca 2026-06-24 — Priorità 1 US-warehouse sourcing pipeline (no publish, only sourcing/ranking/evidence/output)"
method: "Cracked AutoDS Marketplace filter API (POST gw.autods.com/marketplace/api/products/). Authenticated
  replay via captured Bearer headers. 11 cluster pulls (categories + search_query), demand-gated rating>4.3 &
  rating_count>300 server-side, ordered spv_param desc. US-warehouse + on-niche filtered + brand/VeRO heuristic
  client-side. Evidence cache: 90_CACHE/fetches/autods/mkt_source_2026-06-24_021122 (raw + ranked JSON)."
tools: "marketplace_filter_probe.py, marketplace_filter_probe2.py (filter-API crack), marketplace_source.py
  (authenticated pull), rank_us_source.py (offline ranker)."
---

# US-Warehouse Sourcing Shortlist — Pool/Water · Kitchen · Meat/Food prep · Commodity (2026-06-24)

## Headline (the structural finding)
The AutoDS Marketplace filter API is **cracked and replayable**. Across 11 cluster pulls we pulled **1,669
unique demand-gated products** (rating>4.3 & review-count>300, the owner's >reviews method, server-side),
of which **1,077 are US-warehouse** and **693 are on-niche US-warehouse** (Pool/Kitchen/Meat-food/Cleaning/Storage).

**The key trade-off the data exposes — and it directly answers the sourcing question:**
> In this marketplace, **"US-warehouse + fast (1–5 day) + generic commodity" = Amazon-US sourced** (FBA).
> The **AliExpress US-warehouse** items exist but **ship 10–14 days** (slow). There is **no** "AliExpress +
> fast + generic" item in the entire 1,669-product pull.

So the 51 TEST candidates below are all **Amazon-US** (same source as the 10 already-live amazon10 listings,
~$7.5 profit each). They are generic-titled and VeRO-LOW, BUT carry the **retail-arbitrage account-health
risk** (flagged `eBay-policy = MED` on every row). The lower-policy-risk AliExpress US-warehouse items are
in the HOLD tier purely because of slow shipping. **This is the honest choice the owner now owns** (see §Decision).

## Demand gate & economics labels (read before the table)
- **[FACT]** Every product cleared `rating > 4.3 AND rating_count > 300` (AutoDS server-side filter — the
  exact filter the marketplace "winning" feed uses, which is the owner's confirmed >reviews demand proxy).
- **[ESTIMATE]** `Est.sell` = AutoDS `min_msrp_price` (its *suggested* sell). `Est.margin` = `min_msrp − buy − ship`.
  This is **GROSS, pre-eBay-fee**. After eBay's ~13.25% FVF + $0.40 the **net** is ~$3.5–5 lower per item.
  Our real listing price would be set by the pricing policy (buy + ~$12–14) to net ~$7.5 — so these gross
  margins **understate** what we'd actually list at; they are a conservative floor, not the final number.
- **[FACT]** `WH`, `Ship(d)` (=max_shipping_time), `Cost` (=min_price) are observed from product_details.
- **[UNKNOWN]** per-item exact review count (server-gated but not in payload); live eBay sell-through; whether
  each Amazon source stays in stock; the precise VeRO status of each brand token (heuristic, not a legal check).

## TEST shortlist (top 24 of 51) — US-warehouse · generic(VeRO-LOW) · fast(≤5d) · on-niche
Source/evidence for every row: AutoDS Marketplace pull run **2026-06-24_021122** (cache above); `id_on_site`
is the supplier ASIN for AutoDS import. Recommendation rule: TEST = US + on-niche + VeRO-LOW + ship≤5 + gross-margin≥$5.

| # | Product | Source / supplier | WH | Ship(d) | Cost$ | Est.sell$ | Est.margin$ (gross) | VeRO | eBay-policy | Rec | id_on_site |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [25 Set] 20oz Meal Prep Containers with Lids | Amazon-US / Shoplenty | US | 1 | 15.99 | 23.83 | 7.84 (32.9%) | LOW | MED | TEST | B079VX6DSG |
| 2 | Stainless Steel Spider Strainer / Skimmer (kitchen) | Amazon-US | US | 2 | 13.86 | 20.37 | 6.51 (32.0%) | LOW | MED | TEST | B07PCM3BNL |
| 3 | Meat Thermometer Instant Read (strip "GAISTEN") | Amazon-US | US | 2 | 19.99 | 26.19 | 6.20 (23.7%) | LOW | MED | TEST | B08789RNLH |
| 4 | 4 Pack Bento Snack Containers (4-compartment) | Amazon-US | US | 2 | 13.57 | 19.54 | 5.97 (30.6%) | LOW | MED | TEST | B0B5HM5VRN |
| 5 | 3 Pack Spin Mop Replacement Head Microfiber | Amazon-US / SSGP | US | 2 | 15.99 | 21.91 | 5.92 (27.0%) | LOW | MED | TEST | B07W18LHMB |
| 6 | Stainless Steel Fish Spatula (1.2mm blade) | Amazon-US | US | 2 | 16.99 | 22.77 | 5.78 (25.4%) | LOW | MED | TEST | B08RJ4RHBS |
| 7 | Drill Brush Power Scrubber Kit (cleaning) | Amazon-US / Drillbrush | US | 2 | 17.99 | 23.03 | 5.04 (21.9%) | LOW | MED | TEST | B07CNW7Q77 |
| 8 | Pan/Pot Lid Holder Rack Organizer (strip "blitzlabs") | Amazon-US | US | 4 | 13.99 | 20.29 | 6.30 (31.0%) | LOW | MED | TEST | B08GPHPMMN |
| 9 | Scrub Brush Set of 3 (ergonomic handle) | Amazon-US | US | 4 | 16.99 | 22.94 | 5.95 (25.9%) | LOW | MED | TEST | B0921KYLZQ |
| 10 | 12x Large Storage Bags w/ Zipper, 5-Gallon | Amazon-US / Clear Goods | US | 4 | 14.99 | 20.09 | 5.10 (25.4%) | LOW | MED | TEST | B09W6WT613 |
| 11 | E-Cloth Deep Clean Microfiber Mop | Amazon-US / E-Cloth Inc. | US | 5 | 34.99 | 51.79 | 16.80 (32.4%) | LOW | MED | TEST | B003WKSTJY |
| 12 | Glass Food Storage Containers Airtight (locking) | Amazon-US | US | 5 | 29.99 | 44.39 | 14.40 (32.4%) | LOW | MED | TEST | B087Z1RDN2 |
| 13 | Kitchen Gadget Set Stainless (strip "COOK WITH COLOR") | Amazon-US | US | 5 | 29.99 | 43.49 | 13.50 (31.0%) | LOW | MED | TEST | B08WR3KT8F |
| 14 | Silicone Kitchen Utensils Set 34pc, 450°F | Amazon-US | US | 5 | 26.99 | 40.22 | 13.23 (32.9%) | LOW | MED | TEST | B01HE1FVVU |
| 15 | 10 Pack Wooden Cooking Utensils (teak) | Amazon-US | US | 5 | 29.99 | 42.59 | 12.60 (29.6%) | LOW | MED | TEST | B08CZWHH4W |
| 16 | Round Grill Cover Heavy Duty Waterproof (strip "i COVER") | Amazon-US | US | 5 | 24.75 | 36.38 | 11.63 (32.0%) | LOW | MED | TEST | B07H57D1R2 |
| 17 | Stainless Steel Griddle Spatula/Scraper Set | Amazon-US | US | 5 | 25.99 | 37.43 | 11.44 (30.6%) | LOW | MED | TEST | B07H4QBWMT |
| 18 | 35 Pack 8" Square Baking Cake Pans w/ Lids (strip "Fig & Leaf") | Amazon-US | US | 5 | 25.99 | 37.17 | 11.18 (30.1%) | LOW | MED | TEST | B07DNMK1W7 |
| 19 | Microfiber Wet Mops 24in Heavy Duty Flat Floor Mop | Amazon-US | US | 5 | 27.19 | 38.07 | 10.88 (28.6%) | LOW | MED | TEST | B07NQD63DG |
| 20 | Copper Measuring Cups & Spoons Set 8pc | Amazon-US / Styled Settings | US | 5 | 22.99 | 32.88 | 9.89 (30.1%) | LOW | MED | TEST | B07QRYPVG9 |
| 21 | Extra Large Plastic Cutting Boards (Set of 3) | Amazon-US | US | 5 | 24.98 | 34.22 | 9.24 (27.0%) | LOW | MED | TEST | B0CKXN981F |
| 22 | Large Glass Food Storage 4pc (63oz) | Amazon-US / Razab | US | 5 | 29.99 | 38.39 | 8.40 (21.9%) | LOW | MED | TEST | B08514ZZ8G |
| 23 | 12in Pre-Seasoned Cast Iron Skillet | Amazon-US / Italic Labs | US | 5 | 24.99 | 33.24 | 8.25 (24.8%) | LOW | MED | TEST | B074ND5RDT |
| 24 | 4 Pack Overnight Oats Glass Mason Jars w/ Lids+Spoons | Amazon-US | US | 5 | 19.99 | 28.19 | 8.20 (29.1%) | LOW | MED | TEST | B0DHXSFDXL |

*(Full 51-row TEST list + 404 HOLD + 238 KILL in cache `_ranked_onniche.json`.)*
By niche (on-niche US-WH total / TEST): kitchen 250/22 · storage 137/7 · meat_food 117/6 · pool 91/7 · cleaning 98/9.

## HOLD contrast — AliExpress US-warehouse (lower policy risk, but slow)
These avoid retail-arb risk (eBay-policy LOW) but **ship 10–14 days** → HOLD, not TEST. Useful if the owner
prefers AliExpress sourcing and accepts slow delivery (or for items where speed matters less).

| Product | Source | WH | Ship(d) | Cost$ | Est.sell$ | Est.margin$ | VeRO | Rec |
|---|---|---|---|---|---|---|---|---|
| French Press Coffee Pot Stainless | AliExpress | US | 11 | 23.48 | 30.99 | 7.51 | LOW | HOLD |
| Portable BBQ Charcoal Grill Mini (meat) | AliExpress | US | 13 | 25.19 | 34.01 | 8.82 | LOW | HOLD |
| 3-in-1 Rotary Cheese Grater / Veg Slicer (strip "LMETJMA") | AliExpress | US | 10 | 20.44 | 26.78 | 6.34 | MED | HOLD |
| 5L Electric Meat Grinder Stainless | AliExpress | US | 12 | 33.02 | 48.54 | 15.52 | MED | HOLD |
| Adjustable Mandoline Slicer Stainless (strip "LMETJMA") | AliExpress | US | 10 | 38.05 | 55.55 | 17.50 | MED | HOLD |

## Decision (recommended, confidence MEDIUM-HIGH)
1. **Sourcing rule is now operational, not theoretical.** We can pull demand-gated, US-warehouse, on-niche
   candidates on demand via the cracked filter API. This replaces guesswork. **[FACT — tool runs, evidence cached.]**
2. **The fast generic winners are Amazon-US** = the *proven amazon10 path*. Recommended next launch batch =
   the top ~10 TEST rows (kitchen + cleaning + pool commodity, ship 1–4d, gross-margin ≥ $5), titles rewritten
   generic (strip the brand tokens flagged) — VeRO-safe. **Risk owned: retail-arbitrage (eBay-policy MED), same
   as the 10 already live.** This is a deliberate, labeled risk, not a hidden one.
3. **If the owner wants to cut policy risk → go AliExpress US-warehouse (HOLD tier), accept 10–14d shipping.**
   Trade speed for account-health. A blended batch (some Amazon-fast, some AliExpress-low-risk) is also viable.
4. **Rejected:** the high-ticket US items ($200–750 saunas/fridges/motors) — off-model (thin-margin commodity
   is our lane) and heavily branded (VeRO HIGH). The CN-warehouse AliExpress items — they reproduce the
   location wall (E-008/E-010) the whole prior session hit. Branded megabrand items — VeRO HIGH → KILL.

## Owner role / next gate
- **No live action taken** (sourcing/ranking only — per mandate). Importing any of these as drafts and
  publishing them is **GO-CLASS** (separate GO). On GO: import top-N as drafts → generic-title rewrite →
  publish via the proven amazon10 pipeline.
- Permanent sourcing rule recorded in `07_LEARNING/sop_improvements.md` (US-warehouse-first).

> Evidence basis: marketplace filter API crack + authenticated pull, run 2026-06-24_021122 [OBSERVED, cached].
> Demand gate server-side [FACT]. Margins gross/pre-fee [ESTIMATE]. Sell-through & stock persistence [UNKNOWN].
> No invented numbers; brand/VeRO is a heuristic flag, not a legal clearance.
