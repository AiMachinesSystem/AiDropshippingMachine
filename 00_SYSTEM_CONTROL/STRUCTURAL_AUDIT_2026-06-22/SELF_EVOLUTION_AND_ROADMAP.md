---
machine: "eBay / AutoDS Dropshipping Machine"
type: self_evolution + optimization_roadmap + skill_candidates + enforcement_test_plan
phase: "Core Intelligence Architect — Phase 3"
status: complete
date: 2026-06-22
created_real: 2026-06-22
covers: SELF_EVOLUTION_PLAN + OPTIMIZATION_ROADMAP + SKILL_AND_AUTOMATION_CANDIDATES + ENFORCEMENT_AND_TEST_PLAN
---

# SELF-EVOLUTION & OPTIMIZATION — Phase 3

## A. Self-evolution plan (3 horizons)
**Short (safe internal, mostly done/queued):**
- ✅ `.gitignore` hygiene (R3) · ✅ ERROR_REGISTRY E-005/E-006 · ✅ knowledge index + audit.
- Queue: reprice winners to market (M1 read → GO apply); kill remaining 12 dead (GO); restock 13 winners (GO).
**Medium (repeatable workflows → capabilities):**
- ✅ Codified `dropship-profit-run`, `aliexpress-resourcing`, `listing-optimizer` skills.
- Data-quality gates: E-005 destructive-verify rule + canonical-numbers rule are now enforced patterns.
- Refresh process: weekly profit-run loop (pull → re-baseline → simulate → 1 improvement → log).
**Long (framework):**
- Enforce CORE→DOMAIN→CATEGORY→INSTANCE separation; remove other-domain residue (R4) once owner decides.
- Registry enforcement (every run registers in RESEARCH_MEMORY_INDEX + cockpit — already a rule).
- n8n / MCP integrations = PLAN ONLY (activation = GO).

## B. Optimization roadmap (impact-first)
1. **Reprice 13 winners to market** (3× under today) — biggest quick profit lift. [M1 read → GO]
2. **Re-source winners on AliExpress** — margin 19→45-55% + survival. [URLs → GO]
3. **Fix fulfillment** (buyer account + wallet) — unlocks all scaling. [owner GO]
4. **Kill remaining 12 dead + de-brand/delist Lian Li (VeRO)** — cut ban risk. [GO]
5. **Source deeper in pool/water cluster** (seasonal peak). [internal → import GO]
6. Cleanup: archive `_IMPORT/`+zip, untrack stray `.pyc`, resolve R4 residue. [GO]

## C. Skill & automation candidates
| Candidate | Status | Note |
|---|---|---|
| `dropship-profit-run`, `aliexpress-resourcing`, `listing-optimizer` | ✅ BUILT | this session |
| `promoted-listings-planner` | **STUB (not built)** | ads gated + not imminent (anti-overbuilding) |
| `catalog-health-monitor` (auto-flag OOS/error/VeRO) | RECOMMENDED | wraps `audit_listings.py`; build when run cadence justifies |
| Weekly profit-run via `/schedule` or `/loop` | PLAN ONLY | scheduling/automation = GO; needs operational store first |

## D. Enforcement & test plan
- **Anti-contamination test:** before any cross-domain reference, assert source domain == active machine; flag `n8n_digital_products`/`shopify` residue (R4) until owner rules. (n8n half ruled and archived 2026-09-08 — see `99_ARCHIVE/MISPLACED__n8n_digital_products/`.)
- **Anti-overlap:** new skill must not duplicate an existing one (checked: the 3 new skills are distinct).
- **Data-quality gates:** (1) destructive actions verified by independent read (E-005); (2) market numbers only from CANONE CORRENTE; (3) freshest registered run wins on conflict (skill rule added).
- **Refresh gate:** a research/profit run is INCOMPLETE without RESEARCH_MEMORY_INDEX + cockpit update.
- **Secret gate:** secrets stay gitignored; never commit `storage_state.json`/`.env` (verified clean).
