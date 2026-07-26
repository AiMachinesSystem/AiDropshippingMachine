---
tags: [machine, mission, report]
type: mission-report
mission: MISSION_REPRICE_PLUS19_2026-07-26
created_real: 2026-07-26
status: PARTIAL_COMPLETE — tutte le fasi interne fatte; applicazione live = GO-CLASS, NON eseguita
---

# REPORT MISSIONE — REPRICE +19% (2026-07-26)

## Verdetto
Piano +19% **pronto da applicare** su 1098 listing live: da $56.324,98 → $67.591,02 di prezzo listino totale (+$10,26 medio/listing). Nessuna azione live eseguita. Confidence: HIGH sul calcolo (dati registrati), MED sulla freschezza (snapshot 2026-07-18, 8 giorni).

## Fasi
| Fase | Esito |
|---|---|
| 1 · Inventory | ✅ DONE — base autorevole = pull AutoDS 2026-07-18 (`90_CACHE/fetches/autods/audit_2026-07-18_111303/`): 1098 LIVE con prezzo+costo+sold [OBSERVED]. ~108 listing pubblicati il 20/07 con prezzo corrente [UNKNOWN — refresh = GO-CLASS read] → nel piano come nota-formula. |
| 2 · Piano +19% | ✅ DONE — `REPRICE_PLUS19_PLAN_2026-07-26.md` (1098 righe old→new) + `_reprice19_plan.json` (ready-to-apply). Regola dichiarata: new = cur×1,19 arrotondato IN SU al `.99` (mai sotto +19%; base: ending vincente `.99` registrato). |
| 3 · Cross-check Amazon×Temu | ⚠️ PARZIALE — **Temu = MURO** (CAPTCHA su pagine prodotto, 2 metodi × 2 pagine; registrato in MURI NOTI, no retry prima del 2026-08-02) → prezzi Temu per-item [UNKNOWN]. CONFERMATO però [OBSERVED — WebSearch 2026-07-26] che gli equivalenti esistono su Temu per 4/15 categorie top testate (premessa owner valida a livello esistenza). Fallback su dati registrati: net margin al nuovo prezzo per i top-15 venduti = **27–47% net, 0 negativi, 0 ancora sottoprezzati** vs costo Amazon + fee eBay. |
| 4 · Report + GO | ✅ DONE — questo file. |

## Finding chiave
1. **Il +19% è direzionalmente giusto e sano sul margine**: tutti i top-15 venduti restano nel canone registrato di arbitraggio (30–42% net) o sopra; nessuno va negativo.
2. **6 BET dichiarate** (gate data-first §2): Deck Jet e Dog Ramp sono GIÀ ×2,9–4,6 sopra la mediana sold registrata (eppure vendono — banda probabilmente spostata o spec diversa: verificare al momento dell'apply); Ham Maker e le 2 Stock-Tank Cover superano la banda col +19%; **Grooming Loops = anomalia dati** (buy $133,13 per un 2-pack di loop nylon → probabile supplier swap: VERIFICARE il listing prima di riprezzarlo).
3. **Price monitoring AutoDS attivo su 1098/1098**: una scrittura manuale del prezzo rischia il revert al prossimo sync. Applicazione raccomandata = alzare la markup/price-rule AutoDS del +19% (o fixed price + monitoring off per-item). Decisione nel GO step.
4. Esisteva un dry-run reprice precedente (2026-07-18, ~+2%) mai applicato — superseded da questo piano.

## File + commit (prefisso `REPRICE19:`)
- `3b4b22b` fase1 — mission + run log + `_reprice19_plan.json`
- `416cb71` fase2 — `REPRICE_PLUS19_PLAN_2026-07-26.md`
- `ca3ec55` fase3 — sezione cross-check + MURI NOTI (Temu)
- fase4 — questo report (commit di chiusura)
- Cache evidenze: `90_CACHE/fetches/temu/2026-07-26_*.txt` (non versionata, regola cache)

## Auto-audit (§3 AUTONOMIA CONTROLLATA)
- §0 rispettate: zero azioni live/esterne, zero login, zero spesa, solo letture pubbliche (Temu wall gestito da regola, no loop) ✅
- Evidenze etichettate su ogni claim; conteggi lower bound; staleness dichiarata ✅
- Git: 4 commit mission-only, file sporchi pre-esistenti NON toccati ✅
- Errore di processo auto-corretto: 2 timestamp stimati invece che letti (REGOLA OROLOGIO) → corretti nel run log e dichiarati; candidato ERROR_REGISTRY a discrezione (violazione minore, auto-rilevata in-run)
- Zero contaminazioni cross-project ✅ · Nessuna metrica nuova inventata ✅

## ⏳ GO-CLASS RIMANENTE (una riga)
**GO REPRICE → applico la tabella `_reprice19_plan.json` (1098 listing, +19%, .99) su AutoDS/eBay** — con sotto-decisione: via markup-rule (consigliato, monitoring-proof) o per-item fixed price; le 6 BET flaggate si applicano o si escludono su tua indicazione; i ~108 del 20/07 si riprezzano con la stessa formula dopo una pull fresca (anch'essa GO).
