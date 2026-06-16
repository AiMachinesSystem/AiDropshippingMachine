---
machine: "eBay / AutoDS Dropshipping Machine"
type: raw_source_notes
module: 02_DATA
topic: eBay policy + seller performance standards
status: raw
date: 2026-06-15
created_real: 2026-06-15
collection: public_web_readonly
analysis: none
---

# RAW — eBay Policy + Seller Performance Standards (2026-06-15)

> Raw capture. Facts only, no analysis. Every fact is `[OBSERVED — source url, 2026-06-15 (cache: path)]`.
> **Market caveat (applies to ALL rows):** figures are eBay's general / eBay.com (US) policy text unless
> stated; whether they bind Luca depends on his registered eBay site (eBay.it / eBay.co.uk / eBay.com) —
> **USER INPUT NEEDED**. Some eBay `/help/` pages were a fetch wall on 2026-06-15; substance recovered from
> `export.ebay.com` (equivalent policy text, cached) + ebay.com WebSearch.

## A. Dropshipping & listing policy / IP

| # | Fact | Value | Label | Source (cache) |
|---|---|---|---|---|
| A1 | Dropshipping ALLOWED when seller owns items before listing OR has a wholesale-supplier agreement; fulfilling directly from a wholesale supplier is allowed. Seller must be clearly identified on documentation. | own-before-listing OR wholesale agreement | [OBSERVED] | export.ebay.com/.../drop-shipping/ (cache: 90_CACHE/fetches/ebay.com/2026-06-15_dropshipping-policy.txt) |
| A2 | Dropshipping PROHIBITED: "Listing an item on eBay and then purchasing the item from another retailer or marketplace that ships directly to your customer is not allowed." (retail/marketplace arbitrage) — prohibited regardless of margin. | retail arbitrage banned | [OBSERVED] | export.ebay.com/.../drop-shipping/ (cache: …_dropshipping-policy.txt) |
| A3 | Violation consequences: ending/canceling listings; hiding/demoting in search; lowering seller rating; buying/selling restrictions; loss of buyer/seller protections; account suspension; fees paid/payable NOT refunded. | enforcement ladder | [OBSERVED] | export.ebay.com/.../drop-shipping/ (cache: …_dropshipping-policy.txt) |
| A4 | Even when dropshipping, seller remains responsible for safe delivery within the listing's stated timeframe and for the buyer's overall satisfaction. | seller liable for delivery+satisfaction | [OBSERVED] | export.ebay.com/.../drop-shipping/ (cache: …_dropshipping-policy.txt) |
| A5 | Supplier documentation requirement: seller clearly identified on packing slips; contractual limit preventing supplier from using eBay order info beyond fulfilling the transaction. | seller-of-record on docs | [OBSERVED] | export.ebay.com/.../drop-shipping/ (cache: …_dropshipping-policy.txt) |
| A6 | VeRO (Verified Rights Owner) program: rights owners report listings infringing IP, counterfeit/fakes/replicas, or unauthorized copyrighted content. Applies to IP only, not distribution/pricing. | VeRO IP-reporting program | [OBSERVED] | export.ebay.com/.../ebay-verified-rights-owner.../ (cache: 90_CACHE/fetches/ebay.com/2026-06-15_vero-ip-policy.txt) |
| A7 | VeRO/IP enforcement: infringing listing removed + seller notified; continued/repeat IP violations → selling restrictions / account suspension. | IP enforcement | [OBSERVED] | export.ebay.com/.../ebay-verified-rights-owner.../ (cache: …_vero-ip-policy.txt) |
| A8 | Prohibited & Restricted Items policy exists; some categories restricted/banned (country/state-law dependent); violations → remove listing, warning, restrict activity, suspension. | prohibited-items policy exists | [OBSERVED] | ebay.com help id=4207 (cache: 90_CACHE/fetches/ebay.com/2026-06-15_prohibited-restricted-items.txt) |

## B. Seller performance / account-health standards

