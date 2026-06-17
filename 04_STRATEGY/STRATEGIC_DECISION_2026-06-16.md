---
machine: "eBay / AutoDS Dropshipping Machine"
type: strategic_decision
status: decided (execution GO-gated)
scope: autonomous strategic decision from registered data — NO live action taken
date: 2026-06-16
created_real: 2026-06-17
inputs: 10_OUTPUTS/autods_status_report.md · 10_OUTPUTS/DROPSHIPPING_MACHINE_CAPABILITY_AUDIT_2026-06-16.md · 03_ANALYSIS/DEEP_PRODUCT_RESEARCH_2026.md · 03_ANALYSIS/2026-06-15_ebay-autods-policy-fee-feature_analysis_v1.md
method: 3-lens strategist judge-panel (cash-now · margin&moat · risk&compliance) + synthesis, then owner-facing decision
---

# STRATEGIC DECISION — eBay/AutoDS (7-day window, 2026-06-16)

> **This file decides; it does not execute.** Every value-creating live step is GO-CLASS and CLOSED. Decision basis is [OBSERVED] data registered this week. Aggregate eBay demand is [UNKNOWN] (403 wall) — sizing reflects that.

## ⚡ BOTTOM LINE (the decision in one paragraph)
**PRUNE-AND-REPOSITION on a protected base. Do NOT grow first.** Renew the **cheapest AutoDS monitoring tier today** (drop the auto-ordering add-on, ignore the paid REST API) so the **214 live listings survive the 2026-06-18 trial cliff**; **fix the free VeRO draft today**; **tally the 214 read-only**, then **end the OOS/error and sub-50%-margin Amazon-arbitrage listings and reprice the proven "X sold" winners**; **replant a small, clean, AliExpress-sourced, brand-free core of 2 SKUs** (rubber duck antenna topper *generic* as lead, 3D anatomy torso *bundled*). **Drop mascara wands** (commodity floor), **bench the phone tether** (generic-only later). **Keep auto-ordering OFF.** Underneath it all: the **Amazon-retail-arbitrage model is the real liability** — this plan is also the cheapest **30-day test** of whether defensible margin is reachable on eBay at all. If it isn't, **wind down, don't feed it.**

---

## 🔁 UPDATE 2026-06-17 — read-only audit of the 214 sharpens the product direction
A full read-only tally of the 214 active listings (cache `90_CACHE/fetches/autods/audit_2026-06-17_012312/`) refines DECISION 1:
- **Only 13 of 214 listings have ever sold** (34 units total, max 6 on one); **201 are zero-sellers.** 42 have **no available stock** (30 OOS + 15 on-hold); **136 carry errors** (100 supplier-title-changed, **63 VeRO-word**, 10 duplicate); **37 run <20% gross margin** — [OBSERVED].
- **The proven winners are NOT cheap commodities — they are mid-ticket ($23–$286) niche/problem-solvers:** Pool Fountain Jet ($138, 6 sold), Pet Grooming Loops ($286, 4), Dog Water Ramp ($202, 4), PC ARGB Display ($127, 3), Ham Maker meat press ($42, 5), Dryer Balls ($23, 3) — [OBSERVED].
- **AliExpress validation of the two keepers:** rubber duck topper **PASSES** the 50% gate (56.9% @ $8.99) → keep as a **cheap novelty probe** only; **3D anatomy torso → DOWNGRADED to bench** — clears 50% only at ≥$17.99 while eBay is saturated with sub-$5 China sellers (conversion doubtful) [OBSERVED 2026-06-17].

**Refined DECISION 1 (supersedes the SKU picks below):** the new core should imitate the account's OWN proven winners — **mid-ticket ($40–$150) niche, problem-solving, low-competition products** (pool/pond, specialty pet, BBQ/meat-prep, PC/desk), **AliExpress/CJ-sourced, brand-free** — NOT cheap commodities and NOT the stale 7 repo drafts. The duck topper stays only as a low-cost test. Dedicated run: `03_ANALYSIS/MIDTICKET_PRODUCT_RESEARCH_2026-06-17.md`. Prune-and-reposition is unchanged and now **quantified**: prune the **201 dead + 42 no-stock + 37 low-margin**, reprice/fix the **13 winners + 63 VeRO + 100 title-changed** (per-listing action list: `05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/listings/LISTING_AUDIT_2026-06-17.md`).

---

