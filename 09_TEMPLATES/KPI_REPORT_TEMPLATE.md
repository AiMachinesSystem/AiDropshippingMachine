---
tags:
  - machine
type: playbook
status: active
date: 2026-06-10
---

# KPI Report — <report name>

> Standard template for tracking results, KPIs, expected vs actual outcomes,
> variance, and result classification.
> Module: 06_MEASUREMENT · Rules: [[PERFORMANCE_TRACKING_RULES]]

## Metadata

| Field | Value |
|---|---|
| Source action | <action being measured> |
| Date | <YYYY-MM-DD> |
| Objective | <what this measures> |

## KPI Results

| KPI | Source | Expected | Actual | Variance |
|---|---|---|---|---|
| <from [[KPI_DICTIONARY]]> | <source> | <expected> | <actual> | <gap> |

## Interpretation

<what the result means — facts only>

## Result Classification

| Field | Value |
|---|---|
| Classification | <from [[RESULT_CLASSIFICATION]]> |
| Decision signal | <from [[KEEP_FIX_ELIMINATE_SCALE_RULES]]> |

## Missing Data / Flags

<gaps flagged; unclear performance is NOT marked as success>

## Handoff

Learning input ready for [[MEASUREMENT_HANDOFF_TO_LEARNING]]: <yes \| no>
