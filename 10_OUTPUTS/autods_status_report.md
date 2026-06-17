---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: status_report
status: complete
go_scope: GO_AUTODS_READ_SESSION (read-only, via Playwright)
date: 2026-06-16
created_real: 2026-06-16
method: Playwright headless + saved storage_state.json (no login this run); data from the AutoDS SPA's own GET API responses + rendered UI + screenshots
evidence_cache:
  - 90_CACHE/fetches/autods/run_2026-06-16_225027/   (dashboard, products, orders, settings)
  - 90_CACHE/fetches/autods/run_2026-06-16_224918/   (home discovery)
  - 90_CACHE/fetches/autods/run_2026-06-16_225346/   (products retry)
  - 90_CACHE/screenshots/autods/run_2026-06-16_225027/
---

# AutoDS account status report — read-only (2026-06-16)

> **Scope.** READ-ONLY reconnaissance of the AutoDS account via the saved Playwright session. No clicks on
> actionable controls, no writes, no imports/publishes/pricing/orders. Numbers come from the AutoDS app's own
> backend API responses (`v2-api.autods.com`, `gw.autods.com`) captured while navigating, cross-checked against
> the rendered UI and screenshots. Evidence cached before citing (paths in frontmatter).

## TL;DR
- **Store:** `Divinit-92-Us` (ID `3713044`) — **eBay US** store, currency USD. **Active** (real sales) but a brand-new account in onboarding, on a **3-day trial expiring 2026-06-18**.
- **Sales so far:** 23 orders all-time; last 7 days = 3 orders, **$320 revenue / $62 profit**. Top sellers: *Dog Water Ramp* (2), *Hedgehog Dryer Balls* (1).
- **Pricing:** primary profile = **27% margin**, 15% break-even, **$7 min profit**, prices rounded to `.97`, dynamic eBay business policies ON (3-day handling).
- **Auto-ordering:** **toggled ON** (cap $500/order, max loss $5) — **BUT 0 buyer accounts connected and $0 wallet**, so it cannot actually purchase yet. ⚠️
- **Product counts (drafts/published):** **not directly readable** — `/products` redirects to a trial UGC-video upsell that blocks the list. Proxies point to a very small/early catalog. Needs one harmless "No Thanks" dismiss-click (owner OK pending).
- **Notifications:** header bell badge = **1** (Beamer announcements); active marketing upsells (UGC video, TikTok Ads). No critical system/error alerts observed.

---

## 1. Active store (name · marketplace · status)
- **Name:** `Divinit-92-Us` — [OBSERVED — dashboard header + Settings store selector, 2026-06-16]
- **Store ID:** `3713044` — [OBSERVED — `v2-api.autods.com/store/3713044/...`]
- **Marketplace:** **eBay (US)** — [OBSERVED — product images served from `i.ebayimg.com`; eBay-specific settings present: dynamic business policies, Global Shipping Program option, listing fee; location United States / Las Vegas, NV 89103; currency USD]
- **Status:** **Active & transacting** — 23 lifetime orders, sales in the last 7 days — [OBSERVED — `dashboard/3713044/sales-overview`, `orders/3713044/count`]. However the account is **early-stage / in onboarding**: the "Store Setup Guide" still shows incomplete steps (incl. "Connect your store", "Add your first draft") — [OBSERVED — dashboard].
- **Subscription:** trial plan (package `701`), started 2026-06-15, **expires 2026-06-18**; `orders_processor` add-on (auto-ordering) also on trial to 2026-06-18; next payment 2026-06-18 — [OBSERVED — `subscriptions/user-subscription`].
- **Credits / wallet:** AI credits 30 (plus credit buckets 5 / 400 / 30); auto-order wallet **$0 USD, £0 GBP** — [OBSERVED — `auto-order-v3/wallet/external/list`].

## 2. Products in DRAFT
- **Exact count: UNKNOWN via pure read-only** — navigating `/products` (and `/products` on retry) **redirects to `/ugc-offer`**, a trial UGC-video upsell interstitial, so the Drafts/Products list and its count API never load — [OBSERVED — redirect captured twice, runs 225027 & 225346].
- **Proxies (→ likely 0 or very few):** onboarding step "Add your first draft" still **incomplete**; `store_quotes` count = 0; new products in the last period = 0 — [OBSERVED — dashboard, `store_quotes/3713044/count`].
- **To get the exact number:** dismiss the upsell ("No Thanks, I'll Miss Out") to reach the list — a click that writes nothing to the store. **Held pending owner OK** (read-only gate).

