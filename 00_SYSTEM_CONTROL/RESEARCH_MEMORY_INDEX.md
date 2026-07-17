---
tags:
  - machine
type: hub
status: template
description: "Memoria interrogabile di tutti i run di ricerca. Ogni run di niche-validation, competitor-analysis e ads-scan si registra qui a fine corsa (skill rule). PARTE VUOTO (solo schema) in una nuova macchina."
---

# RESEARCH_MEMORY_INDEX

> Queryable memory of all market-research runs. Every niche-validation,
> competitor-analysis, and ads-scan run MUST register here at close-out
> (skill rule — a run without registration is INCOMPLETE).
> QUERY MODE answers come from this file + the linked reports.
> Re-run only on explicit owner request or stale data (>30 days).
>
> **REGOLA NUMERI CANONICI:** più run sulla stessa nicchia → vince SEMPRE
> l'ultimo registrato. Il blocco nicchia con più run DEVE avere un'unica
> sezione `### CANONE CORRENTE` in testa (QUERY MODE legge SOLO quella) e i
> numeri superati sotto `### STORICO (superato da ...)`. Vietato lasciare
> numeri vecchi in campi schema (`census:`, `leader:`, `key numbers:`) fuori
> dallo STORICO.

## ENTRY SCHEMA (one block per niche — copy this template)

### `<NICHE LABEL>`

#### CANONE CORRENTE (run `<YYYY-MM-DD>`, `<type vN>` — QUERY MODE risponde SOLO da questa sezione)
- last_run: `<YYYY-MM-DD>` · type: `<niche-validation|competitor-analysis|ads-scan>` vN · file: `<path>`
- market: `<PROVEN|UNPROVEN|UNKNOWN>` · space: `<YES|TIGHT|NO>` (`<gap>`) · confidence: `<HIGH|MED|LOW>`
- census: `<N>` active advertisers · T1=`<n>` · T2=`<n>` · T3=`<n>` · leader: `<name>`
- top ad patterns: `<comma list>`
- key numbers: `<prices, longevities, counts worth remembering>`
- open items: `<owner-manual checks, unknowns>`
- integrity flags: `<anti-patterns observed in the market — never replicate>`

#### STORICO (superato da ...)
<!-- run precedenti dello stesso blocco, mai citabili come correnti -->

---

### `COMMODITY 8-NICHES — PROVEN LISTING PATTERN` (velvet hangers · over-door hooks · silicone trivet · shower curtain hooks · adhesive wall hooks · mesh laundry bags · silicone utensil set · ice cube tray)

#### CANONE CORRENTE (run 2026-07-17, competitor-analysis v1 — QUERY MODE risponde SOLO da questa sezione)
- last_run: 2026-07-17 · type: competitor-analysis v1 (eBay SOLD-comp, authenticated `read_ebay_sold.py`, read-only) · file: `10_OUTPUTS/COMPETITOR_ANALYSIS/2026-07-17_commodity-8niches_PROVEN-LISTING-PATTERN_v1.md`
- market: PROVEN · confidence: HIGH (pattern+endings) / MED (medians) · basis: 85–110 sold prices/niche
- **PROVEN PATTERN:** title = `[Type] + [Pack-count front-loaded] + [material] + [feature] + [use-case]`, brand-free
- **WINNING PRICE ENDING: `.99`** (dominant 6/8; `.00` co-leads only where decorative/vintage skews — shower hooks, over-door hooks)
- sold medians: velvet hangers $23.37 · utensil set $15.99 · trivet $14.08 · shower hooks $12.25 · over-door hooks $11.04 · ice tray $9.45 · mesh laundry $9.26 · adhesive hooks $9.23
- SEO autocomplete (front-load): pack-count numbers, "heavy duty", "with lid", "delicates/zipper", "rustproof/non-slip"
- key numbers: price at/just-under sold-median = Best-Match competitive band; above-median = punished
- integrity flags: competitor sold listings carry FULL specifics + multi-photo = OUR leak (A2/B1) — replicate STRUCTURE only, never content (§8)
- cache: `90_CACHE/fetches/ebay/sold_2026-07-17_18*`

