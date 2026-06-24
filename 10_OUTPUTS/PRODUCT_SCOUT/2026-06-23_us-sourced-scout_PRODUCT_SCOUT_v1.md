---
type: product-scout
status: PARTIAL   # batch-1 = 2/8 categories; 6 rate-limited, re-run in progress
run_date: 2026-06-23
run_id: wf_1b7e7c8e-880
agent: us-product-scout (Workflow fan-out)
created_real: "<first git commit>"
---

# US-Sourced eBay Dropship Scouting — Run 2026-06-23 (v1, BATCH-1)

## RUN STATUS — PARTIAL (read this first)

8-category scout workflow launched (find → adversarial verify → synthesize). **6 of 8 finders FAILED** with transient API rate-limiting ("Server is temporarily limiting requests — not your usage limit"): a server-side throttle from 8 concurrent Opus-4.8-1M agents hitting the web tools at once. **NOT** an owner usage/billing limit.

- **Completed:** Car & auto accessories · Home organization & storage (12 candidates verified)
- **Failed (re-run in progress, throttled = sonnet + batched):** kitchen · pet · garden · fitness · tools · bath

> The "no GOOD candidate" headline below is over **2 of 8 categories**, not the full universe. This is a partial first pass. Failure registered as **E-009** in ERROR_REGISTRY.

| Phase | Result |
|---|---|
| Find | 2/8 done (auto, organization) · 6/8 rate-limited |
| Verify | 12 candidates verified |
| Synthesize | 0 GOOD · 7 MAYBE · 5 AVOID |

---

# US-Sourced eBay Dropship Scouting — Synthesis Report

**Run date:** 2026-06-23 · **Scope:** 12 verified candidates across 2 categories (Car & auto accessories, Home organization & storage) · **Grade:** RESEARCH-ONLY (no live action; publishing is a separate GO-gated step)

## Headline

**No candidate qualified as GOOD** under the rule GOOD = margin-after-fees >= $5 AND >= 20% of sell. Every item either fell short on absolute dollars, on percentage, or had an unconfirmed Amazon cost. The batch yields **7 MAYBE** and **5 AVOID**. The MAYBE set is real (credible US source, VeRO-clean when listed generically, observed demand), but margins are thin and one return can erase the per-unit profit — so these advance only to a *re-source / re-price* stage, not to publish.

## Ranked shortlist (GOOD first by margin, then MAYBE)

No GOOD items. MAYBE ranked by margin-after-fees (descending); UNKNOWN-margin items listed last because cost was never fetched.

| # | Name | Category | Amazon $ | eBay $ | Margin $ | VeRO | Verdict | Why |
|---|------|----------|----------|--------|----------|------|---------|-----|
| 1 | Clear acrylic drawer organizer tray set (6-pack) | Home organization & storage | 6.83 | 16.99 | 4.61 | Clean | MAYBE | Best margin of the batch (27.1%) but FAILS the absolute >=$5 test; the unusually low $6.83 buy may not hold and a bulkier 6-pack can ship heavier, eroding the thin cushion. |
| 2 | Magnetic spice rack shelf for refrigerator (4-pack) | Home organization & storage | 12.99 | 22.99 | 3.65 | Clean | MAYBE | Both prices OBSERVED; 15.9% after FVF + $3 ship. Real US source, strong demand (6K+ bought/mo). Too thin to absorb returns/price competition. |
| 3 | Leak-Proof Car Trash Can with Lid & Storage Pockets (2 gal) | Car & auto accessories | 6.99 | 14.85 | 2.59 | Clean | MAYBE | Best of the car batch; 17.5% after fees. Light PEVA/fabric, solid demand (2K-10K/mo). Merely positive, not strong. |
| 4 | Car Back Seat Headrest Hooks (4-pack, stainless) | Car & auto accessories | 4.46 | 9.99 | 0.91 | Clean | MAYBE | Strong demand (8K+/mo, >10k eBay results) but only 9% margin; one bad return wipes it out. Tiny commodity, easy US source. |
| 5 | Over-the-door hanging shoe organizer (24-pocket) | Home organization & storage | [UNKNOWN] | 16.99 | [UNKNOWN] | Clean* | MAYBE | Amazon cost not fetched — margin stays UNKNOWN. *Elevated TM hazard: "Gorilla Grip" is a live, actively-enforced mark in the brand pool — strict title/imagery discipline required. Mildly seasonal (back-to-school). |
| 6 | Stackable plastic storage drawers / bins (2-4 pack) | Home organization & storage | [UNKNOWN] | 24.99 | [UNKNOWN] | Clean | MAYBE | Amazon cost not fetched (est ~$18-28, NOT used). Multi-pack dimensional weight can blow past a $3 ship buffer and quietly go negative — scout's own "keep to 2-pack" note is a red flag. |
| 7 | Cable management box / cord organizer (ABS) | Home organization & storage | [UNKNOWN] | 16.99 | [UNKNOWN] | Clean* | MAYBE | Amazon cost not fetched (est ~$9-15, NOT used). *VeRO-clean ONLY if a generic/unbranded box is sourced — the brand pool (D-Line, Legrand/Wiremold/CordMate, UT Wire) carries real IP exposure. Upside looks thin even if real. |

