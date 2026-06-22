---
machine: "eBay / AutoDS Dropshipping Machine"
type: risk_gap_register
phase: "Core Intelligence Architect — Phase 1"
status: complete
date: 2026-06-22
created_real: 2026-06-22
---

# RISK & GAP REGISTER — Phase 1

> Each item: severity · evidence · classification (EXECUTED / STAGED / RECOMMENDED / NEEDS OWNER GO).

| ID | Severity | Finding | Evidence | Classification |
|---|---|---|---|---|
| R1 | LOW (contained) | Live secrets present (`.env`, `autods_credentials.env`, `storage_state.json` = live AutoDS session) | git check-ignore = IGNORED; `git ls-files` = 0 tracked | RECOMMENDED: keep ignored; never commit storage_state |
| R2 | MED | `05_EXECUTION/.../playwright/.venv` = ~124MB (13 .exe @89MB) bloats the project dir | scan | OK (0 tracked); RECOMMENDED: confirm .venv stays gitignored |
| R3 | LOW (hygiene) | `90_CACHE/*.py` scratch scripts were not git-ignored (showed untracked) | git status `??` on `_analyze_audit.py` etc. | **EXECUTED**: added `/90_CACHE/*.py` + `/90_CACHE/sims/**` to .gitignore |
| R4 | MED (firewall) | Other-domain residue inside this eBay machine: `10_OUTPUTS/n8n_digital_products/` (Stripe/digital-product delivery), `PLAYBOOKS/n8n_workflows/03_shopify_daily_snapshot.json` | scan | NEEDS OWNER GO: confirm intentional template scaffolding vs contamination; do not act unilaterally |
| R5 | LOW | Stale duplicate: `_IMPORT/ebay_autods_initialization/...` full nested machine copy + root `ebay_autods_dropshipping_machine.zip` | scan; both already gitignored | RECOMMENDED (archive/remove = NEEDS OWNER GO — deletion boundary) |
| R6 | LOW | `06/07/08` (Measurement/Learning/Scaling) are stubs | scan (2-3 files) | OK (activate on evidence) |
| R7 | PROCESS | 18 uncommitted changes; no reversible checkpoint commit | git status | RECOMMENDED: checkpoint commit (NEEDS GO-light per owner's standing commit rule) |
| R8 | LOW | 1 stray `.pyc` tracked in git | `git ls-files *.pyc` = 1 | RECOMMENDED untrack (NEEDS GO — touches index) |

## GAPS / UNKNOWN
- **G1 [UNKNOWN]** Git *history* not scanned for past secret commits — current state is clean, but a one-time `git log` history scan would fully close R1. RECOMMENDED.
- **G2** Per-file role of the 1390 files in `05_EXECUTION` beyond `.venv` not fully enumerated (Phase 2 data-mining will cover the project's own files).
