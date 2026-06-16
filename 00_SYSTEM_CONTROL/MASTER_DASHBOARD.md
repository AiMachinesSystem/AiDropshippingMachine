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
| Progetto: store eBay/AutoDS (buyer market: **US / eBay.com**, USD) | Analisi policy/fee/feature completa → gate **Analysis → Strategy (CHIUSO)** (Strategy richiede GO owner + paese seller + dati economici) |

## 2 · Decisioni owner pendenti

| # | Decisione | Perché blocca |
|---|---|---|
| 1 | GO alla **Strategy** — solo dopo aver colmato i blocker (paese seller + dati fornitori/economici) | Blocca tutto il flusso a valle |
| 2 | Fornire il **paese di registrazione del seller** (NON assumere USA) | Determina lo schema fee/tax/payment vincolante; i numeri US/eBay.com sono il riferimento buyer, non confermati lato seller |

> **Risolte 2026-06-15 (governance closeout):** identità owner = **Luca**; etichette evidenza = **solo set costituzionale §0.4** (il superset di `OPERATING_RULES §3` resta in **quarantena**, NON ratificato); compilazione `VISION_ALIGNMENT` **rinviata** per scelta owner.
> **Risolte 2026-06-15 (owner context):** buyer market/marketplace = **US / eBay.com** (USD); secondario = NESSUNO. Resta aperto: **paese/posizione del seller** (USER INPUT NEEDED — niente assunzione "seller USA").

## 3 · Prossime azioni (per impatto)

| # | Azione | Chi | Min | Scadenza/blocco |
|---|---|---|---|---|
| 1 | Decidere il prossimo gate: GO Strategy (dopo blocker) o approvare raccolta dati fornitori/economics | 👤 owner | ~5 | blocca la fase Strategy |
| 2 | Fornire il paese di registrazione del seller | 👤 owner | ~1 | sblocca lo schema fee/tax seller-side |

Lista completa e priorità: ![[BACKLOG.base#Aperti per priorità]]

## 4 · Ultimi run con verdetto

| Data | Run | Verdetto |
|---|---|---|
| 2026-06-15 | Import foundation eBay/AutoDS | Foundation importata e integrata; 0 azioni live; gate Data Collection in attesa di GO |
| 2026-06-15 | Ricerca pubblica policy/fee/feature (eBay+AutoDS) | 21 fonti in cache; 6 output dati + intake report; 0 azioni live; stop prima dell'analisi |
| 2026-06-15 | Analisi policy/fee/feature (eBay+AutoDS) | Mappe constraint/fee/risk/account-health/dependency evidence-graded; buyer vs seller-country split; niente strategia/raccomandazioni; verifica adversarial PASS; gate Analysis→Strategy chiuso |

Memoria interrogabile di tutti i run: [[RESEARCH_MEMORY_INDEX]] (QUERY MODE).

## 5 · KPI vault

| KPI | Valore |
|---|---|
| Report datati in 10_OUTPUTS | 4 (init · stabilization · data-collection · analysis) |
| Note attive nel vault | n/d (non conteggiate) |
| % vision realizzata | n/d (vision non compilata) |
| Azioni live mai eseguite | 0 |

## 6 · Bases live

- 📊 Tutti i report: ![[REPORTS.base#Tutti i report]]
- ⏳ Decisioni: ![[DECISIONS.base#Pendenti owner]]
