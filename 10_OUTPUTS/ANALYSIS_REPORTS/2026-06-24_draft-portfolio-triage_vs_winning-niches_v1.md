---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: draft_portfolio_triage
status: complete (internal analysis — dispositions per owner rule 2026-06-24; live execution GO-gated)
date: 2026-06-24
created_real: 2026-06-24
method: cross-reference live draft pull (read_draft_economics.py + read_draft_errors.py, cache draft_econ_2026-06-23_234208) against proven-demand niches (SECTOR RUN-03 + per-SKU audit, 2026-06-22).
owner_rule: "EbayViolation -> kill + replace; VeRO word -> strip the word." (Luca, 2026-06-24)
---

# Draft Portfolio Triage — 13 drafts vs proven demand (2026-06-24)

## Headline finding
Of **13 drafts, only 2 sit in a proven-demand niche** (Kitchen). The other 11 are scattered across niches
the account's **own sales data shows are dead or thin** (Pet 0u, Candle 1u, Home/Storage 0u, Beauty 0u,
Outdoor 0u, Bath 4u). **Every publish wall this session (EbayViolation ×3, shipping ×2) hit a dead/weak-niche
commodity.** We have been fighting the AutoDS UI to publish products the data says shouldn't be published.
This batch is the exact "scattergun me-too" anti-pattern RUN-03 flagged.

## Demand map (the yardstick) [OBSERVED — RUN-03, 99 live listings, 35 lifetime units, 2026-06-22]
TOP: **Pool/Water 15u (26% mgn) · Kitchen 8u (27%)** = 66% of all sales. · Weak: Cleaning 3u (best units/listing), Bath 4u, Tech 3u. · **DEAD: Pet 0u · Garden 0u · Home/Storage 0u · Beauty 0u · Outdoor 0u · Candle 1u.**

## Triage table
Draft data [OBSERVED — live pull this session]; niche tag [INFERRED from RUN-03 buckets]; disposition = owner rule + demand tier.

| # | Draft | Source | Niche [demand] | eBay error | Profit | Disposition |
|---|---|---|---|---|---|---|
| 11 | Splatter Screen Frying Pan | Amazon | **Kitchen [TOP]** | none | $7.48 | **KEEP** — only clean draft in a winning niche; US-origin → no shipping wall [INFERRED] |
| 12 | Microwave Splatter Cover | Amazon | **Kitchen [TOP]** | VeRO "Panasonic" | $7.72 | **STRIP VeRO + KEEP** — winning niche; fixable per your rule |
| 8 | Shower Squeegee | AliExpress | Cleaning [weak/efficient] | shipping/location | $7.03 | PARK — only shipping-walled draft in a niche that converts; revive only if eBay US policy gets set |
| 6 | Baby Bath Thermometer | AliExpress | Bath [weak] | shipping/location | $7.07 | PARK/low — weak niche + shipping wall |
| 7 | Dog Water Bowl | AliExpress | Pet [DEAD 0u] | **EbayViolation** | $7.26 | **KILL** (your rule) — dead niche anyway |
| 9 | Collapsible Water Bottle | AliExpress | Outdoor [DEAD 0u] | **EbayViolation** | $7.08 | **KILL** (your rule) |
| 10 | Clip-On Book Light | AliExpress | lighting [no proven niche] | **EbayViolation** | $7.44 | **KILL** (your rule) |
| 1 | Big Pencil Case | Amazon | Home/Storage [DEAD] | none | $35.64* | **KILL** — broken cost $133.13 / **0 stock**, never publishable |
| 13 | Mini Flat Iron | Amazon | Beauty [DEAD 0u] | already uploaded (dup) | $7.48 | **KILL** — duplicate + dead niche |
| 3 | LED Tea Lights 24pk | Amazon | Candle [DEAD 1u] | too many item specifics | $7.33 | KILL/deprioritize — dead niche, not worth the fix |
| 5 | Aerial Dog Trolley | Amazon | Pet [DEAD 0u] | VeRO "Loop" | $7.78 | STRIP VeRO (your rule) but **dead niche → low priority** |
| 4 | Dog Car Seat Cover | Amazon | Pet [DEAD 0u] | none | $7.73 | DEPRIORITIZE — dead niche |
| 2 | Trampoline Spring Tool | Amazon | Tools [≈dead] | none | $7.53 | DEPRIORITIZE — dead niche, commodity |

\* Pencil Case "profit $35.64" is an artifact of a broken $133.13 buy cost on 0 stock — not real.

