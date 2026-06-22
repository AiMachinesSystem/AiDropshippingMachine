---
machine: "eBay / AutoDS Dropshipping Machine"
type: sector_practice_run
run_id: SECTOR-PRACTICE-2026-06-22-02
status: PASS
date: 2026-06-22
created_real: 2026-06-22
---

# SECTOR PRACTICE RUN-02 — Full-Catalog Economics (all 99)

## 1. SYSTEM
- **Sector:** eBay/AutoDS dropshipping. **Objective:** analyze ALL 99 live listings (not just the 13 winners) to find the catalog's real failure mode + decide what to do with the 86 non-sellers.
- **Scope:** 99 listings, post-kill. **Input:** `audit_2026-06-22_044324/_products_list.json` (variation_statistics + watchers). **Limit:** watchers = engagement proxy (views not populated); lifetime data.

## 2. DATA  [OBSERVED — AutoDS, 2026-06-22]
99 listings, 99 with price data. Source mix: **91 Amazon, 8 AliExpress** (some AE listings already exist).

## 3. ANALYSIS — the key reframe
| Segment | Finding |
|---|---|
| All 99 | avg margin **29.7%** · 47 healthy (≥30%) · 31 thin (<22%) · **0 negative** |
| **86 non-sellers** | avg margin **30.7%** (healthy!) · **81/86 = ZERO watchers** · only 5 with watchers |
| 44 non-sellers | **healthy margin (≥30%) BUT 0 sales** → not mispriced — **no visibility** |
| 20 non-sellers | thin (<22%) AND 0 watchers → dead commodity |
| 5 non-sellers | watchers>0 → interest, closest to converting |

**INSIGHT (new):** the catalog's failure mode is **NOT price/margin — it's VISIBILITY/demand.** 81/86 non-sellers get zero eBay traffic. These are me-too commodity listings buried in saturated search → confirms "demand ≠ opportunity" **at catalog scale**. Two different levers by segment:
- **13 winners:** sourcing-bound (they sell, but thin margin → AliExpress).
- **86 non-sellers:** visibility-bound (healthy margin, no traffic → SEO/promoted/angle, or cut).

## 4. MEASUREMENT
- **Baseline:** avg margin 29.7% · 86/99 = 0 sales · 81/86 = 0 watchers (no traffic).
- **KPI to move:** non-seller traffic (watchers>0 count: 5 → target ≥20) BEFORE any reprice/scale.
- **Success:** ≥10 non-sellers gain watchers after a visibility action (better title / promoted ≤3%). **Failure:** watchers stay ~0 → confirms niches are unrankable → cut.
- **Tracking:** re-run this script on next audit. **Result file:** this report.

## 5. LEARNING
- ✅ New, non-obvious: the bulk problem is **traffic, not margin** — I'd been over-indexing on sourcing.
- 📌 Decision segments: **20 dead+thin → KILL** (live → decision pack); **44 healthy-no-traffic → visibility test** (title/SEO via listing-optimizer; promoted ≤3% only if margin supports); **5 with-watchers → optimize first**.
- 🔧 Correct: "reprice the catalog" was wrong — 47/99 already healthy; the lever is demand, not price.
- 🚧 Needs data: which non-seller niches CAN rank (eBay search-rank data = 403-walled) → visibility test is the cheapest way to learn.
- **No scaling without validated KPI:** visibility actions stay STAGING until watchers move.

**Status: PASS.** Updates: LEARNING (this), feeds OWNER_GO_DECISION_PACK (20 kill candidates).
