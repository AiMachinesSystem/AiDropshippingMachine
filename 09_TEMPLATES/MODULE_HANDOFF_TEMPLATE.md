---
tags:
  - machine
type: playbook
status: active
date: 2026-06-10
---

# Module Handoff — <from module> → <to module>

> Standard template for passing work from one module to the next.
> Reference: [[MODULE_MAP]] · [[OPERATING_RULES]]

## Loop Position

```
Data → Analysis → Strategy → Execution → Measurement → Learning → Scaling → (New Data Cycle)
```

## Metadata

| Field | Value |
|---|---|
| From module | <module> |
| To module | <module> |
| Date | <YYYY-MM-DD> |
| Item | <what is being handed off> |

## Handoff Payload

| Field | Value |
|---|---|
| Output produced | <result from sending module> |
| Source / trace | <where it came from> |
| Evidence / strength | <strong \| medium \| weak> |
| Owner | <owner type> |

## Handoff Requirements

- [ ] Output is complete
- [ ] Traced to a valid source
- [ ] Evidence strength labeled
- [ ] Owner assigned
- [ ] Meets the sending module's handoff rules

## Receiving Module Entry Check

- [ ] Required inputs present
- [ ] Passes receiving module's entry rule
- [ ] Accepted (not returned)

## Status

Handoff: <ready \| returned \| accepted>
