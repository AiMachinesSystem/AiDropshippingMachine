---
machine: "eBay / AutoDS Dropshipping Machine"
type: learning_entry
module: 07_LEARNING
category: reusable_sop_improvements
status: active
date: 2026-06-15
---

# Learning — Reusable SOP Improvements

> Schema per `01_SYSTEM`/`07_LEARNING/LEARNING_SYSTEM.md`. Internal process learnings only
> (no market/product/strategy learning — measurement has not started).

## L-001 — Reconcile import coverage before commit

| Field | Value |
|---|---|
| Date | 2026-06-15 |
| Source action | Foundation import/merge (mission EBAY-IMPORT, commit c994aed) |
| Source KPI/report | N/A (pre-measurement; internal process) |
| What happened | A copy glob (`STERILE_BASELINE__*`) silently excluded 1 of 42 import files (`99_ARCHIVE/README.md`). Caught by a per-file reconciliation before commit; zero real impact. |
| Evidence label | [OBSERVED — reconciliation output `UNRESOLVED MISSING: 0/42`, 2026-06-15] |
| Affected module | System / 99_ARCHIVE |
| KPI impact | None (no live KPIs yet) |
| Root cause | Coverage proven by pattern instead of by full source→target inventory. |
| Prevention rule | Before committing any import/merge: run a per-file reconciliation (every source file maps to an existing target; 0 missing of N). A glob is never proof of complete coverage. Logged as ERROR_REGISTRY E-001. |
| Repeatability condition | N/A (this is an error-prevention learning, not a win) |
| SOP update needed | No new SOP. Reconciliation step folded into the import/merge checklist via E-001. |
| Scaling relevance | Not applicable (validated only). |

## L-002 — Keep the dispatcher aware of the instantiated machine

| Field | Value |
|---|---|
| Date | 2026-06-15 |
| Source action | Stabilization sprint (machine-test readiness review) |
| Source KPI/report | N/A (internal process) |
| What happened | After instantiation, `02_DATA/_ROUTINES/MASTER_ROUTINE.md` still routed only generic research intents and had no row for eBay/AutoDS operational intents or machine-status lookups, so a fresh session could mis-route an operational request. No unsafe action could result (GO gates always catch live actions), but orientation was incomplete. |
| Evidence label | [OBSERVED — MASTER_ROUTINE.md content, 2026-06-15] |
| Affected module | System / routing |
| KPI impact | None |
| Root cause | Instantiation filled module content but not the intent dispatcher for the new domain. |
| Prevention rule | When instantiating a machine, complete the intent dispatcher with: (a) the domain's operational intents → phase-discipline + gate files, and (b) a status/next-step lookup → cockpit. Live actions stay GO-gated regardless. |
| Repeatability condition | N/A |
| SOP update needed | No. Fixed in this sprint by adding 2 routing rows. |
| Scaling relevance | Not applicable. |

## L-003 — Mock/test-data isolation convention

| Field | Value |
|---|---|
| Date | 2026-06-15 |
| Source action | Internal dry-run mock-data test (DRY_RUN_MOCK_TEST mission) |
| Source KPI/report | `10_OUTPUTS/SYSTEM_TESTS/2026-06-15_dry-run-mock/DRY_RUN_TEST_REPORT.md` (15/15 PASS) |
| What happened | The machine had no explicit, written convention for where MOCK/test data lives or how it is labeled, creating a latent risk of mock data contaminating real `02_DATA`/`03_ANALYSIS` or being mistaken for business evidence. The dry-run handled isolation correctly but only by ad-hoc discipline. |
| Evidence label | [OBSERVED — dry-run test, 2026-06-15] |
| Affected module | System / test & data hygiene |
| KPI impact | None (no live KPIs) |
| Root cause | No declared test-data isolation rule in conventions. |
| Prevention rule | Mock/test data lives ONLY under `10_OUTPUTS/SYSTEM_TESTS/<date>_<slug>/`, every item labeled `MOCK DATA / NOT REAL`, never written to `02_DATA`/`03_ANALYSIS`/`RESEARCH_MEMORY_INDEX`, never treated as business evidence, never advances a real gate. |
| Repeatability condition | N/A (hygiene rule) |
| SOP update needed | Optional: fold the rule into `VAULT_CONVENTIONS` on owner request (not done now — convention proposed, not yet ratified into governance). |
| Scaling relevance | Not applicable. |

## L-004 — US-warehouse-first sourcing (no China warehouse when item-location US creates a policy/shipping mismatch)

| Field | Value |
|---|---|
| Date | 2026-06-24 |
| Source action | US-warehouse sourcing mission (MISSION_US_WAREHOUSE_SOURCING_AND_DELETE_GUARD_2026-06-24), owner GO Luca 2026-06-24 |
| Source KPI/report | `10_OUTPUTS/SOURCING_REPORTS/2026-06-24_us-warehouse-sourcing-shortlist_v1.md` + draft triage `10_OUTPUTS/ANALYSIS_REPORTS/2026-06-24_draft-portfolio-triage_vs_winning-niches_v1.md`. Evidence cache `90_CACHE/fetches/autods/mkt_source_2026-06-24_021122`. |
| What happened | The 5 AliExpress drafts could not be published: they are **CN-warehouse**, so eBay resolves a China-origin shipping service against a **US item-location** → "This shipping service is not available for this item location" (errors E-008, E-010). The item-location field would not persist via automation (E-010), so the wall could not be cleared at publish time. Cross-referencing the AutoDS Marketplace `product_details.min_price_warehouse` field showed the fix is at the SOURCE, not the listing: **US-warehouse products validate natively against a US item-location** (like the ~91 working live listings) and ship in 1–5 days vs ~22. |
| Evidence label | [OBSERVED — products API `error_list` + `item_country_location`, 2026-06-23/24] · [FACT — `min_price_warehouse` US/CN field, marketplace pull 2026-06-24] |
| Affected module | Data Source Discovery / Execution (sourcing) |
| KPI impact | Removes a hard publish-blocker (0/5 → avoidable at source); faster shipping improves conversion & defect risk. |
| Root cause | Sourcing did not constrain on warehouse; CN-warehouse + US item-location is an invalid shipping/location pair that no listing-side edit reliably fixes via automation. |
| Prevention rule | **PERMANENT SOURCING RULE — US-WAREHOUSE-FIRST.** When the eBay item-location is US, source ONLY products whose AutoDS `min_price_warehouse == "US"`. Do **not** source CN-warehouse items into a US-located store: it reproduces the China-origin-service / US-location mismatch (E-008/E-010) that automation cannot clear. Verify warehouse from the products/marketplace API (`min_price_warehouse`), never from a UI label. Prefer ship-time ≤ 5 days. Trade-off to weigh explicitly: in the AutoDS marketplace, fast US-warehouse generic commodities are predominantly `site_name == "amazon"` (retail-arbitrage account-health risk — label it `eBay-policy = MED`), whereas `aliexpress` US-warehouse items carry lower policy risk but ship 10–14 days. Choose per the owner's risk/speed preference; never hide the retail-arb risk. |
| Repeatability condition | Applies to every sourcing run while the store's item-location is US. |
| SOP update needed | Yes — folded into the sourcing toolchain: `marketplace_source.py` + `rank_us_source.py` filter on `min_price_warehouse == "US"` by default. Linked from `VISION`/sourcing playbook on next pass. |
| Scaling relevance | Validated mechanism (directly observed); safe to scale to all future sourcing. |
