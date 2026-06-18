---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: run_guide
status: active
date: 2026-06-16
created_real: 2026-06-16
---

# How to run the AutoDS read-only connection test

> `autods_readonly_test.py` is **read-only** (one GET to the verified `user-details` endpoint). It never
> writes/imports/publishes and never prints secrets. Python 3.8+ (stdlib only — nothing to install).

## 1. Put credentials in a LOCAL `.env` (NEVER committed, NEVER pasted in chat)
Create `.env` **in this folder** (`integrations/autods/.env`) — it is gitignored. Use `.env.example` as the shape:

```
AUTODS_API_BASE_URL=https://gw.autods.com
AUTODS_API_KEY=        # your AutoDS API JWT (or use AUTODS_JWT=)
AUTODS_STORE_NAME=divinit-92-us
AUTODS_STORE_ID=       # if your account exposes one
```

- The **API key/JWT comes from the AutoDS API feature** — which is application-gated + paid (see
  `AUTODS_API_READINESS.md` ⛔). If you don't have API credentials yet, you cannot run this test; choose the
  UI-based read-only intake instead.

## 2. Verify the file exists WITHOUT revealing its contents
- Windows PowerShell: `Test-Path .\.env`  → should print `True`
- Confirm it's ignored: `git check-ignore integrations/autods/.env` → should print the path (ignored).
- Do **not** `cat`/print the file in chat.

## 3. Run
```
cd 05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/integrations/autods
python autods_readonly_test.py
```

## 4. Interpret output
- `CREDENTIAL ACTION REQUIRED` → `.env` missing/incomplete; add the named variable(s) and re-run.
- `autods_reachable: yes` + `auth_valid: yes` → connection OK.
- `auth_valid: no (401/403)` → the JWT is wrong/expired or API access isn't active.
- The script prints only status/endpoint/meta — never your key, never the raw response body.

## Hard limits
This script does READ-ONLY only. Import/publish/price/relist/repricing/auto-ordering remain behind their GO gates
(`GO_IMPORT_5_DRAFTS`, `GO_PUBLISH_5`, `GO_UPDATE_PRICES`, `GO_RELIST_ITEMS`, `GO_ENABLE_REPRICING`).