## 3. Products PUBLISHED (active)
- **Exact count: UNKNOWN via pure read-only** — same `/products` → `/ugc-offer` wall — [OBSERVED].
- **Proxies (→ small live catalog):** at least **2 products are live and have sold** — *Dog Water Ramp for Boats & Pools (Holds 200 lbs)* and *Hedgehog Reusable Dryer Balls* — [OBSERVED — `dashboard/3713044/products_report`]; the store has **23 lifetime orders**, implying several live listings. Exact active count pending the dismiss-click above. [LOW-SAMPLE on full catalog.]

## 4. Active pricing settings
[OBSERVED — `v2-api.autods.com/store/3713044/settings/list` + Settings → Supplier Settings screenshot, 2026-06-16]

**Primary supplier profile** (supplier `11971105`, site_id 1, US / Las Vegas, NV):
| Setting | Value |
|---|---|
| Profit margin | **27%** (percentage) + $0 fixed |
| Break-even % | 15% |
| Minimum profit | **$7.00** |
| Price rounding | round cents to **.97** (enabled) |
| Default quantity | 4 (minimum allowed 3) |
| Include shipping in price | Yes |
| Max shipping time | 10 days |
| Listing fee factored | $0.35 |
| Dynamic profit | Off |
| Currency | USD → USD |
| Dynamic business policies (ship/pay/return) | **Enabled** — handling time 3 days |
| Global Shipping Program | Off |
| Allow OOS variations | Yes · Capitalize title: Yes · Watermark: Off · Upload variations: Off |

- A **second supplier profile** exists (id `12809249`, site_id 2, Denver, CO): profit **10%**, break-even 13%, default qty 1, max shipping 60 days — [OBSERVED]. (Supplier-source names not asserted; reported by observed attributes only.)

## 5. Auto-ordering status
[OBSERVED — `v2-api.autods.com/store/3713044/order_settings` + `gw.autods.com/auto-order/*`, 2026-06-16]
- **Auto-order: ENABLED** (`auto_order = true`, `managed_auto_order = true`).
- Guardrails: **max order price $500**, **max acceptable loss $5**, mark "update as shipped" on, auto-delivery **disabled**.
- Automatic buyer messages: **1 active** ("Thank you for buying from us!"); 4 more templates configured but inactive.
- ⚠️ **Functional gap:** **0 buyer accounts connected** (`auto-order/buyaccount/filter` → 0 results) and **auto-order wallet $0**. Auto-ordering is switched on but, as configured now, **cannot actually place supplier orders** (no buying account, no funds). The `orders_processor` add-on enabling this is on **trial until 2026-06-18**.

## 6. Notifications / alerts
- **Header bell badge = 1** — [OBSERVED — dashboard & settings header]. Backed by the **Beamer** announcements feed (`getbeamer.com`) and **Pusher** real-time channel — i.e. a product/announcement notification, not necessarily an operational alert.
- **Active marketing upsells** (not system errors): UGC video-ads offer (the `/ugc-offer` that blocks `/products`); "TikTok Ads — limited-time offer" dashboard banner — [OBSERVED].
- **Onboarding to-dos**: "Store Setup Guide" with incomplete steps acts as a checklist/alert — [OBSERVED].
- **No critical error/policy/out-of-stock alerts surfaced** on the pages traversed — [OBSERVED]. ([LOW-SAMPLE]: per-product and per-order detail pages were not opened, so operational alerts there are not covered.)

---

## Flags worth the owner's attention
1. **Auto-ordering can't fulfill as-is** — ON but 0 buyer accounts + $0 wallet. If a supplier order is needed, it would fail/stall until a buying account + funds are added. (GO-gated to fix.)
2. **Trial ends 2026-06-18 (in 2 days)** — subscription + auto-ordering add-on lapse then; decide upgrade vs. let-expire.
3. **`/products` blocked by the UGC upsell** — exact draft/active counts and per-product health need the upsell dismissed.

## What needs a click or a new GO (not done — read-only gate)
- Dismiss the UGC upsell → read **exact drafts/published counts** + per-product status (stock/price-monitoring errors).
- Open **Settings → Buyer Accounts** and **→ Notifications** tabs for detail.
- Open **Orders** detail to classify the 23 orders (paid / shipped / pending fulfillment).

## How this was produced (reproducible)
`integrations/autods/playwright/read_autods_status.py` — reuses `storage_state.json`, navigates read-only, and
captures API JSON + text + screenshots into `90_CACHE/` (gitignored). Re-run:
`.venv\Scripts\python.exe read_autods_status.py "https://platform.autods.com/dashboard" ...`
