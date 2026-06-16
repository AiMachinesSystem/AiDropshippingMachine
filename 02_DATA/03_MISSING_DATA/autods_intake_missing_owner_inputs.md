---
machine: "eBay / AutoDS Dropshipping Machine"
type: missing_owner_inputs
module: 02_DATA
topic: AutoDS read-only intake prerequisites
status: active
date: 2026-06-15
created_real: 2026-06-15
---

# Missing Owner Inputs — AutoDS Read-Only Intake

> What the owner must provide/confirm BEFORE any AutoDS read-only intake starts. Plan only; nothing collected yet.

## Required before intake
| # | Input | Label | Needed for |
|---|---|---|---|
| 1 | Is there a live AutoDS account at all? (yes/no) | USER INPUT NEEDED | Decides whether intake is possible now |
| 2 | AutoDS plan tier + add-ons (e.g. Orders Processor) | USER INPUT NEEDED | Account/plan category (A) |
| 3 | Which eBay store is (or will be) connected | USER INPUT NEEDED | Connected-store category (B) |
| 4 | Chosen capture method(s): exports / screenshots / guided review | USER INPUT NEEDED | Capture approach (plan §2) |
| 5 | Redaction confirmation (credentials/billing/PII removed before sharing) | USER INPUT NEEDED | Safe storage (plan §3) |
| 6 | Explicit GO to START the read-only intake | OWNER GO REQUIRED | Authorizes the capture |
| 7 | (Only if controlled login wanted) separate explicit GO + secure credential channel | OWNER GO REQUIRED | Controlled-login is a distinct, not-yet-granted authorization |

## Notes
- AutoDS access is currently **NOT CONNECTED**; nothing about the live account is known (plan, store, products, settings, orders) = USER INPUT NEEDED.
- Default stance: **no login, no controlled login** unless input #7 is explicitly granted later.
- These prerequisites are separate from the broader open inputs in `MISSING_OWNER_INPUTS.md` (eBay account health, suppliers, category, margins, business data).
