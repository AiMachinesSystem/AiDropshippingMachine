---
tags:
  - machine
type: playbook
status: active
date: 2026-06-10
---

# Scaling Decision — <what is being scaled>

> Standard template for deciding whether something is ready to scale based on
> validation, KPI evidence, risk, and monitoring requirements.
> Module: 08_SCALING · Rules: [[SCALING_DECISION_RULES]]

## Metadata

| Field | Value |
|---|---|
| Scaling type | <from [[SCALING_TYPES]]> |
| Date | <YYYY-MM-DD> |
| Source pattern | <validated pattern> |
| Validation signal | <present \| absent> |

## Readiness Check (all must pass — [[SCALING_READINESS_RULES]])

- [ ] Validated result
- [ ] Clear KPI improvement
- [ ] Repeatable process
- [ ] Controlled risk
- [ ] Available resources
- [ ] Measurement system ready
- [ ] Owner defined
- [ ] Rollback option available

## Decision

| Field | Value |
|---|---|
| Reason | <why scale> |
| What increases | <exact variable> |
| What is monitored | <KPIs> |
| Risk check | <from [[RISK_CONTROL_FOR_SCALING]]> |

## Monitoring Plan ([[SCALING_MONITORING_RULES]])

| Field | Value |
|---|---|
| Baseline | <pre-scaling value> |
| Expected result | <prediction> |
| Warning signal | <early failure sign> |
| Stop condition | <halt threshold> |
| Next review | <YYYY-MM-DD> |

## Handoff

New data feeds [[SCALING_HANDOFF_TO_NEW_DATA_CYCLE]]: <yes \| no>
