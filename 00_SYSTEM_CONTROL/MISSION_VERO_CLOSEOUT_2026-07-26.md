---
tags:
  - machine
  - mission
type: mission
status: ready
description: "Close the 13-day-old VeRO escalation: end the 2 IP-flagged 'Best Pet Supplies' listings and blocklist the brand in AutoDS. Live write is GO-GRANTED for this specific act."
created_real: 2026-07-26
---

# MISSION_VERO_CLOSEOUT — RUN (2026-07-26)

**Owner:** Luca · **Autorizzazione:** OWNER GO EXPLICIT, given in an interactive Claude Code
session on 2026-07-26 ("completa l'opera ora. go owner"), on an item the machine itself had
listed as blocked-awaiting-owner. Provenance: eBay Resolution Center notice mailed to
sam@masteryforgecrafts.com 2026-07-13 (msg 19f5a3b0e37518f6), escalated in
`MASTERYFORGE_CRAFTS/MACHINE_INBOX/STATE/escalations.md` row 1, **OPEN for 13 days**.
**Durata target:** 30–45 min. **Modalità:** autonoma fino al gate dichiarato sotto.

## WHY THIS IS TIME-CRITICAL
Two listings are flagged **Intellectual property rights (VeRO)**: "Best Pet Supplies Cat…"
($199.88 and $103.88). An unresolved VeRO strike escalates toward **account suspension**.
Ending the listings is the risk-REDUCING action (an appeal would lose — no IP rights exist
on a dropshipped brand — and would keep the strike).

---

## §0 · REGOLE DI INGAGGIO (vincolanti)

**GO-GRANTED (this mission only, these exact acts):**
1. **End / delete the 2 VeRO-flagged listings** ("Best Pet Supplies" branded), via the
   existing AutoDS Playwright path (same mechanism as `remove_oos_listings.py`) or the eBay
   Seller Hub session. This is the ONLY live write authorized.
2. **Add "Best Pet Supplies" (and branded pet items from that brand) to the AutoDS
   supplier/brand blocklist** so it cannot be re-listed — if a blocklist UI exists.
3. **Read** AutoDS billing/subscription page (plan, start/renewal date, last charge) —
   READ ONLY, for the owner's pending refund decision. Do NOT request/cancel anything.

**STILL FORBIDDEN (unchanged):**
- Any OTHER listing may not be touched. **HARD GUARD: end ONLY listings whose title/brand
  matches "Best Pet Supplies" AND which the Resolution Center flags. If the flagged items
  cannot be positively identified, STOP and report — never guess which listing to end.**
- No appeal filed, no message sent to eBay/VeRO/rights-owner, no refund requested, no
  subscription cancelled, no purchase, no price change (that is the separate REPRICE19
  mission, still at its own GO gate).
- No password reset, no new account, no 2FA bypass. If the saved session is expired →
  report that as the blocker; do NOT type credentials into a headless browser.

**OBBLIGATORIO:**
- Evidence labels [OBSERVED — source+date] / [INFERRED] / [UNKNOWN]. Screenshot every
  live-write step before and after, into `90_CACHE/fetches/vero_2026-07-26/`.
- Run log `00_SYSTEM_CONTROL/MISSION_VERO_CLOSEOUT_RUN_LOG.md`, updated per step.
- REGOLA OROLOGIO: real time from `Get-Date` at write time.
- STOP CONDITION: expired session · ambiguous listing identity · any prompt for
  credentials/2FA · ≥2 failures on the same obstacle → stop, report, no guessing.

---

## FASE 1 · IDENTIFY (read-only)
Locate the 2 flagged listings with certainty. Sources in order: eBay Seller Hub /
Resolution Center via `ebay_storage_state.json`; AutoDS products list filtered on title
containing "Best Pet Supplies"; the registered `_products_list.json` snapshots. Record
item_id, title, price ($199.88 / $103.88 expected), current status (they may ALREADY be
ended by eBay after 13 days — if so, this mission becomes a verification and phases 2 is
skipped as already-satisfied). Output: an explicit 2-row identification table.

## FASE 2 · END THE 2 LISTINGS (the GO-granted live write)
Dry-run first (identify + report the exact rows), then execute the end/delete on exactly
those 2. Screenshot before/after. Re-read the listing state to CONFIRM ended — a claim of
success without an observed post-state is not acceptable.

## FASE 3 · BLOCKLIST + BILLING READ
Add the brand to the AutoDS blocklist if such a control exists (screenshot). Then read the
AutoDS billing page: plan, subscription start/renewal date, last charge amount+date.
Report the numbers — take NO billing action.

## FASE 4 · REPORT (obbligatoria)
`00_SYSTEM_CONTROL/MISSION_VERO_CLOSEOUT_RUN_REPORT_2026-07-26.md`: what was ended (with
proof), what was blocklisted, the billing facts for the refund decision, residual UNKNOWNs,
and anything still needing the owner. Final run-log line `DONE — <real time>`. Write the
owner-facing summary in Italian.
