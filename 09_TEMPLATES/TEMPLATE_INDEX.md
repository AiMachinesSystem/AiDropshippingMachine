---
tags:
  - machine
type: hub
status: active
date: 2026-06-11
---

# Template Index

> Index of all reusable templates and when to use each one.

## Purpose

These templates are the standard, reusable formats for the whole system. They are
brand-agnostic, product-agnostic, and market-agnostic — copy one, fill the
placeholders, and save it into the matching module folder.

## Templates

| # | Template | Use When | Feeds Module |
|---|---|---|---|
| 1 | [[DATA_ENTRY_TEMPLATE]] | Recording raw or cleaned data. | 02_DATA |
| 2 | [[ANALYSIS_REPORT_TEMPLATE]] | Turning data into insight. | 03_ANALYSIS |
| 3 | [[STRATEGY_BRIEF_TEMPLATE]] | Turning insight into decisions. | 04_STRATEGY |
| 4 | [[EXECUTION_TASK_TEMPLATE]] | Turning a decision into a task. | 05_EXECUTION |
| 5 | [[SOP_TEMPLATE]] | Documenting a repeatable procedure. | 05_EXECUTION |
| 6 | [[KPI_REPORT_TEMPLATE]] | Measuring a result. | 06_MEASUREMENT |
| 7 | [[LEARNING_ENTRY_TEMPLATE]] | Recording a lesson, error, or success. | 07_LEARNING |
| 8 | [[SCALING_DECISION_TEMPLATE]] | Deciding whether to scale. | 08_SCALING |
| 9 | [[MODULE_HANDOFF_TEMPLATE]] | Passing work between modules. | All |

## Usage Rules

1. Copy the template — do not edit the master file.
2. Replace every `<placeholder>` before saving.
3. Save the filled copy into the matching module folder.
4. Keep one record per file.

## Loop Reference

```
Data → Analysis → Strategy → Execution → Measurement → Learning → Scaling → (New Data Cycle)
```
