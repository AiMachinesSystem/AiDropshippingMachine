---
machine: "eBay / AutoDS Dropshipping Machine"
type: control_hub_bootstrap
status: lean seed (anti-overbuilding applied)
date: 2026-06-22
created_real: 2026-06-22
---

# CONTROL HUB — Bootstrap Report (lean)

> The Orchestrator spec requested ~40 control files. Per its own rule ("non creare caos / non duplicare / non automazioni premature") and constitution §9, I built a **lean hub that points to existing work** instead of duplicating it. Stubs with no near use are declared, not generated.

## What already exists (Phases 0-3 = DONE, do not rebuild)
- **Structural audit / knowledge index / risk register / next-actions:** `00_SYSTEM_CONTROL/STRUCTURAL_AUDIT_2026-06-22/` (9 files: STRUCTURE_AUDIT, UNIVERSAL_KNOWLEDGE_INDEX, RISK_AND_GAP_REGISTER, NEXT_ACTIONS_INTERNAL, DATA_INVENTORY_AND_SOURCE_QUALITY, INTELLIGENCE_AND_PATTERNS, MISSING_DATA_REGISTER, SELF_EVOLUTION_AND_ROADMAP, OWNER_GO_DECISION_PACK).
- **Kernel/registries/playbooks:** `00_SYSTEM_CONTROL/` (VISION_ALIGNMENT, RESEARCH_MEMORY_INDEX, ERROR_REGISTRY, MASTER_DASHBOARD, NEXT_ACTIONS, PLAYBOOKS/EBAY_DROPSHIP_PROFIT_MASTERY).

## What this hub ADDS (genuinely new, non-duplicative)
- `00_SYSTEM_CONTROL/KERNEL_PRINCIPLES.md` — the extracted governing rule-set (pointer to CLAUDE.md).
- This bootstrap report + the health scorecard + source-of-truth register below.

> **Moved 2026-09-08.** This report and `KERNEL_PRINCIPLES.md` were written into a top-level
> `_CONTROL_HUB/` directory that the vault map in `CLAUDE.md` does not declare. They now live under
> `00_SYSTEM_CONTROL/` (this report inside the structural-audit folder it describes); the empty
> `_CONTROL_HUB/` was removed. Content unchanged.

## MACHINE HEALTH SCORECARD (0-100, INFERRED from audit 2026-06-22)
| Dimension | Score | Why |
|---|---|---|
| Structural clarity | 75 | clear vault; stale dups (`_IMPORT`) + cross-domain residue |
| Evidence discipline | 90 | strong labeling + registries |
| Data availability | 45 | walls: eBay 403, AliExpress CAPTCHA → LOW-SAMPLE |
| Risk control | 80 | gates, firewall, error registry; secrets clean |
| Automation readiness | 35 | fulfillment broken, AutoDS trial expired, price tool fragile |
| Execution maturity | 60 | publish works; reprice/price-set not yet tooled |
| Measurement maturity | 40 | baseline exists but LOW-SAMPLE; no live metrics feed |
| Learning loop | 70 | error registry + playbook + weekly loop defined |
| Documentation | 85 | rich registries/reports |
| Maintainability | 65 | good structure; some bloat/dups |
| Context efficiency | 55 | large vault; `.venv` bloat (124MB, untracked) |
| **Overall** | **~63** | viable; bottleneck = data availability + automation readiness |

## SOURCE-OF-TRUTH REGISTER (which file is canonical)
| Topic | Source of truth | NOT current |
|---|---|---|
| Catalog state | `RESEARCH_MEMORY_INDEX` owned-store block (post-kill: 99 live) | `autods_status_report` (214-era), audit_2026-06-17 |
| Winner economics | `audit_2026-06-22_044324/_products_list.json` (variation_statistics) | — |
| Profit canon | `PLAYBOOKS/EBAY_DROPSHIP_PROFIT_MASTERY.md` | older strategy docs |
| Errors/walls | `ERROR_REGISTRY.md` (E-001..E-006) | — |
| Owner decisions pending | `STRUCTURAL_AUDIT_2026-06-22/OWNER_GO_DECISION_PACK.md` | — |

## STAGED — NOT built (anti-overbuilding; build on real need + owner nod)
Activation manifests (DEFAULT/AUDIT/EXECUTION/MAINTENANCE), full contracts set, automation staging registry, resource-orchestration policy, the remaining ~30 named files. **Reason:** no near use; would duplicate existing governance. Available on request.

## Owner decisions (see existing OWNER_GO_DECISION_PACK)
Unchanged: D1 firewall residue, D2 Lian Li VeRO, D3-D7 live business moves, D8 commit, D9-D11 hygiene.
