---
machine: "eBay / AutoDS Dropshipping Machine"
type: source_access_notes
module: 02_DATA
status: active
date: 2026-06-15
created_real: 2026-06-15
collection: public_web_readonly
---

# Source Access Notes — Public Research Run (2026-06-15)

> Access method: **public web, read-only**. No login, no account access, no credentials, no live changes.
> Every load-bearing page cached to `90_CACHE/fetches/<domain>/2026-06-15_<slug>.txt` (21 files) BEFORE citation.
> 90_CACHE is non-versioned (audit trail). Tools: WebSearch (US-only, used to locate official URLs) + WebFetch.

## Sources accessed (public, official)
| Domain | Pages (cached) | Topic | Notes |
|---|---|---|---|
| export.ebay.com / ebay.com | dropshipping-policy, vero-ip-policy, prohibited-restricted-items, seller-levels, abcs-metrics-defects, selling-limits(+detail), seller-fees, final-value-fees, store-subscriptions-fees, international-fees, money-back-guarantee, order-cancellation, handling-time-delivery, how-returns-work-seller | eBay policy, fees, standards, returns, cancellations, shipping, limits | export.ebay.com EN/IN mirrors used where www.ebay.com /help/ pages hit a fetch wall |
| autods.com / help.autods.com | ebay-automation-features, suppliers-and-channels, product-upload-supported-suppliers-regions, subscription-pricing-addons, ebay-dropshipping-policy-guidance | AutoDS features, suppliers, pricing, policy guidance | vendor source; eBay-policy items = AutoDS restatement |

## Access walls encountered (recorded, not retried beyond 2–3 tries)
- **www.ebay.com `/help/` portal**: repeated WebFetch timeouts / socket drops (JS-heavy) on id=4176, 4206, 4080, 4347, 4351, 4107, 4822, 4809, 5224, 4210, 4079. → substance recovered from `export.ebay.com` EN/IN static mirrors (cached). Verbatim US-help text NOT captured for these = [PUBLIC RESEARCH REQUIRED] to re-capture.
- **autods.com/pricing/** rendered placeholder "$__" prices → plan figures taken from the Help Center billing article instead.
- autods.com/ebay-dropshipping/ and /supported-suppliers/ → HTTP 404 (not used).

## Confirmations
- No eBay login. No AutoDS login. No supplier access. No credentials used. No platform modified. No order/listing/config action. No analysis performed.
- WebSearch (US-only) used ONLY to locate official URLs; not used as a standalone fact source. WebSearch-only items that were not captured from a fetched page are logged as unverified, never presented as [OBSERVED].
