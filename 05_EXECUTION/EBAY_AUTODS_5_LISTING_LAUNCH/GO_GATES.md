---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: go_gates
status: active
date: 2026-06-16
created_real: 2026-06-16
---

# GO Gates — 5 Listing Launch

> Every live/external action is blocked until the owner types the exact GO token. Per-action; approval never
> transfers to the next action (CLAUDE.md §0.3). Default state of every gate below = **CLOSED**.

| GO token | Unlocks | Type | Status | Pre-conditions |
|---|---|---|---|---|
| `GO_AUTODS_API_READ_ONLY_TEST` | a read-only AutoDS API connectivity/auth check (no writes) | live read | CLOSED | API key available in a secure place (NOT in repo/chat) |
| `GO_CREATE_N8N_CREDENTIAL` | store the AutoDS key inside the n8n credential vault | secret handling | CLOSED | n8n installed; SECRETS_POLICY followed |
| `GO_IMPORT_5_DRAFTS` | import the 5 prepared rows into AutoDS as **drafts** (no publish) | live write (draft) | CLOSED | read-only test passed; 5 rows validated |
| `GO_PUBLISH_5` | publish the 5 listings live on eBay `divinit-92-us` | live publish | CLOSED | drafts reviewed; validation checklist all-pass |
| `GO_ENABLE_REPRICING` | turn on AutoDS repricing for the listings | live automation | CLOSED | listings live + measured stable |
| `GO_ENABLE_AUTO_ORDERING` | turn on AutoDS auto-ordering | live automation | CLOSED | repricing + supplier reliability validated |

## Rules
- No gate is implied by another; each is explicit and separate.
- A failed/uncertain step at a gate boundary → STOP and ask (CLAUDE.md §6).
- Nothing in this repo may execute a gated action; the machine prepares, the owner authorizes.
