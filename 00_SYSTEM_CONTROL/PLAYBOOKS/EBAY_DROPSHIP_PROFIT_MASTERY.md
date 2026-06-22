---
machine: "eBay / AutoDS Dropshipping Machine"
type: playbook
status: v1 (living — improved each cycle, rule "non fermarti mai")
date: 2026-06-22
created_real: 2026-06-22
risk_class: INTERNA
sources:
  - OBSERVED account: 10_OUTPUTS/autods_status_report.md (2026-06-16)
  - canon: 04_STRATEGY/PROFITABILITY_VS_COMPETITION_2026-06-17.md
  - census: RESEARCH_MEMORY_INDEX (multi-niche 2026-06-20; amazon-to-ebay 2026-06-21)
  - model: 10_OUTPUTS/ANALYSIS_REPORTS/2026-06-22_profitability-model_short-mid-long_v1.md
  - simulation: 03_ANALYSIS/simulations/profit_montecarlo.py (20k runs, seed 42)
---

# eBay/AutoDS Profit Mastery — Playbook v1

> **What this is.** The machine's codified "how to be maximally profitable on eBay dropshipping",
> distilled from OUR data + a Monte Carlo simulation of the levers. Living document: every cycle
> adds one improvement (rule: *non fermarti mai*). All forward numbers = [ESTIMATE], LOW-SAMPLE base.

## 1. The 5 laws (learned from our own runs)
1. **Demand ≠ opportunity.** 14/15 of our niches are PROVEN-demand but commodity-SATURE. Raw demand is a trap; you win only with an **ANGLE** (premium/decor tier · bundle · XL format · exact-compatibility title · original photos+copy). [census 2026-06-20]
2. **Sourcing is the margin ceiling.** Amazon→eBay caps at ~30–42% net (we *realize* ~19%). AliExpress/CJ on the same niche → 45–55% **and** removes the retail-arbitrage policy risk. Same product, double the profit/order. [canon 2026-06-17]
3. **List the bundle, never the floor.** Every niche has a race-to-bottom single-item floor AND a thin "complete-kit / with-stand / with-bins" band. The profit lives in the band, just under the branded cluster.
4. **Scale only on VERIFIED demand** (eBay "X sold" badges), never on watchers/hope. Push budget where a live comparable already shows real sold counts.
5. **VeRO + weight silently kill you.** Generic titles only (no brand, no "compatible-with <trademark>"); light-to-ship only (dimensional shipping eats the spread).

## 2. What the SIMULATION taught (20k runs, computed — not invented)
Baseline OBSERVED = **$8.87/day**. Net profit/day, median [P10–P90]:

| Strategy | 3mo | 6mo | 12mo |
|---|---|---|---|
| S0 status-quo (Amazon, broken fulfill) | 8 [7-10] | 9 [7-11] | 10 [7-13] |
| S1 fix fulfill + clean catalog | 20 [15-27] | 31 [23-42] | 38 [28-52] |
| S2 + AliExpress sourcing | 49 [37-65] | 78 [57-108] | 101 [73-138] |
| S3 + promoted listings (scale winners) | 75 [50-110] | 152 [103-225] | 193 [130-281] |
| **S4 full stack (all levers)** | **130 [84-199]** | **284 [193-419]** | **345 [230-507]** |

**Lever ranking @6mo (marginal lift over S1 $31/day):**
1. **Volume/scale (more winners + promoted): +$56/day** ← biggest single lever
2. **AliExpress margin: +$34/day**
3. Bundling AOV alone: +$5/day (small solo, but compounds inside the others)

### The mastery takeaways
- **Doing nothing = flat at ~$9/day forever** (S0). The status quo is not "slow growth", it's *no* growth.
- **No single lever wins — they multiply.** S4 ($284) ≫ S1+S2+S3 added naively, because margin × volume × AOV compound.
- **Order of operations = volume-enablement first, then margin.** You can't scale (lever #1) until fulfillment works and the catalog is clean (S1). So S1 is the unlock even though its own lift is small.
- **Tail risk the sim does NOT price: account suspension.** Amazon arbitrage violates eBay policy; a VeRO/policy hit = profit → $0 overnight (ruin, not a dip). This is why **law #2 (move to AliExpress)** is not just margin — it's survival. Mastery = de-risking the engine, not only maximizing the median.

## 2bis. Risk-adjusted study (cycle 2 — `profit_montecarlo_risk.py`, 20k runs, seed 7)
Same scale ceiling for both engines; they differ ONLY in sourcing risk. Metric = expected
cumulative net profit over 12 months (zeroed after suspension). Suspension hazard = declared
assumption [ESTIMATE]; returns 4–10%, ad 5–12%.

| Engine | E[cum 12mo] | median | P10 (downside) | **P(survive 12mo)** |
|---|---|---|---|---|
| Amazon-sourced (high policy risk) | $22,358 | $23,096 | **$716** (near-wipeout) | **42.6%** |
| AliExpress-sourced (low policy risk) | $51,959 | $53,336 | $26,742 | **85.5%** |

