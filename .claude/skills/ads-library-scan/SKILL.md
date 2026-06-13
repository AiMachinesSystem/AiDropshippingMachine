---
name: ads-library-scan
description: Meta Ad Library scan for any page, brand, keyword, or niche — active ad counts, start dates and longevity (performance proxy), hooks and copy patterns, duplicated-winner clusters, language/geo rollout. Use this skill whenever the owner asks anything about competitor ads or ad patterns — triggers include "che ads fanno", "quante ads attive ha", "da quanto girano le ads", "pattern delle ads", "quali hook usano", "ads library", "scan delle ads", "cosa pubblicizza X", "fammi vedere le ads di". ALSO use it in QUERY MODE to answer ad-pattern questions already covered by past runs (read RESEARCH_MEMORY_INDEX first, never re-scan for a lookup). This skill is also the data engine that niche-intelligence-run and competitor-scan call for Tasks involving the Ad Library.
---

# Ads Library Scan

Reproducible Meta Ad Library reader. Read-only, no login, zero spend.
**v1.1 (2026-06-13)** — adds: canonical-numbers rule, universe separation,
Library-ID collision protocol, QUERY MODE answer template, freshness rule.
**v1.2 (2026-06-13)** — adds: evidence fetch-cache rule, KNOWN_WALLS registry rule.
**v1.3 (cockpit auto-refresh)** — AUTO-REFRESH cockpit obbligatorio
al close-out (MASTER_DASHBOARD + NEXT_ACTIONS), stessa forza della regola
indice.

## EVIDENCE CACHE + KNOWN WALLS (v1.2)

- **Fetch cache:** every load-bearing render (Ad Library pages, products.json,
  policy pages) is saved to `90_CACHE\fetches\<domain>\<date>_<slug>.txt`
  BEFORE being cited; citations read `[OBSERVED — url + date (cache: path)]`.
  Re-runs within ~7 days check the cache before fetching.
- **Known walls:** before retrying a blocked surface, check the KNOWN WALLS
  table in `00_SYSTEM_CONTROL\VAULT_CONVENTIONS.md` — a registered wall is
  re-tested only if >7 days old or on explicit owner request. New walls get a
  row (wall · date · outcome).

## MODE SELECTION (first decision, always)

- **QUERY MODE** — the question is answerable from past scans: open
  `RESEARCH_MEMORY_INDEX.md` (expected at `00_SYSTEM_CONTROL/`), answer from
  the niche block + linked report, cite file + scan date; offer a re-scan if
  >30 days old or if the question needs fresher granularity.
- **RUN MODE** — new scan → protocol below.

## QUERY MODE DISCIPLINE (v1.1)

- **Canonical numbers:** census/ad counts come ONLY from the niche block's
  most recent registered run (`last_run` line + its headline). Older lines in
  the same block (earlier runs' census rows) are HISTORY — never quote them
  as current. If two lines conflict, the newest run wins; say so.
- **Answer template:** `<answer> — fonte: <report file>, run <date>` +
  (only if >30 days old) refresh offer.
- **Freshness:** if the index block was updated within ~7 days, answer from
  the index directly; open the linked report only when the question needs
  per-ad/per-competitor detail the index line doesn't carry.

## INPUTS

Page name · page ID · keyword(s) · or a niche label. For niches, expand to
localized keyword seeds taken from the target's own slugs/locales (never
invent translations blindly — read them off the target's site).

## METHOD (the reproducible recipe)

Base URLs:
- keyword: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q=<KW>&search_type=keyword_unordered`
- page history: `https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&view_all_page_id=<PAGE_ID>`
- single ad: `https://www.facebook.com/ads/library/?id=<LIBRARY_ID>`

Direct fetch = blocked (socket close / 403 JS-challenge). Working route:
**prefix the full URL with `https://r.jina.ai/`** (public rendering proxy).
Flaky ~1-in-3 (CAPTCHA/503): retry ≤2 per URL, then mark [UNKNOWN].
Renders Library IDs, start dates, page names, full ad copy. Renders only
≈10–28 ad blocks per page → **all counts are lower bounds; always say so.**

Known walls — mark [UNKNOWN] + add exact URLs to the owner-manual
checklist, do not burn retries: EU-transparency reach/demographic dropdowns ·
Page Transparency box (page creation date, manager countries) · ad
formats/media types · reliable `country=` filtering on page-ID views.

## PER-AD EXTRACTION

Library ID · start date · days active (longevity = the performance proxy) ·
page name/ID · hook (first line / first 3s) · angle class · CTA ·
destination URL/domain · language · near-duplicate cluster size (copies of
the same creative).

**Library-ID collision protocol (v1.1):** the proxy occasionally attributes
the same Library ID to two different pages across renders. When detected:
(1) flag the row `[UNKNOWN — extraction collision]` with both candidate
pages; (2) count the ad at most ONCE, under the page whose other ads share
its hook/destination (conservative attribution), or exclude it from both
counts if no overlap; (3) never let a disputed row flip an advertiser's
tier; (4) report the total number of collisions in the scan's caveats.

**Universe separation (v1.1):** structurally different markets (different
geo/price/funnel universe — e.g. LATAM WhatsApp-funnel sellers vs EU/US web
funnels) are counted and reported SEPARATELY. The headline census number is
the core market; other universes are named alongside it, never silently
summed ("~25 core + ≥27 LATAM-ES", not "52").

## PATTERN SYNTHESIS

- Hook taxonomy: pain · dream-outcome · value-arbitrage · proof · urgency.
- Duplication structure: copies per winning creative (testing style).
- Format escalation: plain product ad → long-form advertorial → VSL.
- Rollout sequencing by language/geo (what they advertise vs what exists
  on-site).
- Warm-audience layers (page-follow / engagement campaigns).
- **Noise filter**: keyword results are routinely hijacked by unrelated
  coordinated networks (supplement/dropship swarms). Verify advertiser
  relevance at PAGE level before counting it in any census.

## EVIDENCE & SAFETY (binding)

Every claim labeled [OBSERVED — source + access date] / [INFERRED — basis]
/ [UNKNOWN]. Lower bounds stated. Absence claims carry a LOW-SAMPLE flag.
Read-only public data; zero spend, logins, purchases, contact. Quantitative
claims verified against raw rendered text, never reconstructed from memory.

## OUTPUT

- Standalone scan:
  `10_OUTPUTS/ADS_LIBRARY_SCANS/YYYY-MM-DD_<TARGET-SLUG>_ADS_SCAN_vN.md`
  (findings + per-ad table + pattern synthesis + owner-manual checklist).
- When called by `niche-intelligence-run` or `competitor-scan`: deliver as a
  section of that run's report instead (no duplicate file).

## MANDATORY CLOSE-OUT

Write/refresh the "top ad patterns" and key counts in the niche's block in
`RESEARCH_MEMORY_INDEX.md`. **No registration = scan INCOMPLETE.** Report
the file path (or host report) + the index lines written.
**AUTO-REFRESH cockpit (v1.3, stessa forza della regola indice):** after
index registration, update `00_SYSTEM_CONTROL\MASTER_DASHBOARD.md` (ultimi
run · KPI) + `00_SYSTEM_CONTROL\NEXT_ACTIONS.md`; new owner actions become
task notes in `00_SYSTEM_CONTROL\TASKS\`. **No cockpit refresh = scan
INCOMPLETE.**
