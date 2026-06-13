---
tags:
  - machine
type: log
status: template
description: "Stato sintetico della macchina: skill installate con versioni, strumenti locali, integrazioni, fase dei progetti, indici e routine. Fonte di verità per /daily-brief. PARTE VUOTO (solo genealogia) in una nuova macchina."
---

# MACHINE_STATE — stato sintetico della macchina

> **GENEALOGIA (origine tecnica, NON identità):** template estratto da una macchina di
> intelligence & execution in data `<DATA_ESTRAZIONE>`, post CLOSEOUT + AUTONOMIA v0.1 +
> TOOLSMITH + SESSION_START. Questa riga dichiara solo la provenienza dello scheletro: la
> nuova macchina NON è la macchina sorgente e non ne eredita dati, progetti, output o decisioni.
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
- `<connettore dati / MCP>`: `<stato>`. Solo lettura finché non c'è GO per write-action.
- Metodo web validato: pagine bloccate leggibili via prefisso `https://r.jina.ai/` (lower bound, retry ≤2).

## PROGETTI E FASE
| Progetto | Fase | Note |
|---|---|---|
| `<PROJECT_A>` | `<fase>` | `<firewall/gate se applicabile>` |
| `<PROJECT_B>` | `<fase>` | `<note>` |

## INDICI E ROUTINE
- `00_SYSTEM_CONTROL\RESEARCH_MEMORY_INDEX.md` = memoria interrogabile dei run (QUERY MODE).
- `02_DATA\_ROUTINES\MASTER_ROUTINE.md` = dispatcher owner.
- Convenzione output: `10_OUTPUTS\<TIPO>\YYYY-MM-DD_<slug>_<tipo>_vN.md`.
