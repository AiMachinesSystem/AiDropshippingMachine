---
tags:
  - machine
  - mission
type: mission
status: complete
risk_class: GO-CLASS (external public research — AUTHORIZED by owner GO 2026-06-15)
date: 2026-06-15
created_real: 2026-06-15
description: "Data collection (path B): eBay + AutoDS PUBLIC policy, fee, feature, risk, and operational-constraint research. Public web only. Stop before analysis. No account login, no live changes, no strategy, no execution."
---

# DATA_COLLECTION_PUBLIC_RESEARCH — mission (2026-06-15)

**Owner:** Luca · **GO:** "APPROVE DATA COLLECTION ONLY — PUBLIC POLICY / FEE / FEATURE RESEARCH".
**Risk class:** GO-CLASS (external research) — the GO opens the gate for THIS scope ONLY.

## Scope (authorized)
eBay + AutoDS PUBLIC policy, fee, feature, risk, and operational-constraint research, via public web pages only.

## Hard limits (from GO + constitution)
- Stop BEFORE analysis. No interpretation/scoring/verdicts/recommendations. Collect + organize + label only.
- No strategy. No execution. No account login (eBay/AutoDS/suppliers). No live platform changes. No spending.
- Public sources only (eBay Help/Seller Center, eBay fee pages, AutoDS docs). NOT in scope this run: competitor/product/market/supplier-price research (different data type).
- Evidence §0.4: every load-bearing fact = [OBSERVED — url + date (cache: path)] or [UNKNOWN] / [PUBLIC RESEARCH REQUIRED]. No invented numbers. Account/market-specific = USER INPUT NEEDED.
- CACHE rule: save each fetch to `90_CACHE/fetches/<domain>/2026-06-15_<slug>.txt` BEFORE citing. (90_CACHE is gitignored = audit trail.)
- Fees/policies are market/category/account dependent and change over time → label market + capture date; flag US-bias of search.

## Phases
1. Recon + dirs + mission (DONE).
2. Fan-out fetch (workflow): A eBay dropshipping/listing policy + VeRO/prohibited; B eBay seller-performance/account-health standards; C eBay selling fees structure; D AutoDS features/plans/suppliers/automation + compliance guidance. Each: fetch authoritative pages → cache → return labeled facts + unverified list.
3. Assemble 02_DATA: raw excerpts (01_RAW_DATA/policies, /autods_docs), cleaned tables (02_CLEANED_DATA/fee_table.md, policy_risk_table.md, autods_features_table.md), source-access notes, data-quality notes, missing-data update.
4. Verify (adversarial): every cited fact traces to a cached fetch; zero analysis/strategy leakage; market/date flags present.
5. Data intake report (10_OUTPUTS/SYSTEM_REPORTS) + cockpit AUTO-REFRESH + RESEARCH_MEMORY_INDEX + commit (no push).

## Stop condition
Data intake report delivered, stopped before analysis. Hand back to owner for Analysis authorization.

## RUN LOG
- 2026-06-15 ~21:40 — GO received (path B). Source plan read; cache+data dirs created; web tools loaded; mission recorded. Next: fan-out fetch (Phase 2).
- 2026-06-15 ~22:10 — Fetch complete: 4-agent workflow (eBay policy / standards / fees / AutoDS) + 1 supplementary agent (returns/cancellations/shipping/limits). 21 pages cached to 90_CACHE/fetches/ (verified on disk, headers present). www.ebay.com /help/ portal = fetch wall → export.ebay.com EN/IN mirrors used (logged). AutoDS pricing from Help Center (live page placeholders).
- 2026-06-15 ~22:20 — Assembled 02_DATA: 3 raw notes + 3 cleaned tables (fee/policy/feature) + source_access + data_quality + missing-data log + intake report. Cockpit refreshed (CURRENT_STATUS/NEXT_ACTIONS/MASTER_DASHBOARD/ACTION_LOG) + RESEARCH_MEMORY_INDEX registered. Next: adversarial verify → commit.

## AUTO-AUDIT (mission close)
- §0 / GO scope respected: SÌ — public web read-only only; NO login, NO account access, NO credentials, NO live changes, NO analysis, NO strategy/execution. Stopped at the data intake report.
- Evidence §0.4: every load-bearing fact [OBSERVED — url + 2026-06-15 (cache: path)]; 21 cache files written BEFORE citation (verified on disk); WebSearch-only items quarantined as unverified; ZERO invented numbers; market/category/tier dependency flagged on every figure.
- Missing data: USER INPUT NEEDED (market/account/plan) + PUBLIC RESEARCH REQUIRED (eBay.it/EU, walled US-help numerics) logged, not invented.
- Labels: constitutional §0.4 set only; extended OPERATING_RULES §3 set NOT used (quarantine respected).
- Git: commit EBAY-DATA, no push; 90_CACHE not versioned (gitignored audit trail).

DONE — 2026-06-15 ~22:25 (real clock).
