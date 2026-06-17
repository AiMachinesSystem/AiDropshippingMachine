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
| Progetto: store eBay/AutoDS (**US seller → US buyers**, eBay.com, USD) | Account live letto (**214 listing attivi, 11 draft, 23 ordini, $62 profitto/7gg**). **Deep product research + decisione strategica prodotte (2026-06-16).** Execution live ancora **gated** (import/publish/prezzi/auto-order = GO chiusi). |

## 2 · Decisioni owner pendenti

| # | Decisione | Perché blocca |
|---|---|---|
| 1 | **Rinnovo trial AutoDS — scade 2026-06-18** (GO/spesa): senza rinnovo i 214 listing perdono il monitoraggio stock/prezzo | ⏰ urgente (2 gg); rischio salute account eBay (oversell/OOS) |
| 2 | GO alle azioni di execution della **decisione strategica** (`04_STRATEGY/STRATEGIC_DECISION_2026-06-16.md`): fix VeRO/OOS, prune/reprice catalogo, test SKU alto-margine | sblocca le mosse a 7 giorni |

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
