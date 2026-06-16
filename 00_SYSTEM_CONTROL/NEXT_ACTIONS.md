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
> **APPROVE STRATEGY + EXECUTION PLANNING ONLY — 5 eBay Listing Launch Sprint**
>
> Obiettivo owner: **5 listing eBay.com pubblicati** (launch-oriented — vedi `01_SYSTEM/LAUNCH_ORIENTED_OPERATING_PROTOCOL.md`). Il prossimo passo è il tuo **GO** per sbloccare **Strategy + Execution planning (SOLO interno)** dello sprint dei 5 listing. La pubblicazione live e ogni azione AutoDS/eBay/fornitori restano dietro **GO finale esplicito, per azione**.

## Parked Options (each needs its own explicit GO)
1. **Avviare l'intake AutoDS read-only** — pending prerequisiti (§6 del piano) + GO; metodo: export/screenshot/guided. (Controlled login = GO separato.)
2. **Analysis Delta Only** — aggiornare le conclusioni di dependency dell'analisi al contesto US-seller (interno).
3. **Strategy** (offer/pricing/listing/supplier/risk) — BLOCCATA: richiede GO owner + dati fornitori/economici.
4. **Raccolta dati owner** (eBay Seller Hub, AutoDS, fornitori da export/screenshot) — GO classe: accesso a dati owner.
5. **Raccolta dati fornitori/competitor/prodotto** (economics) — GO classe: ricerca esterna (nuovo scope).
6. **Ricerca pubblica di follow-up** (numerici US-help esatti; pricing AutoDS) — GO classe: ricerca esterna. (eBay.it/EU NON più rilevante.)
7. Sempre bloccate finché non c'è strategia approvata: execution/SOP oltre la gate structure · pubblicazione/modifica listing · automazioni AutoDS · ordini/pagamenti fornitori · scaling.

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
- Dati account-specifici eBay/AutoDS/fornitori/economics (account health, limiti, store tier, payment settings, piano AutoDS, fornitori, categoria, margini, dati business) — USER INPUT NEEDED ([[MISSING_OWNER_INPUTS]]).
- Numerici US-seller esatti dietro le pagine US-help (fetch wall) — PUBLIC RESEARCH REQUIRED. (eBay.it/EU non più rilevante.)

## Completed
- [x] 2026-06-15 — Import e merge della foundation eBay/AutoDS nella struttura della macchina (Phase 1 — system initialization completata).
- [x] 2026-06-15 — Governance closeout: owner = Luca; etichette = solo set §0.4 (superset `OPERATING_RULES §3` in quarantena, non ratificato); compilazione `VISION_ALIGNMENT` rinviata.
- [x] 2026-06-15 — Ricerca pubblica policy/fee/feature eBay+AutoDS (percorso B): 21 fonti in cache → 3 raw + 3 tabelle pulite + note fonti/qualità/missing + data intake report. Stop prima dell'analisi.
- [x] 2026-06-15 — Contesto owner salvato (USER-PROVIDED): buyer market = US / eBay.com, USD; seller country/location restano USER INPUT NEEDED. Gate Data → Analysis preservato.
- [x] 2026-06-15 — Analisi policy/fee/feature completata (evidence-graded; buyer vs seller-country split; niente strategia/raccomandazioni/profittabilità; verifica adversarial 3-agent = PASS). Gate Analysis → Strategy chiuso.
- [x] 2026-06-15 — Contesto seller salvato (USER-PROVIDED): seller US-registrato + US-located, USD; Italy/EU non rilevante. Dependency principale dell'analisi risolta; Strategy resta bloccata.
- [x] 2026-06-15 — AutoDS Read-Only Data Intake Plan creato (piano + prerequisiti + report). Solo piano; nessun login/accesso/dato AutoDS; intake non avviato.
