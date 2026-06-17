---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: status_report
status: complete
go_scope: GO_AUTODS_READ_SESSION (read-only, via Playwright)
date: 2026-06-16
created_real: 2026-06-16
method: Playwright headless + saved storage_state.json (no login this run); data from the AutoDS SPA's own GET API responses + rendered UI + screenshots. Read-only clicks performed (owner-approved): dismiss UGC upsell ("No Thanks") + navigate to the Drafts list. No data-mutating clicks.
evidence_cache:
  - 90_CACHE/fetches/autods/run_2026-06-16_225027/        (dashboard, products, orders, settings)
  - 90_CACHE/fetches/autods/run_2026-06-16_224918/        (home discovery)
  - 90_CACHE/fetches/autods/run_2026-06-16_225346/        (products retry)
  - 90_CACHE/fetches/autods/products_2026-06-16_230501/   (upsell dismissed -> 214 active)
  - 90_CACHE/fetches/autods/drafts_2026-06-16_230951/     (drafts -> 11)
  - 90_CACHE/screenshots/autods/run_2026-06-16_225027/
---

# AutoDS account status report — read-only (2026-06-16)

> **Scope.** READ-ONLY reconnaissance of the AutoDS account via the saved Playwright session. No clicks on
> actionable controls, no writes, no imports/publishes/pricing/orders. Numbers come from the AutoDS app's own
> backend API responses (`v2-api.autods.com`, `gw.autods.com`) captured while navigating, cross-checked against
> the rendered UI and screenshots. Evidence cached before citing (paths in frontmatter).

## TL;DR
- **Store:** `Divinit-92-Us` (ID `3713044`) — **eBay US** store, currency USD. **Operating** (214 live listings + real sales) but a young account on a **3-day trial expiring 2026-06-18**.
- **Catalog:** **214 published/active eBay listings** (+4 untracked) and **11 drafts** (Scheduled 0 · Recurring 0). Supplier: **Amazon US**. Some listings flagged OOS / On-Hold / supplier-title-change; **1 draft has a VeRO keyword alert ("alcohol")**.
- **Sales so far:** 23 orders all-time; last 7 days = 3 orders, **$320 revenue / $62 profit**. Top sellers: *Dog Water Ramp* (2), *Hedgehog Dryer Balls* (1).
- **Pricing:** primary profile = **27% margin**, 15% break-even, **$7 min profit**, prices rounded to `.97`, dynamic eBay business policies ON (3-day handling).
- **Auto-ordering:** **toggled ON** (cap $500/order, max loss $5) — **BUT 0 buyer accounts connected and $0 wallet**, so it cannot actually purchase yet. ⚠️
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
- **Drafts: 11** — [OBSERVED — Drafts page (`/upload`, "Drafts (11)") + `products/3713044/count/` → 11, 2026-06-16].
- Also **Scheduled 0 · Recurring 0** (no scheduled or recurring listings queued) — [OBSERVED].
- Draft source supplier: **Amazon US** — [OBSERVED — draft cards]. Recent draft-creation jobs visible (e.g. #158504443, 7/7 finished).
- ⚠️ **At least one draft carries a compliance flag:** *"Product Description contains a VeRO word, keyword (alcohol)"* — an eBay VeRO/keyword warning to resolve before publishing — [OBSERVED — drafts page].
- Access note: the Drafts list lives at the `/upload` route; the `/products` deep-link first hits a trial UGC upsell, which was dismissed ("No Thanks") to read the lists.

## 3. Products PUBLISHED (active)
- **Published / active listings: 214** (paginated 20×11) **+ 4 untracked** eBay products not linked to AutoDS — [OBSERVED — Products page "Products (214)" / "out of 214" + `products/3713044/count/` → 214, 2026-06-16].
- Catalog imported **Dec 18, 2025**; supplier **Amazon US**; sell prices set with the 27% profile (e.g. buy $49.79 → sell $79). Top sellers to date: *Dog Water Ramp* (2 sold), *Hedgehog Dryer Balls* (1) — [OBSERVED].
- ⚠️ **Listing health issues present:** several products show **Out Of Stock** or **On Hold**, and there are **supplier-side errors** (e.g. "Title on the supplier's side changed") flagged on listings — [OBSERVED — `products/3713044/list/` `error_list` + products page status columns]. Exact per-status breakdown not tallied this run — [LOW-SAMPLE].

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
3. **Compliance: a draft has a VeRO keyword alert ("alcohol")** — review/edit before publishing to avoid an eBay policy hit.
4. **Listing health** — some of the 214 listings are OOS / On-Hold / carry supplier-change errors; worth a cleanup pass (full per-status tally not done this run).

## Open follow-ups (not done this run)
- **Per-status tally** of the 214 listings (active / OOS / on-hold / error) and the 11 drafts — to quantify the health issues.
- Open **Settings → Buyer Accounts** and **→ Notifications** tabs for detail (auto-order source accounts + the alert list behind the bell badge).
- Open **Orders** detail to classify the 23 orders (paid / shipped / pending fulfillment).
- Resolve the **VeRO draft flag** before any publish (GO-gated).

## How this was produced (reproducible)
`integrations/autods/playwright/read_autods_status.py` — reuses `storage_state.json`, navigates read-only, and
captures API JSON + text + screenshots into `90_CACHE/` (gitignored). Re-run:
`.venv\Scripts\python.exe read_autods_status.py "https://platform.autods.com/dashboard" ...`
