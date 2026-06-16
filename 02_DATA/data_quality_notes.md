---
machine: "eBay / AutoDS Dropshipping Machine"
type: data_quality_notes
module: 02_DATA
status: active
date: 2026-06-15
created_real: 2026-06-15
---

# Data Quality Notes — Public Research Run (2026-06-15)

> What to trust, with what caveats, before this data feeds Analysis. No analysis here — quality flags only.

## Strengths
- All [OBSERVED] facts captured verbatim from official eBay/AutoDS pages and cached (21 files) before citation.
- Exact figures retained WITH their conditions (category, tier, window, market) rather than generalized.
- Unverified / WebSearch-only items kept strictly separate from [OBSERVED] facts.

## Quality risks / limitations (load-bearing)
1. **Market dependency (highest).** Almost every fee/threshold is eBay.com (US) or EN/export-mirror text. Luca's governing eBay site (likely eBay.it / EU given Italian, but **not confirmed**) sets the real schedule. → market confirmation USER INPUT NEEDED before any figure is treated as binding.
2. **Fetch wall on www.ebay.com `/help/`.** Canonical US help pages timed out; substance came from export.ebay.com EN/IN mirrors. Mirrors are official eBay but may lag or differ in exact numerics from the live help pages → some thresholds are [PUBLIC RESEARCH REQUIRED] to re-confirm verbatim.
3. **Vendor vs primary source.** AutoDS's eBay-policy statements are AutoDS's restatement, not eBay's own policy text. Treat as vendor claim until confirmed against eBay primary policy for Luca's site.
4. **AutoDS pricing.** Live pricing page rendered placeholders; figures came from the Help Center billing article; USD only (EUR/Italy pricing not confirmed); plan figures change frequently.
5. **Incomplete numerics.** A few thresholds were not present on fetched pages (exact late-ship minimum-volume gate, Below-Standard FVF uplift %, US flat international fee, +5% INAD fee, Promoted Listings ad rate, exact starter selling-limit counts) → [PUBLIC RESEARCH REQUIRED], not invented.
6. **Freshness.** Captured 2026-06-15. eBay/AutoDS fees and policies change (e.g. a reported Feb-2025 FVF change); re-verify before action. Every fact carries its capture date.
7. **Account-specific data absent by design.** No Seller Hub / AutoDS dashboard data (no login) → Luca's actual limits, account health, plan = USER INPUT NEEDED.

## Usability verdict (data-readiness only, NOT market analysis)
Sufficient as a **policy/fee/feature reference baseline** for the future Analysis phase, on condition that (a) Luca's eBay market is confirmed and the eBay.it/EU schedule re-pulled, and (b) the [PUBLIC RESEARCH REQUIRED] numerics are filled. Not sufficient to compute margins/breakeven yet (missing exact market fees + supplier costs — out of this run's scope).
