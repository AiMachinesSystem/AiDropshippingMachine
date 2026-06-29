---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: ebay_demand_validation
status: complete (read-only, GO-1); next = import economics + publish (GO-4)
date: 2026-06-28
created_real: 2026-06-28
skill: dropship-profit-run
method: "Authenticated eBay session (owner login GO-1) -> SOLD/completed-comp reader read_ebay_demand.py (bypasses 403). Terapeak /sh/research account-gated (E-018) -> sold-comp pivot. Net via owner formula (FVF 13.5%+$0.40, ship/tax $3, AutoDS $0.50, return $2)."
evidence: "90_CACHE/fetches/ebay/demand_batch_2026-06-28_043735/ (sold+active page text + _demand.json)"
---

# eBay REAL demand validation (GO-1) — 2026-06-28

## What changed (the unlock)
For the first time the machine validated candidates on **REAL eBay sold-comps**, not an Amazon/AliExpress proxy. Owner completed the eBay login (GO-1); session verified authenticated. **Terapeak Product Research is account-gated** (302 → /sh, both headless & headed — E-018), so I pivoted to the **authenticated SOLD-search reader** (`read_ebay_demand.py`), which bypasses the anonymous 403 wall and reads completed/sold listings directly.

## Data (OBSERVED 2026-06-28)
`max Amazon cost (net≥$4)` = 0.865 × median_sold − 9.90 (owner net formula). Source = **Amazon-US / US-warehouse** (AliExpress = discovery only, owner directive).

| Candidate | sold (exact) | recent-30d | median sold $ | active comp | sell-through~ | max source $ (net $4) | read |
|---|---|---|---|---|---|---|---|
| **Dog pool ramp / steps** ⭐ | 36 | 41 | **70.00** | **107** | **25.2%** | **50.65** | best demand×margin |
| **Stock-tank pool cover / kit** | 59 | 34 | **54.99** | 665 | 8.1% | **37.67** | high AOV, margin room |
| Deck jet pool fountain | 31 | 42 | 29.99 | 206 | 13.1% | 16.04 | proven, tight margin |
| Pool fountain nozzle | 71 | 31 | 28.29 | n/d | n/d | 14.57 | expansion |
| Ham maker meat press | 27 | 26 | 32.79 | 366 | 6.9% | 18.46 | proven, tight on Amazon |
| Pool cleaner parts (generic) | 595 | 59 | 19.22 | n/d | n/d | 6.73 | high demand, thin |
| Pool chlorine floater | 197 | 58 | 15.98 | n/d | n/d | 3.92 | thin + E-014 category |
| Dog life jacket | 835 | 57 | 16.99 | n/d | n/d | 4.80 | thin |

## Verdict
- **Demand/margin inversion CONFIRMED at eBay-real level:** highest demand (life jacket 835, cleaner parts 595, chlorine 197) = lowest price = thinnest margin.
- **Margin escape WITHOUT AliExpress = go UP-TICKET.** Where the eBay sold price is ≥$50, the Amazon-source ceiling is $37-50 → Amazon-US sourcing clears net ≥$4 (often much more). This resolves the thin-margin wall while keeping sourcing US-warehouse.

## Recommended depth batch (ranked; each step GO-gated)
1. **Dog pool ramp / dog boat steps (XL, weight-rated)** — AOV $70, low competition (107), ST 25%, $50 source ceiling. Proven account winner. **Top priority.**
2. **Stock-tank pool cover + "complete kit" (drain plug / leaf cover / filter parts)** — AOV $55, $37 ceiling, steady recent sales. Proven winner; bundle for AOV.
3. **Deck jet pool fountain nozzle + fitting kit** — proven, in-season, ST 13%; tighter margin ($16 ceiling) → list as a multi-fitting KIT to lift price/margin.
4. *(watch)* Ham maker bundle — demand proven but $18.46 ceiling vs ~$25-50 Amazon cost → only viable as a higher-priced **bundle** (press + thermometer + casings + recipe) that lifts the sold price above the thin zone.
- **De-prioritize** (thin margin on Amazon): dog life jacket, pool cleaner parts, chlorine floater (also category risk).

## Next gate (GO-4, per-batch)
For #1-#3: pick single-config Amazon-US ASINs (in-stock, generic, VeRO-safe) → import as DRAFT → read economics (reject $133.13/0 scrape-fail E-012) → confirm **real source cost ≤ the ceiling above** → SEO title ≤80 + rewritten desc → error pre-check (E-014) → publish, paced ≤~10/day. Then measure sell-through vs the $/day baseline.

## Caveats (honest)
- `active_listings=None` for 4 low-priority queries (rapid-burst served a thin ACTIVE page) → sell-through proxy partial; doesn't affect the top-3 which all have it.
- Net per SKU is not final until AutoDS import economics give the **real source cost** (the ceiling tells us the max we can pay, not the actual cost).
- sell-through = proxy (sold / (sold+active)); median from completed/sold comps (OBSERVED). No fabricated numbers. Terapeak gated → not used.

## Files
read_ebay_demand.py (new canonical reader); RESEARCH_MEMORY_INDEX (eBay-demand block); ERROR_REGISTRY E-018/E-019; cockpit refreshed.
