---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: project_readme
status: scaffold
date: 2026-06-16
created_real: 2026-06-16
---

# eBay / AutoDS — 5 Listing Launch (internal integration scaffold)

> **Internal execution-planning scaffold.** No live actions, no API calls, no secrets, no publishing.
> Subordinate to `CLAUDE.md` + `01_SYSTEM/LAUNCH_ORIENTED_OPERATING_PROTOCOL.md`. This is the sealed
> project folder (firewall §0.6) for the 5-listing launch.

## Goal
Prepare **5 eBay.com listings** for the US store **`divinit-92-us`** via a controlled pipeline:

```text
Claude Code (builds the system)  →  n8n (executes the workflow)  →  AutoDS API (talks to eBay)  →  eBay store divinit-92-us
```

- **Claude Code** — builds local scaffolding, schemas, blueprints, checklists, validation; never calls live APIs.
- **n8n** — executes the workflow once built/credentialed (owner-operated; not connected yet).
- **AutoDS API** — the integration layer to eBay; **no calls until `GO_AUTODS_API_READ_ONLY_TEST`**.
- **eBay store `divinit-92-us`** — eBay.com / US / USD; live writes need explicit per-action GO.

## Folder map
- `CURRENT_STATUS.md` · `NEXT_ACTIONS.md` · `GO_GATES.md` · `SECRETS_POLICY.md`
- `integrations/autods/` — API readiness, client spec, store mapping, `.env.example`
- `n8n/` — workflow blueprint, payload template, credential setup
- `listings/` — eBay listing JSON schema, sample CSV, validation checklist
- `measurement/` — 5-listing KPI tracker

## Hard rule
Nothing here calls a live platform. Every live/external step is gated (see `GO_GATES.md`).
