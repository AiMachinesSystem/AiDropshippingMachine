---
machine: "eBay / AutoDS Dropshipping Machine"
type: missing_data_log
module: 02_DATA
status: active
date: 2026-06-15
created_real: 2026-06-15
scope: "gaps from the 2026-06-15 public policy/fee/feature research run"
---

# Missing-Data Log — Public Research Run (2026-06-15)

> Complements `MISSING_OWNER_INPUTS.md` (owner account data). This log = research gaps surfaced by THIS run.

## A. USER INPUT NEEDED (only Luca / his accounts can resolve)
| # | Item | Needed for |
|---|---|---|
| U1 | **Confirm eBay market/site** (eBay.it / eBay.co.uk / eBay.com) | Selects the binding fee schedule, policy text, Top Rated criteria |
| U2 | eBay account: store tier (if any), seller level, current selling limits, account health metrics | Real fees, limits, performance baseline |
| U3 | AutoDS: current plan/tier, add-ons (Orders Processor?), billing currency | Real automation capability + cost |
| U4 | Intended product category | FVF varies by category; limits vary by category |

## B. PUBLIC RESEARCH REQUIRED (re-fetchable later, not approved/captured this run)
| # | Item | Why missing |
|---|---|---|
| P1 | eBay.it / EU localized fee schedule + policy text | This run captured eBay.com (US) / EN-mirror; market not confirmed |
| P2 | Verbatim www.ebay.com US help pages (id=4080/4347/4351/4107/4822/4809/5224/4210/4079) | Fetch wall (timeouts) on 2026-06-15 |
| P3 | Exact late-shipment minimum-volume gate; stricter Top Rated numerics; Below-Standard FVF uplift % | Not present on fetched pages |
| P4 | US-registered flat international fee (reported 1.65%); +5% INAD/below-standard fee; Promoted Listings ad rate | WebSearch-only, not captured verbatim |
| P5 | Exact starter selling-limit counts ("10 items/$500" unconfirmed) | Not on fetched official pages |
| P6 | AutoDS EUR pricing + live pricing-page figures | Live page rendered placeholders; Help Center = USD |
| P7 | Confirm eBay primary dropshipping/sourcing policy on Luca's site (vs AutoDS restatement) | Vendor source only this run for some claims |

## C. Explicitly NOT collected (out of this run's scope)
- Competitor listings, product/market demand, supplier prices/stock, profitability — NOT in the policy/fee/feature GO. (Different data type; separate GO.)
