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
| 2 | Confermare l'identità owner (nome per la costituzione) | `<OWNER_NAME>` resta placeholder in CLAUDE.md |
| 3 | Ratificare o respingere il set esteso di evidence label proposto in `01_SYSTEM/OPERATING_RULES.md §3` | Conflitto con il set costituzionale §0.4 (non adottato finché non ratificato) |

## 3 · Prossime azioni (per impatto)

| # | Azione | Chi | Min | Scadenza/blocco |
|---|---|---|---|---|
| 1 | Scegliere il percorso dati (A o B) e dare il GO | 👤 owner | ~10 | blocca la fase Data |
| 2 | Fornire il nome owner | 👤 owner | ~1 | sblocca `<OWNER_NAME>` |

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
