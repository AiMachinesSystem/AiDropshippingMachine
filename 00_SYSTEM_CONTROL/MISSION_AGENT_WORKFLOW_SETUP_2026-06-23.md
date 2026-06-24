---
tags:
  - mission
type: mission
status: complete
created_real: "<first git commit>"
risk_class: MIXED  # internal agent files (no gate) + 1 GO-CLASS step (Airtable base/table = external write)
owner_command: "TUTTO! (build subagents + Airtable agent activity log)"
---

# MISSION — AGENT WORKFLOW SETUP (2026-06-23 23:09 -04:00)

> Compaction-proof run log. Recovery: re-read this file + `.remember/remember.md`, resume from last logged step.

## Objective
Stand up the machine's autonomous-agent stack:
1. Three repo-versioned subagents in `.claude/agents/` that wrap the machine's recurring workflows.
2. An opt-in Airtable `Agent activity log` (auditable decision/blocker/completion trail), adapted to a file-based vault (URL/path-ref fallback, not per-table linked records — the machine has no Airtable workflow tables).

Owner gave "TUTTO!" in response to the build-everything option. The Airtable base creation was named as a GO-gated external write inside that option.

## Risk class: MIXED
- **INTERNAL (no gate):** writing the 3 agent `.md` files, the activity-log pointer file, this mission, local git commit.
- **GO-CLASS (stop + cite gate):** creating the Airtable base + `Agent activity log` table (external write). Discovery (list bases/workspaces) is read-only and already done.

## Phases
- [x] P1 — 3 subagents written in `.claude/agents/` (us-product-scout, draft-publisher, vault-auditor)
- [x] P2 — activity-log pointer written `00_SYSTEM_CONTROL/AGENT_ACTIVITY_LOG.md`
- [x] P3 — **GO given (TUTTO)**: base `appPgvhRkzqSdVciL` + table `Agent activity log` (`tblRhHSf0kzb62RHi`) created
- [x] P4 — pointer backfilled with base/table/field ids; log seeded with 7 real session events; local commit

## Schema (Agent activity log) — adapted to file-based vault
Single table. Fields:
- `Summary` (singleLineText, primary)
- `Timestamp` (createdTime)
- `Agent` (singleSelect: us-product-scout, draft-publisher, vault-auditor, orchestrator)
- `Action` (singleSelect: Decision, Blocker, Question, Completion, Error, Create, Update)
- `Reasoning` (multilineText — intent + alternatives rejected)
- `Outcome` (singleSelect: Completed, Partial, Failed, Blocked)
- `Status` (singleSelect: Open, Acknowledged, Resolved, Stale)
- `Target area` (singleSelect: Research, Draft, Publish, Vault, Mission, Error)
- `Target ref` (URL/text — vault path or git/eBay/AutoDS link to the touched artifact)
- `Session ID` (singleLineText — ties one run's events)

## Constitutional checks (§0)
- Evidence labels enforced in agent prompts. GO gate hard. Firewall to this machine. No invented numbers. Owner replies in Italian.

## Recovery log
- 2026-06-23 23:09 — mission written; discovery done (0 bases, 1 workspace owner). Next: P1 agent files.
- 2026-06-23 23:09 — P1+P2 done: 3 agent files + pointer written. Parked at P3 GO gate (Airtable create_base shown).
- 2026-06-23 23:22 — owner GO ("TUTTO" x2). P3 done: base `appPgvhRkzqSdVciL` / table `tblRhHSf0kzb62RHi` created.
- 2026-06-23 23:22 — P4 done: pointer backfilled with field ids; 7 real session events seeded to the log; MACHINE_STATE updated. Mission COMPLETE. Next (separate task): first us-product-scout run — BLOCKER to check first = AutoDS Marketplace access/login state.