\* "Clean*" = VeRO-clean only under strict sourcing/title discipline (a live-trademark neighbor or branded-SKU risk sits in the candidate pool).

### AVOID (excluded from shortlist, counted in stats)

| Name | Category | Amazon $ | eBay $ | Margin $ | Reason |
|------|----------|----------|--------|----------|--------|
| Foldable Car Windshield Sun Shade | Car & auto accessories | 9.99 | 15.99 | 0.58 | ~3.6% margin (near-zero) + spring/summer seasonality -> dead-stock/timing risk. |
| Car Seat Gap Filler Organizer with Cup Holder & Phone Slot (2-pack) | Car & auto accessories | 12.00 | 17.99 | 0.31 | ~1.7% (break-even); Amazon $12 is INFERRED so could tip negative. "Drop Stop" IP caution. |
| Car Seat Gap Filler Organizer (2-pack, PU leather) | Car & auto accessories | 9.00 | 12.99 | -1.03 | NEGATIVE per unit; Amazon $9 is INFERRED. Elevated "Drop Stop" patented/TM landmine. |
| Foldable Car Trunk Organizer (collapsible) | Car & auto accessories | 13.00 | 15.80 | -2.59 | NEGATIVE and BULKY (600D Oxford) — real ship likely exceeds $3 buffer, loss larger. |
| Under-sink 2-tier pull-out sliding cabinet organizer (metal, 1-pack) | Home organization & storage | 26.38 | 24.99 | -8.00 | Clearly NEGATIVE (-32%); buy/sell spread underwater, heavy metal strains ship buffer. |

## Data caveats (read before acting)

- **Research-grade, not publish-grade.** All prices and demand signals are **search-based estimates** captured ~Jun 2026 via Amazon/eBay snippets and `r.jina.ai` fetches. Several eBay sell prices are INFERRED from active-listing ranges (eBay sold-listing pages were 403-walled), and four Amazon costs are explicitly **[UNKNOWN — not fetched]** (shoe organizer, stackable drawers, cable box) or **[INFERRED]** (both gap fillers). Per constitution, UNKNOWN margins are kept null and no estimate was substituted into the math.
- **Margins use a model, not a quote.** Computed as `sell - cost - (13.25% x sell + $0.30) - $3 ship buffer`. The flat $3 buffer understates real cost on bulky items (trunk organizer, stackable drawers, under-sink basket); actual eBay FVF varies by category/store subscription and promoted-listing fees are not included — real margins skew lower, not higher.
- **Live confirmation is mandatory before any listing.** Before publish, the live **AutoDS sourcing cost** and the **current eBay sell price** must both be re-verified. **Publishing/importing is a separate GO-gated action** — nothing here authorizes a live listing.
- **VeRO discipline is load-bearing, not cosmetic.** "Clean" verdicts assume generic titles/descriptions with all seller brands stripped. Two candidates carry live IP neighbors: the shoe organizer (**Gorilla Grip** registered mark) and the cable box (**D-Line / Legrand-Wiremold / UT Wire**). Both gap fillers must avoid the **Drop Stop** patented/trademarked design and name entirely. Sourcing a branded SKU by accident breaks the clean status.
- **All sell prices are approximate ranges**; demand "X bought/month" figures are single-ASIN proxies and should be treated as lower-bound directional signals, not guarantees of velocity at our price point.

## Recommended top 3 to prep next

1. **Clear acrylic drawer organizer (6-pack)** — highest confirmed margin (27.1%, both prices OBSERVED) and evergreen vanity/desk demand. Next step: re-confirm the $6.83 buy holds on AutoDS and check real shipped weight of the 6-pack; if both hold, it is the closest to GOOD.
2. **Magnetic spice rack for refrigerator (4-pack)** — both prices OBSERVED, strongest demand signal in the batch (6K+ bought/mo), $3.65 cushion. Next step: hunt a sub-$12 source or a $24-25 sell to push it over the 20%+$5 bar.
3. **Leak-Proof Car Trash Can (2 gal)** — best car-category economics, light/easy-ship PEVA, real eBay sold examples. Next step: confirm live AutoDS cost near $6.99 and target a $15-16 sell to lift margin past the GOOD threshold.

*All three advance to a re-source / re-price verification stage, not to publish. None should be listed until live cost and live sell price are confirmed under a dedicated GO.*

---

## Files & next steps

- **BATCH-2** (kitchen, pet, garden, fitness, tools, bath) = re-run with throttled workflow (sonnet model + reduced concurrency); results appended to this file on completion.
- Airtable log: base `appPgvhRkzqSdVciL`, Session `2026-06-23-scout-run`.
- **Publish remains a separate GO-gated step.** The 3 recommended items go only to a re-source/re-price verification stage next, via `draft-publisher`.
