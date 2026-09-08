---
tags:
  - machine
  - mission
type: mission
status: ready
description: "GO-granted live application: +19% reprice on live listings (6 BETs excluded), Furhaven brand-strip on 2 titles, AutoDS refund request for the Jul 4 charge. Auto-renew is NOT to be touched."
created_real: 2026-07-26
---

# MISSION_APPLY_REPRICE_AND_CLEANUP — RUN (2026-07-26)

**Owner:** Luca · **Autorizzazione (chain documented):** owner email 2026-07-23 msg
19f91d98a637d263 "Di alla macchina di alzare i prezzi del 19%… Non ci siamo coi prezzi" →
interactive session 2026-07-26 "completa l'opera ora. go owner" → interactive session
2026-07-26 "pensaci tu. io devo fare altro" (owner delegated the pending decisions).
Decisions taken by the mother machine under that delegation, declared here:
- **Reprice mechanism = AutoDS markup/price-rule** (not per-item manual writes), because
  price monitoring is ON for 1098/1098 and would revert manual writes (REPRICE19 report).
- **The 6 flagged BETs are EXCLUDED** from the +19% (conservative; they keep current
  prices pending data): Deck Jet, Dog Ramp, Ham Maker, 2× Stock-Tank Cover, Grooming
  Loops (data anomaly — buy $133 for a nylon 2-pack, suspected supplier swap).
- **Furhaven fix = brand-strip the titles** (keeps the sale, removes the VeRO trigger),
  NOT ending the listings.
- **Refund = request only.** Auto-renew / subscription stays UNTOUCHED (cancelling it
  would shut down the live store's operating tool — that stays an owner decision).

**Input plan:** `_reprice19_plan.json` + `REPRICE_PLUS19_PLAN_2026-07-26.md` (built by
MISSION_REPRICE_PLUS19, 2026-07-26). **Durata target:** 60–90 min.

---

## §0 · REGOLE DI INGAGGIO (vincolanti)

**GO-GRANTED (this mission only, these exact acts):**
1. **Apply +19% to live listings** per `_reprice19_plan.json`, EXCLUDING the 6 BET rows.
   Preferred mechanism: AutoDS bulk/markup/price-rule so the change survives price
   monitoring; if only per-item edit exists, set the monitoring-compatible sell price
   field (the existing `reprice_apply.py` path). Batch in chunks; verify a sample of
   ≥10 items post-write against the plan's new price before continuing past the first
   chunk. Screenshot before/after per chunk.
2. **Rewrite the 2 Furhaven titles brand-free** (items `407050802464`, `407050787699`):
   remove "Furhaven" (and any other third-party brand token) from the title, keep every
   descriptive attribute (orthopedic dog bed, size, material). Use the existing
   `set_title_live_by_id.py` path. VeRO-safe rule: no brand names not owned by us.
3. **Send ONE refund request via AutoDS support chat** (if a chat/ticket UI is reachable
   from the logged-in session): factual, polite, citing the **Jul 4 2026 charge of
   [redatto]** on card [redatto], requesting refund of that charge. NO threats, no
   cancellation talk. If the chat requires human-verification loops or is unreachable,
   STOP that phase and report — do not improvise other contact channels.

**FORBIDDEN (unchanged):**
- Do NOT touch auto-renew, plan, or subscription settings. Do NOT cancel anything.
- Do NOT reprice the 6 excluded BET rows or any draft. Do NOT touch any other listing's
  title. Do NOT end any listing.
- No credentials typed anywhere (expired session = report blocker). No purchases.
- HARD GUARD: before each write phase, re-verify the target identity (item_id match);
  ambiguity → skip that item and report, never guess.

**OBBLIGATORIO:**
- Evidence labels + screenshots before/after per phase into
  `90_CACHE/fetches/apply_2026-07-26/`.
- Run log `00_SYSTEM_CONTROL/MISSION_APPLY_REPRICE_AND_CLEANUP_RUN_LOG.md` per step;
  REGOLA OROLOGIO (real `Get-Date` timestamps).
- STOP CONDITION: monitoring reverts prices on the sample check · UI writes fail ≥2×
  on the same control · any prompt for credentials/payment → stop, report.

## FASE 1 · REPRICE APPLY (act 1) — sample-verify, then roll
## FASE 2 · FURHAVEN TITLES (act 2)
## FASE 3 · REFUND REQUEST (act 3)
## FASE 4 · REPORT — `MISSION_APPLY_REPRICE_AND_CLEANUP_RUN_REPORT_2026-07-26.md`,
final counts (repriced OK / skipped / failed), the exact refund message sent (or the
blocker), post-state evidence paths. Owner-facing summary in Italian. Last log line
`DONE — <real time>`.
