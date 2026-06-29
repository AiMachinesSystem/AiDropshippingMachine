---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: strategic_diagnosis
status: NEEDS_OWNER_DECISION (analysis INTERNA complete; pivot + unlocks require owner GO)
date: 2026-06-28
created_real: 2026-06-28
skill: dropship-profit-run
basis: "RESEARCH_MEMORY_INDEX owned-store block + per-SKU audits (06-22) + live snapshot reprice_dryrun 06-25 (144 live) + publish-50 run (06-27, +36 live) + ERROR_REGISTRY E-001..E-017 + PROFIT_TEST_001 + PUBLISHING_PLAYBOOK v2"
---

# Why no sales — diagnosis + pivot (2026-06-28)

## Verdict (one line)
**It is not bad luck or one bug. The machine has been optimizing VOLUME of proxy-validated commodity listings — the wrong variable. In ~6 days the live catalog grew 99 → 144+ (≈45 new listings) and lifetime sales stayed EXACTLY at 35 units / 13 SKUs. More listings ≠ more sales when the listings are invisible commodities sourced thin.**

## Confidence
MED-HIGH. The "0 incremental sales despite +45 listings" fact is OBSERVED (06-22 audit vs 06-25 live snapshot, both show 35 units / same 13 SKUs). Root-cause ranking is INFERRED from our own data + sector canon. The one thing that would make it HIGH — eBay impressions/sold data — is the missing piece (see Unlock #1).

## Evidence basis
- [OBSERVED 06-25, cache reprice_dryrun_2026-06-25_065630/_listings_raw.json] 144 live listings; **13 SKUs with lifetime sales; 35 units total** — identical to the 06-22 audit.
- [OBSERVED 06-22, RESEARCH_MEMORY_INDEX owned-store] pre-kill 194/207 (94%) ZERO lifetime sales; top-5 = 66%, top-10 = 91% of sales; sales concentrate in **Pool/Water (25 list→15 units) + Kitchen (12→8) = 37% of listings, 66% of sales**.
- [OBSERVED 06-22] demand/margin INVERSION: the niches that sell carry the THINNEST margin (Pool 26%, Kitchen 27%); high-margin niches (Beauty 37%, Home 36%) don't sell.
- [OBSERVED 06-27 commit 752aeac] +36 listings live this session via Amazon arbitrage; no sales lift recorded.
- [FACT, PROFIT_TEST_001 06-24] of 50 clean Amazon candidates only 8 clear net ≥$4; net margins 8-10% → max ad budget ≈ the net profit → almost no room for Promoted Listings.
- [OBSERVED, ERROR_REGISTRY] 17 errors logged; ~12 of them (E-002,003,005,007,008,010,011,012,013,014,015,016,017) are PUBLISHING/automation walls, ~0 are demand-side.

## Why no sales — root causes (ranked by leverage)

1. **Flying blind on eBay demand (the #1 structural gap).** Every research run validates demand on Amazon reviews / AliExpress orders — never eBay actual sold/sell-through (Terapeak/API not connected; tool built 06-27, needs owner eBay login). "Sells on Amazon" ≠ "sells on eBay." Result: we keep listing items with demand *somewhere* into saturated, price-compressed eBay categories. Three product runs all concluded "demand proven = commodity saturated" — the signature of proxy-validated commodity hunting.

2. **Scattergun catalog = zero ranking authority.** 99→144 listings spread across ~70 eBay categories. eBay Best Match rewards category depth + sales velocity + relevance. A store 1-2 listings deep in 70 categories has no ranking signal anywhere → **81/86 non-sold listings had ZERO traffic.** They don't lose on price; they're invisible.

3. **No velocity flywheel + no ad margin to force visibility.** Best Match heavily weights recent sales. At ~0.014 orders/listing/week and 8-10% net margin, we can neither climb organically (no sales) nor pay for Promoted Listings (ads would erase profit). Chicken-and-egg, and we keep adding more eggs.

4. **We are ignoring our own winner cluster.** Data screams Pool/Water (7/13 winners, #1 Deck Jet) + Kitchen meat-press + pet. The last week's publishing was scattershot Amazon kitchen/generic instead of deepening the 2 fields that actually grew — and Pool/Water is IN SEASON RIGHT NOW (summer peak).

5. **Sourcing = Amazon arbitrage = thin + fragile.** ~19% net ceiling, ~50% AutoDS scrape-fail, suspension risk (Amazon TBA tracking → "Retailer Dropshipping" flag; OOS defects = ~45% of terminations). Even a sale is thin and risky.

6. **Fulfillment is broken.** Auto-order non-functional (0 buyer accounts, $0 wallet); AutoDS trial expired 06-18 → stock/price sync off (oversell risk). Doesn't stop the first sale, but caps everything and adds account risk.

## Dominant pattern
Plumbing-rich, demand-poor. We got very good at *putting listings up*; we did not get better at *putting up listings that sell*.

## Recommended move — THE PIVOT (stop wide, go deep, in-season)
Three plays, in order:

**A. Go DEEP in the proven in-season cluster (Pool/Water), not wide.** Build 10-15 listings of *category depth* in pool/water accessories (NOT chemicals — E-014). Depth + the existing sold badges = the only path to Best Match authority. Window closes end of summer — prioritize now.

**B. Lift margin WITHOUT changing source — AliExpress sourcing is OFF the table (owner directive 2026-06-28).** Sourcing stays US-warehouse / Amazon-US (L-004); AliExpress is for product *discovery only* (seeing what kits/angles/demand exist), never as supplier. Source-independent margin levers: **price-to-market** (the pricing sim says the 27% floor markup is ~3× under profit-max → room to raise the proven winners toward market), **bundle/kit AOV**, and the organic velocity that depth + Terapeak unlock. (Note: AliExpress dropship via AutoDS also doesn't publish anyway — US item-location wall E-008/E-010.)

**C. Deepen the kitchen meat-press sub-cluster (secondary).** Ham Maker is a proven 2× winner; add casings/thermometer/recipe bundles and adjacent meat-prep — generic, single-config, light-ship.

### Product selection (ready to verify → draft → publish; each = GO)
Source = **US-warehouse / Amazon-US** (L-004). AliExpress used for product *discovery only*, never as supplier. Ranked by (proven adjacency × in-season demand × AOV/pricing headroom × wall-clearance):

| # | Product (generic, VeRO-safe) | Anchor winner | Angle | Wall to clear (Amazon-US) |
|---|---|---|---|---|
| 1 | Pool fountain / return-jet **nozzle + fitting KIT** | Deck Jet (6 sold) | bundle multi-fitting, repeat-buy part | single-config + in-stock (E-012) |
| 2 | **Dog pool/boat ramp & steps** (XL, weight-rated) | Dog Water Ramp (5) | XL/200lb angle; swim-season | dim-weight (bulky) + variant scrape-fail |
| 3 | **Stock-tank pool "complete kit"** (drain plug, leaf cover, filter parts) | 2× pool cover | kit bundle, light parts | single-config only (E-012) |
| 4 | **Pool-cleaner spare-part kit** (tracks/tires/diaphragms) GENERIC | Roller idler pulley | repeat-buy spares | NO brand names (Hayward/Polaris = VeRO) |
| 5 | **Dog life vest** (sizes/colors, ripstop) | Dog life jacket | sizing range, pet pool safety | one config/listing (variant scrape-fail) |
| 6 | **Floating chemical dispenser** (device, not chemicals) + o-ring kit | Chlorine feeder | consumable-adjacent, low ship | device OK; NO chlorine/bromine (E-014) |
| 7 | **Ham/meat press bundle** (+ thermometer, casings, recipe) | Ham Maker (5+3) | kit AOV, instructions fix (top pain) | single-config |
| 8 | **Pet grooming-table accessory bundle** (loops, arm clamp) | Grooming loops (4) | bundle, generic | "Loop" is a VeRO word → reword |

Margin lever (AliExpress sourcing OFF the table): **price-to-market** (~3× under profit-max at the 27% floor markup) + **bundle/kit AOV** + velocity/depth — all source-independent. Price ≈ market / ~2.1× cost, list the kit, never the floor. Verify a real eBay sold badge on a comparable before pushing ad budget.

## The 2 unlocks that turn listings into SALES (without these, depth still underperforms)
1. **Connect eBay demand data (Terapeak).** Free in Seller Hub → Research. The `read_terapeak`/`ebay_demand_gate` tools are built (06-27) and pass self-test; they need ONE owner eBay login. This converts selection from proxy-blind to eBay-real — the single highest-leverage fix. **Owner action: ~5 min login.**
2. **Fix fulfillment + AutoDS plan.** Decide AutoDS (renew ~$29.90/mo vs alternative) and wire auto-order (buyer account + wallet), or commit to manual ordering. Without this, every sale is a manual scramble and stock sync is off.

## Why (the logic)
eBay sales = visibility × relevance × velocity × margin-for-ads. We've been adding listing *count*, which moves none of those four. Depth-in-one-proven-in-season-category moves relevance + velocity; price-to-market + bundle AOV move margin (no cheaper source needed); Terapeak makes selection hit real demand. Volume of commodities moves nothing — proven by 45 listings → 0 sales.

## Rejected alternatives
- **"Publish 50 more" (status quo):** rejected — it is the exact action that produced 0 incremental sales.
- **Hunt more Amazon generics:** rejected — 24 tested across 3 runs, 0 "good"; thin-margin wall is structural.
- **Blind global reprice +X%:** rejected — E-011 (collapses margin / overshoots market).
- **Chase new trendy niches:** rejected — no eBay-demand data yet; would repeat the proxy-blind mistake.

## Owner role (GO gates — per-action)
- **GO-1 (5 min):** eBay Seller Hub login so Terapeak activates → I validate the 8 candidates on REAL eBay sold-data before any draft.
- **GO-2 (decision):** approve the PIVOT (deep+in-season+AliExpress) vs keep publishing wide.
- **GO-3 (decision):** AutoDS renew/replace + fulfillment wiring.
- **GO-4 (per-batch):** import → draft → publish the verified pool/water depth batch (10-15), paced ≤ ~10/day (velocity/suspension).
- **Wall handoff:** AliExpress exact cost = CAPTCHA-walled → paste 5 URLs OR an owner-assisted visible-browser session.

## Measurement plan (same criterion — no new metric)
Baseline = $/day gross profit (OBSERVED $8.86/day, RUN-03). Success of the pivot = (a) sell-through > 0 on the new pool/water depth within 14 days, (b) $/day baseline rises, (c) ≥1 new SKU joins the 13-winner list. Re-audit weekly via `audit_listings.py` (read-only).

## Blockers
eBay demand data (GO-1), fulfillment (GO-3), AliExpress cost wall (handoff). All owner-side.

## Files updated
This report; NEXT_ACTIONS (exact-next-step); MASTER_DASHBOARD (last-run row).
