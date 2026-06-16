---
machine: "eBay / AutoDS Dropshipping Machine"
type: intake_plan_report
module: 10_OUTPUTS
status: complete
date: 2026-06-15
created_real: 2026-06-15
external_access: none
live_changes: none
analysis: none
---

# AutoDS Read-Only Data Intake Plan — Report (2026-06-15)

> Deliverable for the "AutoDS Read-Only Data Intake Plan" GO (option 2). **Planning only** — no AutoDS login,
> no access, no live data, no strategy/recommendations/SOPs/product-selection/config. Full plan:
> `02_DATA/00_SOURCE_DISCOVERY/2026-06-15_autods-read-only-intake-plan.md`.

## 1. Plan created
Yes — defines categories, capture methods, storage map, forbidden actions, intake checklist, and required owner inputs. Nothing collected.

## 2. AutoDS data categories defined (12)
A Account & plan · B Connected store & sync · C Product catalogue · D Supplier configuration · E Pricing/repricing settings · F Automation settings · G Orders & fulfillment · H Tracking sync · I Monitoring events · J Errors/logs · K Notifications · L AutoDS analytics. (All read-only.)

## 3. Capture options defined
**Screenshots** (redacted) · **native exports** (CSV products/orders, download-only) · **guided read-only review** (owner screen-share/read-aloud) · **controlled login** — DEFERRED, only with a separate explicit future GO + secure credential channel (not authorized now). Preferred order: exports → screenshots → guided → (controlled login only if approved).

## 4. Storage map
Raw notes/exports → `02_DATA/01_RAW_DATA/autods/` · screenshots → `90_CACHE/screenshots/autods/` (non-versioned) · cleaned tables → `02_DATA/02_CLEANED_DATA/autods_cleaned.md` · gaps → `02_DATA/03_MISSING_DATA/autods_intake_missing_owner_inputs.md`. Every fact `[OBSERVED — owner-provided, <date>]`; **credentials/billing/PII redacted, never stored**.

## 5. Forbidden actions recorded (none without explicit GO)
No login/connect · no settings/automation/pricing/supplier changes · no orders/listings/payments · no exports that trigger platform changes · no eBay/supplier access · no credential or unredacted-PII storage. Controlled login = separate, not-yet-granted GO.

## 6. Required owner inputs (before intake)
Whether an AutoDS account exists; plan/add-ons; connected eBay store; chosen capture method(s); redaction confirmation; **explicit GO to start intake**; (if controlled login) a separate GO + secure channel. Detail: `02_DATA/03_MISSING_DATA/autods_intake_missing_owner_inputs.md`.

## 7. Missing data
AutoDS is NOT CONNECTED → plan/store/products/settings/orders all USER INPUT NEEDED; controlled login = OWNER GO REQUIRED. No live AutoDS fact exists yet.

## 8. Current phase
Unchanged: **Analysis → Strategy gate CLOSED.** This is a Data/Source-Discovery planning artifact; it advances no business gate and collects no data.

## 9. Next allowed step
Owner gives the prerequisites (§6) + an explicit **GO to start the AutoDS read-only intake**, choosing a capture method. Until then, no AutoDS data is collected. Strategy remains blocked (separate gate + economic data needed).

## 10. Owner approval required?
- For this plan: already authorized (this GO); **complete**.
- To START intake: **YES** — needs the owner inputs in §6 and an explicit GO; controlled login needs its own separate GO.
