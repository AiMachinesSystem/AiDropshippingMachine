---
tags:
  - machine
  - agents
type: reference
status: active   # Airtable base/table created 2026-06-23; ids below
description: "Pointer + write protocol for the machine's Agent activity log (Airtable). The 3 subagents and the orchestrator append decision/blocker/completion rows here. File-based fallback (.remember/now.md) when the base id is absent or the MCP is unreachable."
created_real: "0d4aed3 (2026-06-23)"
---

# AGENT ACTIVITY LOG — pointer & protocol

Opt-in audit trail of what the machine's agents did and why (decisions, blockers, completions),
adapted from the `airtable:agent-activity-log` pattern to a **file-based vault**: no per-table
linked records (the machine has no Airtable workflow tables) — instead a `Target ref` URL/path
field points at the touched vault artifact, with a `Target area` selector.

## Airtable coordinates
- **Workspace:** `wspiarbJDHGIZJpVn` (My First Workspace)
- **Base id:** `appPgvhRkzqSdVciL`
- **Table id:** `tblRhHSf0kzb62RHi`
- **Table name:** `Agent activity log`
- **Field ids:**
  - `Summary` = `fldFM7R1A4CjY6bF0` (primary) · `Agent` = `fldGzBR5wujzltcPU` · `Action` = `fldeXGjan7F4TDZaE` · `Reasoning` = `fldVOwSWUWi6Kk4SB` · `Outcome` = `fldQexQxDpQSypKlz` · `Status` = `fldWjB6Cdv6Idc1W0` · `Target area` = `fld4UEh3InTNkfyM2` · `Target ref` = `fld6fXf4vJrwSgqbh` · `Session ID` = `fldE9xcYs7NXYqool`
- **View:** Grid view `viwU36ZqKc1UajFcz`
- **URL:** https://airtable.com/appPgvhRkzqSdVciL/tblRhHSf0kzb62RHi

## Schema (single table)
| Field | Type | Notes |
|---|---|---|
| `Summary` | singleLineText (primary) | one-line what-happened |
| `Timestamp` | createdTime | auto |
| `Agent` | singleSelect | us-product-scout · draft-publisher · vault-auditor · orchestrator |
| `Action` | singleSelect | Decision · Blocker · Question · Completion · Error · Create · Update |
| `Reasoning` | multilineText | intent + alternatives rejected |
| `Outcome` | singleSelect | Completed · Partial · Failed · Blocked |
| `Status` | singleSelect | Open · Acknowledged · Resolved · Stale |
| `Target area` | singleSelect | Research · Draft · Publish · Vault · Mission · Error |
| `Target ref` | singleLineText | vault path or eBay/AutoDS/git url to the touched artifact |
| `Session ID` | singleLineText | ties one run's events together |

## Write protocol (for agents & orchestrator)
1. **Session start:** write one `Completion`/`Completed` row naming what the session starts on; its `Session ID` is the tie-thread.
2. **Meaningful decision:** `Decision` row with full `Reasoning` (alternatives rejected).
3. **Blocker / GO-gate wait:** `Blocker` or `Question` row, `Status=Open`.
4. **Error:** `Error` row, `Outcome=Failed`, context in `Reasoning`.
5. **Session end:** `Completion` row summarizing outputs + unresolved items.
Don't over-log: meaningful decisions/changes only, not every tool call. Reads usually aren't logged.

## Fallback
If the base id above is still a placeholder, or the Airtable MCP is unreachable, append the same
one-line event to `.remember/now.md` instead, prefixed `[agent-log]`. Never block work on the log.
