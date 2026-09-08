---
machine: "eBay / AutoDS Dropshipping Machine"
type: structure_audit
phase: "Core Intelligence Architect — Phase 1"
status: complete
date: 2026-06-22
created_real: 2026-06-22
scope: active machine root only (firewall: poker/trading/other machines NOT touched)
evidence: PowerShell recursive scan 2026-06-22 (counts/sizes OBSERVED)
---

# STRUCTURE AUDIT REPORT — Phase 1

> Snapshot of the active machine. Read-only map; no rename/move/delete performed (git = reversible snapshot; 18 uncommitted = this session's work).

## Top-level map (OBSERVED 2026-06-22)
| Block | Files | Size | Role | Layer | State |
|---|---|---|---|---|---|
| `00_SYSTEM_CONTROL` | 44 | 0.2MB | governance: vision, registries, playbooks, dashboard, mission state | core-local | ACTIVE |
| `01_SYSTEM` | 4 | — | optional detailed protocols | core-local | thin |
| `02_DATA` | 18 | 0.1MB | data + routines (MASTER_ROUTINE dispatcher) | instance | ACTIVE |
| `03_ANALYSIS` | 9 | 0.1MB | analyses + `simulations/` (new: 3 Monte Carlo) | instance | ACTIVE |
| `04_STRATEGY` | 4 | — | strategy docs (profitability canon) | instance | ACTIVE |
| `05_EXECUTION` | 1390 | **124.8MB** | the eBay/AutoDS project; **dominated by `integrations/autods/playwright/.venv`** (13 .exe=89MB, 559 .py, 517 .pyc) | instance | ACTIVE+bloat |
| `06_MEASUREMENT` | 2 | — | stub (activate on metrics) | instance | STUB |
| `07_LEARNING` | 3 | — | stub | instance | STUB |
| `08_SCALING` | 2 | — | stub | instance | STUB |
| `09_TEMPLATES` | 11 | — | reusable output templates | core-local | ACTIVE |
| `10_OUTPUTS` | 29 | 0.2MB | dated reports + `n8n_digital_products/` (⚠ other-domain residue — archived 2026-09-08 to `99_ARCHIVE/MISPLACED__n8n_digital_products/`) | instance | ACTIVE |
| `90_CACHE` | 210 | 29.6MB | evidence cache (gitignored) | staging | ACTIVE |
| `_IMPORT` | 42 | 0.2MB | **full nested duplicate of original machine** + foundation | import/stale | STALE |
| `_ARCHIVE` / `99_ARCHIVE` | 1 / 12 | 0.1MB | milestone/deprecated readable copies | archive | OK |
| `_tmp` | 1 | — | ephemeral scratch | staging | OK |
| `.claude` | 20 | 0.1MB | local skills/settings | core-local | ACTIVE |
| `docs` | 1 | — | docs | misc | thin |
| root files | — | — | CLAUDE.md, PROJECT_INDEX.md, README(_TEMPLATE).md, **ebay_autods_dropshipping_machine.zip** (import zip, stale) | — | mixed |

## Layer classification (firewall CORE→DOMAIN→CATEGORY→INSTANCE)
This is a single **INSTANCE** machine (eBay/AutoDS dropship). No domain/category packs live here. Governance (`00_SYSTEM_CONTROL`, `09_TEMPLATES`, `.claude`) is local-core for this instance. No cross-domain assumptions should be absorbed upward.

## Git state
- Repo local, branch `master`. **18 uncommitted changes = this session** (registries, playbook, simulations, 5 pre-existing untracked playwright scripts, 4 reports, scratch). No checkpoint commit yet (see NEXT_ACTIONS_INTERNAL).
- Secrets (`.env`, `autods_credentials.env`, `storage_state.json`): **git-ignored, 0 tracked** (verified). `.venv`: 0 tracked. 1 stray `.pyc` tracked.
