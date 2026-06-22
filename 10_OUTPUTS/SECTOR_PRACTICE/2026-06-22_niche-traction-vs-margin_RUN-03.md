---
machine: "eBay / AutoDS Dropshipping Machine"
type: sector_practice_run
run_id: SECTOR-PRACTICE-2026-06-22-03
status: PASS
date: 2026-06-22
created_real: 2026-06-22
---

# SECTOR PRACTICE RUN-03 — Niche traction vs margin (all 99)

## 1. SYSTEM
- **Objective:** group the 99 live listings into meta-niches and cross **traction** (real sales) with **margin**, to direct future sourcing — which niches to deepen, which to stop listing.
- **Input:** `audit_2026-06-22_044324/_products_list.json` (`category`, `total_sold_count`, `variation_statistics`). **Method:** bucket by eBay `category.name` + title keywords into 12 meta-niches; traction = `total_sold_count`; margin = `min_profit/min_sell_price`.
- **Data-quality flag [OBSERVED]:** this JSON has **no watcher field** (`variation_statistics` keys: stock/price/profit/region only). RUN-02's watcher segmentation is **not reproducible from this source** → the only verifiable engagement signal here is `total_sold_count`. Treat watcher figures from prior runs as UNVERIFIED until a source with that field is re-confirmed.

## 2. DATA [OBSERVED — AutoDS cache, 2026-06-22]
99 listings · **70 distinct eBay categories** · total lifetime **35 sold-units** across 13 selling listings.
**Catalog is scattergun:** 0.7 niche-concentration (70 categories / 99 listings) — no focus, me-too spread.

## 3. ANALYSIS — the cross-tab (the finding)
| Meta-niche | # listings | sellers | sold-units | avg margin % |
|---|---:|---:|---:|---:|
| **Pool/Water** | 25 | 6 | **15** | 26.0 |
| **Kitchen** | 12 | 2 | **8** | 27.1 |
| Bath | 14 | 1 | 4 | 33.6 |
| Tech/PC | 8 | 1 | 3 | 28.3 |
| **Cleaning** | 4 | 1 | 3 | 28.1 |
| Candle/Craft | 10 | 1 | 1 | 31.9 |
| Auto/Baby | 1 | 1 | 1 | 26.5 |
| Pet | 8 | 0 | 0 | 29.6 |
| Garden | 5 | 0 | 0 | 31.4 |
| Home/Storage | 4 | 0 | 0 | 35.9 |
| Beauty | 3 | 0 | 0 | 37.4 |
| Outdoor | 3 | 0 | 0 | 24.8 |

**INSIGHT 1 — sales concentrate, listings don't.** Pool/Water + Kitchen = 37 listings (37% of catalog) but **23/35 units = 66% of all sales**. The catalog's demand lives in two niches; the other ~62 listings produce ~12 units between them.

**INSIGHT 2 — the demand/margin inversion (confirms Law #1).** The niches that **sell** have the **lowest** margins (Pool 26.0%, Kitchen 27.1%, Cleaning 28.1%); the niches with the **highest** margins (Beauty 37.4%, Home/Storage 35.9%, Bath 33.6%, Candle 31.9%) **don't sell at all or barely**. Demand ≠ margin — and AliExpress re-sourcing leverage is **highest exactly where demand already exists** (Pool/Water + Kitchen).

**INSIGHT 3 — dead weight is concentrated and identifiable.** Pet (8), Candle/Craft (10), Garden (5), Home/Storage (4), Beauty (3), Outdoor (3) = **33 listings → 2 units total.** Healthy margin, zero demand: classic me-too commodity buried in saturated search. These are the cut/leave-fallow set.

## 4. MEASUREMENT
- **Baseline (unchanged criterion):** 35 lifetime sold-units, 13 selling listings, $/day still LOW-SAMPLE.
- **KPI this run informs:** future sourcing allocation — % of next import batch aimed at Pool/Water + Kitchen vs spread.
- **Success:** next sourcing batch is ≥70% Pool/Water + Kitchen (proven demand), 0% Pet/Beauty/Garden/Candle (proven dead). **Failure:** another scattergun import across 10+ unrelated categories.

## 5. LEARNING
- ✅ **New, non-obvious:** the demand/margin **inversion** — our two proven niches are also our two thinnest-margin niches → they are the **#1 AliExpress re-source targets** (raise margin where velocity is already real). This sharpens the playbook's Law #2 from "re-source winners" to "**re-source the proven-demand niche, not just the individual winner**."
- 📌 **Sourcing directive (next import, when unblocked):** DEEPEN Pool/Water + Kitchen (+ Cleaning, best units-per-listing). STOP listing Pet / Candle / Garden / Home-Storage / Beauty / Outdoor commodity.
- 🔧 **Correction logged:** no watcher field in this source → prior watcher counts UNVERIFIED (data-quality flag, feeds ERROR_REGISTRY candidate).
- 🚧 **Limit:** lifetime sold-counts (not last-30d), small N (35 units) → directional, not a velocity ranking. Re-cut on next fresh audit with date-bounded sales if available.

**Status: PASS.** Internal/data only — no live action. Feeds: playbook Law #2 refinement, sourcing allocation for next import batch.
