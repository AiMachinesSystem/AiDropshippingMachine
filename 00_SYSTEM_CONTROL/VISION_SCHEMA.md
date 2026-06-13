---
tags:
  - machine
type: playbook
status: template
---

# `<MACHINE_NAME>` — REQUIRED STACK SCHEMA (template v1)

**Purpose:** definire esattamente cosa serve per ottenere la macchina descritta in `VISION_ALIGNMENT.md`.
**Core principle:** Claude Code resta il motore principale. Tutto il resto serve a dargli memoria, dati, sicurezza, connessioni, automazioni, creatività, misurazione e apprendimento.

> **TEMPLATE STERILE.** Sostituisci `<DATA_SOURCES>`, i nomi degli strumenti e le priorità con
> lo stack reale della tua macchina. Lo schema sotto è AI-agnostic e tool-agnostic: i tool nominati
> sono ESEMPI di categoria, non vincoli.

## 0. VERDETTO

La macchina non si ottiene con una sola app. Configurazione tipica:

> **Claude Code = cervello operativo** · **Obsidian = memoria ufficiale** · **Git/GitHub = sicurezza e rollback** ·
> **Graph plugin = mappa semantica** · **MCP + automazioni = connessione** · **`<DATA_SOURCES>` = fonti dati** ·
> **scraping/browser = intelligence esterna** · **tool creativi = produzione** · **sheets/dashboard = misurazione** ·
> **GO Gate = freno umano obbligatorio per ogni azione live**

## 1. LAYER DELLA MACCHINA (schema generale)

| Layer | Ruolo | Necessità |
|---|---|---|
| **1 · Motore** | Claude Code + skill/command custom | OBBLIGATORIO |
| **2 · Memoria e stato** | Obsidian vault · VISION_ALIGNMENT · 00_SYSTEM_CONTROL · 02→08 moduli · 10_OUTPUTS | OBBLIGATORIO |
| **3 · Sicurezza/rollback** | Git locale · GitHub remoto · commit discipline · password manager | OBBLIGATORIO |
| **4 · Comprensione semantica** | graph/backlink · tagging/naming standard · module index | UTILE/OBBLIGATORIO |
| **5 · Connessioni controllate** | MCP · automazioni (es. n8n) · OAuth/API token · permission model read-only-first | OBBLIGATORIO per 360° |
| **6 · Dati interni** | `<DATA_SOURCES>` (es. email, drive, sheets, store, ads, analytics) — read-only first | ALTA |
| **7 · Intelligence esterna** | scraping/browser (es. Apify/Playwright) · ads-library process · review mining · SERP | ALTA |
| **8 · Produzione creativa** | tool immagini/video/design (es. Higgsfield/Canva) — sempre con brief data-driven | ALTA |
| **9 · Misurazione** | sheets/dashboard · weekly learning · decision log · KPI map | OBBLIGATORIO |
| **10 · QC avanzato AI** | tracking prompt/output/qualità (es. Langfuse) | FUTURO |

## 2. ORDINE DI IMPLEMENTAZIONE (sintesi)

1. Stabilizzare il cuore (Claude Code + Obsidian puliti, Git/GitHub, password manager, skill/command minimi).
2. Comprensione semantica (graph, naming standard, module index).
3. Connettere fonti interne read-only (`<DATA_SOURCES>`).
4. Intelligence esterna (scraping/browser, ads-library).
5. Produzione creativa data-driven.
6. Dashboard e learning loop.

Ogni fase lascia output in `10_OUTPUTS`; nessun account esterno collegato in scrittura senza GO.

## 3. GO GATE — REGOLE DI SICUREZZA

- **Senza GO (interno):** leggere file vault · analizzare · sintetizzare · raccomandare · generare prompt/draft/report · preparare execution plan · aggiornare file interni autorizzati.
- **Con OWNER GO (live/esterno):** `<LIVE_ACTION_RULES>`.
- **Regola base:** Read-only first · Internal write only when requested · Live write only with OWNER GO.

## 4. OUTPUT STANDARD (§8)

Ogni output sostanziale segue il template in `00_SYSTEM_CONTROL\TEMPLATES\`: Verdict · Confidence · Evidence basis · Dominant pattern · Demand/pain signal · Recommended move · Why · Rejected alternatives · Execution assets · Owner role · Measurement plan · Blockers · Files updated.

## 5. DEFINIZIONE DI "MACCHINA COMPLETA"

Dato un comando come "analizza `<ASSET>` negli ultimi 30 giorni e dimmi cosa fare", la macchina sa: leggere stato + dati interni + customer voice + ads + analytics + competitor; produrre verdict; raccomandare UNA strada; produrre asset pronti; indicare cosa misurare; aggiornare decision log e learning; fermarsi prima di ogni azione live; chiedere OWNER GO solo se serve.
