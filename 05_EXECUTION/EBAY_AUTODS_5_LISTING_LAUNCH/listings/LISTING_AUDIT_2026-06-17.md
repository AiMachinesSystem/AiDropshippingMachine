---
machine: "eBay / AutoDS Dropshipping Machine"
type: listing_audit_actions
status: review (NO live action taken — owner reviews before any GO)
date: 2026-06-17
created_real: 2026-06-17
source: read-only Playwright tally — 90_CACHE/fetches/autods/audit_2026-06-17_012312/_products_list.json
---

# Listing Audit — recommended actions (214 active, read-only)

> **Nothing executed.** This is a review list. Per-listing rows: `listing_audit_actions_2026-06-17.csv`.
> Closing/repricing/fixing on eBay/AutoDS = live writes = GO-gated.

## Summary
- Active listings: **214** · recommended **KEEP** (sold>0): **13** · recommended **CLOSE**: **201**
- Error fixes needed: **VeRO-word: 63** · **supplier-title-changed: 100**
- Stock risk: 42 no-available-stock · Low margin (<20%): 37

## KEEP + REPRICE/RESTOCK (the proven winners — 13)
| Sold | Sell $ | Margin% | Stock | Flags | Title |
|---|---|---|---|---|---|
| 6 | 137.98 | 14.8 | 1 | - | Deck Jet J Style Pool Fountain Jet Replacement Fitting for Inground Pools |
| 5 | 41.83 | 19.7 | 1 | VeRO,title-changed | Ham Maker Stainless Steel Meat Press w/ Thermometer + 20 Cooking Bags | Deli DIY |
| 4 | 285.98 | 38.3 | 0 | VeRO | 2 Pack Adjustable Pet Grooming Loops – Nylon Restraint Noose for Dogs & Cats – Hands-Free  |
| 4 | 201.98 | 18.0 | 0 | title-changed | Dog Water Ramp for Boats & Pools (Holds 200 lbs) - 2025 Model with Pump |
| 3 | 127.0 | 17.8 | 1 | - | Lian Li 8.8" PC Display Universal - ARGB USB Screen Temp Monitor US88 V1 Black |
| 3 | 22.98 | 35.6 | 1 | VeRO,title-changed | Hedgehog Reusable Dryer Balls - Set of 2 (White) |
| 3 | 46.98 | 20.4 | 0 | VeRO,title-changed | Homemade Ham Maker & Deli Meat Press | Stainless Steel w/ Thermometer & Bags |
| 1 | 38.44 | 34.7 | 1 | VeRO | Beginner Crochet Kit Make Snail Dora Amigurumi Plush DIY Starter Set Video Guide |
| 1 | 69.98 | 14.6 | 1 | - | Hydrotools 8750 In Line Automatic Chlorine Feeder 9 lb Capacity Pool Chlorinator |
| 1 | 41.98 | 17.4 | 6 | - | Dog Life Jacket, Ripstop American Flag Dog Life Vest for Swimming Boating, Shark Puppy Lif |
| 1 | 69.95 | 21.6 | 1 | VeRO,duplicate,title-changed | Solar Stock Tank Pool Cover 8Ft Heavy Duty All Weather w/ Wire Rope & Winch |
| 1 | 67.98 | 21.2 | 0 | title-changed | 8FT Round Stock Tank Pool Cover Upgraded Full Coverage Wire Rope & Winch Blue |
| 1 | 28.98 | 26.5 | 0 | VeRO | Roller Idler Pulley Wheel 6x30x30mm with 626RS Bearing – Black (1Pc) |

## CLOSE candidates (0 sold / no stock / low margin — 201)
> Full list in the CSV. Breakdown by reason:
- 0 sold (dead weight) — **142**
- no available stock (OOS 1 / on-hold 0) — **24**
- no available stock (OOS 0 / on-hold 1) — **11**
- low margin 19% — **6**
- low margin 18% — **4**
- low margin 17% — **3**
- no available stock (OOS 2 / on-hold 0) — **2**
- low margin 20% — **2**
- low margin 16% — **2**
- low margin 14% — **2**
- low margin 13% — **1**
- low margin 15% — **1**
- low margin 2% — **1**

## FIX (compliance/data — live edit = GO)
- **VeRO-word flags: 63** (keywords e.g. Shenzhen/fidget/Masks/needle/Knife/alcohol — triage: real risk = fidget/knife/needle/masks; noise = Shenzhen/scent).
- **Supplier-title-changed: 100** (re-sync title from supplier or rewrite).

## How to use
1. Owner reviews the CSV. 2. Decide CLOSE scope (e.g. all 0-sold, or only no-stock+low-margin first). 3. Give per-batch GO: `GO_PRUNE_LISTINGS` (closes), `GO_UPDATE_PRICES` (reprice winners), `GO_FIX_LISTINGS` (VeRO/title). Auto-ordering stays OFF.
