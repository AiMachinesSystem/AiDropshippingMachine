---
tags: [competitor-analysis, commodity, listing-pattern, data-first]
type: competitor-analysis
status: active
date: 2026-07-17
created_real: 2026-07-17
niche: [velvet-hangers, over-door-hooks, silicone-trivet, shower-curtain-hooks, adhesive-wall-hooks, mesh-laundry-bags, silicone-utensil-set, ice-cube-tray]
method: authenticated eBay SOLD-comp reader (read_ebay_sold.py), read-only
---

# Commodity 8-niches — PROVEN LISTING PATTERN (eBay SOLD comps, competitors making money TODAY)

> **Scope:** extract the *proven* listing pattern that actually sells — NOT our data. Feeds
> QUALITY_LISTING_PROTOCOL with real sold-comp evidence. Read-only.
> **Method:** authenticated eBay session → SOLD/completed search (`&LH_Sold=1&LH_Complete=1`),
> ~85–110 parsed sold prices per niche. Cache: `90_CACHE/fetches/ebay/sold_2026-07-17_18*`.

## VERDICT
The winning commodity listing pattern is consistent across all 8 niches:
**Title = `[Product Type] + [Pack/Count front-loaded] + [key material] + [feature] + [use-case]`, brand-free.**
**Price ending = `.99`** (dominant in 6/8; `.00` co-leads only where decorative/vintage skews the niche).
**Price = at/just under sold-median** to stay in Best-Match competitive band.

## CONFIDENCE
HIGH on pattern + endings (85–110 sold prices/niche, live today). MEDIUM on exact median (mixed
lot-sizes/decorative inflate tails; medians reported as central tendency, not a price target).

## PROVEN PATTERN TABLE  [OBSERVED — eBay SOLD, 2026-07-17, cache 90_CACHE/fetches/ebay/sold_2026-07-17_18*]
| Niche | n | Sold median | Winning ending | Title structure (from top sold) |
|---|---|---|---|---|
| velvet hangers | 102 | $23.37 | **.99** (30) > .00 (21) | Velvet Hangers + N Pack + Non-Slip + Swivel Hook + garment |
| silicone utensil set | 97 | $15.99 | **.99** (26) > .00 (17) | Silicone Utensil Set + N Pc + Heat Resistant + Nonstick |
| silicone trivet mat | 87 | $14.08 | **.99** (21) > .00 (14) | Silicone Trivet Mats + N Pack + Heat Resistant + Non-Slip + Hot Pots |
| shower curtain hooks | 96 | $12.25 | .00 (18) ≈ .99 (15) | Rings + N Pack + Rustproof + Metal (decorative skew) |
| over the door hooks | 91 | $11.04 | .99 (15) ≈ .00 (14) | N Pack + Metal/SS + Heavy Duty + coats/towels |
| ice cube tray | 95 | $9.45 | **.99** (27) > .00 (13) | Ice Cube Tray + N Pack + with Lid + Easy Release + Stackable |
| mesh laundry bags | 110 | $9.26 | **.99** (22) > .00 (12) | Mesh Laundry Bags + N Pack + Delicates + Zipper + lingerie |
| adhesive wall hooks | 99 | $9.23 | **.99** (16) > .00 (15) | N Pack + Heavy Duty + Waterproof + Clear + No Drill |

## SEO AUTOCOMPLETE (the words THAT niche searches — front-load these)
- velvet hangers: `100 pack`, `50`, `30`, `pink`, `white`, `space saving`
- over the door hooks: `rack`, `heavy duty`, `metal`, `plastic`
- shower curtain hooks: `rings`, `double hooks`, `rustproof`, `black`
- adhesive wall hooks: `heavy duty`
- mesh laundry bags: `heavy duty`, `zipper`, `delicates`, `small`
- ice cube tray: `with lid`, `large`, `mini`

## DOMINANT PATTERN → how we apply it
1. Front-load **pack count** (buyers literally search "velvet hangers 50 pack").
2. Lead with product type + count, then material, then the 1–2 top feature keywords, then use-case.
3. Target **.99** ending on all commodity (AutoDS price-optimization rule, not per-listing edit).
4. Item-specifics 100% (leak #1) + 8–12 photos (leak #2) remain the biggest conversion levers.

## OUR LEAK vs THESE COMPETITORS
- Their sold listings carry **complete item specifics + multiple photos**; ours import 1 scraped photo + partial specifics → we're buried in filters and convert low. Priority fix (protocol A2/B1).

## RECOMMENDED MOVE
Build/publish commodity listings in these 8 validated niches with the pattern above (titles already
aligned in `_qbatch181a.json`). Then close the item-specifics + photo leak on the winners.

## REJECTED ALTERNATIVES
- Copying competitor titles verbatim → §8 violation (VeRO/duplicate). We replicate STRUCTURE only.
- Anchoring price to a fantasy premium → sold data says commodity buyers punish above-median.

## OWNER ROLE
None for research (read-only, done). Publish = safe de-brand method (routine GO implicit).

## MEASUREMENT PLAN
Track sell-through on the published batch vs these medians; if a niche underperforms at median, it's a
specifics/photo leak, not a price problem (price already validated).

## BLOCKERS / OPEN
- JS row-parser in read_ebay_sold.py still obsolete (E-019) — worked around via raw page.txt parse. Fix pending.
- Medians inflated by decorative/vintage lots in hooks niches — treated as MEDIUM confidence.

## FILES UPDATED
This report · RESEARCH_MEMORY_INDEX (block) · QUALITY_LISTING_PROTOCOL (validated numbers).
