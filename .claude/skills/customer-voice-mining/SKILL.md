---
name: customer-voice-mining
description: Mining of REAL customer voice from PUBLIC sources (product reviews, Reddit via gummysearch, forums, Q&A) — pains, objections, desired outcomes, exact language patterns, quote bank with sources for creative briefs and offer design. Use when the owner asks "cosa dicono i clienti", "scava le recensioni", "che obiezioni hanno", "il linguaggio dei clienti", "customer voice". PUBLIC sources only run autonomously; Gmail/store/owner data = class B, each single read is GO-gated. Every quote carries url+date+cache path or is NOT USABLE.
---

# Customer Voice Mining

**v1.0 (2026-06-12).** Estrazione di voce-cliente da fonti PUBBLICHE. Processo classe A; dati owner = classe B gated.

## PERIMETRO DATI (regola dura)
- **Autonomo (classe A):** review pubbliche (Amazon, Trustpilot, marketplace), Reddit via
  gummysearch (Reddit diretto = MURO noto), forum/Q&A pubblici, commenti pubblici alle ads.
- **GO-gated (classe B):** Gmail, ordini/clienti store, DM, qualunque dato dietro login owner
  — OGNI lettura richiede GO esplicito per-azione (l'approvazione non si trasferisce).
- Muri noti rispettati (Etsy 403, gruppi FB login): fallimento ≥2 retry → [UNKNOWN] e avanti.

## PROCEDURA
1. FIREWALL check: il mining serve UN progetto; mai travasi cross-progetto.
2. Definire 3–5 domande di mining (pain? obiezione? outcome? linguaggio?) PRIMA di leggere.
3. Fetch fonti pubbliche via proxy → cache `90_CACHE\fetches\` PRIMA di ogni citazione.
4. Estrarre quote VERBATIM con url+data; classificare per tema; conteggi = lower bound
   dichiarati; tema visto 1 volta = [LOW-SAMPLE], mai generalizzare.
5. Distillare: top pains/obiezioni con frequenza osservata, glossario del linguaggio reale,
   gap tra ciò che il mercato promette e ciò che i clienti lamentano.

## OUTPUT (template §8)
UN file `10_OUTPUTS\ANALYSIS_REPORTS\YYYY-MM-DD_<slug>_customer-voice_v1.md`: quote bank
(ogni quote: testo verbatim · fonte url+data · cache path · tema) + sintesi pains/objections
+ vincoli di substantiation pronti per creative-brief-builder + **AUTO-REFRESH cockpit**
(run senza = INCOMPLETO).

## MINI SELF-TEST (3 domande + risposte attese)
- **Q1.** Posso leggere le email di supporto per estrarre obiezioni? → **A.** NO senza GO
  esplicito per quella singola lettura (dato owner-only, classe B); in autonomia la skill
  lavora SOLO su fonti pubbliche.
- **Q2.** Una recensione perfetta per il brief ma senza URL recuperabile/cache: si usa? →
  **A.** NO — quote senza fonte+cache = NOT USABLE; nei draft ogni claim porta la sua
  substantiation o non entra.
- **Q3.** Dove finiscono i pattern estratti? → **A.** Quote bank nel report datato in
  ANALYSIS_REPORTS + vincoli passati a creative-brief-builder; refresh cockpit obbligatorio.

## SCENARIO D'USO TIPICO
Mining del pain dei principianti in una `<NICHE>`: subreddit di settore (via gummysearch) +
review pubbliche dei prodotti best-seller per sostanziare hook e copy dei brief della pipeline
creativa (creative-brief-builder → higgsfield-prompt-builder) — i claim del mercato (es.
"beginner-friendly") vanno verificati contro le lamentele reali dei clienti.
