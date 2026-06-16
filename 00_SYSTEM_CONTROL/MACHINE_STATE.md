---
tags:
  - machine
type: log
status: template
description: "Stato sintetico della macchina: skill installate con versioni, strumenti locali, integrazioni, fase dei progetti, indici e routine. Fonte di verità per /daily-brief. PARTE VUOTO (solo genealogia) in una nuova macchina."
---

# MACHINE_STATE — stato sintetico della macchina

> **GENEALOGIA (origine tecnica, NON identità):** template `machine-template` estratto da una macchina
> di intelligence & execution in data 2026-06-12 (commit `af792f0`), post CLOSEOUT + AUTONOMIA v0.1 +
> TOOLSMITH + SESSION_START. **Istanziata come `eBay / AutoDS Dropshipping Machine` il 2026-06-15**
> tramite import della foundation in `_IMPORT/ebay_autods_initialization/`. Questa riga dichiara solo la
> provenienza dello scheletro: la macchina NON eredita dati, progetti, output o decisioni della sorgente.
>
> Aggiornare a ogni cambiamento di skill, integrazione o fase progetto. Fonte di verità per `/daily-brief`.

## SKILL DI BUSINESS INSTALLATE (in `~\.claude\skills\` o in `.claude\skills\` del repo)
| Skill | Versione | Ruolo |
|---|---|---|
| niche-intelligence-run | `<vN>` | validazione nicchia + censimento |
| competitor-scan | `<vN>` | teardown competitor + scoring |
| ads-library-scan | `<vN>` | motore dati Ad Library (proxy r.jina.ai; cache evidenze; known walls) |
| launch-prep | `<vN>` | launch pack GATED (gate zero = provenienza/diritti) |
| vault-librarian | `<vN>` | manutenzione conservativa vault/indici |
| vision-check | `<vN>` | check di allineamento costituzione/vision |
| creative-brief-builder | `<vN>` | brief creativi data-driven |
| higgsfield-prompt-builder | `<vN>` | prompt generazione (GO per crediti) |
| test-plan-builder | `<vN>` | piani test con metriche pre-spesa |
| landing-page-review | `<vN>` | audit landing pubblica, rubrica 1-5, integrity flags |
| offer-diagnosis | `<vN>` | diagnosi offerta vs CANONE CORRENTE |
| weekly-learning-update | `<vN>` | sintesi settimanale: delta indici, muri ri-testabili, drift |
| customer-voice-mining | `<vN>` | voce cliente da fonti PUBBLICHE; dati owner = classe B GO-gated |
| portfolio-review | `v0.1-STUB` | STUB dichiarato: si attiva con ≥2 progetti live + connettori dati |
Commands: /niche-run · /competitor-scan · /ads-scan · /launch-prep · /daily-brief.

> **Skill esterne (dipendenza personale/globale, NON parte del template):** eventuali skill
> di terze parti installate in `~\.claude\skills` (es. set Obsidian) si installano per macchina
> e si annotano qui — non vengono ereditate dal template.

## STRUMENTI LOCALI
- `<es. Playwright + Chromium headless>` — screenshot evidenza in `90_CACHE\screenshots\`; vedi playbook.
- `<es. n8n>` — stato install (playbook + workflow JSON in PLAYBOOKS).
- Cache evidenze: `90_CACHE\fetches\` (non versionata).
- Costituzione operativa: `CLAUDE.md` · convenzioni: `VAULT_CONVENTIONS.md` · vision: `VISION_SCHEMA.md` + `VISION_GAP_MATRIX.md`.

## INTEGRAZIONI
- Connettori/MCP dati: nessuno collegato. Nessun accesso a eBay, AutoDS o fornitori. Solo lettura di pagine pubbliche (via proxy) finché non c'è GO per write-action.
- Metodo web validato: pagine bloccate leggibili via prefisso `https://r.jina.ai/` (lower bound, retry ≤2).

## PROGETTI E FASE
| Progetto | Fase | Note |
|---|---|---|
| store eBay/AutoDS (US seller → US buyers, eBay.com, USD) | Analisi policy/fee/feature completa → gate **Analysis → Strategy (CHIUSO)** | seller = US-registrato + US-located (USER-PROVIDED); Italy/EU non rilevante; GO owner per Strategy + dati economici; firewall attivo; execution in `05_EXECUTION\ebay-autods-store\` (da creare) |

## INDICI E ROUTINE
- `00_SYSTEM_CONTROL\RESEARCH_MEMORY_INDEX.md` = memoria interrogabile dei run (QUERY MODE).
- `02_DATA\_ROUTINES\MASTER_ROUTINE.md` = dispatcher owner.
- Convenzione output: `10_OUTPUTS\<TIPO>\YYYY-MM-DD_<slug>_<tipo>_vN.md`.
