---
name: weekly-learning-update
description: Weekly synthesis of what the machine learned — index deltas, new walls or fallen walls, skill version changes, aging open loops, walls past the 7-day retest window, backlog drift. Use when the owner asks "cosa hai imparato questa settimana", "weekly update", "punto settimanale", "learning update". Reads logs/indexes/git only; writes ONE dated report in 10_OUTPUTS/SYSTEM_REPORTS + cockpit refresh. Never re-runs research from inside this skill.
---

# Weekly Learning Update

**v1.0 (2026-06-12).** Sintesi settimanale di apprendimento. Read-only sui dati; scrive UN report + cockpit.

## FONTI (tutte, in quest'ordine)
1. `git log --since="7 days ago"` — cosa è cambiato davvero (commit = fatti).
2. `RESEARCH_MEMORY_INDEX` — delta blocchi nicchia (nuovi run, correzioni canone).
3. `MACHINE_STATE` + `BACKLOG` — skill/strumenti nuovi, item aperti/chiusi, drift (item fermi >7gg).
4. `VAULT_CONVENTIONS` registro MURI NOTI — muri con ultima verifica >7gg = **candidati ri-test**.
5. `SELF_IMPROVEMENT_NOTES` + run log missioni della settimana — lezioni di processo.

## STRUTTURA DEL REPORT (≤1 pagina, schema §8 dove applicabile)
1. **Imparato** — 3–7 punti, ognuno con etichetta evidenza e fonte (file/commit).
2. **Canone cambiato** — correzioni ai numeri citabili (prima → dopo, perché).
3. **Muri** — nuovi muri · muri caduti · candidati ri-test (>7gg) — SOLO proposta, il ri-test
   non parte da questa skill.
4. **Drift** — item BACKLOG/NEXT_ACTIONS fermi da >7gg, con proprietario (macchina vs owner).
5. **Prossima settimana** — strada raccomandata + alternative scartate (mai solo lista opzioni).

## OUTPUT
UN file `10_OUTPUTS\SYSTEM_REPORTS\YYYY-MM-DD_weekly-learning-update_vN.md` (REGOLA OROLOGIO:
data da Get-Date) + **AUTO-REFRESH cockpit** (MASTER_DASHBOARD + NEXT_ACTIONS) — run senza
entrambi = INCOMPLETO.

## MINI SELF-TEST (3 domande + risposte attese)
- **Q1.** Da dove vengono i delta della settimana? → **A.** git log 7 giorni + confronto
  indici (RESEARCH_MEMORY_INDEX, MACHINE_STATE, BACKLOG, registro MURI) — mai dalla memoria
  della sessione.
- **Q2.** Un muro risulta verificato 9 giorni fa: che fa la skill? → **A.** Lo segnala come
  candidato RI-TESTABILE (finestra 7gg superata) nel report; NON lo ri-testa — il ri-test è
  un'azione separata che l'owner o una missione autorizza.
- **Q3.** Qual è l'output minimo perché il run sia COMPLETO? → **A.** Il file datato in
  10_OUTPUTS\SYSTEM_REPORTS + refresh MASTER_DASHBOARD/NEXT_ACTIONS (regola AUTO-REFRESH).

## SCENARIO D'USO TIPICO
Prima esecuzione dopo una settimana piena di storia (più run di ricerca, missioni, eventuali
FIX di datazione/canone): il report sintetizza i delta del canone di `<NICHE>`, i muri in
scadenza di ri-test (finestra 7gg), e gli item di decision pack in drift se ancora aperti.
Cadenza candidata: lunedì.
