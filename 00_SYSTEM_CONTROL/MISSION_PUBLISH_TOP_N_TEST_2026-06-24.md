---
machine: "eBay / AutoDS Dropshipping Machine"
mission_id: PUBLISH_TOP_N_TEST
date: 2026-06-24
created_real: 2026-06-24
owner_go: "Luca 2026-06-24 — 10-point directive: stop reprice, leave prices unchanged, proceed ONLY with publish top-N TEST, publish only selected test listings, no delete, no other product edits, no pricing changes, verify live, stop after. Final state: PUBLISH_TOP_N_TEST_COMPLETE | _BLOCKED."
risk_class: GO-CLASS (live eBay publish — owner GO given). Scope strictly limited per directive.
status: PUBLISH_TOP_N_TEST_COMPLETE
---

## RESULT (2026-06-24 ~03:0x) — PUBLISH_TOP_N_TEST_COMPLETE
- **4/5 PUBLISHED LIVE** (verified gone-from-drafts via read_draft_errors; drafts back to the original 8 untouched):
  1 Meal Prep Containers 20oz 25pk (B079VX6DSG) ✓ · 2 Spider Strainer Skimmer (B07PCM3BNL) ✓ ·
  4 Snack Containers Bento 4pk (B0B5HM5VRN) ✓ · 5 Spin Mop Heads (B07W18LHMB) ✓ [corrected 3pk→2pk for accuracy].
- **1/5 import-FAILED**: 3 Meat Thermometer (B08789RNLH) — draft count did not increase (likely duplicate already in
  store / AutoDS sourcing block). NOT an account restriction (the other 4 published fine). Documented, not retried (anti-hammer).
- Prices of the 96 active listings UNTOUCHED. No drafts deleted. No other products modified. Pricing logic unchanged.

# MISSION — Publish top-N TEST (N=5) from US-warehouse sourcing shortlist

## Hard scope (owner 10-point directive — do NOT exceed)
1 stop reprice ✓ · 2 no A/B · 3 prices unchanged · 4 ONLY publish top-N TEST · 5 only the selected test listings ·
6 NO draft delete · 7 NO other product edits · 8 NO pricing-logic change · 9 verify published are live · 10 stop after.

## Batch (top 5 TEST, cleanest: VeRO LOW, ship 1-2d, generic) — source: sourcing shortlist 2026-06-24, all Amazon-US
| # | ASIN | niche | buy | generic title (<=80) | desc file |
|---|---|---|---|---|---|
| 1 | B079VX6DSG | kitchen | 15.99 | 20oz Meal Prep Containers 25 Pack Lids Reusable Lunch Bento Food Storage | copy_test_mealprep.html |
| 2 | B07PCM3BNL | kitchen | 13.86 | Stainless Steel Spider Strainer Skimmer Ladle Mesh Kitchen Frying Food | copy_test_spider.html |
| 3 | B08789RNLH | meat | 19.99 | Digital Meat Thermometer Instant Read Waterproof Food Cooking BBQ Grill | copy_test_meatthermo.html |
| 4 | B0B5HM5VRN | kitchen | 13.57 | 4 Pack Snack Containers 4 Compartment Bento Box Reusable Meal Prep Lunch | copy_test_bento.html |
| 5 | B07W18LHMB | cleaning | 15.99 | 3 Pack Spin Mop Replacement Heads Microfiber Refill Round Mop Pads | copy_test_spinmop.html |

## Pipeline per product (proven amazon10 flow)
manage_draft.py full --url https://www.amazon.com/dp/<ASIN> --match <scraped substr> --title "<generic>" --desc-file <file>
  -> prints draft id ; then publish_one_draft.py <id> "<guard substr>" -> RESULT: PUBLISHED (left drafts) | BLOCKED | UNCONFIRMED.
Pricing: NOT touched (AutoDS default applies). Verify live: read_draft_errors.py (published items leave the draft list).

## Discipline
Publish PRODUCT 1 end-to-end + verify LIVE first; only then 2-5 (catch pipeline issues at #1). One publish at a time
(stop on eBay account restriction — never hammer). Prices of the other 96 untouched (rule 3/8).

## Exit proof
PUBLISH_TOP_N_TEST_COMPLETE = the test batch attempted, each successful item verified gone-from-drafts (live);
report per-item PUBLISHED/BLOCKED. PUBLISH_TOP_N_TEST_BLOCKED = systemic blocker (eBay account restriction / pipeline wall).

## Recovery log
- 2026-06-24 02:5x — Mission written. Batch=5 ASINs. Next: write 5 desc files, run product 1 full+publish+verify.
