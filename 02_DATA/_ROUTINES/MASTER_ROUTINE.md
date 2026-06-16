---
tags:
  - machine
type: playbook
status: template
description: "Dispatcher owner: mappa intento → routine/skill. PARTE come scheletro; popola le righe coi tuoi intenti ricorrenti."
---

# MASTER_ROUTINE — dispatcher degli intenti owner (template v1)

> Regola §1 della costituzione: ogni richiesta owner passa di qui. Intent map →
> routine/skill, seguite come scritte. Aggiungi una riga per ogni intento ricorrente.

## INTENT MAP

| Intento owner (esempi di trigger) | Routine / Skill | Note |
|---|---|---|
| "analizza questa nicchia / c'è mercato per…" | `niche-intelligence-run` (`/niche-run`) | validazione + censimento; QUERY MODE se già studiata |
| "analizza/studia questo competitor" | `competitor-scan` (`/competitor-scan`) | teardown + scoring |
| "che ads fa X / pattern ads" | `ads-library-scan` (`/ads-scan`) | proxy r.jina.ai; lower bound |
| "prepara il lancio / launch pack" | `launch-prep` (`/launch-prep`) | GATED; gate zero = provenienza/diritti |
| "cosa dicono i clienti / customer voice" | `customer-voice-mining` | fonti pubbliche autonome; dati owner = GO |
| "diagnosi offerta / che prezzo" | `offer-diagnosis` | QUERY MODE: numeri solo da CANONE CORRENTE |
| "analizza questa landing" | `landing-page-review` | read-only; cache prima di citare |
| "prepara le creative / brief" | `creative-brief-builder` → `higgsfield-prompt-builder` → `test-plan-builder` | drafting; generazione/spesa = GO |
| "vision check / siamo allineati?" | `vision-check` | verdetto, mai fix silenziosi |
| "brief del giorno" | `/daily-brief` | legge dashboard + TASKS + git |
| "cosa hai imparato questa settimana" | `weekly-learning-update` | un report + cockpit refresh |
| "riordina/audit del vault" | `vault-librarian` | manutenzione conservativa output di ricerca |
| intenti operativi eBay/AutoDS ("setup AutoDS", "crea/modifica listing", "pricing/repricing", "fulfillment/ordini", "fornitori", "account/policy eBay") | disciplina di fase: `01_SYSTEM/SYSTEM_BLUEPRINT.md` + `01_SYSTEM/OPERATING_RULES.md` + `00_SYSTEM_CONTROL/APPROVAL_GATES.md` | TUTTO GO-gated; fase corrente in `00_SYSTEM_CONTROL/CURRENT_STATUS.md`; niente live/esterno senza GO; execution solo entro la gate structure |
| "a che punto siamo / prossimo passo / stato macchina" | `00_SYSTEM_CONTROL/CURRENT_STATUS.md` + `NEXT_ACTIONS.md` + `/daily-brief` | lookup di stato dal cockpit; mai ri-lanciare ricerche per un lookup |
| `<altro intento ricorrente>` | `<routine/skill>` | `<note>` |

## REGOLE DI ROUTING
- QUERY MODE prima di RUN MODE: se la risposta è già nell'indice, non ri-lanciare ricerche.
- Ogni run di ricerca CHIUDE registrando il blocco nicchia nell'indice + refresh cockpit (AUTO-REFRESH).
- HARD GATE / azione live → stop al gate, chiedi GO citandolo.
