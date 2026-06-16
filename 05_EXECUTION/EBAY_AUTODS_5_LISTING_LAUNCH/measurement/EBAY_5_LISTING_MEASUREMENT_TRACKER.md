---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: measurement_tracker
status: template
date: 2026-06-16
created_real: 2026-06-16
---

# 5 Listing Measurement Tracker (template)

> KPI template for the 5 listings. **Empty until real post-publish data exists.** Values fill in only from
> actual eBay/AutoDS measured data (USER-PROVIDED or read-only API once authorized) — no invented numbers.

| # | SKU | listing_status | upload_errors | publish_status | impressions | clicks | watchers | sales | revenue (USD) | fees (USD) | cost (USD) | est_profit (USD) | policy_warnings | next_action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  | draft |  | not_published |  |  |  |  |  |  |  |  |  |  |
| 2 |  | draft |  | not_published |  |  |  |  |  |  |  |  |  |  |
| 3 |  | draft |  | not_published |  |  |  |  |  |  |  |  |  |  |
| 4 |  | draft |  | not_published |  |  |  |  |  |  |  |  |  |  |
| 5 |  | draft |  | not_published |  |  |  |  |  |  |  |  |  |  |

## Notes
- `est_profit` = revenue − fees − cost (computed from REAL measured values only; blank until data exists; not a pre-launch projection).
- `policy_warnings` = any eBay account-health/policy flag observed post-publish.
- Source of truth for live values = eBay Seller Hub / AutoDS (owner-provided or read-only API, once `GO_AUTODS_API_READ_ONLY_TEST` is given).
- This tracker is updated only with measured data; it advances no gate.
