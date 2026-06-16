---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: n8n_credential_setup
status: guide
date: 2026-06-16
created_real: 2026-06-16
---

# n8n Credential Setup (owner-operated)

> How the AutoDS key will live in n8n **without ever entering the repo or chat**. Setup happens later,
> behind `GO_CREATE_N8N_CREDENTIAL`. No key is requested or stored now.

## Principle
The workflow references a credential **by name** (`autods_api`). n8n stores the actual key encrypted in its
own credential vault. The repo, the workflow JSON, and this chat never hold the raw key.

## Steps (owner, when GO given)
1. [ ] Install/run n8n locally (owner-operated; separate from this repo).
2. [ ] In n8n → Credentials → New → (HTTP Header Auth / AutoDS) → name it exactly **`autods_api`**.
3. [ ] Paste the AutoDS API key into the n8n credential field (in n8n only — never in chat/repo).
4. [ ] Set non-secret env in n8n: `AUTODS_STORE_NAME=divinit-92-us`, `EBAY_MARKETPLACE=eBay.com`, `EBAY_COUNTRY=US`, `CURRENCY=USD`.
5. [ ] Keep `AUTODS_API_BASE_URL` / `AUTODS_STORE_ID` in env or the credential (confirm exact values from AutoDS docs/account).
6. [ ] Import the workflow blueprint; confirm the AutoDS HTTP node stays **disabled** until the import/publish GO.

## Forbidden
- Pasting the key into chat, a repo file, or a screenshot.
- Committing any real `.env`.
- Enabling the AutoDS write node before `GO_IMPORT_5_DRAFTS` / `GO_PUBLISH_5`.

## Verify
- `git status` shows no `.env` and no credential file.
- Workflow JSON contains only the credential **name**, never the key.
