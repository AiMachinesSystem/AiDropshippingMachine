---
tags:
  - machine
type: log
status: active
description: "Lista chiara delle prossime azioni. Refreshata a fine run (regola AUTO-REFRESH). Popolata 2026-06-15 con lo stato post-import foundation eBay/AutoDS."
---

# Next Actions

> Modulo: 00_SYSTEM_CONTROL. Aggiornata a ogni fine run insieme a MASTER_DASHBOARD
> (regola AUTO-REFRESH: run senza refresh = INCOMPLETO). Dettaglio fase in [[CURRENT_STATUS]].

## ⚡ CHECKLIST MANUALE BROWSER OWNER
<!-- Azioni che solo l'owner può fare a mano (login, dropdown geo/reach, ecc.), con URL espliciti. -->
- Nessuna azione browser autorizzata in questa fase: nessun login, nessun accesso a eBay/AutoDS/fornitori. Ogni azione esterna richiede GO esplicito.

## Exact Next Step
> Analisi policy/fee/feature **COMPLETATA** (2026-06-15) → `03_ANALYSIS/` + `10_OUTPUTS/ANALYSIS_REPORTS/`. Siamo al **gate Analysis → Strategy (CHIUSO)**. **Prossimo step consentito: nessuna Strategy senza GO owner.** Per sbloccare servono (analisi §9): **paese di registrazione del seller** (dependency principale) + dati **fornitori/economici** (GO di raccolta separato). L'owner può: (1) dare il GO alla Strategy una volta colmati i blocker, (2) fornire il paese seller, (3) approvare una raccolta dati fornitori/competitor (nuovo GO).

## Parked Options (each needs its own explicit GO)
1. **Strategy** (offer/pricing/listing/supplier/risk) — BLOCCATA: richiede GO owner + paese seller + dati fornitori/economici.
2. **Fornire il paese di registrazione del seller** (+ posizione) — sblocca lo schema fee/tax/payment vincolante.
3. **Raccolta dati owner** (eBay Seller Hub, AutoDS, fornitori da export/screenshot) — GO classe: accesso a dati owner.
4. **Raccolta dati fornitori/competitor/prodotto** (economics) — GO classe: ricerca esterna (nuovo scope, fuori da policy/fee/feature).
5. **Ricerca pubblica di follow-up** (fee seller-side se EU; numerici US-help; pricing AutoDS EUR) — GO classe: ricerca esterna.
6. Sempre bloccate finché non c'è strategia approvata: execution/SOP oltre la gate structure · pubblicazione/modifica listing · automazioni AutoDS · ordini/pagamenti fornitori · scaling.

## Comando pronto (data collection, GATED — copia/incolla per dare il GO)
```text
APPROVE DATA COLLECTION ONLY

Machine: eBay / AutoDS Dropshipping Machine

Scope:
Use owner-provided screenshots/exports only.
Do not access accounts. Do not browse public web.
Do not analyze. Do not create strategy. Do not create execution plans.
Do not modify eBay, AutoDS, suppliers, payment accounts, or any live platform.

Inputs I will provide:
1. eBay Seller Hub screenshots/exports: [attach]
2. AutoDS dashboard screenshots/exports: [attach]
3. Supplier list or screenshots: [attach]
4. Fee/shipping/return/account health screenshots if available: [attach]

Output:
Raw data notes, cleaned data tables, missing data log, data quality notes, source access notes, final data intake report.
Stop before analysis.
```

## Waiting / Blocked
- Stato account eBay / AutoDS, lista fornitori, nicchia/categoria, target margine, baseline performance — USER INPUT NEEDED (lista completa: [[MISSING_OWNER_INPUTS]]).
- **Paese di registrazione + posizione fisica del seller** — USER INPUT NEEDED (NON assumere seller USA; determina lo schema fee/tax/payment vincolante).
- Policy/fee/feature: baseline eBay.com/US raccolta 2026-06-15; **fee seller-side (se seller EU) + numerici US-help dietro fetch wall + pricing AutoDS in EUR** — PUBLIC RESEARCH REQUIRED (dettaglio: `02_DATA/03_MISSING_DATA/2026-06-15_public-research-missing-data-log.md`).

## Completed
- [x] 2026-06-15 — Import e merge della foundation eBay/AutoDS nella struttura della macchina (Phase 1 — system initialization completata).
- [x] 2026-06-15 — Governance closeout: owner = Luca; etichette = solo set §0.4 (superset `OPERATING_RULES §3` in quarantena, non ratificato); compilazione `VISION_ALIGNMENT` rinviata.
- [x] 2026-06-15 — Ricerca pubblica policy/fee/feature eBay+AutoDS (percorso B): 21 fonti in cache → 3 raw + 3 tabelle pulite + note fonti/qualità/missing + data intake report. Stop prima dell'analisi.
- [x] 2026-06-15 — Contesto owner salvato (USER-PROVIDED): buyer market = US / eBay.com, USD; seller country/location restano USER INPUT NEEDED. Gate Data → Analysis preservato.
- [x] 2026-06-15 — Analisi policy/fee/feature completata (evidence-graded; buyer vs seller-country split; niente strategia/raccomandazioni/profittabilità; verifica adversarial 3-agent = PASS). Gate Analysis → Strategy chiuso.
