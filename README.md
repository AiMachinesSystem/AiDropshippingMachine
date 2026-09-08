---
machine: "eBay / AutoDS Dropshipping Machine"
type: master_foundation
status: active
date: 2026-06-15
created_real: 2026-06-15
---

# eBay / AutoDS Dropshipping Machine — Master Foundation

This machine is a dedicated implementation of the AI Market Intelligence & Execution System for
eBay dropshipping using AutoDS.

> **Governance:** the sovereign rulebook is **[`CLAUDE.md`](CLAUDE.md)** (machine constitution:
> permanent rules §0 + controlled autonomy v0.1). The navigation hub is
> **[`PROJECT_INDEX.md`](PROJECT_INDEX.md)**. This README is the domain overview only; where it and
> `CLAUDE.md` differ, `CLAUDE.md` wins. `README_TEMPLATE.md` documents the sterile template origin
> and is kept for genealogy.

## Core Loop

```text
Data → Analysis → Strategy → Execution → Measurement → Learning → Scaling → New Data Cycle
```

## Active Phase

**Execution — live store, publishing through the eBay Sell Inventory API.**

The machine is past initialization and past the AutoDS-only phase. The last recorded launch is
batch 5 on 2026-09-04: **30 listings LIVE**, 4 blocked on item specifics, 0 system errors
(`05_EXECUTION/ebay-direct/audit/publish-outcome-20260904-batch5.md`). The write path is the
local Deno client in `05_EXECUTION/ebay-direct/`; AutoDS remains the read/source side driven by
the Playwright integration under `05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/`.

The Hard Gates below still hold — none of them is retired by the machine being live. For the
current state and the open owner decisions, read `00_SYSTEM_CONTROL/MASTER_DASHBOARD.md` and
`00_SYSTEM_CONTROL/NEXT_ACTIONS.md`, which are refreshed per run; this README is not.

## Key Files

| Component | File |
|---|---|
| Machine Constitution | CLAUDE.md |
| System Blueprint | 01_SYSTEM/SYSTEM_BLUEPRINT.md |
| Operating Rules | 01_SYSTEM/OPERATING_RULES.md |
| Approval Gates | 00_SYSTEM_CONTROL/APPROVAL_GATES.md |
| Current Status | 00_SYSTEM_CONTROL/CURRENT_STATUS.md |
| Module Index | 00_SYSTEM_CONTROL/MODULE_INDEX.md |
| Next Actions | 00_SYSTEM_CONTROL/NEXT_ACTIONS.md |
| Data Map | 02_DATA/DATA_MAP.md |
| Source Discovery Plan | 02_DATA/00_SOURCE_DISCOVERY/SOURCE_DISCOVERY_PLAN.md |
| Missing Owner Inputs | 02_DATA/03_MISSING_DATA/MISSING_OWNER_INPUTS.md |
| Risk Map | 03_ANALYSIS/RISK_MAP.md |
| KPI Map | 06_MEASUREMENT/KPI_MAP.md |
| Execution Gate Structure | 05_EXECUTION/EXECUTION_GATE_STRUCTURE.md |
| Learning System | 07_LEARNING/LEARNING_SYSTEM.md |
| Scaling Gate | 08_SCALING/SCALING_GATE.md |
| Initialization Report | 10_OUTPUTS/SYSTEM_REPORTS/2026-06-15_ebay-autods-initialization-foundation_report_v1.md |

## Hard Gates

- External research requires owner approval.
- Account login/access requires owner approval.
- Live platform changes require explicit owner GO.
- Publishing listings requires explicit owner GO.
- AutoDS configuration changes require explicit owner GO.
- Supplier orders/payments require explicit owner GO.
- Scaling is forbidden until measurement validates performance and risk stability.
