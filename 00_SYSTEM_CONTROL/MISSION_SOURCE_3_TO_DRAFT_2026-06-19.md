---
tags:
  - machine
  - mission
type: mission
status: active
date: 2026-06-19
created_real: 2026-06-19
description: "Missione: ricerca 3 NUOVI prodotti winner (fonte Amazon/AliExpress importabile AutoDS) + pacchetto draft-ready (titolo <=80 + descrizione VeRO-safe riscritta). Step 1-4 INTERNI; import draft = GO-CLASS (GO_IMPORT_5_DRAFTS). Esegue la routine source-products-to-draft."
---

# MISSION — Source 3 Products → Draft (2026-06-19)

**Owner:** Luca · **Origine:** intento owner 2026-06-19 ("ricerca 3 prodotti e mettili in draft... ricordatela come routine").
**Routine eseguita:** `02_DATA/_ROUTINES/source-products-to-draft.md` (scritta in questa run).

## Obiettivo
3 prodotti NUOVI (diversi dai draft esistenti), fonte Amazon US/AliExpress (importabile AutoDS), domanda validata (proxy), VeRO-safe, leggeri/economici, ognuno con **titolo <=80** e **descrizione riscritta**. Pacchetto draft-ready + comandi `manage_draft.py full` pronti.

## Classe di rischio
- **Fasi 1-4 (recon, ricerca, validazione, copy, file) = INTERNA** → eseguo senza attendere.
- **Fase 5 (import draft su AutoDS) = GO-CLASS** → stop al gate `GO_IMPORT_5_DRAFTS`, GO citato. Publish/prezzi/ordini = gate separati, fuori scope.

## Fasi
1. **Recon anti-dupe** — leggi draft/copy esistenti, lista da evitare. [fatto in-run]
2. **Ricerca live** (workflow multi-agente) — per candidato: fonte+costo [OBSERVED], domanda eBay [PUBLIC RESEARCH], margine [ESTIMATE], VeRO, ship profile.
3. **Verifica avversariale** — titolo <=80, VeRO/brand scan, fonte importabile, margine, evidenza domanda con URL.
4. **Selezione 3 + copy** — titolo <=80 + descrizione VeRO-safe riscritta; file `LISTING_COPY_3_drafts_2026-06-19.md` + comandi; refresh cockpit.
5. **GATE** — `GO_IMPORT_5_DRAFTS`: chiedo GO per il write live. (Precondizione: sessione AutoDS valida.)

## Criterio di misura
Niente metrica nuova. Output = 3 prodotti con evidenze etichettate (no numeri inventati), titoli verificati <=80, descrizioni riscritte VeRO-safe, comandi eseguibili. Progresso vision misurato col criterio esistente (VISION_GAP_MATRIX), non gonfiato.

## Regole §0 applicabili
GO gate (§0.3) · etichette evidenza (§0.4) · constitutional filter (§0.5) · firewall (§0.6) · versioning a fine fasi (§0.7) · integrita'/no prove fabbricate (§0.8) · orologio reale (§0.9).

## Recovery
Se compatta: rileggi questa missione + `02_DATA/_ROUTINES/source-products-to-draft.md`, controlla `listings/LISTING_COPY_3_drafts_2026-06-19.md` (se esiste = fasi 1-4 fatte → resta solo il GO gate).
