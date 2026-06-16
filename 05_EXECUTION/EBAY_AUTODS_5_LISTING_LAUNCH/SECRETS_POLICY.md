---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: secrets_policy
status: active
date: 2026-06-16
created_real: 2026-06-16
---

# Secrets Policy — 5 Listing Launch

> Binding for anything touching AutoDS/eBay/n8n credentials in this project.

## Rules
1. **Never store real keys/tokens/passwords in the repo.** Not in any `.md`, `.json`, `.csv`, or committed file.
2. **`.env` must be gitignored** and contains real values **only on the owner's local machine** — never committed, never shared in chat. The repo ships only `.env.example` (variable **names**, no values).
3. **n8n credentials preferred** — store the AutoDS API key in the n8n credential vault (encrypted), not in flat files. The workflow references the credential by name, never the raw key.
4. **No secrets in chat** — the assistant never asks for, and the owner never pastes, API keys/tokens/passwords here.
5. **No screenshots with visible tokens** — redact keys/tokens/emails/billing before sharing any screenshot.
6. **Rotation** — if a key is ever exposed (chat, screenshot, commit), rotate it immediately in AutoDS.

## Variable handling
| Variable | Where the real value lives | In repo? |
|---|---|---|
| `AUTODS_API_KEY` | owner's local `.env` (gitignored) → later n8n credential vault | NO |
| `AUTODS_API_BASE_URL` | `.env` (non-secret but env-managed) | example only |
| `AUTODS_STORE_ID` | `.env` | NO (value) |
| store name / marketplace / country / currency | non-secret context (`divinit-92-us` / eBay.com / US / USD) | OK as context |
| `N8N_WEBHOOK_URL` | `.env` / n8n | example only |

## Enforcement
`.gitignore` blocks `.env` and common secret patterns. Any accidental secret in a diff = stop, scrub, rotate, do not commit.