## What the numbers say (analysis)
1. **The walls are a feature, not a bug.** The 3 EbayViolation + 2 shipping-walled drafts are all dead/weak-niche commodities (Pet, Outdoor, Bath, lighting). eBay rejecting them saved us from publishing dead weight. Your "kill EbayViolation" rule and the demand data **point at the same drafts** — strong convergence.
2. **Only 2 drafts deserve effort:** Splatter Screen + Microwave Cover (both Kitchen, the #2 proven niche). They are **Amazon US-origin**, so they avoid the China-location shipping wall entirely (US service validates for US location, like the 91 working live listings). Microwave Cover just needs "Panasonic" stripped.
3. **But they're Amazon = retail-arbitrage policy risk** (the standing suspension concern). The compliant play per the playbook + RUN-03 directive: **re-source Kitchen (and Pool/Water) from AliExpress**, where margin is also higher (19%→45-55%) and survival risk drops.
4. **Margins are thin across the board (~$7, ~27% markup).** Even the keepers are commodity-thin. Volume in a proven niche > another thin commodity in a dead one (profit model: scale is the #1 lever).

## Dispositions (per owner rule 2026-06-24)
- **KILL now (5):** Dog Water Bowl, Water Bottle, Book Light (EbayViolation rule) + Pencil Case (broken), Mini Flat Iron (dup). All dead/weak niche or unpublishable.
- **KILL/deprioritize (3):** LED Tea Lights, Dog Car Seat, Trampoline Tool — dead niches, not worth fixing.
- **STRIP VeRO (2):** Microwave Cover ("Panasonic" — KEEP, winning niche) · Aerial Trolley ("Loop" — dead niche, low priority).
- **KEEP/test (2 Kitchen):** Splatter Screen (clean) + Microwave Cover (post-VeRO). Publishable now if Amazon retail-arb risk accepted; otherwise re-source from AliExpress.
- **PARK (1):** Squeegee — revive only if the eBay US shipping policy is set (it's the one shipping-walled draft in a converting niche).

## Strategic move (the redirect)
Stop spending automation cycles on dead-niche AliExpress commodities. **Next sourcing batch = ≥70% Pool/Water + Kitchen, sourced on AliExpress** (RUN-03 directive + per-SKU audit §4). Pool/Water is seasonal (summer peak NOW) → scale while in-window. The current draft batch survives this filter with **2 of 13** items.

## Next action (recommended)
1. Execute the KILL batch (5 confirmed) behind a keep-list guard (never touch the 2 Kitchen keepers). *(needs a verified draft-delete path; live = GO.)*
2. Strip "Panasonic" from Microwave Cover → it becomes a clean Kitchen draft.
3. Launch a focused **AliExpress sourcing run on Pool/Water + Kitchen** (the proven cluster) — replaces the killed commodities with on-niche product. This is the "passa ad un altro prodotto" done by data, not by guesswork.

> Evidence basis: live draft pull this session [OBSERVED]; RUN-03 + per-SKU audit [OBSERVED 2026-06-22]; niche tags per draft [INFERRED]; Amazon-Kitchen publishability [INFERRED, untested]. No invented numbers; thin-margin caveats carried.

---

## ADDENDUM — AutoDS Marketplace sourcing pull (2026-06-24) + the warehouse unlock

**Pull:** `read_marketplace.py` over discovery feeds (trending / hand-picked / winning) + 6 cluster keyword searches. Cache `90_CACHE/fetches/autods/marketplace_2026-06-24_000709`. **220 unique products** [OBSERVED].

**THE UNLOCK — `min_price_warehouse`.** Each marketplace product declares its warehouse (US vs CN) + shipping time/cost. This is the root fix for this whole session's wall:
- The 5 AliExpress drafts failed publish because they're **CN-warehouse** → China-origin shipping service vs **US item-location** = "service not available for item location". 
- **US-warehouse products avoid the wall entirely** (US location + US domestic service validates natively, like the 91 working live listings) AND ship in **1–5 days** vs 22. 
- **New permanent sourcing rule: prefer `min_price_warehouse = US`.** Don't fight the location field — source around it.

**Limitations of THIS pull (honest):**
- The marketplace **UI search did not filter** (redirected to /marketplace) → the 220 are the *generic trending/winning feed*, not cluster-targeted. Only 16 loose Pool/Kitchen matches, **0 pool gear**.
- The trending "winning" feed is **mostly branded** (Dash, Costway, ReadyWise, Tstars, Pauwer, HEBE…) → **VeRO/IP risk**, wrong for our generic-title VeRO-safe approach. The account's proven cluster (pool covers, chlorine feeder, meat press) is generic-commodity and is **NOT** in AutoDS's promoted "winning" feed.
- The marketplace search/category-filter API params are not in the captured cache (UI posts a hidden body) → a clean cluster pull needs that filter cracked (next step).

**Candidates surfaced anyway (US-warehouse, GOOD = ≥$5 & ≥20%, but most branded → re-check VeRO):**
| Product | WH | buy→sell | margin | ship d | note |
|---|---|---|---|---|---|
| Dash Rapid Egg Cooker 6-egg | US | 16.99→24.98 | $7.99 (32%) | 5 | branded (Dash) — VeRO risk |
| HEBE Anti-Fatigue Kitchen Mat | US | 13.99→20.85 | $6.86 (33%) | 22 | branded; slow ship |
| Active Pets Dog Bowl Set (steel) | US | 12.96→17.88 | $4.92 (28%) | 3 | branded; near GOOD |

→ None are clean generic on-niche winners. **Conclusion: the generic marketplace feed is not the right replacement source; need the cluster/category filter.**

## Forward plan (recommended, confidence MEDIUM)
1. **Sourcing rule = US-warehouse only** (permanent) — kills the shipping wall at the source + fast shipping. Confidence HIGH (directly observed mechanism).
2. **Crack the marketplace category/keyword filter** (modify the reader to log+replay the search API body) → pull **US-warehouse + Pool/Water + Kitchen + generic (VeRO-clean)** candidates. This is the clean replacement pipeline.
3. **Kill the dead-niche draft tail** (5 confirmed) once a guarded draft-delete tool exists (manage_draft.py has no delete; remove_oos_listings.py is /products-only).
4. Rejected: forcing the CN-warehouse AliExpress drafts live (the location field won't persist — E-010) and publishing the branded Amazon Kitchen drafts (VeRO + retail-arb risk).
