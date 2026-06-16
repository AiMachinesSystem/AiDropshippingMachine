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
| Progetto: store eBay/AutoDS | System initialization completa → gate **Data Collection** (richiede GO owner) |

## 2 · Decisioni owner pendenti

| # | Decisione | Perché blocca |
|---|---|---|
| 1 | Scegliere il percorso dati: (A) export/screenshot owner oppure (B) ricerca pubblica esterna | Blocca l'intero flusso Data → Analysis → Strategy |

> **Risolte 2026-06-15 (governance closeout):** identità owner = **Luca**; etichette evidenza = **solo set costituzionale §0.4** (il superset di `OPERATING_RULES §3` resta in **quarantena**, NON ratificato); compilazione `VISION_ALIGNMENT` **rinviata** per scelta owner.

## 3 · Prossime azioni (per impatto)

| # | Azione | Chi | Min | Scadenza/blocco |
|---|---|---|---|---|
| 1 | Scegliere il percorso dati (A o B) e dare il GO | 👤 owner | ~10 | blocca la fase Data |

Lista completa e priorità: ![[BACKLOG.base#Aperti per priorità]]

## 4 · Ultimi run con verdetto

| Data | Run | Verdetto |
|---|---|---|
| 2026-06-15 | Import foundation eBay/AutoDS | Foundation importata e integrata; 0 azioni live; gate Data Collection in attesa di GO |

Memoria interrogabile di tutti i run: [[RESEARCH_MEMORY_INDEX]] (QUERY MODE).

## 5 · KPI vault

| KPI | Valore |
|---|---|
| Report datati in 10_OUTPUTS | 1 (initialization foundation report) |
| Note attive nel vault | n/d (non conteggiate) |
| % vision realizzata | n/d (vision non compilata) |
| Azioni live mai eseguite | 0 |

## 6 · Bases live

- 📊 Tutti i report: ![[REPORTS.base#Tutti i report]]
- ⏳ Decisioni: ![[DECISIONS.base#Pendenti owner]]
