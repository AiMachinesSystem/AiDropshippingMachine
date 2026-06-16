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
> L'owner sceglie UN percorso dati: **(A)** approvare la raccolta dati SOLO da export/screenshot forniti dall'owner, **oppure (B)** approvare la ricerca pubblica esterna su policy/fee/feature di eBay e AutoDS. Finché non arriva un GO, la macchina resta in stop di inizializzazione.

## Parked Options (each needs its own explicit GO)
1. **Raccolta dati owner** (eBay Seller Hub, AutoDS dashboard, lista fornitori da export/screenshot) — GO classe: accesso a dati owner. Stop prima dell'analisi.
2. **Ricerca pubblica esterna** (policy/fee/feature correnti eBay + AutoDS) — GO classe: ricerca esterna.
3. Bloccate finché non esistono dati + analisi autorizzati: strategia · execution/SOP oltre la gate structure · pubblicazione/modifica listing · modifiche/automazioni AutoDS · ordini e pagamenti fornitori · scaling.

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
- Identità owner (nome) — USER INPUT NEEDED.
- Stato account eBay / AutoDS, lista fornitori, nicchia/categoria, target margine, baseline performance — USER INPUT NEEDED (lista completa: [[MISSING_OWNER_INPUTS]]).
- Policy/fee/feature correnti eBay + AutoDS — PUBLIC RESEARCH REQUIRED (ricerca non ancora approvata).

## Completed
- [x] 2026-06-15 — Import e merge della foundation eBay/AutoDS nella struttura della macchina (Phase 1 — system initialization completata).
