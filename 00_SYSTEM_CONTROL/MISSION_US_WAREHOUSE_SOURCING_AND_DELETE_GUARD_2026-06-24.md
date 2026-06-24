---
machine: "eBay / AutoDS Dropshipping Machine"
mission_id: US_WH_SOURCING_AND_DELETE_GUARD
project: EBAY_AUTODS_5_LISTING_LAUNCH
date: 2026-06-24
created_real: 2026-06-24
owner_go: "Luca 2026-06-24 — 'GO per procedere con 2 e 3' (sourcing pipeline + guarded delete dry-run), con confini espliciti"
risk_class: INTERNAL (sourcing/ranking/evidence + dry-run delete tool). LIVE actions (real delete, publish, live listing edit, destructive Airtable) = SEPARATE GO required, NOT in scope.
status: in_progress
---

# MISSION — US-Warehouse Sourcing Pipeline + Guarded Draft-Delete (dry-run)

## Owner mandate (verbatim boundaries)
**PRIORITÀ 1 — US-WAREHOUSE SOURCING PIPELINE.** Crack the AutoDS marketplace category/keyword
filter API → clean shortlist. Target: US warehouse only · shipping 1–5d preferred · generic/VeRO-clean ·
no obvious brands · no Amazon-branded replacement if it raises risk · clusters: Pool/Water, Kitchen utility,
Meat/Food prep, useful commodity. **No publish live, no live listing creation — only sourcing/ranking/evidence/output.**
Output columns required: product · supplier/source · warehouse · shipping time · cost · est. price · est. margin ·
VeRO risk · eBay policy risk · source/evidence · recommendation TEST/HOLD/KILL.

**PRIORITÀ 2 — DRAFT-DELETE GUARDED TOOL (dry-run only).** Don't delete anything yet. Mandatory keep-list
(2 Kitchen to evaluate). Kill-list (5 proposed KILLs). Dry-run must show exactly which drafts would be deleted,
each with ID · title · kill reason · risk · rollback possible/not. **Stop before the real delete.**

**SEPARATE GO required for:** real draft delete · publish new products · live listing edit · destructive Airtable update.

**ALSO:** save permanent rule "US warehouse first / no China warehouse when item-location US creates policy mismatch"
in machine learning/rules · update report with FACT/ESTIMATE/UNKNOWN · final git status + commit hash + PR if needed.

## Constitution rules in force
§0.3 GO gate (per-action; live=blocked) · §0.4 evidence labels · §0.9 clock rule · §AUTONOMIA STOP&ASK after 2 failures
· §AUTONOMIA error→ERROR_REGISTRY · §0.7 commit local at start/end (no push without GO) · firewall (project-sealed).

## Phases (timeboxed)
- [ ] P0  Mission on disk + start commit.                                          (done at write)
- [ ] P1a Build `marketplace_filter_probe.py` — capture request method/url/post_data of marketplace/api/products.
- [ ] P1b Run probe (read-only, GO_AUTODS_READ_SESSION) → inspect filter request shape.
- [ ] P1c Build filtered pull (replay filter via authenticated ctx.request: US-WH + clusters) + paginate + collect.
- [ ] P1d Parse + rank → write shortlist output file (all required columns + FACT/ESTIMATE/UNKNOWN).
- [ ] P2a Re-pull LIVE drafts (read_draft_economics + read_draft_errors) → current IDs/titles/error_list.
- [ ] P2b Build `delete_drafts_guarded.py` — keep/kill config, HARD GUARD, dry-run default, per-draft report, confirm hard-gated.
- [ ] P2c Run dry-run → capture real output (the exit proof).
- [ ] P3  Save permanent US-warehouse-first rule in 07_LEARNING/sop_improvements.md.
- [ ] P4  Update triage report with FACT/ESTIMATE/UNKNOWN section.
- [ ] P5  git add+commit (local) → report status + commit hash. (push/PR only on owner GO.)

## Exit proof (defined before completion)
1. A committed shortlist file with the required columns, produced by a reader that actually captured the
   marketplace filter request shape (evidence cached). If the filter can't be cracked in ≤2 tries → honest
   UNKNOWN + best-effort from the captured feed, clearly labeled.
2. A committed dry-run delete tool whose REAL run output lists the kill drafts (ID/title/reason/risk/rollback)
   + keep-list, reconciled against LIVE drafts, and which CANNOT delete without an explicit separate-GO token.
3. Permanent rule saved. Report carries FACT/ESTIMATE/UNKNOWN. git status + commit hash reported.

## Recovery log (update every step)
- 2026-06-24 02:02 — Mission written. Read manage_draft.py / remove_oos_listings.py / read_draft_economics.py /
  read_draft_errors.py / inspect_delete_dialog.py / read_marketplace.py / LEARNING_SYSTEM.md. Next: P1a build probe.
- 2026-06-24 02:06 — P1a/P1b DONE. marketplace_filter_probe.py + probe2 → **filter API cracked**:
  POST gw.autods.com/marketplace/api/products/, filters search_query/category/rating/rating_count/price; auth=Bearer.
- 2026-06-24 02:11 — P1c/P1d DONE. marketplace_source.py pulled 1669 (1077 US-WH); rank_us_source.py → 51 TEST.
  Report 10_OUTPUTS/SOURCING_REPORTS/2026-06-24_us-warehouse-sourcing-shortlist_v1.md.
- 2026-06-24 02:21 — P2 DONE. delete_drafts_guarded.py dry-run: 5 would-delete, keep-list safe, 3 retained, 0 deleted.
- 2026-06-24 02:22 — P3 DONE (L-004 US-warehouse-first in sop_improvements.md). P4 (FACT/EST/UNK in report). Cockpit refreshed.
  NEW owner intent queued: "rinnuova tutti gli annunci +2%" = live GO-CLASS → next: reprice dry-run + STOP at gate. Committing P1-P4.
- 2026-06-24 02:26 — REPRICE DRY-RUN DONE (reprice_all_dryrun.py): 96 active, total $6211.97 -> +2% $6336.25 (Δ$124.28).
  **Blocker found: price-monitoring ON for all 96** → a fixed +2% would be auto-overwritten; durable +2% = markup-rule change.
  No verified price-WRITE mechanism yet; "rinnuova" ambiguous. STOPPED at GO gate. Nothing changed. Committing reprice tool.
