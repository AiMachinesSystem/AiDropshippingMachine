---
machine: "eBay / AutoDS Dropshipping Machine"
type: read_only_intake_plan
module: 02_DATA
topic: AutoDS read-only data intake
status: plan_only
date: 2026-06-15
created_real: 2026-06-15
collection_status: not_started
external_access: none
analysis: none
---

# AutoDS Read-Only Data Intake Plan (2026-06-15)

> **PLAN ONLY.** Defines WHAT AutoDS data to collect later, HOW to capture it read-only, WHERE to store it,
> and WHAT stays forbidden without explicit owner GO. **No login, no access, no live data collected here.**
> No strategy, no recommendations, no SOPs-for-execution, no product selection, no AutoDS configuration.
> Context: US seller → US buyers, eBay.com (owner_context.md). AutoDS access = NOT CONNECTED.

## 1. AutoDS data categories to collect later
| # | Category | What it contains (read-only) | Feeds module |
|---|---|---|---|
| A | Account & plan | plan tier, product/variation cap, add-ons (e.g. Orders Processor), billing cadence (NO card data) | System, Measurement |
| B | Connected store(s) & sync | which eBay store is connected, connection/sync status, sync errors | System, Execution |
| C | Product catalogue | imported/monitored products, variant counts, listing status, source supplier per product | Data, Analysis |
| D | Supplier configuration | configured suppliers, default supplier, supplier-region mapping, supplier links per product | Data, Analysis |
| E | Pricing/repricing settings | current price-optimization rules, markup/floor settings, breakeven settings (READ current values; never change) | Data, Analysis |
| F | Automation settings | current state of price/stock monitoring, auto-order (Orders Processor), auto-tracking (READ on/off + params) | System, Execution, Measurement |
| G | Orders & fulfillment records | order list, statuses, supplier-order references, handling/fulfillment timestamps | Measurement, Learning |
| H | Tracking sync | tracking-upload status/logs, carrier-validation outcomes | Measurement |
| I | Monitoring events | stock-change/out-of-stock events, price-change events | Measurement, Learning |
| J | Errors / automation logs | mapping/repricing/order/tracking errors and incident logs | Learning, Execution |
| K | Notifications / alerts | AutoDS notifications, warnings, account messages | System, Learning |
| L | AutoDS analytics/reports | any AutoDS-side performance/report views (if present on plan) | Measurement |

## 2. Safe capture methods (read-only)
| Method | Use | Constraint |
|---|---|---|
| **Screenshots** | any dashboard panel (account, settings, products, orders, logs) | owner captures; redact billing/card/credentials/PII before sharing |
| **Exports** | CSV/exports AutoDS natively offers (products, orders) | export = download only; must NOT trigger any platform change/sync/order |
| **Guided read-only review** | owner shares screen / reads values aloud; machine records them | machine never controls the session; observation only |
| **Controlled login (deferred)** | a supervised read-only look — **ONLY if explicitly approved in a separate future GO** | requires its own GO + secure credential channel; **NOT authorized now**; default = never |

Preferred order: exports → screenshots → guided review → (controlled login only if separately approved).

## 3. Data storage map
| Artifact | Destination | Versioned? |
|---|---|---|
| Raw notes / transcribed values / export contents | `02_DATA/01_RAW_DATA/autods/` (e.g. `autods_raw.md`) | yes |
| Screenshot image files | `90_CACHE/screenshots/autods/` (referenced from raw notes) | NO (non-versioned) |
| Cleaned tables | `02_DATA/02_CLEANED_DATA/autods_cleaned.md` (+ per-topic tables) | yes |
| Missing/owner-input gaps | `02_DATA/03_MISSING_DATA/autods_intake_missing_owner_inputs.md` | yes |
| Evidence labels | each captured fact → `[OBSERVED — owner-provided AutoDS screenshot/export, <date>]`; never invented | — |
| **Redaction rule** | credentials, card/billing numbers, payout/bank data, buyer PII → **REDACT, never stored** | — |

## 4. Forbidden actions (NONE without explicit owner GO)
- Log in to / connect AutoDS (controlled login is a separate, not-yet-granted GO).
- Change ANY AutoDS setting (pricing/repricing, monitoring, automation, templates, notifications).
- Enable/disable automation; add/remove/switch suppliers; change supplier mapping.
- Place/trigger supplier orders; publish/edit eBay listings; change prices live.
- Make payments; change billing/plan; export in any way that triggers a sync/order/platform change.
- Access eBay or supplier accounts; collect live account data without GO.
- Store credentials or unredacted PII anywhere.

## 5. Read-only intake checklist (owner-side, read-only — run only after GO)
> These are capture steps for the OWNER, read-only; they modify nothing. NOT a machine execution SOP.
1. [ ] Confirm AutoDS plan tier + add-ons → screenshot Subscription page (redact billing).
2. [ ] Connected store + sync status → screenshot Integrations/Stores page.
3. [ ] Product catalogue → export products CSV (if available) OR screenshot product list + a sample product (source supplier visible).
4. [ ] Supplier configuration → screenshot supplier settings + default supplier.
5. [ ] Pricing/repricing settings → screenshot current pricing rules (do not edit).
6. [ ] Automation settings → screenshot monitoring/auto-order/auto-tracking toggles + params.
7. [ ] Orders → export orders CSV (if available) OR screenshot recent orders + statuses.
8. [ ] Tracking sync → screenshot tracking status/logs.
9. [ ] Monitoring events → screenshot stock/price change events.
10. [ ] Errors/logs → screenshot automation error log.
11. [ ] Notifications → screenshot notifications/alerts.
12. [ ] Redact all credentials/billing/PII before sharing; hand off to machine for raw → cleaned tables.
> Stop after capture. The machine produces raw + cleaned notes only — no analysis/strategy until separately authorized.

## 6. Required owner inputs before AutoDS intake
See `02_DATA/03_MISSING_DATA/autods_intake_missing_owner_inputs.md`. In short: confirm plan/add-ons; choose capture method(s); confirm which eBay store; confirm redaction; give explicit GO to start intake; (only if wanting controlled login) a separate explicit GO + secure credential channel.

## 7. Stop condition
This is the plan. No AutoDS data collected. Intake begins only after a separate owner GO that authorizes the chosen capture method.
