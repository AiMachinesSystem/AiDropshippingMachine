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
