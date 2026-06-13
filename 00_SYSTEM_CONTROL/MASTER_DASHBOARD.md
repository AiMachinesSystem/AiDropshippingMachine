---
tags:
  - machine
type: hub
status: template
description: "Cockpit unico della macchina: stato, decisioni owner pendenti, top azioni con minuti, ultimi run con verdetti, KPI vault, Bases live. Refreshato a ogni fine run."
---

# Master Dashboard — COCKPIT

> Sala di controllo unica. Aggiornata a ogni fine run (regola AUTO-REFRESH).
> PARTE VUOTA in una nuova macchina: si popola coi primi run.

## 1 · Stato macchina

| Voce | Stato |
|---|---|
| Costruzione | `<in corso / chiusa>` |
| Vision (criterio dichiarato) | `<%>` — [[VISION_GAP_MATRIX]] |
| Skill di business | `<n installate>` — [[MACHINE_STATE]] |
| Integrazioni | `<connettori / MCP>` |
| `<PROJECT_A>` | `<fase>` |
| `<PROJECT_B>` | `<fase>` |

## 2 · Decisioni owner pendenti

| # | Decisione | Perché blocca |
|---|---|---|
| 1 | `<decisione>` | `<perché>` |

## 3 · Prossime azioni (per impatto)

| # | Azione | Chi | Min | Scadenza/blocco |
|---|---|---|---|---|
| 1 | `<azione>` | 👤 owner / 🤖 macchina | `<min>` | `<scadenza/blocco>` |

Lista completa e priorità: ![[BACKLOG.base#Aperti per priorità]]

## 4 · Ultimi run con verdetto

| Data | Run | Verdetto |
|---|---|---|
| `<YYYY-MM-DD>` | `<run>` | `<verdetto>` |

Memoria interrogabile di tutti i run: [[RESEARCH_MEMORY_INDEX]] (QUERY MODE).

## 5 · KPI vault

| KPI | Valore |
|---|---|
| Report datati in 10_OUTPUTS | `<n>` |
| Note attive nel vault | `<n>` |
| % vision realizzata | `<%>` |
| Azioni live mai eseguite | `<n>` |

## 6 · Bases live

- 📊 Tutti i report: ![[REPORTS.base#Tutti i report]]
- ⏳ Decisioni: ![[DECISIONS.base#Pendenti owner]]
