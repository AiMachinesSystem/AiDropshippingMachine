---
machine: "eBay / AutoDS Dropshipping Machine"
type: raw_source_notes
module: 02_DATA
topic: eBay returns / MBG / cancellations / shipping-handling / selling-limits
status: raw
date: 2026-06-15
created_real: 2026-06-15
collection: public_web_readonly
analysis: none
---

# RAW — eBay Returns / Cancellations / Shipping / Selling Limits (2026-06-15)

> Raw capture, facts only. `[OBSERVED — source url, 2026-06-15 (cache: path)]`. Market caveat applies to all:
> figures are eBay EN / export-mirror general text; Luca's governing site (eBay.it/eBay.co.uk/eBay.com) = **USER INPUT NEEDED**.
> www.ebay.com `/help/` pages (id=4210 MBG, id=4079 return-policy) timed out → substance from `export.ebay.com` EN/IN mirrors (cached).

## Returns & eBay Money Back Guarantee (MBG)
| # | Fact | Value | Label | Cache (90_CACHE/fetches/ebay.com/) |
|---|---|---|---|---|
| R1 | Seller return options: No returns · 30-day buyer-paid · 30-day free · 60-day buyer-paid · 60-day free. | 30 / 60 days | [OBSERVED] | 2026-06-15_how-returns-work-seller.txt |
| R2 | "Free returns" = seller pays return shipping for any reason, no restocking fee. | — | [OBSERVED] | _how-returns-work-seller.txt |
| R3 | After receiving a return, seller has 2 business days to refund; else eBay auto-refunds 2 business days after delivery confirmed. | 2 business days | [OBSERVED] | _how-returns-work-seller.txt |
| R4 | Top Rated / free-returns sellers may give partial refund up to 50% if item returned in different condition. | up to 50% | [OBSERVED] | _how-returns-work-seller.txt |
| R5 | MBG — Item Not Received: buyer may open from after est. delivery date up to 30 calendar days after. | 30 cal days | [OBSERVED] | 2026-06-15_money-back-guarantee.txt |
| R6 | MBG — Not As Described: report by 30 cal days after delivery OR seller's return window, whichever longer; seller covers return shipping. | 30 cal days / longer | [OBSERVED] | _money-back-guarantee.txt |
| R7 | MBG — Remorse: return shipping per seller's listing policy. Seller must respond within 3 business days or eBay may step in; refund within 2 business days of receiving return. | 3 / 2 business days | [OBSERVED] | _money-back-guarantee.txt |
| R8 | MBG — item not arriving → buyer refunded full item cost + original shipping. | full + shipping | [OBSERVED] | _money-back-guarantee.txt |
| R9 | MBG exclusions: digital content/NFTs, motor vehicles, real estate/businesses, services, items paid outside eBay checkout. Trading Cards stricter (3-day window if no returns). | — | [OBSERVED] | _money-back-guarantee.txt |

## Cancellations
| # | Fact | Value | Label | Cache |
|---|---|---|---|---|
| C1 | Buyer cancellation request window: up to 60 minutes after committing to buy. | 60 min | [OBSERVED] | 2026-06-15_order-cancellation.txt |
| C2 | Valid seller-cancel reasons: buyer asked (pre-ship), no payment in time, wrong address, OR out of stock. | — | [OBSERVED] | _order-cancellation.txt |
| C3 | Seller must respond to a buyer cancel request within 3 calendar days; seller may initiate cancel up to 30 calendar days after sale notice. | 3 / 30 cal days | [OBSERVED] | _order-cancellation.txt |
| C4 | **Canceling for out-of-stock = transaction defect, affects performance & Seller Level.** | defect | [OBSERVED] | _order-cancellation.txt |
| C5 | Seller cancel (buyer paid via eBay) → full refund to buyer's original payment method. Misuse (false non-payment) → suspension/restrictions/rating cuts/fees. | full refund; misuse penalised | [OBSERVED] | _order-cancellation.txt |

## Shipping / handling time
| # | Fact | Value | Label | Cache |
|---|---|---|---|---|
| S1 | Handling time = business days between receiving payment and carrier acceptance scan. | def. | [OBSERVED] | 2026-06-15_handling-time-delivery.txt |
| S2 | 1-day handling: acceptance scan by next day 11:59:59 p.m. seller local time; Fri/Sat/Sun buys → tracking by Mon 11:59pm. | 1 business day | [OBSERVED] | _handling-time-delivery.txt |
| S3 | eBay recommends ≤ 2 days handling time. | ≤2 days (rec.) | [OBSERVED] | _handling-time-delivery.txt |
| S4 | Late deliveries don't hurt performance IF shipped within handling time + acceptance scan + valid tracking. | protection condition | [OBSERVED] | _handling-time-delivery.txt |
| S5 | **Late shipment rate must be ≤ 3% to qualify for Top Rated.** (fills the Cat-B late-ship % gap) | ≤3% (Top Rated) | [OBSERVED] | _handling-time-delivery.txt |
| S6 | Non-delivery within estimated dates → buyer Item-Not-Received case → possible defect. | — | [OBSERVED] | _handling-time-delivery.txt |

## Selling limits
| # | Fact | Value | Label | Cache |
|---|---|---|---|---|
| L1 | All new sellers have a selling limit (+ zero-insertion-fee listings). | exists | [OBSERVED] | 2026-06-15_selling-limits-detail.txt |
| L2 | Limits unique per account; vary by account age, identity confirmation, registered address, site of registration, performance, sales history, item-type risk. | account-specific | [OBSERVED] | _selling-limits-detail.txt |
| L3 | eBay reviews monthly and auto-adjusts based on sales volume + buyer feedback. | monthly | [OBSERVED] | 2026-06-15_selling-limits.txt |
| L4 | Active + sold + Good-'Til-Cancelled listings count toward the monthly limit. | — | [OBSERVED] | _selling-limits.txt |
| L5 | Near limit → seller can request increase (eBay may need contact/business details). | — | [OBSERVED] | _selling-limits.txt |
| L6 | At the monthly limit: cannot create listings, raise prices, or add items until active listings end or next month. | per cal month | [OBSERVED] | _selling-limits-detail.txt |

## Unverified / flagged
- Exact starter limit figures ("10 items / $500") — NOT on any fetched page → [PUBLIC RESEARCH REQUIRED].
- 14-day return option "in limited categories"; restocking-fee % rules; buyer refund-processing timeline; "BUYER_ASKED_CANCEL doesn't count as defect" — WebSearch synthesis only → [PUBLIC RESEARCH REQUIRED].
- www.ebay.com US help id=4210 / id=4079 verbatim not captured (fetch wall) → [PUBLIC RESEARCH REQUIRED].
- eBay.it / EU equivalents and Luca's governing site → USER INPUT NEEDED.
