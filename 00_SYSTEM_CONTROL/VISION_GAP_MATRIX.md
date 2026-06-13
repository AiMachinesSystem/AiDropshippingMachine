---
tags:
  - machine
type: playbook
status: template
---

# VISION GAP MATRIX — stato vs VISION_SCHEMA (template v1)

> Stato di ogni componente dello schema vs realtà. Stati verificati [OBSERVED — check locale].
> Classi: **A** = fattibile ora in locale senza owner · **B** = serve account/credenziale/OAuth
> owner · **C** = serve decisione owner · **D** = futuro/dipendente.
>
> **CRITERIO DI PUNTEGGIO (invariato, mai gonfiare):** FATTO = 1 · PARZIALE = 0,5 · ASSENTE = 0.
> Il progresso vision si misura SOLO con questo criterio; il progresso sotto-riga si dichiara a
> parte, senza numeri inventati. PARTE VUOTA: compila una riga per componente dello schema.

| Componente (schema) | Stato | Cosa manca esattamente | Classe | Effort | Rischio | Dipendenze |
|---|---|---|---|---|---|---|
| Claude Code (motore) | `<FATTO/PARZIALE/ASSENTE>` | `<...>` | — | — | — | — |
| Obsidian vault (memoria) | `<...>` | `<...>` | A | — | — | — |
| Git locale | `<...>` | `<...>` | — | — | — | — |
| GitHub remoto | `<...>` | `<...>` | B | — | — | account owner |
| Password manager | `<...>` | `<...>` | C | — | — | — |
| Graph/semantica | `<...>` | `<...>` | C | — | — | — |
| MCP layer | `<...>` | `<...>` | B | — | — | OAuth owner |
| Automazioni (n8n) | `<...>` | `<...>` | C | — | — | node |
| Fonti dati interne `<DATA_SOURCES>` | `<...>` | `<...>` | B | — | — | OAuth owner |
| Intelligence esterna (scraping/browser) | `<...>` | `<...>` | A/B | — | — | — |
| Produzione creativa | `<...>` | `<...>` | A/B | — | — | — |
| Misurazione/dashboard | `<...>` | `<...>` | B/D | — | — | dati puliti |
| GO Gate | `<...>` | codificato in CLAUDE.md | A | — | — | — |
| Skill custom §7 | `<n/m>` | `<quali mancano>` | A/B | — | — | — |
| Struttura output §8 | `<...>` | `<...>` | A | — | — | — |
| Cache fetch / audit trail | `<...>` | `<...>` | A | — | — | — |
| QC avanzato (Layer 10) | ASSENTE | dichiarato FUTURO dallo schema | D | — | — | processi stabili |

## PUNTEGGIO CORRENTE
`<somma>/<righe>` = `<%>` (criterio dichiarato: FATTO=1 / PARZIALE=0,5 / ASSENTE=0).