## DECISION 1 — Product direction: **PIVOT (prune-and-reposition), not "add the 3 found"**
**Verdict:** The product question is the wrong *first* question. Clean the existing **214** before adding anything. Then add a **2-SKU clean core**, AliExpress/CJ-sourced, strictly generic titles:
- ✅ **Rubber duck antenna topper — GENERIC** (cost $2.25 / sell $9.99 / **60% margin** / **LOW competition**). The single best fit and the proof-of-concept for the new thesis. *Never* a Disney/branded duck.
- ✅ **3D human-body torso anatomy model (kids/educational)** (cost $6.14 / **59%** / 204 sold-per-listing [OBSERVED]). Differentiated/educational; **bundle** quiz cards/labels to lift AOV and defend price. Verify ship weight (bulky).
- 🪑 **Bench: phone anti-lost tether** — best raw margin (68%) but its natural framing ("compatible with Apple Watch/AirTag") is a VeRO/brand-keyword minefield; re-enter **generic-only** after the core proves out.
- ❌ **Drop: disposable mascara wands** as a lead — 51% is the thinnest gate-pass and it is a saturated race-to-the-bottom (529 sold/listing = everyone sells it); only re-enter as a **multi-pack bundle** where margin holds.

**Why [data]:** at the eBay floor, cheap commodities **fail the 50% gate** after FVF 13.6%+$0.40 [computed, DEEP_PRODUCT_RESEARCH_2026]. The current catalog is **Amazon retail-arbitrage**, which structurally violates eBay's retail-arbitrage prohibition [policy analysis 2026-06-15]. Adding SKUs onto an unstable, partly-OOS, prohibited-source base grows risk surface without fixing fragility. **Cheaper AliExpress/CJ sourcing is the only durable margin lever AND removes the arbitrage tension.** Defensible margin = low-competition/novelty/bundle, not "cheapest seller of a commodity."

> ⚠️ **Reconcile before any import:** the **7 drafts already in the repo** (cable clips, drawer dividers, garlic peeler, pet glove, car-seat gap filler, ice roller, motion LED) are a **different SKU set** from the 4 research candidates. Decide the actual import list first.

## DECISION 2 — Renew the AutoDS trial (expires 2026-06-18)? **YES — cheapest base tier only**
**Verdict:** **Renew the cheapest paid tier that keeps stock + price monitoring** on the 214 listings. **Drop the orders_processor / auto-ordering add-on.** **Do NOT** pursue the paid/application-gated REST API. Treat it as a **30-day defensive stay-of-execution, not a growth commitment.** *(Billing = GO/owner.)*

**Why [data]:** this is a **risk decision, not an ROI decision**. The 214 live listings depend on AutoDS monitoring; if the trial lapses 6/18, monitoring stops → OOS items keep selling → oversells/cancellations/INAD+late-ship defects → on a retail-arbitrage catalog that **compounds into account restriction**. Letting it lapse is the one move that can quietly detonate the account. The add-on is pure waste (auto-ordering is **NON-FUNCTIONAL**: 0 buyer accounts, $0 wallet [OBSERVED]). The REST API is out of scope (application-gated, paid, **no read-only scope**; cited ~$5k activation is **UNVERIFIED**) — keep the proven Playwright read path. Profit proxy ~**$248/mo** (from $62/7d) comfortably covers a base tier (~$30/mo per the fee index), so **cost is not the constraint**. **Caveat:** if prune+reposition shows no traction in 30 days, **do not renew again**.

## DECISION 3 — Strongest 7-day sequence: **two tracks (safety/cash + reposition)**
Track A protects the base and harvests existing demand; Track B replants a clean core. Same action set all three lenses agreed on.

| Day | Step | Action | Track | GO? |
|---|---|---|---|---|
| 1 (6/17) | A1 | **Fix VeRO 'alcohol' draft** + scrub brand keywords (Invisalign/Tuya/Apple Watch/AirTag/Disney) from all 11 drafts + 7 repo drafts | safety | **no-GO** (draft edit)* |
| 1 (6/17) | A2 | **Renew AutoDS base tier**, drop add-on, no REST API — confirm monitoring active before 6/18 | safety | **GO** (billing) |
| 2 (6/18) | A3 | **Read-only tally of the 214**: OOS / On-Hold / supplier-title-error / price-broken → kill/fix list | safety | **no-GO** (proven Playwright) |
| 3 (6/19) | A4 | **END** OOS/error + sub-50%-margin arbitrage SKUs; **reprice/title-optimize** the proven "X sold" winners | cash+safety | **GO** (live writes) |
| 4 (6/20) | B1 | **Validate 2 keepers** vs 50% gate at AliExpress/CJ landed cost; finalize generic titles + torso bundle; reconcile vs 7 repo drafts; prep import rows | reposition | **no-GO** (validation) |
| 5 (6/21) | B2 | **Import keepers as DRAFTS only**; run LISTING_VALIDATION_CHECKLIST (VeRO/margin/title) | reposition | **GO_IMPORT_5_DRAFTS** |
| 6 (6/22) | B3 | **Publish SMALL** (duck topper as lead test); auto-ordering OFF, fulfill manually | reposition | **GO_PUBLISH_5 / GO_PUBLISH_1** |
| 7 (6/23) | M1 | **Log baseline** in EBAY_5_LISTING_MEASUREMENT_TRACKER (active count, margin dist., defect/oversell, profit Δ vs $62/7d); refresh cockpit; decide next 7 days | measure | **no-GO** |

