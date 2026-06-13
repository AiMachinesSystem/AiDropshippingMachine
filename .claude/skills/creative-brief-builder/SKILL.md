---
name: creative-brief-builder
description: Build a data-driven creative brief for an ad/asset test from registered research (hooks, angles, proof constraints, format, naming, test hypothesis). Use when the owner asks for a creative brief, ad concepts, "prepara le creative", "brief per le ads", or as the step before higgsfield-prompt-builder. Drafting only — no spend, no publishing; every claim in copy must carry substantiation.
---

# Creative Brief Builder

**v1.0 (2026-06-13).** Trasforma ricerca registrata in brief eseguibili.

## INPUTS (obbligatori, in quest'ordine)
1. Blocco nicchia in `RESEARCH_MEMORY_INDEX.md` (numeri canonici = ultimo run).
2. Pattern ads del run più recente (hook che girano, longevità, duplication).
3. Lista claim SAFE/UNSAFE del progetto (gate claim attivo del progetto
   `<PROJECT_NAME>`; per brand nuovi: solo claim con base verificabile).
Manca 1 o 3 → STOP: chiedi il run mancante o la decisione claim all'owner.

## BRIEF (uno per concept; 3-5 concept per test tipico)
- **Hypothesis** — cosa deve provare questo creativo (1 riga, falsificabile).
- **Hook family + hook** — dal pattern run (cita la fonte: advertiser/ID che
  lo prova) o dichiarato NEW-UNTESTED.
- **Angle** — pain / dream / proof / value / trust-differentiation.
- **Copy draft** — primary text, headline, CTA; OGNI claim con fonte di
  sostanziazione tra parentesi; claim senza base = NON SI SCRIVE.
- **Visual direction** — scena, soggetto, stile, formato (4:5/9:16/1:1),
  primi 3 secondi (per video).
- **Proof element** — SOLO prove reali disponibili (review vera, build
  gallery, garanzia). Mai contatori inventati, mai foto staged/AI come
  "clienti" (anti-pattern documentato del mercato).
- **Naming** — `<niche>_<concept>_<angle>_<format>_<vN>` (per il tracking).
- **Measurement** — metrica primaria + soglia di successo definita PRIMA.

## OUTPUT
File in `10_OUTPUTS\CREATIVE_BRIEFS\YYYY-MM-DD_<niche>_CREATIVE_BRIEF_vN.md`
+ registrazione riga nel blocco nicchia dell'indice. Lancio/spesa = GO owner.
