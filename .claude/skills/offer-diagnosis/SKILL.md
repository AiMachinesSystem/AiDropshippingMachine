---
name: offer-diagnosis
description: Diagnosis of an offer's structure (owner draft or competitor) against the registered niche canon — price ladder position, anchor legitimacy, guarantee reality, bonus stack, claim substantiation. Use when the owner asks "diagnosi dell'offerta", "perché questa offerta è debole", "confronta la mia offerta col mercato", "che prezzo dovrei fare", "l'offerta regge?". QUERY MODE first — market numbers ONLY from RESEARCH_MEMORY_INDEX (CANONE CORRENTE). Analysis/drafting only — nothing goes live, no prices published.
---

# Offer Diagnosis

**v1.0 (2026-06-12).** Diagnosi struttura-offerta contro il canone registrato. Read-only sul mercato; scrive solo bozze/raccomandazioni.

## FONTI (in quest'ordine)
1. `RESEARCH_MEMORY_INDEX` — blocco nicchia, **SOLO sezione CANONE CORRENTE**, data run citata
   (regola numeri canonici v1.2). Nicchia mai studiata → [UNKNOWN], si raccomanda
   niche-intelligence-run, MAI numeri inventati o "di settore".
2. Report collegati al blocco (ladder, garanzie, anchor osservati) per il dettaglio.
3. L'offerta target: bozza owner (file/testo) o pagina competitor (fetch via proxy + cache
   PRIMA della citazione, regola v1.2).

## DIMENSIONI DI DIAGNOSI (tutte, con evidenza)
1. **Posizione nella ladder** — dove cade vs ladder canonica della nicchia; chi occupa già la fascia.
2. **Anchor** — dichiarato e sostanziabile? (somma prezzi reali osservati = OK; "valore" inventato = NOT USABLE).
3. **Garanzia** — reale e onorabile vs decorativa/no-refund di fatto (anti-pattern documentato).
4. **Bonus stack** — pertinenza e costo marginale; il bonus copre un'obiezione reale?
5. **Substantiation** — ogni claim dell'offerta ha fonte o è marcato NOT USABLE (regola integrità 8).
6. **Difendibilità** — cosa impedisce a uno swarm-clone di copiarla in 7 giorni.

## OUTPUT (template §8 in `00_SYSTEM_CONTROL\TEMPLATES\`)
Verdetto (REGGE / DEBOLE / NOT USABLE) + confidenza · 3 mosse correttive ordinate per impatto
con il perché · alternative scartate · ruolo owner (decisioni, mai prezzi live senza GO).
Diagnosi rapida = inline; run completo = UN file `10_OUTPUTS\ANALYSIS_REPORTS\
YYYY-MM-DD_<slug>_offer-diagnosis_v1.md` + **AUTO-REFRESH cockpit** (run senza = INCOMPLETO).

## MINI SELF-TEST (3 domande + risposte attese)
- **Q1.** Da dove vengono i numeri di mercato per la diagnosi? → **A.** Dalla sezione CANONE
  CORRENTE del blocco nicchia in RESEARCH_MEMORY_INDEX, citando la data del run; mai ri-scan
  per un lookup, mai righe STORICO come correnti.
- **Q2.** La bozza usa un anchor "`<X>` di valore reale" senza base osservata: verdetto? →
  **A.** NOT USABLE — anchor non sostanziato = integrity flag; si propone un anchor
  sostanziabile (es. somma dei prezzi singoli osservati nel canone) o si toglie.
- **Q3.** La nicchia non ha blocco nell'indice: che fa la skill? → **A.** Dichiara [UNKNOWN],
  nessuna diagnosi numerica; raccomanda un niche-intelligence-run prima; può comunque
  auditare substantiation e garanzia (dimensioni non di mercato) dichiarando il limite.

## SCENARIO D'USO TIPICO
Appena l'owner scioglie il gate zero di `<PROJECT_NAME>` (provenienza/diritti), la bozza
d'offerta va diagnosticata contro il CANONE CORRENTE della `<NICHE>` (posizione nella ladder,
anchor osservati, garanzia vera come differenziatore) PRIMA di launch-prep.