#### STORICO (superato da ...)
<!-- primo run del blocco -->

---

## PLATFORM / POLICY REFERENCE RUNS (non-niche)

> Non-niche reference-data runs (policy/fee/feature). QUERY MODE: "what do we know about eBay/AutoDS
> policy/fees?" → read the cleaned tables; numbers are eBay.com (US)/EN-mirror unless market confirmed.

### eBay US July demand census + Q3 price-floor/runway (runs 2026-07-02/03, 6 web agents) — CANONE for batch builds
- last_run: 2026-07-03 · type: demand-census + competitor price-floor + trend-runway (read-only web) · reports: `10_OUTPUTS/MARKET_RESEARCH_REPORTS/EBAY_JULY_DEMAND_CENSUS_2026-07-02.md` + `EBAY_PRICEFLOOR_Q3_RUNWAY_2026-07-03.md`
- **PRICE-FLOOR RULE (canon):** 1.5× buy cost must sit INSIDE the observed eBay sold-badge band — category medians NOT sufficient (solar lights/LED collars: healthy medians, zero demand at target price). 22 types tested.
- VIABLE: diaper caddy · over-door shower caddy · vacuum bags multi-pack (≥10+pump) · wind spinner 3D · donut cushion · patio side table. DEAD at 1.5×: cable tray (street < buy cost) · pot-lid rack · plastic bins w/ lids $15↔$36 dead-zone · solar stake lights (all sold ≤$21.98) · LED collar · drink holder · shaker (BlenderBottle wall) · plain slow-feeder.
- **Q3 RUNWAY:** BTS/dorm storage+desk peak = first 3 weeks Aug (prices 2-3×) · cleaning peaks Aug · pool MAINTENANCE holds to Sept · early-fall/Summerween rising. DYING after Jul-4: floats/beach/patriotic/misting-fans/patio furniture.
- July peaking (sold-badge proof 2026-07-02): camping lanterns 4,357 · BBQ thermometer 2,796 · patio covers 1,509 · gel cushion 779 · jar opener 398.
- method canon: eBay `/b/` + `/shop/` via r.jina.ai = WORKS · `/sch/` + LH_Sold=1 + watchcount/wuanto = WALLED (403/bot) · sold badges = cumulative lower bounds · caches `90_CACHE/fetches/ebay.com/2026-07-03_*`
- applied: `_build_qbatchD.py` (KILL regex + BTS-1.6/desk-1.5/clean-1.4 boosts); AutoDS search clusters return noise (apparel/jewelry/fixtures) → manual title review mandatory (19 pruned across C+D).
- open items: memory-foam cushion velocity LOW-SAMPLE; Terapeak still account-gated (E-018); per-SKU eBay sold check for batch D types not yet run via `read_ebay_demand.py`.

