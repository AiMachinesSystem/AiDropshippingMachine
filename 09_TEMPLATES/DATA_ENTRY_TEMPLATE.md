---
tags:
  - machine
type: playbook
status: active
date: 2026-06-10
---

# Data Entry — <data point name>

> Standard template for recording raw or cleaned data before analysis.
> Module: 02_DATA · Rules: [[DATA_COLLECTION_RULES]] · Quality: [[DATA_QUALITY_RULES]]

## Metadata

| Field | Value |
|---|---|
| Source | <where it came from> |
| Date | <YYYY-MM-DD> |
| Category | <from [[DATA_CATEGORIES]]> |
| Purpose | <why it was collected> |
| Fact / Assumption | <fact \| assumption> |
| Reliability | <high \| medium \| low> |
| Freshness | <fresh \| usable \| stale \| expired \| unknown> (per [[DATA_FRESHNESS_RULES]]) |
| State | <raw \| cleaned> |

## Data

<the raw or cleaned data — values, table, or notes>

## Source Notes

<links, context, how it was captured>

## Quality Check

- [ ] Source recorded
- [ ] Date recorded
- [ ] Category assigned
- [ ] Purpose stated
- [ ] Fact/assumption labeled
- [ ] Duplicates checked
- [ ] Gaps flagged

## Handoff

Ready for [[DATA_HANDOFF_TO_ANALYSIS]]: <yes \| no>
