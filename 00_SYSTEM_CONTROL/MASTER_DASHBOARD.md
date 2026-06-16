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
| Integrazioni | nessuna — nessun connettore, nessun accesso account (eBay/AutoDS/fornitori) |
| Progetto: store eBay/AutoDS (**US seller → US buyers**, eBay.com, USD) | Analisi completa + seller context risolto → gate **Analysis → Strategy (CHIUSO)** (Strategy richiede GO owner + dati economici) |

## 2 · Decisioni owner pendenti

| # | Decisione | Perché blocca |
|---|---|---|
| 1 | GO alla **Strategy** — solo dopo i dati fornitori/economici | Blocca tutto il flusso a valle |
| 2 | Scegliere il prossimo step: **avviare l'intake AutoDS** (prereq + GO) o **Analysis Delta** | Determina cosa fa la macchina dopo il piano AutoDS |

> **Risolte 2026-06-15 (governance closeout):** identità owner = **Luca**; etichette evidenza = **solo set costituzionale §0.4** (il superset di `OPERATING_RULES §3` resta in **quarantena**, NON ratificato); compilazione `VISION_ALIGNMENT` **rinviata** per scelta owner.
> **Risolte 2026-06-15 (owner context):** buyer = **US / eBay.com** (USD), secondario NESSUNO; **seller = US-registrato + US-located**; Italy/EU **NON rilevante**. Lo schema eBay.com/US è ora il riferimento **vincolante**.

## 3 · Prossime azioni (per impatto)

| # | Azione | Chi | Min | Scadenza/blocco |
|---|---|---|---|---|
| 1 | Fornire prerequisiti AutoDS + GO per avviare l'intake read-only, oppure scegliere Analysis Delta | 👤 owner | ~5 | determina la fase successiva |

Lista completa e priorità: ![[BACKLOG.base#Aperti per priorità]]

## 4 · Ultimi run con verdetto

| Data | Run | Verdetto |
|---|---|---|
| 2026-06-15 | Import foundation eBay/AutoDS | Foundation importata e integrata; 0 azioni live; gate Data Collection in attesa di GO |
| 2026-06-15 | Ricerca pubblica policy/fee/feature (eBay+AutoDS) | 21 fonti in cache; 6 output dati + intake report; 0 azioni live; stop prima dell'analisi |
| 2026-06-15 | Analisi policy/fee/feature (eBay+AutoDS) | Mappe constraint/fee/risk/account-health/dependency evidence-graded; buyer vs seller-country split; niente strategia/raccomandazioni; verifica adversarial PASS; gate Analysis→Strategy chiuso |
| 2026-06-15 | Contesto seller (USER-PROVIDED) | seller US-registrato + US-located, USD; Italy/EU non rilevante; dependency principale dell'analisi risolta; Strategy ancora bloccata |
| 2026-06-15 | AutoDS Read-Only Data Intake Plan | piano (categorie/cattura/storage/forbidden/checklist/prereq) + report; 0 accessi/login/dati; intake non avviato |

Memoria interrogabile di tutti i run: [[RESEARCH_MEMORY_INDEX]] (QUERY MODE).

## 5 · KPI vault

| KPI | Valore |
|---|---|
| Report datati in 10_OUTPUTS | 5 (init · stabilization · data-collection · analysis · autods-intake-plan) |
| Note attive nel vault | n/d (non conteggiate) |
| % vision realizzata | n/d (vision non compilata) |
| Azioni live mai eseguite | 0 |

## 6 · Bases live

- 📊 Tutti i report: ![[REPORTS.base#Tutti i report]]
- ⏳ Decisioni: ![[DECISIONS.base#Pendenti owner]]
