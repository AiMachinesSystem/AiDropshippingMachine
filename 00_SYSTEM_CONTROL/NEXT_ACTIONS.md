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
> Ricerca pubblica policy/fee/feature (percorso B) **COMPLETATA** il 2026-06-15 → dati in `02_DATA`, report in `10_OUTPUTS/SYSTEM_REPORTS`. Siamo al **gate Data → Analysis**. L'owner sceglie: **(1)** autorizzare l'**Analisi** dei dati raccolti (interna), **(2)** confermare il **mercato eBay** (eBay.it/eBay.co.uk/eBay.com) + fornire input account/AutoDS, oppure **(3)** approvare una **ricerca di follow-up** per i gap `PUBLIC RESEARCH REQUIRED`.

## Parked Options (each needs its own explicit GO)
1. **Autorizzare l'Analisi** dei dati policy/fee/feature raccolti (interna; richiede GO del gate Analysis).
2. **Raccolta dati owner** (eBay Seller Hub, AutoDS dashboard, lista fornitori da export/screenshot) — GO classe: accesso a dati owner. Stop prima dell'analisi.
3. **Ricerca pubblica di follow-up** (eBay.it/EU una volta noto il mercato; numerici US-help dietro fetch wall; pricing AutoDS in EUR) — GO classe: ricerca esterna.
4. Bloccate finché non esistono dati + analisi autorizzati: strategia · execution/SOP oltre la gate structure · pubblicazione/modifica listing · modifiche/automazioni AutoDS · ordini e pagamenti fornitori · scaling.

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
- **Mercato eBay di Luca (eBay.it/eBay.co.uk/eBay.com)** — USER INPUT NEEDED (determina lo schema fee/policy vincolante).
- Policy/fee/feature: baseline eBay.com/US raccolta 2026-06-15; **eBay.it/EU localizzati + numerici US-help dietro fetch wall + pricing AutoDS in EUR** — PUBLIC RESEARCH REQUIRED (dettaglio: `02_DATA/03_MISSING_DATA/2026-06-15_public-research-missing-data-log.md`).

## Completed
- [x] 2026-06-15 — Import e merge della foundation eBay/AutoDS nella struttura della macchina (Phase 1 — system initialization completata).
- [x] 2026-06-15 — Governance closeout: owner = Luca; etichette = solo set §0.4 (superset `OPERATING_RULES §3` in quarantena, non ratificato); compilazione `VISION_ALIGNMENT` rinviata.
- [x] 2026-06-15 — Ricerca pubblica policy/fee/feature eBay+AutoDS (percorso B): 21 fonti in cache → 3 raw + 3 tabelle pulite + note fonti/qualità/missing + data intake report. Stop prima dell'analisi.
