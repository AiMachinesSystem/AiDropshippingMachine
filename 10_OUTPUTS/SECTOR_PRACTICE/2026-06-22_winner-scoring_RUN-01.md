---
machine: "eBay / AutoDS Dropshipping Machine"
type: sector_practice_run
run_id: SECTOR-PRACTICE-2026-06-22-01
status: PASS
date: 2026-06-22
created_real: 2026-06-22
---

# SECTOR PRACTICE RUN-01 — Winner Scoring Model

## 1. SYSTEM
- **Sector:** eBay/AutoDS dropshipping. **Objective:** data-driven triage of the 13 real winners → keep / reprice / re-source / drop / fix.
- **Scope:** the 13 sold>0 listings (post-kill catalog). **Inputs:** `audit_2026-06-22_044324/_products_list.json` (variation_statistics). **Limits:** lifetime sold (not recency); cost/price OBSERVED but AliExpress alternative cost = NOT USABLE (CAPTCHA).
- **Output:** scored triage + KPIs. **KPIs watched:** avg net margin, % healthy (≥30%), % thin (<22%), VeRO count, data-integrity count.

## 2. DATA  [OBSERVED — AutoDS variation_statistics, 2026-06-22]
13 winners, all Amazon-sourced. buy/sell/margin per SKU extracted (script run, computed not invented).

## 3. ANALYSIS — pre-declared rubric → verdict + 0-100 profit-health score
Rubric: score = margin×1.8 + min(watchers,9)×2 + 15 (if not VeRO/data-bug). Verdict: data-bug→FIX; VeRO→DROP/DEBRAND; margin≥30→KEEP; cost/sell>0.6→RE-SOURCE; else REPRICE-UP.

| Score | Verdict | Mrg% | Sold | Product |
|---|---|---|---|---|
| 81 | KEEP | 35.6 | 3 | Hedgehog Dryer Balls |
| 77 | KEEP | 34.7 | 1 | Crochet Kit |
| 69 | FIX-DATA | 38.3 | 4 | Grooming Loops (cost $133.13 = bug) |
| 68 | RE-SOURCE | 19.7 | 5 | Ham Maker +thermo |
| 65 | REPRICE-UP | 26.5 | 1 | Roller Pulley |
| 60 | RE-SOURCE | 20.4 | 3 | Ham Maker v2 |
| 57/54 | RE-SOURCE | 21 | 1 | Stock Tank Covers ×2 |
| 53 | RE-SOURCE | 18.0 | 5 | Dog Water Ramp |
| 48 | DROP/DEBRAND | 17.8 | 3 | Lian Li (VeRO) |
| 48/42/42 | RE-SOURCE | 15-17 | 1 | Dog Life Jacket · Chlorine Feeder · Deck Jet |

**Finding:** 8/13 = RE-SOURCE, 2 KEEP, 1 DROP, 1 FIX, 1 REPRICE. Even the Ham Makers score RE-SOURCE (cost = 64% of sell) → **re-sourcing dominates reprice across the board.**

## 4. MEASUREMENT
- **Baseline (OBSERVED):** avg margin **23.2%** · **3/13** healthy (≥30%) · **9/13** thin (<22%) · **100%** Amazon (suspension-exposed) · 1 VeRO · 1 data-bug.
- **Target (post-action):** avg margin **≥35%** · 0 VeRO · 0 data-bug · Amazon-share down.
- **Success threshold:** avg ≥35% AND 0 VeRO AND bug fixed. **Failure:** avg stays <25% after action.
- **Observation period:** after the re-source batch + fixes go live. **Tracking:** re-run this script on the next audit. **Result file:** this RUN_REPORT.

## 5. LEARNING
- ✅ Worked: a simple pre-declared scoring model on real data **refined the manual conclusion** — re-source beats reprice even for the Ham Makers; only 2 winners are keep-as-is.
- 📌 Repeat: this winner-triage scoring is a **reusable capability candidate** → fold into `dropship-profit-run` (STAGE).
- 🔧 Correct: prior "reprice-up the Ham Makers" downgraded — re-source is the stronger lever.
- 🚧 Needs data: AliExpress cost (M3) to quantify the re-source margin gain → owner URLs / visible browser.
- **No scaling without validated KPI:** this run stays at IMPROVE/STAGING until the re-source action moves the baseline.

**Status: PASS** (measurable, data-grounded, artifact produced). Updates: `NEXT_ACTIONS_INTERNAL`.
