---
tags:
  - machine
type: hub
status: active
---

# eBay / AutoDS Dropshipping Machine — Project Index

Mappa di navigazione della macchina (istanziata dal template `machine-template` il 2026-06-15).

## Governo
- [[CLAUDE]] — costituzione operativa sovrana (regole permanenti §0 + autonomia controllata).
- [[README]] — overview di dominio della macchina.
- [[00_SYSTEM_CONTROL/VISION_ALIGNMENT|VISION_ALIGNMENT]] — costituzione owner (vision, North Star, asset map) — *da compilare dall'owner*.
- [[00_SYSTEM_CONTROL/MASTER_DASHBOARD|MASTER_DASHBOARD]] — cockpit · [[00_SYSTEM_CONTROL/CURRENT_STATUS|CURRENT_STATUS]] — stato/gate dettaglio.
- [[00_SYSTEM_CONTROL/MACHINE_STATE|MACHINE_STATE]] · [[00_SYSTEM_CONTROL/BACKLOG|BACKLOG]] · [[00_SYSTEM_CONTROL/NEXT_ACTIONS|NEXT_ACTIONS]] · [[00_SYSTEM_CONTROL/MODULE_INDEX|MODULE_INDEX]].
- [[00_SYSTEM_CONTROL/APPROVAL_GATES|APPROVAL_GATES]] · [[00_SYSTEM_CONTROL/ACTION_LOG|ACTION_LOG]] · [[00_SYSTEM_CONTROL/DECISION_LOG|DECISION_LOG]] · [[00_SYSTEM_CONTROL/RESEARCH_MEMORY_INDEX|RESEARCH_MEMORY_INDEX]] (QUERY MODE).
- [[01_SYSTEM/SYSTEM_BLUEPRINT|SYSTEM_BLUEPRINT]] · [[01_SYSTEM/OPERATING_RULES|OPERATING_RULES]] — blueprint e regole di dominio (subordinate a CLAUDE.md).

## Moduli (alberatura)
| Cartella | Scopo | File chiave |
|---|---|---|
| `00_SYSTEM_CONTROL` | governo, stato, gate, log, indici | MODULE_INDEX, CURRENT_STATUS, APPROVAL_GATES |
| `01_SYSTEM` | blueprint, regole, responsabilità, confini di rischio | SYSTEM_BLUEPRINT, OPERATING_RULES |
| `02_DATA` | source plan, raw/cleaned data, missing data, routine | DATA_MAP, 00_SOURCE_DISCOVERY/, 03_MISSING_DATA/, _ROUTINES/MASTER_ROUTINE |
| `03_ANALYSIS` | risk map e future analisi (non autorizzate) | RISK_MAP, README |
| `04_STRATEGY` | strategy brief solo dopo autorizzazione | README (gate chiuso) |
| `05_EXECUTION` | gate structure e futuri SOP/task per progetto | EXECUTION_GATE_STRUCTURE |
| `06_MEASUREMENT` | KPI map e futuri report | KPI_MAP |
| `07_LEARNING` | sistema di apprendimento e future entry | LEARNING_SYSTEM |
| `08_SCALING` | scaling gate e future decisioni | SCALING_GATE |
| `09_TEMPLATES` | template di output riutilizzabili (sterili, invariati) | TEMPLATE_INDEX |
| `10_OUTPUTS` | output datati (`<TIPO>/YYYY-MM-DD_...`) | SYSTEM_REPORTS/ (initialization report) |
| `90_CACHE` | evidenze/screenshot (non versionata) | — |
| `99_ARCHIVE` / `_ARCHIVE` | baseline sterili e milestone (nessuna cancellazione) | STERILE_BASELINE__* |

## Progetti
- `store eBay/AutoDS` — `05_EXECUTION\ebay-autods-store\` (da creare al gate Execution) — fase: System init completa → gate **Data Collection**.

## Toolkit
- Skill e command in `.claude\` (vedi `.claude\skills\README.md`). Configurazione dei placeholder del toolkit: step separato, GO owner.
