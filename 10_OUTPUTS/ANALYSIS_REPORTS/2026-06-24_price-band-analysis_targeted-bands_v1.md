---
machine: "eBay / AutoDS Dropshipping Machine"
type: price_band_market_study
status: complete (internal analysis; publishing = GO-gated)
date: 2026-06-24
created_real: 2026-06-24
owner_q: "Luca 2026-06-24 — rifai la ricerca sulle fasce di prezzo (60/130 vendono di più + margine) per pubblicare annunci mirati."
method: "Account sold-data by price band (audit_2026-06-22_044324/_products_list.json, 99 listings/35 units) +
  marketplace US-warehouse on-niche margin by band & targeted candidates (mkt_source_2026-06-24_021122, 1669 products)."
---

# Price-Band Market Study — where sales & margin actually are (2026-06-24)

## 1. Account ground truth — sales by price band [OBSERVED, audit 2026-06-22; LOW-SAMPLE 35 units]
| Band | Listings | Units sold | Sold/listing | Avg profit |
|---|---|---|---|---|
| $0-15 | 3 | 0 | 0.00 | $7.35 |
| $15-25 | 30 | 3 | 0.10 | $7.95 |
| $25-40 | 31 | 2 | 0.06 | $9.43 |
| **$40-60** | 12 | 9 | **0.75** | $10.86 |
| $60-90 | 6 | 2 | 0.33 | $14.19 |
| **$90-140** | 6 | 10 | **1.67** | **$20.72** |
| $140+ | 11 | 9 | 0.82 | **$46.69** |

**Read:** the owner's recollection is correct — the **$90-140** band is the best (velocity 1.67/listing + $20.72 profit)
and **$140+** has the highest profit/sale ($46.69). The **$15-40 band — 62% of the catalog (61/99) — barely sells
(0.06-0.10/listing)**. We are over-invested in dead commodity price points. ⚠️ LOW-SAMPLE: high bands rest on 6-11
listings; directional, not statistically robust.

## 2. Marketplace supply — margin & generic availability by band [OBSERVED, 1669-product pull]
| Sell band | US-WH on-niche products | Avg margin | Generic (VeRO-LOW) available |
|---|---|---|---|
| $15-40 | 342 | $7.01 | 50 |
| **$40-60** | 72 | **$14.16** | **21** |
| $60-90 | 27 | $19.10 | 1 |
| $90-140 | 18 | $28.55 | 3 |
| $140+ | 20 | $85.33 | 2 |

**The binding constraint:** margin rises with price, BUT clean **generic (VeRO-safe) supply collapses above $60**
(only 1-3 items). The $90-140 winners are almost all branded (VeRO risk) → wrong for our generic-title approach.
**Sweet spot we can actually execute = $40-72**: 2-3× the commodity margin ($14-22 vs $7), proven $40-60 sell-through,
and ~21 generic candidates.

## 3. Targeted shortlist — US-warehouse, generic, on-niche, sell $40-72 [the publish target]
Cleanest generics (heuristic VeRO check — confirm before publish; titles to be rewritten generic):
| Niche | buy$ | sell$ | margin$ | ship d | Product |
|---|---|---|---|---|---|
| pool | 37.99 | 56.23 | 18.24 | 4 | Pool Cover Pump Above Ground (submersible) — **proven niche + in-season** |
| kitchen | 49.99 | 71.99 | 22.00 | 4 | Enameled Cast Iron Casserole Braiser Pan w/ Lid |
| storage | 39.99 | 59.59 | 19.60 | 4 | Laundry Basket with Wheels, 3-section Hamper |
| kitchen | 35.99 | 53.98 | 17.99 | 2 | Glass Canisters with Bamboo Lids, 3-Pack 80oz |
| kitchen | 44.44 | 59.99 | 15.55 | 2 | 2-in-1 Enameled Cast Iron Dutch Oven + Skillet Lid |
| kitchen | 39.97 | 55.96 | 15.99 | 5 | Ceramic Casserole Baking Dish w/ Lid |
| cleaning | 35.98 | 52.89 | 16.91 | 7 | Toilet Plunger + Brush Set (strip "uptronic") |
| pool | 40.00 | 57.60 | 17.60 | 5 | Extra Large Pool/Beach Utility Tote Bag |

*(25 VeRO-LOW on-niche candidates in $40-140 total; some flagged "generic" by heuristic are actually branded —
e.g. Camp Chef, YIIFEEO, Vtopmart, Fin Fun — and must be excluded or are compatibility-references only.)*

## 4. Recommendation (confidence MEDIUM; LOW-SAMPLE flagged)
1. **Stop publishing into $15-40** (dead zone, $7 thin). The 4 TEST listings just published sit here — leave them
   as a live pipeline test, but don't add more $20 commodities.
2. **Next batch = $40-72 generic kitchen/pool/storage** (table above). Prioritize **Pool** (proven niche + summer
   peak NOW) and **Kitchen** (proven #2 niche). Expected ~$14-22 gross margin/sale vs ~$7 — 2-3× better.
3. **Don't chase $90-140 yet** via this marketplace feed — clean generic supply isn't there; it's branded (VeRO).
   To reach the top band, source the account's OWN proven higher-ticket winners (Dog Booster Seat, Orthopedic Dog
   Bed, etc.) from AliExpress/US-warehouse — a separate sourcing track.

## Owner role / gate
Internal analysis only — no listings created. Publishing a targeted $40-72 batch = GO-CLASS (import → generic title
→ VeRO-safe desc → publish, proven pipeline). Evidence: account audit 2026-06-22 + marketplace pull 2026-06-24.

> [FACT] band sell-through & margins as tabled (observed). [ESTIMATE] marketplace margins are gross/pre-eBay-fee.
> [UNKNOWN] per-band sell-through is LOW-SAMPLE (35 units); brand/VeRO is heuristic, needs per-item confirmation.
