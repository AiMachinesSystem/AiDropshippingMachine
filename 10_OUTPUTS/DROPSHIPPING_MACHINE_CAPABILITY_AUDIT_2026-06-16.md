---
machine: "eBay / AutoDS Dropshipping Machine"
type: capability_audit
status: complete
scope: read-only audit of this repo/vault only
date: 2026-06-16
created_real: 2026-06-16
method: index-first read of 178 tracked files + git; multi-agent read-only audit (5 subsystem readers + 2 adversarial verifiers, Explore agents = structurally cannot write); every claim cites a file path. No live/external actions; no installs; no pushes; nothing else modified.
forbidden_respected: no live AutoDS/eBay actions; no list/publish/edit/delete/buy/order/message; no new credentials; no governance edits; no refactor; no package install; no push; no invented capabilities.
---

# DROPSHIPPING MACHINE CAPABILITY AUDIT

> Evidence labels: **[OBSERVED]** = directly read in a file/git this run · **[INFERRED]** = reasoned from observed facts · **not proven** = claimed but not independently verifiable read-only. Capability grades: **BUILT** (works / proven artifact) · **PARTIAL** (scaffold/incomplete) · **PLANNED** (documented only, not operational) · **MISSING**.

## 1. Executive Truth

**What it can actually do now (proven):**
- Run a **governance-controlled research / planning / analysis workspace**: missions-to-disk, GO gates, evidence labels, error registry, git audit trail — all real and followed [OBSERVED: CLAUDE.md, GO_GATES.md, ACTION_LOG.md, ERROR_REGISTRY.md].
- **Read live AutoDS account data, read-only, via Playwright** — proven 2026-06-16 (store `Divinit-92-Us`/<AUTODS_STORE_ID>, 214 listings, 11 drafts, 23 orders) [OBSERVED: 10_OUTPUTS/autods_status_report.md, integrations/autods/playwright/*.py].
- Produce **evidence-graded analysis** (eBay policy/fee/feature) and **listing drafts** (7 draft files + import CSVs + JSON schema + validation checklist) [OBSERVED: 03_ANALYSIS report, 05_EXECUTION/.../listings/].
- Maintain **durable markdown+git memory** (machine state, dashboards, decision/action logs) [OBSERVED].

**What it cannot do yet:** import to AutoDS, publish to eBay, reprice, or auto-order — **nothing has ever been sold or published**. There is **zero live selling automation in operation**. All execution gates are CLOSED [OBSERVED: GO_GATES.md].

**What is blocked:** (a) AutoDS **REST API** path = application-gated + **paid**, no key issued [OBSERVED: AUTODS_API_READINESS.md]; (b) Strategy/Execution phases = waiting on **owner GO + missing economics/supplier data** [OBSERVED: CURRENT_STATUS.md]; (c) the connected AutoDS account's **auto-ordering is ON but non-functional** (0 buyer accounts, $0 wallet) and on a **trial expiring 2026-06-18**.

**What is only planned/theoretical:** n8n automation (blueprints, `active:false`, placeholder creds), automated repricing, Google Sheets/Drive (absent), unit tests (absent). The 14 "skills" are **prompt-SOPs that have never been run on a real business case** (RESEARCH_MEMORY_INDEX holds 1 entry, the policy analysis — zero market/niche runs).

**One-line truth:** this is a **real, disciplined research-and-planning machine with a proven read-only AutoDS reconnaissance capability and a launch pack in draft — but a 0%-operational revenue engine.** It is gated, not broken.

## 2. Current Machine Identity
- **Project name:** eBay / AutoDS Dropshipping Machine [OBSERVED: CLAUDE.md line 3].
- **Root folder:** `C:\AI Machine ebay-autoDS\AiDropshippingMachine` (git repo, branch `master`).
- **Purpose:** research → validate → launch → manage → measure → improve → scale an eBay dropshipping business via AutoDS [OBSERVED: CLAUDE.md].
- **Dropshipping model assumed:** AutoDS-sourced products listed on eBay; supplier catalogue noted as retailer-heavy (Amazon/AliExpress) — flagged as a policy tension vs eBay's retail-arbitrage rule [OBSERVED: 03_ANALYSIS policy analysis; live account shows supplier "Amazon US"].
- **Target platforms:** eBay.com (US market, USD) primary; AutoDS secondary; suppliers tertiary [OBSERVED].
- **Owner / live-action boundary:** owner = Luca; **every live/external action requires explicit per-action GO** (approval never transfers) [OBSERVED: CLAUDE.md §3, APPROVAL_GATES.md, GO_GATES.md].

## 3. Real Capabilities Matrix
*(Conservative consolidation of 2 independent verifiers; where they disagreed I took the stricter grade.)*

| Capability | Status | Evidence | Risk | Notes |
|---|---|---|---|---|
| AutoDS connector (REST API) | **PLANNED** (connector code MISSING) | AUTODS_API_READINESS.md (paid/app-gated, no key); AUTODS_API_CLIENT_SPEC.md; `autods_readonly_test.py` is a stdlib **scaffold** (GET-only, never run) | HIGH | Spec verified from public OpenAPI; **no working client**; gate `GO_AUTODS_API_READ_ONLY_TEST` CLOSED. One verifier graded this MISSING. |
| AutoDS connector (Playwright/browser, read-only) | **BUILT** | `integrations/autods/playwright/*.py` (5 scripts); `autods_status_report.md` proves a 2026-06-16 live read (214/11/23) | LOW | Operational, read-only only (no write methods). venv local/gitignored, reversible. |
| eBay workflow (publish/list mgmt) | **PLANNED** | `ebay_listing_schema.json`, 7 drafts, `autods_import.csv`, `LISTING_VALIDATION_CHECKLIST.md` — all `validation_status=draft`; gate `GO_PUBLISH_5` CLOSED | MED | Draft-ready, never published; no row has passed all 12 validation checks. |
| Product research (market intel) | **PARTIAL** | `niche-intelligence-run` SKILL.md exists (SOP); **0 niche runs executed**; RESEARCH_MEMORY_INDEX has no market entry | LOW | Tooling = prompt-SOP only; capability unproven on real data. |
| Supplier/source research | **PARTIAL** | `competitor-scan`/`ads-library-scan` SKILL.md (SOPs); jina proxy documented; **0 runs executed** | LOW | Same: SOP exists, never exercised. |
| Listing creation | **PARTIAL** | 7 listing **draft artifacts** exist (manual); import CSV + schema built; automated import/publish PLANNED + gated | MED | Drafting is manual; no automated draft→publish; gates CLOSED. |
| Pricing logic | **PARTIAL** | drafts carry `est_margin` (34–59%, [ESTIMATE]); `offer-diagnosis` SOP; AutoDS UI pricing read (27% / $7 min / .97) | MED | Estimates + SOP; **no automated repricing**; no live supplier-cost verification. |
| Policy/fee awareness | **BUILT** | `2026-06-15_ebay-autods-policy-fee-feature_analysis_v1.md` (21 cached sources, A–D graded); `02_DATA/02_CLEANED_DATA/fee_table.md` (FVF ~13.6%) | LOW | Complete, evidence-graded, analysis-only (no strategy). |
| Credential gate | **BUILT** | `.gitignore` blocks `.env/*.key/credentials.json/storage_state.json`; `git check-ignore` confirms; scripts exit 2/3 if creds missing; `SECRETS_POLICY.md` | LOW | Real secrets present on disk but **gitignored & uncommitted**; fail-safe enforced. |
| Live-action GO gate | **BUILT** (declared, not code-locked) | CLAUDE.md §3; `GO_GATES.md` (6 gates, all CLOSED); `APPROVAL_GATES.md` (32 actions); ACTION_LOG = 30 rows, all "Live Changes: No" | LOW | Honor-system + git audit trail; no runtime lock. Zero violations observed. |
| Tests | **PARTIAL** | No pytest/conftest. Only connectivity probes (`smoke_test.py` PASS per report; `autods_readonly_test.py` never run). `DRY_RUN_TEST_REPORT.md` = 15/15 **mock** gate checks PASS | MED | **No unit tests on business logic.** QA proves gate structure on mock data only. |
| Obsidian/Git memory | **BUILT** (git/markdown) | git history (19 commits, mission prefixes, no force-push); MACHINE_STATE / MASTER_DASHBOARD / DECISION_LOG / ACTION_LOG / RESEARCH_MEMORY_INDEX | LOW | Obsidian itself optional (no `.obsidian/`, gitignored) → vault is plain portable markdown. Dashboard ~1 day stale. |
| Google Sheets/Drive | **MISSING** | grep: no `gspread`/`googleapis`/oauth in repo | NONE | Not implemented, not documented. |
| Browser/scraper tools | **BUILT** (Playwright) / PARTIAL (jina) | Playwright proven 2026-06-16; `r.jina.ai` documented in `PLAYBOOKS/jina-method.md` + n8n blueprint but **not yet invoked in code** | LOW | Playwright = real; jina = documented, unexercised. |
| n8n automation | **PARTIAL** | n8n blueprint + credential-setup + payload template (05_EXECUTION/.../n8n/ and PLAYBOOKS); `active:false`, placeholder creds, API node DISABLED | LOW | Blueprint only; no n8n server installed/connected. |

## 4. Evidence Inventory (most important artifacts)

| Path | Purpose | Works? | Tested? | Touches external? | Safe? |
|---|---|---|---|---|---|
| `CLAUDE.md` | Constitution / operating rules | yes (declarative) | n/a | no | yes |
| `00_SYSTEM_CONTROL/` (GO_GATES, APPROVAL_GATES, ACTION_LOG, DECISION_LOG, ERROR_REGISTRY, MACHINE_STATE, MASTER_DASHBOARD) | Governance + audit trail | yes | n/a | no | yes |
| `00_SYSTEM_CONTROL/VISION_ALIGNMENT/SCHEMA/GAP_MATRIX.md` | Vision framework | **sterile templates** (deferred by owner, DECISION_LOG 2026-06-15) | n/a | no | yes |
| `integrations/autods/playwright/{smoke_test,login_and_save_session,read_autods_status,read_products_counts,read_drafts_count}.py` | Read-only AutoDS browser automation | yes (read proven 2026-06-16) | smoke PASS (per report; not independently re-verified read-only) | **yes** (AutoDS, read-only) | yes (no writes, no secret printing, gitignored session) |
| `integrations/autods/autods_readonly_test.py` | AutoDS REST API GET probe | parses; **never run** (API paid-gated) | py_compile PASS only | would (read-only) | yes (fails safe w/o creds) |
| `integrations/autods/AUTODS_API_READINESS.md` | API blocker documentation | yes | n/a | no | yes |
| `10_OUTPUTS/autods_status_report.md` | Live account read-only report | yes (real data) | n/a | derived from external read | yes |
| `03_ANALYSIS/2026-06-15_ebay-autods-policy-fee-feature_analysis_v1.md` | Policy/fee/feature analysis | yes (output exists) | n/a | from cached public sources | yes |
| `05_EXECUTION/.../listings/drafts/01..07_*.md` + `ebay_listing_schema.json` + `autods_import.csv` | Listing draft pack | drafts exist, **unvalidated** | not validated | no | yes |
| `06_MEASUREMENT/KPI_MAP.md` + tracker | KPI framework | template (empty) | n/a | no | yes |
| `08_SCALING/SCALING_GATE.md` | Scaling readiness gate | template (locked) | n/a | no | yes |
| `.claude/skills/*/SKILL.md` (14) | Prompt-SOP skill layer | specs only; **0 real runs** (1 = portfolio-review STUB) | n/a | varies (gated) | yes |
| `05_EXECUTION/.../n8n/*` | Automation blueprint | not connected | n/a | would | yes (disabled) |

## 5. External Platform Status

### AutoDS
- **Connection:** read-only via **Playwright browser session is LIVE and proven** (`storage_state.json`, reused 2026-06-16). REST API path **not connected**. [OBSERVED]
- **Credentials:** AutoDS login creds + saved session exist **locally, gitignored** (never committed). No REST API key. [OBSERVED]
- **API availability:** REST API is **application-gated + paid**; no read-only free scope; **blocked** until owner applies/pays. [OBSERVED: AUTODS_API_READINESS.md]
- **Can do without API creds:** read store status, catalog counts, drafts, orders, pricing/auto-order settings via Playwright (read-only). [OBSERVED]
- **Requires owner action / paid access:** any **write** (import/publish/reprice/order) and the REST API path; auto-ordering needs buyer account + wallet funding; trial **expires 2026-06-18**.

### eBay
- **Connection:** **none direct.** eBay is reached only indirectly (AutoDS manages the eBay store; listings are read via AutoDS, which surfaces eBay item IDs). [OBSERVED]
- **Can anything be published now?** **No.** 7 drafts are import-ready but unvalidated/unpublished; `GO_IMPORT_5_DRAFTS` and `GO_PUBLISH_5` are CLOSED. [OBSERVED]
- **Live action blocked by GO gate?** Yes — and additionally by missing validation + owner GO. [OBSERVED]

### Google Sheets / Drive / Obsidian / GitHub
- **Google Sheets/Drive:** **MISSING** (no code, no docs). [OBSERVED]
- **Obsidian:** vault is **Obsidian-compatible markdown**, but there is **no functional Obsidian instance** (`.obsidian/` gitignored). Works in any editor. [OBSERVED]
- **GitHub/Git:** **local git is the real memory/rollback layer** (19 commits, clean, no force-push). No CI, no `.github/`, no push automation; no remote operations performed. [OBSERVED]

## 6. Safety & Live-Action Boundaries
- **Require explicit owner GO** (per-action): AutoDS/eBay/supplier writes, logins/credential use, imports, publishes, repricing, auto-ordering, any spend, external posting. [OBSERVED: GO_GATES.md, APPROVAL_GATES.md]
- **Safe internal (no GO):** reading files, analysis, drafting, internal reports, and — as demonstrated this session — **read-only** AutoDS navigation under an explicit read GO.
- **Dangerous accidental-live path?** Low. Write scripts do not exist for AutoDS writes; the Playwright scripts are read-only by contract (login script is the only one that authenticates and is owner-GO-gated). n8n nodes are `active:false`/DISABLED. **Residual risk:** GO gate is honor-system (not code-locked), and a live AutoDS session (`storage_state.json`) exists on disk — a future careless write-script could act with it. [INFERRED]
- **Do credential gates fail safe?** **Yes** — all scripts exit non-zero with a clear message when creds are missing; secrets are gitignored. [OBSERVED]

## 7. Test Results
- **Tests found:** no formal suite (no pytest/conftest/`test_*`). Two **connectivity probes** (`smoke_test.py`, `autods_readonly_test.py`) and one **mock QA** report (`DRY_RUN_TEST_REPORT.md`, 15/15 gate checks PASS on mock data). [OBSERVED]
- **Tests run this audit:** none executed (mandate forbids network/credential execution). `python -m py_compile` was used by the audit agents to confirm all 6 scripts **parse cleanly**. [OBSERVED]
- **What they prove:** the gate architecture holds against a mock scenario; the scripts are syntactically valid and declare read-only contracts. The Playwright read path is independently corroborated by the real data in `autods_status_report.md`.
- **What they do NOT prove:** any business logic correctness (zero unit tests); real economic viability (mock margins); and the documented `smoke_test PASS` is from the README/report, **not independently re-verified** in this read-only audit.

## 8. Gaps / Missing Pieces

**Critical blockers (stop it being useful as a *seller*):**
- No live selling path active: import/publish/reprice/auto-order all CLOSED + unexercised. [OBSERVED]
- Auto-ordering on the live account is **non-functional** (0 buyer accounts, $0 wallet); **trial expires 2026-06-18**. [OBSERVED]
- AutoDS REST API blocked by **paid activation**; the only working live path is Playwright (read-only today). [OBSERVED]
- Strategy phase blocked: **no chosen niche, no supplier economics, no owner GO**. [OBSERVED]

**Capability gaps:** no automated listing creation/validation runner; no repricing engine; skills never executed on a real case (product/competitor/ads research = 0 runs); no jina invocation in code.

**Governance gaps:** GO gate not code-enforced (honor-system); MASTER_DASHBOARD ~1 day stale vs AUTO-REFRESH rule; only 1 error-registry entry / 1 regression test; cold-verification rule declared but exercised once.

**Data gaps:** no market/niche/competitor data (DATA_MAP: ~2–3 of 38 types collected); supplier costs [OBSERVED] for 6/7 SKUs, 1 [ESTIMATE]; no real KPI/order data; account-health of the live store not enumerated (LOW-SAMPLE).

## 9. Realistic Operating Modes Available Now
- **Mode A — Read-only market/analysis research** (web + cached sources + the analysis/skills SOPs): available; produces evidence-graded reports. *Caveat: skills unproven on real niches.*
- **Mode B — Listing draft generation** (drafts + schema + import CSV): available; outputs remain `validation_status=draft`.
- **Mode C — Read-only AutoDS reconnaissance via Playwright**: available and **proven** (store status, catalog, orders, settings).
- **Mode D — AutoDS REST API dry-run**: **NOT available** (paid gate, no key).
- **Mode E — Live import/publish/reprice/auto-order**: **BLOCKED** until explicit GO + validation + (for auto-order) buyer account & funds.

## 10. Recommended Next Step
1. **Next best action:** Run a **per-status health tally of the existing 214 live listings + 11 drafts** (read-only Playwright) — the store already has a real catalog and 23 orders, so the highest-value truth is "what's actually healthy/selling/broken right now," not more planning.
2. **Why:** It uses the one proven live capability (read-only Playwright), needs no new GO beyond the read session already authorized, and turns "214/11" into an actionable picture (OOS, on-hold, supplier-error, VeRO) before the trial expires 2026-06-18.
3. **Exact command:** `cd 05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/integrations/autods/playwright && .venv\Scripts\python.exe read_autods_status.py "https://platform.autods.com/products"` (then extend the reader to page through statuses).
4. **Expected output:** a status breakdown (active / OOS / on-hold / error counts) + the VeRO-flagged draft, cached to `90_CACHE` and summarized.
5. **Stop condition:** stop at any write control (Bulk Edit/Delete/Relist/Import/Publish) — those need explicit GO.

## 11. Final Verdict
- **Operational?** As a **research/planning/governance + read-only AutoDS reconnaissance** system: **yes**. As a **selling/dropshipping automation**: **no**.
- **Partially operational:** correct — strong control plane + analysis + a proven read-only data path; execution stack is scaffold/gated.
- **Mostly a scaffold?** The **revenue engine** is scaffold/planned; the **knowledge & control layer** is genuinely built and used.
- **% real vs planned [INFERRED]:** ~**60%** real & working (governance, git/markdown memory, policy/fee analysis, listing-draft pack, read-only AutoDS via Playwright); ~**40%** scaffold/planned (live execution, REST API connector, n8n, repricing, automated research runs). The **money-making loop specifically is ~0% operational** (never imported/published/sold).
- **What the owner should trust it with today:** read-only research, evidence-graded analysis, draft preparation, and **read-only AutoDS account monitoring**. **Do not** trust it to publish, price, buy, or fulfil without an explicit per-action GO and human verification — and note the connected AutoDS account is a **trial expiring 2026-06-18** with **non-functional auto-ordering**.

---
*Audit method note: produced by a read-only multi-agent pass (5 subsystem readers + 2 adversarial verifiers, all Explore agents with no write capability). Both verifiers independently found **no invented capabilities**; the only over-statements corrected were the AutoDS REST API (down to PLANNED/MISSING) and Obsidian (down to PARTIAL/optional). Raw agent findings are not committed (transient).*
