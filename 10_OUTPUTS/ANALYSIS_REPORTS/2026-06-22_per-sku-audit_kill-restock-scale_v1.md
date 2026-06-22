---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: per_sku_audit
status: complete (read-only pull + analysis — recommendations only, execution GO-gated)
go_scope: GO_AUTODS_READ_SESSION (read-only, Playwright, owner GO "both")
date: 2026-06-22
created_real: 2026-06-22
method: read-only Playwright pull of the SPA products/list API (audit_listings.py) → per-SKU total_sold_count/status/error_list. Analysis scripts in 90_CACHE.
evidence: 90_CACHE/fetches/autods/audit_2026-06-22_041033/_products_list.json (207/214 listings)
---

# Per-SKU audit — kill / restock / scale (2026-06-22)

> Read-only. Numbers are OBSERVED from the AutoDS SPA's own API. Every kill/restock/scale move below is a **recommendation**; execution on eBay/AutoDS is LIVE = GO-gated.

> **⚠️ POST-KILL STATUS (added after execution):** the KILL recommended in §4.1 was executed (GO owner) → **catalog 207→99 live, 13/13 winners survived, errors 129→21** (verified by independent audit `audit_2026-06-22_044324`). **§1 below is the PRE-KILL snapshot** (kept for the record). 12 dead+errored remain (tool-unremovable) → owner manual. For the current catalog state, the authoritative source is the owned-store block in `RESEARCH_MEMORY_INDEX`.

## 1. The brutal truth (OBSERVED)
| Fact | Value |
|---|---|
| Listings pulled | 207 / 214 |
| **Listings with 0 lifetime sales** | **194 (94%)** |
| Listings that ever sold | **13** |
| Total lifetime units sold | 35 |
| **Top-5 share of all sales** | **66%** |
| **Top-10 share of all sales** | **91%** |
| Listings carrying error_list flags | **129 (62%)** — dead+errored = **120 prime kill candidates** |
| status=1 (OOS/inactive) | 14 |

**This empirically confirms the simulation (cycle 1–3): the catalog is 94% dead weight; the business is really ~5–10 SKUs. Concentration isn't a strategy choice — it's already the reality, just un-managed.**

## 2. The 13 real winners (sold>0) — RESTOCK / SCALE these
| Sold | eBay item id | errors | Title (trunc) |
|---|---|---|---|
| 6 | 406382172143 | 0 | Deck Jet J-Style Pool Fountain Jet Replacement Fitting |
| 5 | 406174683287 | 1 | Dog Water Ramp for Boats & Pools (200 lbs) |
| 5 | 406103214230 | 2 | Ham Maker Stainless Meat Press + Thermometer |
| 4 | 406247019968 | 1 | 2-Pack Adjustable Pet Grooming Loops |
| 3 | 406391915026 | 0 | Lian Li 8.8" PC Display ARGB Temp Monitor |
| 3 | 406169382444 | 2 | Hedgehog Reusable Dryer Balls (2) |
| 3 | 406103169166 | 2 | Homemade Ham Maker & Deli Meat Press |
| 1 | 407007332522 | 1 | Beginner Crochet Kit (Amigurumi) |
| 1 | 406382169074 | 0 | Hydrotools 8750 In-Line Chlorine Feeder |
| 1 | 406174659709 | 0 | Dog Life Jacket (Ripstop, swimming) |
| 1 | 406149695098 | 3 | Solar Stock Tank Pool Cover 8ft |
| 1 | 406149693790 | 1 | 8ft Round Stock Tank Pool Cover |
| 1 | 406092460312 | 1 | Roller Idler Pulley 6x30x30mm 626RS |

## 3. The discovered niche (the real edge)
**~7 of 13 winners are POOL / POND / OUTDOOR-WATER gear** (Deck Jet, Dog Water Ramp, Chlorine Feeder, 2× Pool Cover, Roller Pulley, Dog Life Jacket) + **kitchen meat-press** (Ham Maker ×2) + **pet** (grooming loops, dryer balls). The account's proven demand clusters there — not in the 15 saturated commodity niches we keep testing. **This is where to source deeper (bundles, adjacent SKUs) — and on AliExpress, for margin + survival.**
> ⚠️ Pool/pond gear is **seasonal** (summer peak now) — scale fast while in-season; note the window.

## 4. Recommended moves (impact-first; execution = GO)
1. **[GO] KILL the dead+errored tail** — the 120 zero-sale listings carrying error flags (62% of catalog) add VeRO/policy surface and dilute attention for $0 return. Batch-remove (tool exists: `remove_oos_listings.py`, with keep-list guard around the 13 winners).
2. **[GO] RESTOCK/verify the 13 winners** — fix their error flags (8 of 13 carry errors), confirm in-stock + correct cost.
3. **[GO] FIX PRICING** — current 27% markup is ~3× under the profit-max point (cycle-3 sim: optimal ≈ market price / ~2.1× cost). Re-price the 13 winners toward market, not the floor.
4. **[INTERNA→GO] Re-source the pool/pond + ham winners on AliExpress** → margin 19%→45-55% + drop suspension risk (cycle-2: AliExpress engine = 2.3× expected value, 2× survival).
5. **[INTERNA] Source adjacent pool/pond/water SKUs** (the proven cluster) as the next draft batch, not more random commodities.

## 5. Caveats
- `total_sold_count` is lifetime per listing; velocity/recency not split this run (sold badges are cumulative). 7 listings not captured (207/214).
- status codes inferred (2=running, 1=OOS/inactive) from distribution; error_type codes (5/6/4) not yet decoded to messages.
- Kill list must run behind the keep-list guard (the 13 ids above) to avoid removing a winner.
