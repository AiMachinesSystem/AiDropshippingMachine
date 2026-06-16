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

---

<!-- Nessun run registrato. Il primo blocco nicchia reale va sopra questa riga. -->
