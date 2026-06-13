---
tags:
  - machine
type: hub
status: template
description: "Memoria interrogabile di tutti i run di ricerca. Ogni run di niche-validation, competitor-analysis e ads-scan si registra qui a fine corsa (skill rule). PARTE VUOTO (solo schema) in una nuova macchina."
---

# RESEARCH_MEMORY_INDEX

> Queryable memory of all market-research runs. Every niche-validation,
> competitor-analysis, and ads-scan run MUST register here at close-out
> (skill rule — a run without registration is INCOMPLETE).
> QUERY MODE answers come from this file + the linked reports.
> Re-run only on explicit owner request or stale data (>30 days).
>
> **REGOLA NUMERI CANONICI:** più run sulla stessa nicchia → vince SEMPRE
> l'ultimo registrato. Il blocco nicchia con più run DEVE avere un'unica
> sezione `### CANONE CORRENTE` in testa (QUERY MODE legge SOLO quella) e i
> numeri superati sotto `### STORICO (superato da ...)`. Vietato lasciare
> numeri vecchi in campi schema (`census:`, `leader:`, `key numbers:`) fuori
> dallo STORICO.

## ENTRY SCHEMA (one block per niche — copy this template)

### `<NICHE LABEL>`

#### CANONE CORRENTE (run `<YYYY-MM-DD>`, `<type vN>` — QUERY MODE risponde SOLO da questa sezione)
- last_run: `<YYYY-MM-DD>` · type: `<niche-validation|competitor-analysis|ads-scan>` vN · file: `<path>`
- market: `<PROVEN|UNPROVEN|UNKNOWN>` · space: `<YES|TIGHT|NO>` (`<gap>`) · confidence: `<HIGH|MED|LOW>`
- census: `<N>` active advertisers · T1=`<n>` · T2=`<n>` · T3=`<n>` · leader: `<name>`
- top ad patterns: `<comma list>`
- key numbers: `<prices, longevities, counts worth remembering>`
- open items: `<owner-manual checks, unknowns>`
- integrity flags: `<anti-patterns observed in the market — never replicate>`

#### STORICO (superato da ...)
<!-- run precedenti dello stesso blocco, mai citabili come correnti -->

---

<!-- Nessun run registrato. Il primo blocco nicchia reale va sopra questa riga. -->
