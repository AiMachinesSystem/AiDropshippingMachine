---
machine: "eBay / AutoDS Dropshipping Machine"
type: missing_data_register
phase: "Core Intelligence Architect — Phase 2"
status: complete
date: 2026-06-22
created_real: 2026-06-22
---

# MISSING DATA REGISTER — Phase 2

| ID | Missing datum | Why needed | How to get | Label |
|---|---|---|---|---|
| M1 | Current per-SKU **sell price + landed cost** for the 13 winners | compute exact reprice deltas vs market targets | targeted AutoDS read (GO-light) — audit JSON lacks price fields | UNKNOWN (gettable) |
| M2 | **eBay aggregate sold** per niche | true demand sizing (not per-listing badge) | blocked by 403 wall; proxy via Google Shopping/AliExpress orders | NOT USABLE (walled) |
| M3 | **AliExpress per-SKU cost** for re-sourcing winners | verify ≥40% gap + real margin | CAPTCHA wall → owner URLs or visible browser | NOT USABLE (walled) |
| M4 | **Git history secret scan** | fully close R1 (past secret commits) | one-time `git log -p` scan over secret paths (read-only) | UNKNOWN (gettable) |
| M5 | **Fulfillment readiness** (buyer account + wallet) | auto-order is non-functional → can't scale | owner action (connect + fund) = GO | UNKNOWN (owner) |
| M6 | **AutoDS subscription state** post-trial-expiry | scaling tooling on/off | owner decision (trial expired 2026-06-18) | UNKNOWN (owner) |
| M7 | eBay **seller market** confirmation (US assumed) + account health/limits | policy/fee accuracy + suspension standing | owner Seller Hub read | UNKNOWN (owner) |

> M2/M3 are the structural walls that keep research LOW-SAMPLE. M1/M4 are internally gettable on a GO-light read. M5/M6/M7 are owner-only.
