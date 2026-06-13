---
name: test-plan-builder
description: Build a measurable test plan for an offer/creative/funnel hypothesis — variables, structure, success metrics defined BEFORE spend, kill criteria, measurement sources. Use when the owner asks "piano di test", "come testiamo", "test plan", or after creative briefs exist. Planning only — budgets are placeholders for the owner; any spend or launch is GO-gated.
---

# Test Plan Builder

**v1.0 (2026-06-13).** Ogni test risponde: cosa proviamo, come capiamo se ha
funzionato, quando lo uccidiamo. Metriche PRIMA della spesa, sempre.

## INPUT
Ipotesi da testare + asset/brief disponibili + blocco nicchia dall'indice
(benchmark osservati: hook dominanti, prezzi, longevità competitor).

## STRUTTURA DEL PIANO
1. **Hypothesis** — falsificabile, una per test (es. "il trust-hook regge
   ≥80% del CTR del pain-hook con CVR uguale o migliore").
2. **Variables** — UNA variabile primaria per test (hook O visual O prezzo O
   landing); tutto il resto bloccato. Matrice varianti con naming.
3. **Structure** — campagna/adset/ads (stile duplication-testing osservato
   nel mercato: N copie del vincitore); budget = `[OWNER]` placeholder.
4. **Success metrics** — primaria + guardrail (es. CTR, CPC, CVR, refund
   rate), soglie numeriche DICHIARATE PRIMA; finestra di valutazione.
5. **Kill criteria** — quando si spegne senza appello (spesa X senza segnale
   Y); chi spegne (owner via GO o regola pre-autorizzata — da definire).
6. **Measurement sources** — dove si leggono i numeri (connettori dati
   `<DATA_SOURCES>`: es. Ads Manager, store, analytics) e chi li legge; mai numeri stimati nei report.
7. **Learning capture** — dove finisce l'esito (decision log + learning
   file + blocco indice).

## OUTPUT
`10_OUTPUTS\TEST_PLANS\YYYY-MM-DD_<niche>_TEST_PLAN_vN.md` + riga indice.
Lancio, spesa, modifiche campagne = GO owner per-azione, mai impliciti.
