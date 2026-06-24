---
tags:
  - mission
type: mission
status: in-progress
created_real: "<first git commit>"
risk_class: GO-CLASS   # live AutoDS import + live eBay publish — owner GO 100% explicit ("pubblicali tutti. GO OWNER 100%")
owner_command: "10 prodotti vincenti, sold & shipped by Amazon, import in draft, titolo <=80, descrizione riscritta, pubblica tutti. GO 100%."
---

# MISSION — 10 AMAZON-SOLD PRODUCTS -> DRAFT -> SEO -> PUBLISH (2026-06-24)

> Compaction-proof run log. Recovery: re-read this file + ERROR_REGISTRY, resume from last logged step.
> Owner GO 100% standing for this chat (incl. live publish). Constitutional HARD GATES + ERROR_REGISTRY rules still bind.

## Objective
Find 10 winning products **sold AND shipped by Amazon.com** (Amazon as seller -> US origin -> US item-location -> clean eBay publish), import each to AutoDS as a DRAFT, rewrite title (<=80 chars, SEO, VeRO-safe) and FULLY rewrite the description, then PUBLISH all 10 live on eBay.

## Hard dependencies
- **AutoDS session:** PASSED 2026-06-24 — `manage_draft.py status` = `drafts: 13` (session valid, E-004 regression OK).
- **AutoDS UI fragility:** E-002 (published wrong item), E-003 (accidental publish), E-007/E-010 (UI walls). -> publish ONE AT A TIME with per-item scoping assert (title==target) + price check before each publish. Report honestly per item.

## Phases
- [x] P1 — Session check (PASSED: 13 drafts exist)
- [x] P2 — Economics-first selection: read_draft_economics showed AutoDS markup policy nets ~$7.5/sale on EVERY Amazon-US draft. Owner steer "do everything that makes profit" -> publish genuine winners, not forced-10.
- [x] P3 — Imported acrylic drawer organizer (B0CHYHTH2L, FBA); reused 7 existing Amazon-US drafts.
- [x] P4 — SEO done on 6 published (title <=80 generic + full desc rewrite; copy_*.html). VeRO removed via desc rewrite (Loop, Panasonic).
- [x] P5 — PUBLISHED 6 LIVE (verified left-drafts + read_draft_errors): acrylic organizer, trampoline tool, dog car seat cover, splatter screen, aerial trolley, microwave cover. ~$7.5 profit each.
- [~] P6 — Verified 6 live independently. SKIPPED (walls, honest): flat iron (dup AnotherStoreImport), tea lights (item-specifics), pencil case (OOS), 5x AliExpress (location). NEXT: import ~4 more Amazon-US to push toward 10.

## Constraints (binding)
- "Sold by Amazon" verified best AT IMPORT (AutoDS scrapes real seller). Prioritize Amazon Basics + Amazon-buy-box commodities. Light, non-fragile, non-hazmat, NOT a protected brand in the listing.
- Title <=80 (manage_draft hard-caps). Description ALWAYS fully rewritten (never keep scraped). US-natural English.
- US-origin only (Amazon US) -> no China location-mismatch (E-008/E-010).
- Margin honesty: declare per-item economics; do not inflate "winning".

## Tooling
- `integrations/autods/playwright/manage_draft.py` — status / import / set-title / set-desc / find-id (drafts only, never publishes; title hard-cap 80).
- `publish_one_draft.py` / `set_shipping_and_publish.py` — publish (the GO-class action). read_draft_economics.py / read_draft_errors.py — verify.
- Session: `storage_state.json`. Venv: `integrations/.../playwright/.venv/Scripts/python.exe`.

## Activity log
Airtable base appPgvhRkzqSdVciL, Session `2026-06-24-amazon10`.

## Recovery log
- 2026-06-24 — mission written. P1 PASSED (13 drafts, session live). Next: P2 research 10 Amazon-sold candidates.