### eBay + AutoDS — public policy / fee / feature (run 2026-06-15, data-collection v1)
- last_run: 2026-06-15 · type: data-collection (public, read-only) · report: `10_OUTPUTS/SYSTEM_REPORTS/2026-06-15_data-collection-public-research_report_v1.md`
- cleaned data: `02_DATA/02_CLEANED_DATA/{fee_table,policy_risk_table,autods_features_table}.md` · raw: `02_DATA/01_RAW_DATA/` · evidence: `90_CACHE/fetches/` (21 files)
- key canon (eBay.com US / EN-mirror — Luca's market UNCONFIRMED): dropshipping retail-arbitrage **prohibited**, wholesale allowed · defect ≤2% · late-ship ≤3% (TRS) · FVF most cat. 13.6% + $0.30/$0.40 · regulatory fee 0.35% on eBay.it/EU · AutoDS eBay plan ~$29.90/mo (Starter 400)
- open items: confirm eBay market (USER INPUT NEEDED); eBay.it/EU schedule + walled US-help numerics (PUBLIC RESEARCH REQUIRED)
- integrity flags: AutoDS lists many retailer suppliers (Amazon/Walmart) — recording only; arbitrage prohibition noted, never to be advised

### AutoDS account per-SKU audit (run 2026-06-22, Playwright read-only) — SUPERSEDES catalog-health numbers
- last_run: 2026-06-22 · type: account-intel per-SKU (read-only, Playwright `audit_listings.py`) · report: `10_OUTPUTS/ANALYSIS_REPORTS/2026-06-22_per-sku-audit_kill-restock-scale_v1.md`
- **POST-KILL STATE (verified 2026-06-22 audit_044324): catalog 207→99 live** (~108 dead+errored removed, GO owner), **13/13 winners survived**, errors 129→21, total sold unchanged (35). 12 dead+errored not tool-removable (4 un-tickable + 8 no eBay id) → owner manual.
- pre-kill snapshot: 207/214 pulled · **194 (94%) ZERO lifetime sales** · only **13 SKUs ever sold** (35 units total) · **top-5 = 66%, top-10 = 91%** of sales · **129 (62%) carry error_list flags** · 14 status=1 (OOS/inactive)
- **13 winners (sold):** Deck Jet pool fountain (6) · Dog Water Ramp (5) · Ham Maker (5) · Pet Grooming Loops (4) · Lian Li PC display (3) · Hedgehog Dryer Balls (3) · Ham Maker v2 (3) · then 1 each: Crochet Kit, Chlorine Feeder, Dog Life Jacket, 2× Pool Cover, Roller Pulley
- **REAL EDGE = pool/pond/outdoor-water cluster** (~7/13 winners) + kitchen meat-press + pet — NOT the 15 saturated commodity niches; pool gear seasonal (summer peak)
- pricing canon: live 27% markup ≈ 3× underpriced vs profit-max (sim: optimal ≈ market price / ~2.1× cost)
- evidence: `90_CACHE/fetches/autods/audit_2026-06-22_041033/_products_list.json` · session valid (saved 2026-06-20)
- integrity flags: per-SKU sold = lifetime (recency not split); status/error codes inferred; kill actions GO-gated behind keep-list guard
- **NICHE TRACTION×MARGIN (RUN-03, 2026-06-22, `10_OUTPUTS/SECTOR_PRACTICE/2026-06-22_niche-traction-vs-margin_RUN-03.md`):** catalog = scattergun (70 eBay categories/99). Sales concentrate: **Pool/Water (25 list, 15 units) + Kitchen (12 list, 8 units) = 37% of listings, 66% of sales.** **Demand/margin INVERSION:** selling niches have lowest margin (Pool 26%, Kitchen 27%, Cleaning 28%); high-margin niches don't sell (Beauty 37%, Home/Storage 36%, Bath 34%). → AliExpress re-source leverage highest on Pool+Kitchen; STOP listing Pet/Candle/Garden/Home/Beauty/Outdoor (33 list → 2 units). **DATA FLAG:** this JSON has NO watcher field → RUN-02 watcher counts UNVERIFIED.
- **CUSTOMER VOICE winner product-types (2026-06-22, `10_OUTPUTS/ANALYSIS_REPORTS/2026-06-22_winner-customer-voice_v1.md`):** pains/desired/over-promise per i 5 tipi Pool/Water+Kitchen → angoli copy per riscrivere le descrizioni. Top pains: pool cover=**vento** (failure mode #1), ham maker=istruzioni scarse+capacità piccola, chlorine feeder/deck jet=**leak/durabilità**, dog ramp=peso/ingombro. **LIMITE [SOURCED non OBSERVED]:** solo sintesi WebSearch — verbatim quote-bank BLOCCATO da muri (Amazon `product-reviews` 503; TroubleFreePool Cloudflare 403 anche via r.jina.ai). Upgrade a verbatim = browser assistito / chrome-devtools MCP (GO).

### Problem-first product ideation (run 2026-06-28, owner mindset shift) — 10 pains→products, eBay-validated
- last_run: 2026-06-28 · type: product-ideation (problem-first, workflow wf_9b92e0c6-73b + eBay sold-comp validation) · report: `10_OUTPUTS/MARKET_RESEARCH_REPORTS/2026-06-28_problem-first-product-ideation_v1.md`
- method: mined 39 human pains (5 lenses) → top 10 problem→product→angle → top 8 run through `read_ebay_demand.py` (REAL eBay sold). Ideation = [SOURCED directional, unverified]; eBay numbers = [OBSERVED, cache `90_CACHE/fetches/ebay/demand_2026-06-28_050346`].
- **STANDOUT [OBSERVED]: Pool robot cable swivel** — median **$89.99**, 47-48 recent sales, ST 20.5%, source ceiling **$67.94**, light-ship, in-season, pool edge, compatibility angle (no VeRO). Best candidate of the session; high-AOV breaks thin-margin wall without AliExpress.
- secondary: dog anxiety vest (demand 127 sold/ST 21.6% BUT thin $4.45 ceiling + July-4th deadline + sizing-variant risk → bundle-only); stainless slow feeder ($17.99, ceiling $5.66 thin); cling-wrap dispenser ($22.97, high comp).
- reject (thin/no margin on Amazon): cat litter mat ($13.68/ceiling $1.93), cutting board mat ($14/$2.21), dog paw washer ($14.60/$2.73, low ST), pop-up food tent (14 sold, summer-only).
- KEY LESSON: problem-first surfaced a high-margin winner generic product-hunting missed; BUT margin reality persists (low-AOV pain-solvers stay thin) → pick the HIGHER-AOV pains.
- integrity: ideation citations (Cornell/The Kitchn/ThePoolNerd/"37% tear rate") NOT independently verified → directional; eBay sold = observed; active_listings=None on 3 (rapid-burst) → ST partial.

### eBay REAL demand validation — sold-comp reader (run 2026-06-28, GO-1) — FIRST eBay-real demand, supersedes Amazon-proxy
- last_run: 2026-06-28 · type: eBay demand (read-only, authenticated session, `read_ebay_demand.py`) · report: `10_OUTPUTS/ANALYSIS_REPORTS/2026-06-28_ebay-demand-validation_GO1_v1.md`
- **UNLOCK:** owner eBay login saved (`storage_state_ebay.json`, GO-1). **Terapeak `/sh/research` = account-gated (302, E-018)** → pivot to authenticated SOLD-search (bypasses 403). Now the machine validates on REAL eBay sold-comps, not Amazon/AliExpress proxy.
- **DATA (median sold price · recent-30d sold · active comp · sell-through~ · max Amazon cost for net≥$4):** [OBSERVED 2026-06-28, cache `90_CACHE/fetches/ebay/demand_batch_2026-06-28_043735/`]
  - **Dog pool ramp** ⭐ med **$70.00** · 41/30d · active **107** · ST **25.2%** · maxCost **$50.65** — best demand×margin (up-ticket, low comp)
  - **Stock tank pool cover** med **$54.99** · 34/30d · active 665 · ST 8.1% · maxCost **$37.67** — high AOV, margin room
  - Deck jet pool fountain med $29.99 · 42/30d · active 206 · ST 13.1% · maxCost $16.04 (proven, tighter margin)
  - Pool fountain nozzle med $28.29 · 31/30d · maxCost $14.57
  - Ham maker meat press med $32.79 · 26/30d · active 366 · ST 6.9% · maxCost **$18.46** (demand proven, margin TIGHT on Amazon)
  - Pool cleaner parts med $19.22 · 59/30d · maxCost $6.73 (high demand, thin) · Pool chlorine floater med $15.98 · maxCost $3.92 (thin + E-014 category) · Dog life jacket med $16.99 · 835 sold · maxCost $4.80 (thin)
- **KEY FINDING:** demand/margin inversion CONFIRMED at eBay-real level. The margin escape WITHOUT AliExpress = go **up-ticket** (≥$50 sold price → $37-50 Amazon-source ceiling clears net). Top depth targets: **dog ramp/steps + stock-tank pool kit** (Amazon-US sourcing viable); deck jet + ham maker = proven demand but tight margin on Amazon.
- open items: active_listings=None for 4 low-priority queries (rapid-burst thin ACTIVE page) → sell-through proxy partial; net validation per SKU needs AutoDS import economics (GO-4). sold_results (exact) vs sold_parsed (incl. "fewer words") — cite sold_results.
- integrity flags: median from completed/sold comps (OBSERVED); sell-through = proxy (sold/(sold+active)); no fabricated numbers; Terapeak gated (not used).

### AutoDS account read-only status (run 2026-06-16, Playwright read-session)
- last_run: 2026-06-16 · type: account-intel (read-only, Playwright) · report: `10_OUTPUTS/autods_status_report.md`
- store: `Divinit-92-Us` (id 3713044, eBay US, USD) · catalog: **214 active listings + 11 drafts (+4 untracked)** · suppliers: Amazon US + AliExpress/CJ
- sales: 23 lifetime orders; last 7d = 3 orders / $320 rev / $62 profit · pricing: 27% margin, $7 min, round .97 · auto-order ON but **NON-FUNCTIONAL** (0 buyer accts, $0 wallet)
- subscription: **TRIAL → expires 2026-06-18** · AutoDS REST API = paid/gated (no key); **Playwright read-only path = OPERATIONAL**
- integrity flags: 1 draft VeRO keyword ('alcohol'); some listings OOS/On-Hold/supplier-title-changed; AutoDS Trending/Hand-Picked view = paid addon (walled)
- evidence: `90_CACHE/fetches/autods/run_2026-06-16_*` + `products_*` + `drafts_*`

### Deep Product Research 2026 (run 2026-06-16, multi-tool funnel)
- last_run: 2026-06-16 · type: product-research (read-only) · report: `03_ANALYSIS/DEEP_PRODUCT_RESEARCH_2026.md`
- funnel: 7 macro trends → 24 sub-niches → 121 AutoDS Marketplace products → 20 eBay cross-checks → TOP 15 + TOP 5 cards
- top-3 risk-adjusted: phone anti-lost tether ($1.64→$10.99, 68%, 145 sold/listing); 3D anatomy torso kids ($6.14→$23.99, 59%, 204 sold/listing); mascara wands ($3.18→$9.99, 51%, 529 sold/listing)
- key finding: eBay commodities = race-to-bottom; many ≤$8 items FAIL ≥50% margin at the floor; higher margin = low-comp/novelty + bundling + AliExpress (not Amazon) sourcing
- open items / walls: eBay aggregate sold = [UNKNOWN] (403 wall; per-listing 'X sold' badges only); AutoDS Trending view paywalled
- integrity flags: VeRO is the dominant risk (avoid brands in titles even 'compatible-with'); never replicate branded winners (Disney duck, Nike, etc.)
- evidence: `90_CACHE/fetches/autods/marketplace_2026-06-16_233945/`

### Profitability vs Competition — Amazon-sourced niches (run 2026-06-17)
- last_run: 2026-06-17 · type: profitability-strategy (read-only) · report: `04_STRATEGY/PROFITABILITY_VS_COMPETITION_2026-06-17.md`
- **CANON: Amazon→eBay arbitrage net margin ceiling ≈ 30–42%** (after FVF 13.6%+$0.40), NOT 50% — Amazon price sits too high; >50% needs AliExpress/CJ. (10 ASINs verified live, no fabricated data.)
- TOP verified opportunities (niche → Amazon ASIN): dog grooming complete kit `B0BR5H9QM7`/`B0DDBR98MB` (~42%); trunk organizer magnetic-lid `B0DZBFNVZ3` (~33–40%); electric jar opener `B07P1SKJV4` (sold 382/351/160 verified, ~30–37%); neck massager `B0D3DN6CDS` (~27–36%); koi pond aerator `B0CQXHB27H` (largest $ spread, ~28–32%); pegboard+bins kit `B07QR36Z76` (28,838 reviews, ~32–37%)
- profit levers: differentiated BUNDLE not floor · real cost gap verified both ways · undercut the BRANDED cluster (not the generic floor) · scale on verified sold badges · avoid VeRO+weight · lead with deep-review products
- integrity flags: Amazon sourcing = eBay retail-arbitrage policy risk (owner-directed); rejected branded (VeRO) + bulky + negative-margin (pond UV clarifier: Amazon > eBay) items
- evidence: workflow wf_f766e254-d4f (10 ASINs verified live 2026-06-17)

### Mid-Ticket Product Research (run 2026-06-17, modeled on account winners)
- last_run: 2026-06-17 · type: product-research (read-only) · report: `03_ANALYSIS/MIDTICKET_PRODUCT_RESEARCH_2026-06-17.md`
- scope: mid-ticket ($40-150) niche modeled on the 13 proven account winners; 16 candidates cross-checked on eBay
- TOP 3 STRONG: mini PC temp display (55 sold, low comp, native $43-150, mirrors $127 ARGB winner); dog car-seat hammock (271/124 sold, ~60% @ $45-55, light ship); bundled ham/meat press (mirrors $42 winner)
- meta-finding: most mid-ticket niches are ALSO price-compressed near AliExpress cost → only DIFFERENTIATED/bundled/larger SKUs on light-ship goods clear 50%; me-too generics REJECTED
- open items / walls: AliExpress live cost blocked (CAPTCHA) → costs [ESTIMATE], confirm COGS before GO; eBay aggregate sold [UNKNOWN] (403); re-query proven Dog Water Ramp niche with correct keywords
- integrity flags: VeRO kills several niches (Suitical/Lodge/Blackstone/CAROTE/BenQ) — generic-only; never replicate branded winners
- evidence: `90_CACHE/fetches/ebay/2026-06-17_*` + `marketplace_2026-06-17_013237/`

---

### Catalog multi-niche market census (15 nicchie del catalogo)

#### CANONE CORRENTE (run 2026-06-20, niche-validation v1 — QUERY MODE risponde SOLO da questa sezione)
- last_run: 2026-06-20 · type: niche-validation v1 (market census, read-only) · file: `10_OUTPUTS/MARKET_RESEARCH_REPORTS/2026-06-20_multi-niche-catalog_NICHE_VALIDATION_v1.md`
- market: **14/15 PROVEN**, 1 UNPROVEN (clip-on book lights) · space: **TUTTE TIGHT o NO** (nessun gap "facile") · confidence: MED (domanda alta/citata; margini NON valutati; conteggi = lower bound da muri eBay/AliExpress)
- ranking opportunità (score 0-10 verificatore): coffee pod holders **5.5** (TIGHT, solo tier station/decor) · poi a 4.5: shower squeegees · no-spill dog water bowls · stove gap covers · dog booster car seats · microwave splatter covers · mini flat irons · gecko RC toys (trend late-stage) · slow feeder dog bowls · a 3.5: collapsible water bottles · baby bath thermometers · portable neck fans (space=NO, **stagionale** picco giu-ago) · orthopedic dog beds · a 3.0: cable clips · **2.5 UNPROVEN: clip-on book lights**
- key canon: **tutte le nostre nicchie = domanda PROVEN ma commodity SATURE**; si vince SOLO con un **ANGOLO** (tier premium/decor · bundle · formato XL · compatibilità precisa nel titolo · foto+copy originali), MAI come me-too sul floor. **Lezione: domanda-prodotto ≠ opportunità-mercato** (il book light, top a livello prodotto, è UNPROVEN a livello mercato).
- key numbers: coffee pod holders **5.376 listing attivi eBay** (cat 46283), un listing 1.594 sold; shower squeegee AliExpress 10.000+ ordini; book light AliExpress 5.000+ ordini ma sold eBay per-listing 1-4 (domanda spalmata); neck fan stagionale picco giu-ago [OBSERVED 2026-06-20]
- open items: **margini non valutati** (fare costo AutoDS + fee prima del lancio); eBay sch/itm 403/429 + AliExpress CAPTCHA → conteggi lower bound, confermare col filtro Sold; Google Trends non aperto (direzione [INFERRED])
- integrity flags: anchoring prezzo "was/now" diffuso nel mercato = anti-pattern (documentato, mai replicare); VeRO resta il rischio (generico-only)

#### STORICO (superato da ...)
<!-- nessuno (v1) -->

### Trend signals untapped (8 segnali emergenti)

#### CANONE CORRENTE (run 2026-06-20, info-gathering v1 — QUERY MODE risponde SOLO da questa sezione)
- last_run: 2026-06-20 · type: info-gathering v1 (read-only) · file: `10_OUTPUTS/MARKET_RESEARCH_REPORTS/2026-06-20_trend-signals_INFO_GATHERING_v1.md`
- verdetto: nessun "pursue"; **maybe**: AirTag insole holder (score 4.5, rising, **VeRO HIGH** = mai "AirTag" nel titolo), car windshield sun shade umbrella (4.2, rising/**stagionale estate**, AliExpress $3.13-3.74), fridge bins (3.5), chicken shredder (3.0), ultrasonic cleaner (3.0, ticket alto); **avoid**: sunset lamp (2.5, **declining**), drain hair catcher (2.0, saturo), mini vacuum sealer (2.5, overlap "mini bag sealer")
- key numbers: AirTag insole AliExpress 2.000+/900+ ordini, costo ~$6.50, margine 34-46% @ $13-17, eBay 8+ seller $16.99-27.99; sun shade AliExpress $3.13-3.74 (2000+/700+ sold), eBay $10.99-27.99 [OBSERVED 2026-06-20]
- open items: **data_quality debole 7/8** (eBay 403 → domanda da proxy Google-Shop/AliExpress, non venduto eBay confermato); costi AliExpress da confermare in AutoDS; publish bloccato (account eBay)
- integrity flags: AirTag = marchio Apple (VeRO) → titolo generico obbligatorio; prezzi AliExpress $0.99 = trap primo-ordine (esclusi)

#### STORICO (superato da ...)
<!-- nessuno (v1) -->

### Amazon→eBay dropship products (ricerca accurata margine reale)

#### CANONE CORRENTE (run 2026-06-21, accurate v1 — QUERY MODE risponde SOLO da questa sezione)
- last_run: 2026-06-21 · file: `10_OUTPUTS/MARKET_RESEARCH_REPORTS/2026-06-21_amazon-to-ebay-dropship_ACCURATE_v1.md` · workflow wf_80ed0dff-bdc (28 agenti)
- metodo: AutoDS Marketplace (accesso autorizzato) → 36 generici economici → verifica **prezzo/margine eBay REALE** (non MSRP) + domanda + VeRO, giudizio avversariale
- verdetto: **nessun "good"; 2 "maybe", 12 "avoid"** su 14. Causa: costo Amazon spesso ≥ prezzo-pavimento eBay → margine sottile/negativo dopo fee
- **maybe**: Aerial dog trolley 60ft (B01M6A1ATC, $8.49→~$27, **~51% margine**, satur. media — il migliore) · Dog car seat cover 600D (B095GYDX22, $14.99→$27.99, 32%, satur. alta)
- integrity: MSRP Marketplace gonfiato (escluso dal margine); eBay Sold 403 → venduti lower bound, data_quality_ok false 12/14
- tesi confermata (3ª volta): domanda provata = commodity satura; leva = **costo basso + saturazione media**, non domanda grezza
- **round 2 (2026-06-21, wf_da6eb1a3-f6d, 10 candidati):** ancora **0 "good"**, 3 "maybe" thin (Trampoline pull tool, Door ball catch, Pencil case — importati per regola), resto avoid → **24 prodotti Amazon testati in 2 round, 0 good**. Conferma: pool Amazon <$20 = commodity satura. Prossimo: **AliExpress** (costo più basso = margini migliori)
- DRAFT IMPORTATI da questa nicchia (regola "3 ogni ricerca"): R1 = Aerial dog trolley · Dog car seat cover 600D · LED tea lights; R2 = Trampoline pull tool · Door ball catch · Pencil case

#### STORICO (superato da ...)
<!-- nessuno (v1) -->

---

### `Pool / Outdoor-Water` (cluster vincente della macchina)

#### CANONE CORRENTE (run 2026-06-30, competitor-analysis v1 — QUERY MODE risponde SOLO da questa sezione)
- last_run: 2026-06-30 · type: competitor-analysis v1 (3 web agent read-only) · file: `10_OUTPUTS/COMPETITOR_ANALYSIS/2026-06-30_pool-outdoor-water_COMPETITOR_ANALYSIS_v1.md`
- market: **PROVEN** · space: **YES** (2 lane non-presidiate: cover up-ticket bundled + sub-nicchie emergenti) · confidence: MED-HIGH landscape, MED sub-nicchie (eBay sold-comp NON ancora tirati)
- census eBay: campo **brandless, single-item, size-generic**; nessun leader dominante; top seller competono su formula-titolo (denier 600D/420D + aggettivi + size in inch). eBay listing pages BLOCCATE (403 diretto+proxy) → conteggi 'sold' = lower bound da snippet
- price bands [OBSERVED 2026-06-30]: patio/furniture cover $20-50 · grill cover $20-30 · hot-tub soft cover ~$50+ship · stock-tank cover (8ft) = categoria **UNOWNED** (listing ended) · dog ramp $40-90 retail · robotic swivel small-parts
- GAP map: (1) stock-tank cover sized-to-fit · (2) bundle cover+kit+bag+clips ($40-90 AOV) · (3) size-precision matrix · (4) winterizing/snow-load · (5) above-ground dog ramp · (6) robotic-cleaner accessory bundle
- sub-nicchie emergenti da validare (TOP-3): **smart ultrasonic water-level sensor** (WiFi/Tuya $20-70) · **cold-plunge/stock-tank accessories** ($30-120) · **dog/pet splash pad + paw fountain** ($20-45) — tutti light-ship, generic, no-VeRO
- saturati/brand-captured (no entry generico): statement floats (Funboy/Intex) · smart chemistry monitor (ICO/iopool/AIPER) · solar rings (trademark)
- VeRO brand da evitare nei titoli: BeyondNice/Rosefray/UCARE (spa) · Royal Gourmet/iCOVER (grill) · Porch Shield · StorMaster · Skamper Ramp · Dolphin/Maytronics/Pentair (robotic)
- key numbers reali (sold-comp eBay, run 2026-06-28/29): Hot Tub Cover med $50.64/495 sold · Dog pool ramp $70/107 active/ST 25%/maxcost $50.65 · Stock-tank cover $54.99/ST 8%/maxcost $37.67 · Deck jet $29.99/maxcost $16 · accessori <$20 = thin
- integrity flags (anti-pattern del mercato DTC, MAI replicare): superlativi "#1 in North America" · stat interne non verificabili ("<1% warranty claims") · risparmio inventato "$72.50/yr" · claim cover "walk-on/pet-safe"
- open items: **#1 gap = dato eBay sold-velocity dietro muro 403** (serve Terapeak/API o sessione browser); validare TOP-3 sub-nicchie su sold-comp+costo AutoDS prima di ogni batch
- pattern strutturale (3× confermato): **inversione domanda/margine** — accessori pool ad alta domanda <$20 = net ~$0; il margine sta nell'**up-ticket** ($50+, cover/ramp), sourcing Amazon-US clears net senza AliExpress

#### STORICO (superato da ...)
<!-- Dati pool pre-2026-06-30 sparsi nei blocchi: per-SKU audit 2026-06-22 (Pool/Water = 7/13 winner) · eBay demand GO-1 2026-06-28 · profit-run 2026-06-29 (2/3 VIABLE up-ticket). Restano validi come dettaglio; il canone competitivo corrente è sopra. -->

---

<!-- Nessun altro blocco nicchia formale ancora. Il prossimo blocco nicchia reale va sopra questa riga. -->