- **The Amazon engine is a coin-flip on survival** — more likely than not (57%) to eat a suspension within 12 months. Its P10 outcome is ~$700 = effectively wiped.
- **AliExpress earns ~2.3× more in expectation AND survives 2× as often.** It's not an optimization, it's the difference between a business and a gamble.
- **Suspension risk alone destroys ~$15,600 of expected value** on the Amazon engine (~41% of its risk-free potential) — invisible to a median-only view.
- **Mastery rule:** optimize EXPECTED value under ruin, not the median. A higher median with a fat ruin tail loses to a slightly lower median that survives. → sourcing migration is the top priority by impact *and* risk.

## 2ter. EMPIRICAL validation — real per-SKU data (cycle 3, pull 2026-06-22)
Read-only pull of 207/214 listings (`90_CACHE/.../audit_2026-06-22_041033`). The sims predicted concentration; the data **proves** it:
- **194/207 listings (94%) have ZERO lifetime sales.** The business is **13 SKUs**.
- **Top-5 = 66%, top-10 = 91% of all sales.** (sim Q2 said concentrate beats spread +57% — reality is far more extreme.)
- **129/207 (62%) carry error flags** → 120 dead+errored listings = pure drag/risk.
- **Discovered edge: ~7 of 13 winners are POOL/POND/WATER gear** (+ ham-press kitchen, + pet). The real demand is NOT in the 15 saturated commodity niches we keep testing — it's the pool/water cluster (seasonal, summer peak now).
- **Pricing pricing study (sim Q1): optimal price ≈ market / ~2.1× cost; the live 27% markup is ~3× underpriced** → leaving ~2/3 of margin on the table.

**Mastery synthesis:** stop adding random commodities; KILL the 94% dead tail, RESTOCK+RE-PRICE the 13 winners, RE-SOURCE them on AliExpress, and source DEEPER in the proven pool/pond/water cluster. Detail + ids: `10_OUTPUTS/ANALYSIS_REPORTS/2026-06-22_per-sku-audit_kill-restock-scale_v1.md`.

## 3. The operating playbook (apply to every new listing)
1. Confirm a **verified eBay sold badge** on a comparable (demand real).
2. Confirm source price **≥40% below** prevailing eBay sell (the gap) — prefer AliExpress over Amazon.
3. List the **bundle/complete/with-X** variant, priced **just under the branded cluster**.
4. **Generic title (≤80 char) + own photos** → VeRO-safe. Rewrite the scraped description.
5. **Light-to-ship only.** Verify AutoDS landed cost BEFORE publish (protocol from E-003).
6. Model on **~30–42% (Amazon) / 45–55% (AliExpress)**, never 50% from Amazon.

## 4. The continuous-improvement loop ("non fermarti mai")
Each cycle (weekly, or on new data):
1. **Pull** fresh per-SKU data (read-only; GO-light) → orders, sold, margin per listing.
2. **Re-baseline** the model with real numbers (kills LOW-SAMPLE over time).
3. **Re-simulate** with updated priors → re-rank levers.
4. **Extract ONE improvement** to execute (kill a dead listing / restock a winner / shift one SKU to AliExpress / draft one bundle).
5. **Log** the result vs the $/day baseline (same criterion, no metric inflation).
> Real iteration needs fresh account data (GO-light read) and live moves (GO). The *thinking/simulating* never stops; the *live* steps gate.

## 5. GO-class unlocks blocking the engine (owner)
1. Resubscribe AutoDS (trial expired 2026-06-18) — enables scaling tooling.
2. Connect buyer account + fund wallet — enables auto-fulfillment (today every order is manual).
3. Shift sourcing to AliExpress — the margin+survival lever (#1 priority by impact/risk).

## 6. Sector Canon 2026 (external research — corroborates our data)
[Public sources, cached: `90_CACHE/fetches/web/2026-06-22_dropship-sector-research.md`]
- **Margins:** sector "good" = 20-35% net; Amazon-dropship avg 10-30%. Our ~19% = low end → real upside, not a fantasy.
- **Suspension mechanics (CONFIRMS our cycle-2 ruin sim):** eBay now **detects Amazon TBA tracking numbers instantly** → flags "Retailer Dropshipping"; Amazon/Walmart-branded parcels → flag. **Out-of-stock defects = ~45% of all dropshipping account terminations.** Our catalog was 62% errored/OOS → we were sitting on a termination risk; the KILL + AliExpress migration are de-risking, not optional.
- **Promoted Listings discipline (NEW hard rule):** start **2-3%**, raise only after 14-day ROAS. **Never run ≥8% ad rate while net margin <20% = burning money.** If gross margin <40% → Standard only at 5-8%. **2026 attribution change:** fee now charged when ANY buyer buys within 30 days of ANY click (attribution ~50%→80-90%) → ads are pricier than before → ads come AFTER margin is fixed, never before.
- **Compliance checklist:** wholesale/AliExpress-with-US-warehouse sourcing · control packaging (no retailer branding) · real-time stock sync (kill OOS) · accept returns on own policy · defect <2% · reply <24h · keep a supplier Letter of Authorization.
- **Scaling lever (new):** hybrid model — dropship to TEST, then at **~50 units/month consistent switch to bulk buying → +15-25% margin.** Path beyond dropship for our proven winners (pool/water, ham press).
