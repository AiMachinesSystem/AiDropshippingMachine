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

## PLATFORM / POLICY REFERENCE RUNS (non-niche)

> Non-niche reference-data runs (policy/fee/feature). QUERY MODE: "what do we know about eBay/AutoDS
> policy/fees?" → read the cleaned tables; numbers are eBay.com (US)/EN-mirror unless market confirmed.

### eBay + AutoDS — public policy / fee / feature (run 2026-06-15, data-collection v1)
- last_run: 2026-06-15 · type: data-collection (public, read-only) · report: `10_OUTPUTS/SYSTEM_REPORTS/2026-06-15_data-collection-public-research_report_v1.md`
- cleaned data: `02_DATA/02_CLEANED_DATA/{fee_table,policy_risk_table,autods_features_table}.md` · raw: `02_DATA/01_RAW_DATA/` · evidence: `90_CACHE/fetches/` (21 files)
- key canon (eBay.com US / EN-mirror — Luca's market UNCONFIRMED): dropshipping retail-arbitrage **prohibited**, wholesale allowed · defect ≤2% · late-ship ≤3% (TRS) · FVF most cat. 13.6% + $0.30/$0.40 · regulatory fee 0.35% on eBay.it/EU · AutoDS eBay plan ~$29.90/mo (Starter 400)
- open items: confirm eBay market (USER INPUT NEEDED); eBay.it/EU schedule + walled US-help numerics (PUBLIC RESEARCH REQUIRED)
- integrity flags: AutoDS lists many retailer suppliers (Amazon/Walmart) — recording only; arbitrage prohibition noted, never to be advised

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

---

<!-- Nessun altro blocco nicchia formale ancora. Il prossimo blocco nicchia reale va sopra questa riga. -->
