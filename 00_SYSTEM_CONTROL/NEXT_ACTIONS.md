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
> **Stato 2026-06-17:** rimossi 37 OOS morti (AutoDS+eBay) → **177 attivi**. **Trial AutoDS NON rinnovato (owner) → scade 18/06**: il monitoraggio stock/prezzo cessa sui 177.
> 1. ⏰ **DECISIONE OWNER:** wind-down AutoDS? Se sì → piano per i 177 su eBay (gestione manuale / altro tool / chiusura graduale). Se no → riconsiderare un rinnovo minimo prima del 18/06.
> 2. **HOLD — import 3 mid-ticket (PC temp display / amaca cane / ham press):** non importare in un account che scade domani; + sourcing **Amazon = rischio policy** (consigliato **AliExpress alto-recensioni**). Sbloccare solo dopo la decisione su AutoDS.
> 3. **Da fare solo se l'account resta gestito (GO/manuale):** ristoccare i 5 OOS-winner (Dog Water Ramp $202, Pet Grooming Loops $286, Ham Maker…); fix VeRO ('alcohol' draft + 63 attivi) + 100 titoli cambiati.

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
- [x] 2026-06-16 — Playwright installato (venv isolato) + smoke test connettività (HTTP 200 su platform.autods.com). Read-only, nessun login.
- [x] 2026-06-16 — Login AutoDS + sessione salvata (`storage_state.json`, gitignored) sotto GO_PLAYWRIGHT_LOGIN; sessione riutilizzabile verificata.
- [x] 2026-06-16 — AutoDS read-only status (GO_AUTODS_READ_SESSION): store Divinit-92-Us, 214 listing/11 draft/23 ordini, auto-order ON ma non operativo, trial scade 2026-06-18 → `10_OUTPUTS/autods_status_report.md`.
- [x] 2026-06-16 — Capability audit read-only (7 agenti) → `10_OUTPUTS/DROPSHIPPING_MACHINE_CAPABILITY_AUDIT_2026-06-16.md`.
- [x] 2026-06-16 — Deep Product Research (funnel multi-tool) → `03_ANALYSIS/DEEP_PRODUCT_RESEARCH_2026.md`; TOP 15 + 5 schede; muri eBay/AutoDS dichiarati.
- [x] 2026-06-16 — Decisione strategica autonoma (7gg) → `04_STRATEGY/STRATEGIC_DECISION_2026-06-16.md`. Solo piano; nessuna azione live.
- [x] 2026-06-17 — Tally read-only dei 214 + lista azioni per-listing (201 close / 13 keep / 63 VeRO / 100 title) → `05_EXECUTION/.../listings/LISTING_AUDIT_2026-06-17.md` + CSV. Da rivedere prima di GO.
- [x] 2026-06-17 — Update strategia (insight mid-ticket + downgrade torso) + Mid-Ticket Product Research (top 3: PC temp display, dog car hammock, ham press) → `03_ANALYSIS/MIDTICKET_PRODUCT_RESEARCH_2026-06-17.md`. Read-only; costi [ESTIMATE] da confermare prima di GO.
- [x] 2026-06-17 — **LIVE WRITE (GO owner): rimossi 37 listing OOS mai venduti** (AutoDS + eBay, opzione "AutoDS and Selling Platform"), 214→**177**; 13 venditori + 5 OOS-winner protetti (keep-list hard-bloccata); test 2 + batch verificati (count 177, 0 target residui). Tool: `integrations/autods/playwright/remove_oos_listings.py`.
- [x] 2026-06-17 — Owner: **NON rinnovare il trial AutoDS** (scade 18/06).
- [x] 2026-06-17 — **Import draft (GO owner): duck topper AliExpress** (`1005006027632555`, generico, ~60% margine, AliExpress CN) → Drafts 11→**12**. Solo draft, NON pubblicato (publish = GO separato). Tool: `import_drafts.py` (Add-as-Draft only). Pipeline import provata end-to-end.
  - ⛔ Import dei 2 mid-ticket (amaca cane / PC display) **bloccato**: URL AliExpress del finder risultati morti (CAPTCHA wall → non verificabili live). Serve: owner incolla URL validi, OPPURE browser visibile per passare il CAPTCHA AliExpress. Ham press = **ristoccare il vincitore esistente**, non re-importare.
- [x] 2026-06-17 — Profitability-vs-competition study → `04_STRATEGY/PROFITABILITY_VS_COMPETITION_2026-06-17.md` (canon: Amazon→eBay netto ~30-42%, non 50%; 6 leve; top niche+ASIN verificati).
- [x] 2026-06-17 — **Import draft (GO): 4-6 ASIN Amazon** → Drafts 12→16+: jar opener `B07P1SKJV4`, neck massager `B0D3DN6CDS`, koi aerator `B0CQXHB27H`, dog grooming arm `B0DDBR98MB`; trunk organizer `B0DZBFNVZ3` + pegboard `B07QR36Z76` entrati in ritardo (import asincrono). Solo draft, non pubblicati.
- [x] 2026-06-17 — Duck topper: **titolo+descrizione ottimizzati VeRO-safe** → `…/listings/LISTING_COPY_duck_topper_2026-06-17.md` (pronti da applicare).
  - ⛔ **Higgsfield immagine BLOCCATA**: "User not found" → ricollegare il **connettore Higgsfield** nelle impostazioni/connettori dell'app Claude (è MCP, non sbloccabile via browser/Playwright). Prompt immagine salvato, pronto.
  - ⛔ **Applicare la copy al draft via automazione NON persiste** (AutoDS non salva l'edit del titolo draft; 2 metodi falliti). → **Incolla manuale** dal file copy nel draft (1 min), oppure indagare il save-flow AutoDS in seguito.
