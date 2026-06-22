---
machine: "eBay / AutoDS Dropshipping Machine"
type: data_inventory + source_quality_register
phase: "Core Intelligence Architect — Phase 2"
status: complete
date: 2026-06-22
created_real: 2026-06-22
covers: DATA_INVENTORY + SOURCE_QUALITY_REGISTER
---

# DATA INVENTORY & SOURCE QUALITY — Phase 2

> Internal data sources of the active machine, each labeled: OBSERVED / SOURCED / INFERRED / STALE / NOT USABLE.

## Registries & state (`00_SYSTEM_CONTROL`)
| Source | Role | Label |
|---|---|---|
| `RESEARCH_MEMORY_INDEX.md` | canon of all research runs + owned-store block | **OBSERVED** (current) |
| `ERROR_REGISTRY.md` (E-001..E-006) | learned failures + rules | OBSERVED |
| `PLAYBOOKS/EBAY_DROPSHIP_PROFIT_MASTERY.md` | profit canon + Sector Canon 2026 | OBSERVED/SOURCED |
| `NEXT_ACTIONS.md` / `MASTER_DASHBOARD.md` / `MACHINE_STATE.md` | cockpit/state | OBSERVED |

## Cleaned data (`02_DATA/02_CLEANED_DATA`)
- `fee_table.md` · `policy_risk_table.md` · `autods_features_table.md` — **SOURCED** (eBay/AutoDS public, run 2026-06-15; US-mirror; market UNCONFIRMED). Aging → verify if cited as current.

## Reports (`10_OUTPUTS`)
| Source | Label |
|---|---|
| `autods_status_report.md` (2026-06-16) | OBSERVED (account), partly **STALE** (catalog 214→99 since) |
| `ANALYSIS_REPORTS/2026-06-22_*` (profitability, per-SKU, sourcing, reprice) | OBSERVED+INFERRED (sims = ESTIMATE/LOW-SAMPLE) |
| `MARKET_RESEARCH_REPORTS/2026-06-20..21_*` | OBSERVED (run-dated); catalog parts superseded by 06-22 |
| `SYSTEM_REPORTS/2026-06-15_*` (foundation, data-collection, intake, stabilization) | OBSERVED (historical) |

## Execution data (`05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH`)
- 46 Playwright scripts (audit/import/publish/remove/login) — **OBSERVED**, working tooling.
- `listings/`: `listing_audit_actions_2026-06-17.csv`, `autods_import*.csv`, `ebay_listing_schema.json`, `sample_5_listing_input.csv` — OBSERVED; the 2026-06-17 audit CSV is **STALE** (pre-kill 214-era).
- `storage_state.json` — live AutoDS session (sensitive, ignored). **OBSERVED** valid (used 2026-06-22).

## Cache evidence (`90_CACHE/fetches`)
| Source | Label |
|---|---|
| `autods/audit_2026-06-22_044324` (post-kill per-SKU) | **OBSERVED — freshest catalog truth** |
| `autods/audit_2026-06-22_041033` (pre-kill) | OBSERVED (snapshot) |
| `autods/audit_2026-06-17_*`, `products/run/marketplace_2026-06-16/17` | **STALE** (pre-kill) |
| `web/2026-06-22_dropship-sector-research.md` | **SOURCED** (9 public URLs, cited) |
| `ebay/`, `aliexpress/` | partial; eBay sold = NOT USABLE (403), AliExpress cost = NOT USABLE (CAPTCHA) |
