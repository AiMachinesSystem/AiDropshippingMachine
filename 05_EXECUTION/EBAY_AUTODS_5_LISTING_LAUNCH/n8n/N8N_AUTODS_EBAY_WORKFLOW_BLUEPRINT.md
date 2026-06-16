---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: n8n_workflow_blueprint
status: blueprint
date: 2026-06-16
created_real: 2026-06-16
---

# n8n Workflow Blueprint — AutoDS → eBay (`divinit-92-us`)

> **Blueprint only.** n8n not installed/connected; no live execution. The AutoDS write call is a PLACEHOLDER
> behind a hard approval gate. Credentials referenced by NAME only (never raw keys). 5-listing scope.

## Stages
```text
1 Manual trigger
2 Load 5 listing rows      (read listings/sample_5_listing_input.csv)
3 Validate required fields (against listings/ebay_listing_schema.json + LISTING_VALIDATION_CHECKLIST.md)
4 Prepare AutoDS payload   (map validated rows → AutoDS draft payload)
5 Approval gate            (HARD STOP — wait for GO_IMPORT_5_DRAFTS / GO_PUBLISH_5)
6 AutoDS API call PLACEHOLDER  (disabled until gate open; uses n8n credential "autods_api")
7 Response logging         (status + ids only; no secrets/PII)
8 Measurement tracking     (write results → measurement/EBAY_5_LISTING_MEASUREMENT_TRACKER.md)
```

## Stage detail
| # | Node | In | Out | Safety |
|---|---|---|---|---|
| 1 | Manual Trigger | — | run | owner-initiated only |
| 2 | Read CSV | sample_5_listing_input.csv | 5 rows | read-only |
| 3 | Validate (Function/IF) | rows | pass/fail per row | blocks on any fail |
| 4 | Build payload (Function) | valid rows | AutoDS draft payloads | no API call |
| 5 | **Approval gate (Wait/Manual)** | payloads | release on GO | **HARD STOP — no GO, no pass** |
| 6 | AutoDS API (HTTP, DISABLED) | payloads | API response | disabled until gate; cred by name `autods_api`; drafts before publish |
| 7 | Log (Function/Set) | response | status/ids | never log key/PII |
| 8 | Track (Write file) | results | KPI rows | append to tracker |

## Rules
- The HTTP node stays **disabled** in the imported workflow until `GO_IMPORT_5_DRAFTS` (drafts) / `GO_PUBLISH_5` (publish).
- Credential is an n8n credential named `autods_api` — the raw key never appears in the workflow JSON.
- One run = the 5 rows; no auto-scheduling, no auto-ordering, no repricing in this workflow.
