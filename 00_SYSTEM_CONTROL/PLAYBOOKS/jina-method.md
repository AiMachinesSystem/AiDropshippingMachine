---
tags:
  - machine
type: entity
status: active
date: 2026-06-12
description: "Protocollo di accesso alla Meta Ad Library via proxy r.jina.ai: retry max 2, conteggi lower-bound, collisioni Library-ID, universi mai sommati."
---

# Metodo Jina

Protocollo della macchina per leggere la **Meta Ad Library**: proxy `https://r.jina.ai/` + URL completo — facebook.com diretto è un muro noto (socket close / 403) [OBSERVED — registro muri, VAULT_CONVENTIONS].

- **Regole**: retry ≤2 · conteggi pubblicati come lower bound dichiarati · protocollo collisioni Library-ID · universi separati (core vs LATAM) mai sommati [OBSERVED — skill ads-library-scan v1.2]
- Codificato nella skill `ads-library-scan` e nel registro muri di [[VAULT_CONVENTIONS]]
- Cache evidenze obbligatoria prima della citazione: `90_CACHE\fetches\<dominio>\` [regola cache evidenze]
- Motore di lettura per i censimenti ads di QUALSIASI `<NICHE_NAME>` (proxy + cache + universi separati)

## Collegamenti

- Skill: `ads-library-scan` · convenzioni: [[VAULT_CONVENTIONS]]
- Output dei run: `10_OUTPUTS/ADS_LIBRARY_SCANS/` e `10_OUTPUTS/COMPETITOR_ANALYSIS/`
