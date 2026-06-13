---
name: landing-page-review
description: Audit of a PUBLIC landing page (owner draft or competitor) — hook clarity, offer structure, trust/substantiation, friction, integrity/compliance flags — scored 1-5 with a pre-declared rubric. Use when the owner asks "analizza questa landing", "review della landing", "perché questa pagina non converte", "guarda questa pagina" with a landing URL. Read-only — fetch via proxy + Playwright screenshot, evidence cached BEFORE citing; never replicates anti-patterns found.
---

# Landing Page Review

**v1.0 (2026-06-12).** Audit read-only di una landing PUBBLICA. Nessuna azione live.

## FONTI E STRUMENTI (in quest'ordine)
1. Fetch testuale via proxy `https://r.jina.ai/<url completo>` → salva PRIMA in
   `90_CACHE\fetches\<dominio>\<data>_<slug>.txt` (regola cache v1.2, retry ≤2).
2. Screenshot Playwright (`node 90_CACHE\tools\playwright\node_modules\playwright\cli.js`
   o script library-mode) → `90_CACHE\screenshots\<dominio>\<data>_<slug>.png`.
   Solo pagine pubbliche; se chiede login → screenshot dell'esito e STOP su quella pagina.
3. Se la nicchia è già studiata: canone da `RESEARCH_MEMORY_INDEX` (sezione
   CANONE CORRENTE, data run citata) per confrontare prezzi/pattern.

## RUBRICA (pre-dichiarata, score 1–5 per dimensione + flag)
1. **Hook & promessa** — chiarezza in 5 secondi, specificità, coerenza col traffico.
2. **Struttura offerta** — prezzo, anchor DICHIARATO e sostanziabile, garanzia reale, ladder.
3. **Trust & substantiation** — ogni claim ha fonte verificabile? recensioni reali e linkate?
4. **Frizione** — CTA, passi al checkout, campi, distrazioni.
5. **Integrità/compliance** — contatori finti, foto-recensioni AI, badge decorativi, anchor
   non dichiarati, waiver recesso EU → **integrity flag** (anti-pattern: si DOCUMENTA, mai si replica).
6. **Render/mobile** — dalla resa screenshot (limite dichiarato: niente device testing reale).

## PROCEDURA
1. FIREWALL check: la landing appartiene a UN progetto; nessun confronto cross-progetto senza scope owner.
2. Fetch + screenshot (cache prima di ogni citazione; ogni claim etichettato [OBSERVED/INFERRED/UNKNOWN]).
3. Score 1–5 × 6 dimensioni con evidenza per ogni punteggio; lista integrity flag.
4. Output §8 (template in `00_SYSTEM_CONTROL\TEMPLATES\`): verdetto + 3 fix a impatto
   maggiore + alternative scartate. Review rapida = inline; run completo = UN file in
   `10_OUTPUTS\ANALYSIS_REPORTS\YYYY-MM-DD_<slug>_landing-review_v1.md` + **AUTO-REFRESH
   cockpit** (MASTER_DASHBOARD + NEXT_ACTIONS) — run senza entrambi = INCOMPLETO.

## MINI SELF-TEST (3 domande + risposte attese)
- **Q1.** Cosa serve PRIMA di citare qualunque elemento della pagina? → **A.** Raw fetch
  salvato in `90_CACHE\fetches\` (+ screenshot se load-bearing), citazione
  `[OBSERVED — url + data (cache: path)]`. Mai citare da memoria.
- **Q2.** La landing mostra "4.9★ · 4.200 clienti" senza fonte verificabile: che fa la skill?
  → **A.** Integrity flag, score trust penalizzato con motivazione, anti-pattern documentato
  e MAI replicato nei draft owner.
- **Q3.** L'owner chiede di confrontare una landing del progetto `<PROJECT_A>` con il canone
  di un'altra `<NICHE>`: che fa la skill? → **A.** STOP cross-progetto (firewall regola 6):
  review solo nello scope del progetto richiesto; confronto inter-progetto solo con scope esplicito owner.

## SCENARIO D'USO TIPICO
Teardown della landing advertorial di un competitor leader della `<NICHE>` per estrarre
vincoli/contromosse per creative-brief-builder; poi review della futura landing dell'owner
post decision pack, prima di launch-prep.
