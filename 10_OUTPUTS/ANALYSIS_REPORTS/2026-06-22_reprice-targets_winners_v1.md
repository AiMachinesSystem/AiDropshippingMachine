---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: reprice_targets
status: draft (INTERNA — market bands + recommendations; live reprice = GO / Strategic Gate)
date: 2026-06-22
created_real: 2026-06-22
method: WebSearch market-band scan for each top winner (mixed active/sold/retail comps; eBay sold is 403-walled → bands approximate). Reprice rule from elasticity sim (price ≈ market / ~2.1× cost, never the floor).
---

# Reprice targets — the 13 winners (2026-06-22)

> INTERNA. Market bands are [OBSERVED — WebSearch 2026-06-22], approximate (eBay sold = walled). **Exact per-SKU reprice deltas need a quick read of current sell price + landed cost** (not in the audit JSON) — GO-light. Actually changing a price live = GO; a large shift = Strategic Gate.

## ⚠️ REAL PER-SKU ECONOMICS (D3, from cache `audit_2026-06-22_044324` — SUPERSEDES the target bands below)
[OBSERVED — AutoDS `variation_statistics`, 2026-06-22] All 13 winners are **Amazon-sourced**. Current buy/sell/margin:

| Winner (sold) | Buy | Sell | Margin | Read |
|---|---|---|---|---|
| Deck Jet pool fitting (6) | $96.46 | $137.98 | 14.8% | cost too high → sourcing-bound |
| Dog Water Ramp (5) | $135.00 | $201.98 | 18.0% | high-ticket, thin → re-source |
| **Ham Maker +thermo (5)** | $26.99 | $41.83 | 19.7% | **low cost → REPRICE UP to ~$49-55** |
| Pet Grooming Loops (4) | **$133.13** | $285.98 | 38.3% | ⚠ **$133.13 = known placeholder BUG**; $286 absurd for loops → economics NOT USABLE, fix cost |
| Lian Li display (3) | $78.00 | $116.59 | 17.8% | branded (VeRO) + likely > retail → de-brand/drop |
| Hedgehog Dryer Balls (3) | $10.99 | $22.98 | 35.6% | healthy; at/above market — leave |
| **Ham Maker v2 (3)** | $29.99 | $46.98 | 20.4% | **low cost → REPRICE UP to ~$55-65** |
| Crochet Kit (1) | $18.99 | $38.44 | 34.7% | fine |
| Chlorine feeder (1) | $48.48 | $69.98 | 15.2% | thin → re-source |
| Dog Life Jacket (1) | $26.99 | $41.98 | 17.4% | thin |
| Solar Stock Tank Cover (1) | $43.99 | $69.95 | 21.6% | ~at market |
| Stock Tank Cover (1) | $59.99 | $94.69 | 21.3% | **sell > market band ($48-64) → likely won't move; re-source** |
| Roller Pulley (1) | $16.59 | $28.98 | 26.5% | fine |

### CORRECTED CONCLUSION (the earlier "underpriced, leave 2/3 on the table" thesis was WRONG for most winners)
The real data shows margins are mostly **15-21% because Amazon COST is 60-80% of sell** — they're already priced near/above market. **This is a SOURCING problem, not a pricing problem.**
- **Reprice-UP headroom exists ONLY for the 2 Ham Makers** (low Amazon cost ~$27-30, market $25-69). → quick win.
- **All the others are sourcing-bound** → the lever is **re-source on AliExpress** (cut cost), not reprice.
- **Data-quality flags:** Grooming Loops cost `$133.13` = the known AutoDS placeholder bug (economics unusable); `views=0` on all 13 — RESOLVED: **artifact** (AutoDS API doesn't populate `views`; `watchers` IS populated = 35 total, 8/13 winners). Use **watchers** as the engagement proxy, not views.
- **Lian Li:** branded + likely priced above retail → de-brand/drop (D2).

## Target bands (priority = lifetime sold)
| Winner (sold) | Market band [OBSERVED web] | Reprice target | Note |
|---|---|---|---|
| Deck Jet pool fountain fitting (6) | fittings ~$9-30 | **$19-29** (premium/kit, not the $9 floor) | top seller — price to the band |
| Dog Water Ramp pool/boat (5) | no clean comp; dog pool ramps ~$45-90 | **$49-75** (verify comp) | NEEDS-COMP before final |
| Ham Maker meat press +thermo (5) | $25-69; premium w/ thermo+bags ~$49-69 | **$49-69** | bundle (thermo+bags+recipes) justifies top |
| Pet Grooming Loops 2-pack (4) | ~$10-20 | **$15-19** | light, repeat-buy |
| **Lian Li PC display (3)** | retail ~$45-60 | ⚠️ **see flag below** | **VeRO + branded — strategic** |
| Hedgehog Dryer Balls 2pk (3) | $11-20 | **$16-19** | |
| Stock Tank Pool Cover 8ft ×2 (1+1) | $47-90; common $48-64 | **$49-59** | seasonal peak now |
| Chlorine feeder / Dog life jacket / Roller pulley / Crochet kit (1 each) | — | lower priority | reprice after the top 7 |

## ⚠️ Strategic flag — Lian Li PC display (winner #5)
Its title carries the **brand "Lian Li"** → double risk: (1) **VeRO** (trademark in title), (2) it's a genuine branded electronic likely retail-sourced = arbitrage. This is exactly the suspension trigger the sector canon + our ruin-sim warn about. **Options (Strategic Gate — owner):** (a) de-brand the title to generic spec ("8.8in IPS PC Temp Monitor ARGB USB"), accepting it may lose brand-search traffic; (b) delist it (3 sales isn't worth an account-level VeRO strike); (c) keep as-is and accept the risk. **Recommendation: (a) de-brand**, or (b) if it can't sell generic.

## The reprice rule (why)
Elasticity sim: profit-max price ≈ **market / ~2.1× cost**, NOT the commodity floor; the live 27% markup is ~3× underpriced. Move each winner toward the band's mid/upper (we sell on bundle+demand, not on being cheapest). Promoted Listings only AFTER margin is fixed, ≤3% start (sector rule).

## Next step to execute reprice
1. **[GO-light read]** pull current sell price + landed cost for the 13 (one targeted read) → compute exact deltas vs these targets.
2. **[GO / Strategic Gate]** apply new prices (small shifts auto under mandate; large shifts I bring to you first).
3. De-brand/delist Lian Li per your call.
