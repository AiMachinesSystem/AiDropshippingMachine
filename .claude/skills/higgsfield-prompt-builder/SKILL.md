---
name: higgsfield-prompt-builder
description: Turn an approved creative brief into ready-to-run Higgsfield generation prompts (image/video) with negative constraints, format specs, and naming. Use when the owner asks for Higgsfield prompts, "genera i prompt per le immagini/video", or after creative-brief-builder. Produces prompt files only — actual generation via Higgsfield MCP is a separate step the owner triggers (it consumes credits = GO-gated).
---

# Higgsfield Prompt Builder

**v1.0 (2026-06-13).** Brief → prompt pronti. La GENERAZIONE consuma crediti
→ ogni chiamata Higgsfield = GO owner esplicito.

## INPUT
Un creative brief esistente (da `creative-brief-builder`); senza brief →
STOP e raccomanda il brief prima (niente creatività a caso: regola schema
Layer 8).

## PER OGNI CONCEPT DEL BRIEF
- **Prompt principale** — soggetto + azione + ambiente + stile + luce +
  mood; lingua inglese; specifico, niente elenchi di aggettivi vuoti.
- **Negative constraints** — esplicite sempre: niente testo nell'immagine
  (lo aggiunge Canva), niente watermark, niente volti riconoscibili di
  persone reali, niente loghi di terzi, **mai simulare "foto cliente"**
  (anti-pattern integrità: i creativi sono dichiaratamente promozionali).
- **Specs** — formato/aspect ratio dal brief · risoluzione · per video:
  durata, primi 3 secondi descritti frame-by-frame, motion notes.
- **Varianti** — 2-3 variazioni per concept (cambia UNA variabile per volta:
  soggetto O ambiente O stile) per test puliti.
- **Naming output** — stesso schema del brief (`..._<vN>_hf<idx>`).

## OUTPUT
File `10_OUTPUTS\CREATIVE_BRIEFS\YYYY-MM-DD_<niche>_HIGGSFIELD_PROMPTS_vN.md`
accanto al brief. Nessuna generazione eseguita dalla skill. Asset generati
(post-GO) vanno registrati nell'ASSET_REGISTRY con prompt + job id.
