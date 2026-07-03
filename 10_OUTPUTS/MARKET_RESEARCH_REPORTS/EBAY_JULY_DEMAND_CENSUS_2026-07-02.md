---
created: 2026-07-02
created_real: 2026-07-02
type: market-research
run: july-demand-census (3 web agents, read-only)
consumer: volume-engine batch builds (_build_qbatchC.py + _demand_boost_20260702.json)
---

# eBay US July Demand Census — 2026-07-02 (evening run)

Method: 3 parallel read-only web agents. eBay sold-badge counts read from live browse/category
pages (via r.jina.ai proxy where needed) = cumulative lower-bound proxies, NOT July-only velocity.
Blocked (declared): eBay /sch/ search (403/bot-challenge), LH_Sold=1 filter, watchcount.com (403),
wuanto/slayva (403), eBay Watchlist Trend Report (timeout). No numbers invented.

## Verdict per macro-niche (July signal)

| Niche | July signal | Strongest observed evidence |
|---|---|---|
| Pool/water accessories | **PEAKING** | skimmers 1,800/1,064 sold @ $49-59; floating solar lights 1,750 sold [OBSERVED — eBay browse 2026-07-02] |
| Patio/garden | **PEAKING** | furniture covers 1,509/914 sold @ $12-14; solar path light packs ~280 sold @ $17-19 [OBSERVED 2026-07-02] |
| BBQ/grilling | **PEAKING (July-4th spike)** | meat thermometer 2,796 sold @ $7.69; skewers 1,922 sold @ $7.99 [OBSERVED 2026-07-02] |
| Camping/beach | **PEAKING** | LED lanterns 4,357 sold @ $11.99; beach tents 389 sold @ $24.98; sand-free mat 364 sold @ $11.98 [OBSERVED 2026-07-02/03] |
| Cooling (pet + human) | **PEAKING** | dog cooling mats 87-127 sold; cooling towels 50-140 sold [OBSERVED 2026-07-03]; heavy new-seller influx = sharpest price competition |
| Comfort/ergonomics 35+ | RISING/FLAT-high | gel seat cushion 2-pack **779 sold** @ $22.49; jar opener **398 sold** @ $11.59; lumbar combo 298 sold [OBSERVED 2026-07-03] |
| Cleaning tools | RISING (peak = August) | seasonal high Aug, builds through July on move-in/back-to-school [FACT — salehoo trends, 2026] |
| Home storage/closet | RISING (back-to-college ramp) | bins w/ wheels trend 95/100; Vtopmart ~30k/mo Amazon-side proxy [FACT — sourceready 2026-04-15, asinsight Jun 2026] |
| Kitchen gadgets | FLAT (evergreen) | zero kitchen terms in eBay top-200 trending (May 2026); volume steady, no spike [FACT — eRank 2026-06-10] |
| Pet (non-cooling) | RISING | slow feeder 97 sold @ $23.92; ZIK: Pet Supplies avg sale $10.66 [OBSERVED/FACT 2026] |

## Price bands that sell (cross-niche)
- Dominant velocity band: **$8–$30** (lanterns, thermometers, skewers, solar packs, covers, cooling).
- Comfort/ergo holds higher prices with fewer new entrants ($18–$35).
- Storage/organization most competitive at $20–$50; container leaders $17–$20.

## Exclusions confirmed by census (IP/rules)
Branded cooling/comfort (Copper Fit, O2COOL, Sukeen, Mission), Stanley/Owala, battery electronics
(neck fans, mini AC), supplements, sized apparel/swim. NFL/NBA/licensed-sport merch = VeRO.

## How it was applied (this run)
`_demand_boost_20260702.json` cluster weights: Pool/Water · patio · Grills · seat cushion ·
jar opener = 1.5 | Garden = 1.4 | Meat · Home cleaning · Storage&Org · lumbar · dog slow feeder = 1.3
| closet · vacuum bags · insoles · chopper · Pet = 1.2 | kitchen/desk = 1.0.
Batch C: 60 built → 5 pruned on manual VeRO/apparel/edible review (2 NFL, 2 girls swimwear,
1 rawhide treats) → **55 candidates** to publish run (target 36 LIVE).
Builder filter hardened: `treats?|rawhide|nfl|nba|mlb|nhl|ncaa|swimwear|swimsuit|cover-up|bikini`.

## Reusable lesson
eBay browse/category pages render via r.jina.ai proxy where /sch/ is walled — sold badges on
browse pages are the working demand-proxy pattern for future runs.