| # | Fact | Value | Label | Source (cache) |
|---|---|---|---|---|
| B1 | Three seller levels: Top Rated / Above Standard / Below Standard. | 3 levels | [OBSERVED] | export.ebay.com/.../seller-levels/ (cache: 90_CACHE/fetches/web/2026-06-15_ebay-seller-levels-export.txt) |
| B2 | Evaluated on the 20th of each month. | 20th monthly | [OBSERVED] | export.ebay.com/.../seller-levels/ (cache: …_ebay-seller-levels-export.txt) |
| B3 | Lookback: 12 months if <400 sales in prior 3 months; 3 months if ≥400 sales in prior 3 months. | 3 vs 12 mo (400-sale split) | [OBSERVED] | export.ebay.com/.../seller-levels/ (cache: …_ebay-seller-levels-export.txt) |
| B4 | Minimum standard — transaction defect rate ≤ 2% of transactions. | ≤2% | [OBSERVED] | export.ebay.com/.../seller-levels/ (cache: …_ebay-seller-levels-export.txt) |
| B5 | Minimum standard — cases closed without seller resolution ≤ 2 (or ≤0.3% of transactions), higher applies. | ≤2 or ≤0.3% | [OBSERVED] | export.ebay.com/.../seller-levels/ (cache: …_ebay-seller-levels-export.txt) |
| B6 | Defect triggers: seller cancels unexpectedly (e.g. out of stock) OR buyer issue not resolved by seller (case closed without resolution). | out-of-stock cancel = defect | [OBSERVED] | export.ebay.com/.../the-abcs-of-metrics-and-defects.../ (cache: 90_CACHE/fetches/web/2026-06-15_ebay-abcs-metrics-defects-export.txt) |
| B7 | Late shipment: must ship within stated handling time; tracked via integrated-carrier tracking. Exact late-shipment % threshold NOT on fetched pages → PUBLIC RESEARCH REQUIRED. | ship within handling time | [OBSERVED] (% [PUBLIC RESEARCH REQUIRED]) | export.ebay.com/.../the-abcs.../ (cache: …_ebay-abcs-metrics-defects-export.txt) |
| B8 | Top Rated needs: account active ≥90 days; ≥100 transactions and $1,000 US sales over past 12 months; selling-practices compliance. Top Rated Plus listing: ≤1-business-day handling + 30-day-or-longer free returns. | TRS criteria (US program) | [OBSERVED] | export.ebay.com/.../seller-levels/ (cache: …_ebay-seller-levels-export.txt) |
| B9 | Below Standard consequences: lower search ranking; reduced selling limits; blocked from ad tools; order funds held until tracked shipment; higher final value fees. | Below-Standard penalties | [OBSERVED] (fee-uplift % [PUBLIC RESEARCH REQUIRED]) | export.ebay.com/.../seller-levels/ + ABCs page (cache: …_ebay-seller-levels-export.txt) |
| B10 | Selling limits: all sellers have them; account-specific; driven by sales volume + buyer feedback + category; active+sold listings count toward monthly limit; eBay may end listings over the limit. | account-specific limits | [OBSERVED] | export.ebay.com/.../selling-limits/ (cache: 90_CACHE/fetches/web/2026-06-15_ebay-selling-limits-export.txt) |
| B11 | Limits reviewed/auto-adjusted monthly; increase requestable from eBay's near-limit notification; visible in Seller Hub > Overview > Monthly limits. | monthly review; request increase | [OBSERVED] | export.ebay.com/.../selling-limits/ (cache: …_ebay-selling-limits-export.txt) |

## Unverified / flagged (this capture)
- ebay.com `/help/` canonical pages (dropshipping id=4176/4206; seller-levels id=4080; seller-standards id=4347; global-perf id=4351; selling-limits id=4107) TIMED OUT on WebFetch (fetch wall) — verbatim threshold tables not cached; substance recovered from export.ebay.com + WebSearch. → [PUBLIC RESEARCH REQUIRED] to re-capture verbatim.
- Exact late-shipment rate %, stricter Top Rated numeric thresholds, Below-Standard FVF uplift %, and typical starting selling-limit numbers (a WebSearch "10 items/$500" figure was NOT cached) → [UNKNOWN] / [PUBLIC RESEARCH REQUIRED].
- Whether identical wording/thresholds apply on eBay.it / eBay.co.uk / EU → [PUBLIC RESEARCH REQUIRED]; Luca's governing site → USER INPUT NEEDED.