\* If AutoDS treats a draft delete/edit as a live write, gate it as `GO_FIX_DRAFTS`.

## DECISION 4 — Fix FIRST: **VeRO + renewal (Day 1) → OOS/error → auto-ordering LAST**
1. **VeRO 'alcohol' draft + brand-keyword scrub** — TODAY, free, no-GO. Fastest catastrophic risk (a single strike can suspend instantly); a draft = zero revenue, so pure risk elimination.
1-tie. **AutoDS base renewal** — TODAY, hard 6/18 deadline; the only time-critical money decision (GO/billing).
2. **OOS / On-Hold / supplier-title-error listings** — read-only tally (no-GO) → end/relist + reprice winners (GO). Biggest live account-health + cash lever.
3. **Auto-ordering — FIX LAST / DO NOT ARM.** Non-functional = **safe while OFF**; arming it on an arbitrage catalog would *automate the prohibited behavior* eBay penalizes. Keep OFF; `GO_ENABLE_AUTO_ORDERING` stays CLOSED.

---

## What needs GO (owner authorizes, per-action) vs what does NOT

**🔴 GO-CLASS (CLOSED until owner token):**
- **Billing:** renew AutoDS cheapest monitoring tier; explicitly drop orders_processor (confirm before 6/18).
- `GO_PRUNE_LISTINGS`: end OOS/On-Hold/error + sub-50%-margin arbitrage SKUs (live writes; per batch).
- `GO_UPDATE_PRICES`: reprice/title-optimize the proven "X sold" winners.
- `GO_IMPORT_5_DRAFTS`: import validated keeper SKUs as drafts.
- `GO_PUBLISH_5` / `GO_PUBLISH_1`: publish reviewed keeper drafts on divinit-92-us.
- (`GO_FIX_DRAFTS` only if AutoDS treats a draft edit as a live write.)

**🟢 NO-GO (internal, I can do now on request):**
- Fix/strip the VeRO draft + brand-keyword scrub (draft edit).
- Read-only Playwright tally of OOS/On-Hold/error across the 214.
- Validate the 2 keepers vs the 50% gate (AliExpress landed cost); reconcile vs 7 repo drafts; prep import rows.
- Run LISTING_VALIDATION_CHECKLIST on staged drafts.
- Day-7 measurement log + cockpit refresh.
- **Keep auto-ordering OFF; do NOT apply/pay for the REST API.**

## 30-day kill criterion (decide now, not later)
This catalog is **Amazon-arbitrage on eBay at 3 orders/week** — structurally fragile. **Test, don't bet.** If after ~30 days the prune+reposition does **not** show (a) incremental orders above the $62/7d baseline AND (b) the clean AliExpress core clearing ≥50% margin with acceptable defect/oversell, **wind the model down** (stop renewing, archive the catalog) rather than fund it further. Measure with the **existing** KPI criterion (`06_MEASUREMENT/KPI_MAP.md`) — no invented metrics.

## Top risks
- **Trial lapse 6/18** → monitoring dies on 214 → oversell/defect/account damage. *Mitigation: renew base today.*
- **Amazon retail-arbitrage prohibition** → account-suspension risk not fixable by tweaks. *Mitigation: don't expand the arbitrage base; migrate new SKUs to AliExpress/CJ.*
- **VeRO** (brands in titles, incl. "compatible-with") → strikes. *Mitigation: brand-free titles; fix the draft before publish.*
- **Margin illusion** → only ship SKUs validated at the floor with AliExpress landed cost.
- **LOW-SAMPLE** (23 lifetime / 3 orders-7d; aggregate eBay sold [UNKNOWN]) → publish small, let the tracker decide scaling.
- **Auto-ordering armed-but-broken** → keep OFF until buyer accounts + wallet + supplier reliability exist.

---
*Decision produced from registered data via a 3-lens strategist panel + synthesis. No eBay/AutoDS/supplier write, login, or spend was performed. The next move is the owner's: renew (GO/billing) before 2026-06-18, then open gates in the Day-1→Day-7 sequence above. Internal no-GO steps (VeRO fix, 214 tally) I can start on your word.*
