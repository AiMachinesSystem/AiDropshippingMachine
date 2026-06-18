---
tags:
  - machine
type: hub
status: active
description: "Cockpit unico della macchina: stato, decisioni owner pendenti, top azioni con minuti, ultimi run con verdetti, KPI vault, Bases live. Refreshato a ogni fine run. Popolato 2026-06-15 (post-import foundation eBay/AutoDS)."
---

# Master Dashboard — COCKPIT

> Sala di controllo unica. Aggiornata a ogni fine run (regola AUTO-REFRESH).
> Dettaglio stato/gate: [[CURRENT_STATUS]] · prossime azioni: [[NEXT_ACTIONS]].

## 1 · Stato macchina

| Voce | Stato |
|---|---|
| Costruzione | iniziata — foundation eBay/AutoDS importata e integrata (2026-06-15) |
| Vision (criterio dichiarato) | n/d — `VISION_ALIGNMENT`/`VISION_GAP_MATRIX` non ancora compilate dall'owner |
| Skill di business | 14 (toolkit del template, non specifiche eBay) — [[MACHINE_STATE]] |
| Integrazioni | **AutoDS read-only via Playwright OPERATIVO** (sessione salvata, 2026-06-16): letti store/catalogo/ordini/settings. API REST AutoDS = a pagamento/gated (no key). n8n = solo blueprint. **Zero scritture live.** |
| Progetto: store eBay/AutoDS (**US seller → US buyers**, eBay.com, USD) | **2026-06-17: rimossi 37 listing OOS morti (AutoDS+eBay) → 177 attivi** (tenuti 13 venditori + 5 OOS-winner da ristoccare + margine-bassi). **Trial NON rinnovato (owner) → scade 18/06, monitoraggio cessa.** Import 3 nuovi SKU in **HOLD** (conflitto: non si importa in account che scade). |

## 2 · Decisioni owner pendenti

| # | Decisione | Perché blocca |
|---|---|---|
| 1 | **Trial AutoDS NON rinnovato (owner 2026-06-17) → scade 18/06.** Decidere: wind-down AutoDS / gestione eBay manuale / altro tool | i 177 restano senza stock-price sync dal 18/06 (rischio oversell) |
| 2 | **Conflitto da sciogliere:** import 3 nuovi SKU mid-ticket in un account che scade domani = inutile/rischioso; + sourcing Amazon = rischio policy. Decidere se/come | blocca l'import dei nuovi prodotti |

> **Risolte 2026-06-15 (governance closeout):** identità owner = **Luca**; etichette evidenza = **solo set costituzionale §0.4** (il superset di `OPERATING_RULES §3` resta in **quarantena**, NON ratificato); compilazione `VISION_ALIGNMENT` **rinviata** per scelta owner.
> **Risolte 2026-06-15 (owner context):** buyer = **US / eBay.com** (USD), secondario NESSUNO; **seller = US-registrato + US-located**; Italy/EU **NON rilevante**. Lo schema eBay.com/US è ora il riferimento **vincolante**.

## 3 · Prossime azioni (per impatto)

| # | Azione | Chi | Min | Scadenza/blocco |
|---|---|---|---|---|
| 1 | Decidere **rinnovo trial AutoDS** (piano minimo) o lasciar scadere | 👤 owner | ~10 | **entro 2026-06-18** |
| 2 | Dare GO al **fix VeRO + tally salute dei 214 listing** (read-only tally = senza GO; fix/rimozioni = GO) | 👤 owner | ~10 | protegge account |
| 3 | Approvare il **test 3 SKU alto-margine** (phone tether · torso anatomico · duck topper) — import = `GO_IMPORT_5_DRAFTS` | 👤 owner | ~10 | dopo decisione strategica |

