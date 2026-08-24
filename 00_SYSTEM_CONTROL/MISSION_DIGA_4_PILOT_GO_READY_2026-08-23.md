---
tags:
  - machine
  - mission
type: mission
status: in_progress
date: 2026-08-23
created_real: 2026-08-23
issue: DIGA-4
---

# DIGA-4 — eBay pilot GO-ready pack

**Owner:** Luca · **Risk class:** GO-CLASS · **Started:** 2026-08-23T19:40:34-04:00

## Objective

Correct the pilot category with eBay Taxonomy evidence, resolve duplicate-listing risk, regenerate the local action pack, and stop before every external write.

## Inputs

- `05_EXECUTION/ebay-direct/manifests/pilot-01.json`
- `05_EXECUTION/ebay-direct/action-packs/PILOT-20260823-01.json`
- Public/read-only eBay Taxonomy and Browse API responses
- eBay Duplicate listings policy

## Allowed

Read-only public/API checks, internal reversible edits, local validation, dry-run pack generation, tests, and Paperclip issue documentation.

## Forbidden

`apply-inventory`, `create-offer`, `publish-offer`, account modifications, listing modifications, spend, supplier orders, secret disclosure, commits, and push.

## Phases

1. Verify category and live-listing facts.
2. Obtain BAY-PROFIT risk/economics review and BAY-SOURCING identity/provenance review.
3. Select one policy-safe strategy and correct the manifest.
4. Regenerate and verify the pack locally.
5. Record evidence and the exact GO gate in Paperclip.

## Measurement

PASS requires a non-placeholder category supported by eBay Taxonomy, no unresolved duplicate-policy conflict, a fresh local validation PASS, deterministic hash verification, test/typecheck PASS, and zero eBay writes.

## Stop condition

If product identity, supplier provenance, image rights, or policy compliance remains unverified, do not call the pack GO-ready; block on the owning agent/action instead of publishing.
