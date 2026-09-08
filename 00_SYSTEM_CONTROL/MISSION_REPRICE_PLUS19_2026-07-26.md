---
tags:
  - machine
  - mission
type: mission
status: ready
description: "Owner-ordered repricing: +19% on live eBay listings, with Amazon-listing vs Temu-price cross-check. Internal phases autonomous; the live price write is GO-CLASS and stops at the gate."
created_real: 2026-07-26
---

# MISSION_REPRICE_PLUS19 — RUN AUTONOMO (2026-07-26)

**Owner:** Luca · **Autorizzazione:** owner command received via <machine-inbox>
(msg 19f91d98a637d263, 2026-07-23: "Di alla macchina di alzare i prezzi del 19%… Non ci
siamo coi prezzi" + msg 19f91e20f3f903fd: "Va fatto un lavoro incrociato… prendere gli
annunci da amazon ma vedere i prezzi di temu"), re-confirmed in interactive session
2026-07-26 ("completa l'opera ora. go owner"). Relayed cross-machine by the mother
machine (AI_EDGE_OS) per its explicit-GO cross-machine rule — provenance, not invention.
**Durata target:** 60–90 min. **Modalità:** autonoma (internal phases).
**Principio:** il bypass dei popup NON toglie le regole. Le regole §0 sono vincolanti.

---

## §0 · REGOLE DI INGAGGIO (vincolanti, prevalgono su tutto il resto)

**VIETATO in qualunque fase:**
1. Live external actions: purchases, registrations, logins, account creation, sending
   email/messages, contacting people, any spend.
2. Writes to external integrations (eBay, AutoDS, ads, email). Web = public-page reads
   only (existing proxy method). **The actual +19% price write on eBay/AutoDS is
   GO-CLASS: prepare it fully, then STOP at the gate and name the exact step.**
3. Firewall between projects: no cross-project contamination.
4. No deletions outside this mission's folders. Never `git push --force`, never rewrite
   history, never touch `.git` by hand.
5. Installs: local dev packages only, only if a task truly requires them, each logged.
   Preference: zero installs.

**OBBLIGATORIO:**
- Evidence discipline: [OBSERVED — source+date] / [INFERRED — basis] / [UNKNOWN].
  Counts = declared lower bounds. Never invent numbers.
- `git commit` at the end of EVERY phase, message prefix `REPRICE19:`.
- Continuous log in `00_SYSTEM_CONTROL\MISSION_REPRICE_PLUS19_RUN_LOG.md`; on
  compaction re-read this mission + the run log and resume from the last logged step.
- REGOLA OROLOGIO: every date/time from `Get-Date` at write time.
- Wall or fetch failed ≥2 times → [UNKNOWN] + move on. No loops.
- STOP CONDITION: anomalous git state or any ambiguity that would require a forbidden
  action → jump to the final report phase and explain.

---

## FASE 1 · INVENTORY (~20 min)
Build the current live-listing price table from THIS machine's own registered data
(AutoDS export / listing registry / latest audit — QUERY MODE first on
RESEARCH_MEMORY_INDEX and 02_DATA). Output: table `item | current price | source cost |
current margin` with evidence labels. If live-state data is stale, mark [UNKNOWN —
needs fresh pull = GO-CLASS read? follow this machine's own rules] and proceed with the
latest registered snapshot, declared.

## FASE 2 · REPRICE PLAN +19% (~20 min)
Compute new price = current × 1.19 for every live listing (round to marketplace-natural
endings, e.g. .95/.99 — declare the rounding rule used). Flag any listing where +19%
crosses an obvious demand cliff vs the registered competitor/winner price band
(data-first gate §2 of the constitution): the flag is a declared BET note, not a
silent skip. Output: `00_SYSTEM_CONTROL\REPRICE_PLUS19_PLAN_2026-07-26.md` — exact
per-item old→new price list, ready to apply.

## FASE 3 · AMAZON×TEMU CROSS-CHECK (~25 min)
Owner's stated intent: listings sourced from Amazon are mispriced vs what the same
product costs on Temu. For each live listing (or top-N by sales if the list is long):
public-read the Temu price of the same/equivalent product, compare against our source
cost and new +19% price, and mark: `OK (margin healthy)` / `STILL UNDERPRICED` /
`OVERPRICED vs market`. Evidence-labeled, lower-bound counts, LOW-SAMPLE flags where
matching is uncertain. Feed conclusions back into the plan as per-item notes.

## FASE 4 · REPORT + GO REQUEST (OBBLIGATORIA)
Create `00_SYSTEM_CONTROL\MISSION_REPRICE_PLUS19_RUN_REPORT_2026-07-26.md`: phases
done/skipped · files + commits · findings · the exact GO-CLASS step remaining, phrased
for the owner as ONE line (e.g. "GO REPRICE → applico la tabella su AutoDS/eBay").
The live application itself does NOT run in this mission. Last run-log line:
`DONE — <real time>`.