Lista completa e priorità: ![[BACKLOG.base#Aperti per priorità]]

## 4 · Ultimi run con verdetto

| Data | Run | Verdetto |
|---|---|---|
| 2026-06-17 | **Import 3 nuovi draft + titolo≤80 + descrizione VeRO-safe** (GO owner) | Playwright riattivato; ricercati 3 prodotti generici (slow feeder bowl, coffee pod holder, neck fan) con URL Amazon live; draft 16→**19**; titoli 80/79/79 applicati e persistiti; **descrizioni applicate via CKEditor API (muro caduto)** e persistite; 0 publish. |
| 2026-06-17 | **Rimozione 37 listing OOS morti** (GO owner) | 214→**177** attivi; chiusi anche su eBay ("AutoDS+Selling Platform"); 13 venditori + 5 OOS-winner protetti; verificato. Trial non rinnovato. |
| 2026-06-17 | Listing audit + mid-ticket research + strategy update | lista azioni per-listing; top 3 mid-ticket; downgrade torso |
| 2026-06-16 | Decisione strategica autonoma (7gg) | Verdetto su prodotto/trial/sequenza/fix; piano prioritizzato GO vs no-GO → `04_STRATEGY/STRATEGIC_DECISION_2026-06-16.md` |
| 2026-06-16 | Deep Product Research (funnel multi-tool) | 7 trend → 24 nicchie → 121 prodotti AutoDS → 20 cross-check eBay; TOP 15 + 5 schede; muri eBay/AutoDS dichiarati [UNKNOWN] |
| 2026-06-16 | Capability audit (read-only, 7 agenti) | Governance/memoria/analisi + AutoDS read-only PROVATE; motore vendite 0% operativo; ~60% reale/40% scaffold |
| 2026-06-16 | AutoDS read-only via Playwright (login + status + counts) | Sessione salvata; letti 214 listing/11 draft/23 ordini; auto-order ON ma non operativo; trial scade 2026-06-18; 0 scritture |
| 2026-06-16 | Playwright integration scaffold + smoke test | Browser headless funziona (HTTP 200 su platform.autods.com); venv isolato; safety contract read-only |
| 2026-06-15 | Import foundation eBay/AutoDS | Foundation importata e integrata; 0 azioni live; gate Data Collection in attesa di GO |
| 2026-06-15 | Ricerca pubblica policy/fee/feature (eBay+AutoDS) | 21 fonti in cache; 6 output dati + intake report; 0 azioni live; stop prima dell'analisi |
| 2026-06-15 | Analisi policy/fee/feature (eBay+AutoDS) | Mappe constraint/fee/risk/account-health/dependency evidence-graded; buyer vs seller-country split; niente strategia/raccomandazioni; verifica adversarial PASS; gate Analysis→Strategy chiuso |
| 2026-06-15 | Contesto seller (USER-PROVIDED) | seller US-registrato + US-located, USD; Italy/EU non rilevante; dependency principale dell'analisi risolta; Strategy ancora bloccata |
| 2026-06-15 | AutoDS Read-Only Data Intake Plan | piano (categorie/cattura/storage/forbidden/checklist/prereq) + report; 0 accessi/login/dati; intake non avviato |

Memoria interrogabile di tutti i run: [[RESEARCH_MEMORY_INDEX]] (QUERY MODE).

## 5 · KPI vault

| KPI | Valore |
|---|---|
| Report datati in 10_OUTPUTS / analysis | 9 (init · stabilization · data-collection · analysis · autods-intake-plan · autods-status · capability-audit · deep-product-research · strategic-decision) |
| Note attive nel vault | n/d (non conteggiate) |
| % vision realizzata | n/d (vision non compilata) |
| Scritture live eseguite | **0** (import/publish/prezzi/ordini mai fatti) · letture read-only AutoDS via Playwright = eseguite 2026-06-16 |

## 6 · Bases live

- 📊 Tutti i report: ![[REPORTS.base#Tutti i report]]
- ⏳ Decisioni: ![[DECISIONS.base#Pendenti owner]]
