---
created: 2026-07-03
created_real: 2026-07-03
type: market-research
run: batch-D deep research (3 web agents: 2 competitor price-floor teardowns + Q3 runway census)
consumer: _build_qbatchD.py (KILL regex + boosts) and all future batch builds
---

# eBay price-floor + Q3 runway research — 2026-07-03 (00:00-00:30 EDT)

Method: eBay /b/ browse + /shop/ pages via r.jina.ai proxy (2 agents, 22 product types,
31 cached fetches incl. `90_CACHE/fetches/ebay.com/2026-07-03_*`), plus a July→September
trend-runway census. Sold badges = cumulative lower-bound proxies. /sch/ = 403 (confirmed).
Rule tested per type: our list price ≈ 1.5× Amazon-US buy cost must sit INSIDE the observed
eBay selling band.

## Price-floor verdicts (22 types)

**VIABLE:** diaper caddy ($21 vs 154-sold comp @ $19.99) · over-door shower caddy ($30 inside
$24.55–34.72 cluster) · vacuum bags multi-pack ($24; sold badges 75/112/98 @ $24.85–25.64;
spec ≥10 bags + pump) · wind spinner 3D ($22 = median; low density) · memory-foam donut
cushion ($30 < $41 median; velocity unproven, LOW-SAMPLE) · patio side table (TIGHT-VIABLE $39).

**TIGHT (reposition or skip):** under-sink organizer (2-pack only) · corner wire shelf ·
monitor riser (1,087-sold incumbent @ $18.99) · blanket basket (XL angle only) · massage ball
(therapy SET only) · fire-pit cover (40"+ only; 32" dead @ $14 winners) · pool float ($42 =
brand/fabric turf) · cat tree (53" @ $44 value-dominates 34" @ $40).

**DEAD at 1.5× (KILL list):** cable management tray (street $9.30–17 < our $19.95 buy;
226K-fb incumbent) · pot lid rack ($37 vs $12–25 demand cluster) · plastic bins w/ lids
mid-tier ($27 = dead zone between Sterilite $8–18 and $36+ multi-packs) · solar stake/flower
lights (all 14 sold badges ≤ $21.98) · LED dog collar/leash ($5–12 race-to-bottom) · floating
drink holder (winners $11–17) · insulated shaker (BlenderBottle wall) · plain slow-feeder bowl
($5–15; only elevated-with-stand clears $24).

## Q3 runway (2026-07-03 → September)

**RISING:** dorm/BTS storage & org (peak = first 3 weeks of August, prices 2-3× — kase.com,
voolist) · desk drawer organizers (search index peak Aug) · cleaning tools (Aug = seasonal
high) · kitchen viral (rice dispenser, stretch lids, magnetic knife holder) · pool MAINTENANCE
(holds to Sept + closing-season bump) · early fall/Summerween decor (rising now, Aug→Oct).
**DYING after July 4:** patriotic/July-4th anything · pool floats/inflatables (June peak,
Aug = clearance) · water guns/beach toys · beach tents/wagons/coolers · misting/neck fans ·
patio furniture (Aug price lows).

## Applied (batch D, 2026-07-03)

`_build_qbatchD.py`: merges BTS pull (mkt_source_2026-07-03_001909: 610 TEST US) + general
pull (2026-07-02_230426); KILL regex = DEAD lanes above; boosts: BTS Dorm 1.6, desk-drawer 1.5,
Clean-Aug/Kitchen-viral/bathroom-org 1.4, pool-maint/fall-early/laundry 1.3; title boosts for
VIABLE types. Built 60 + manual prune 14 (3 apparel, 2 jewelry, sunglasses, brand bottle,
2 faucets + shower head no-evidence, 4 tumbler near-dupes) + top-up 29 − 1 (plastic-bins dead
zone) = **74 candidates** → publish run D target 36.

## Reusable lessons
1. Category medians are NOT sufficient — solar lights and LED collars have healthy medians but
   zero sold badges at our target price. Sold-badge price bands are the real filter.
2. AutoDS search clusters return noise (apparel/jewelry/fixtures in "dorm storage" search);
   builder BAD regex hardened accordingly — manual title review remains mandatory before publish.
3. eBay /b/ and /shop/ via r.jina.ai works; /sch/ and LH_Sold=1 are walled; /b/…181055 nodes dead.
