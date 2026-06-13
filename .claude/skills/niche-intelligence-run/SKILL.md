---
name: niche-intelligence-run
description: Full niche validation and market census for ANY niche, anchored on a competitor URL, a product page, or a niche name. Use this skill whenever the owner asks to analyze, validate, size, or explore a niche or market — triggers include "analizza questa nicchia", "analizza questo mercato", "c'è mercato per", "valida la nicchia", "niche analysis", "quanto è grande il mercato di", "possiamo entrare in", "fammi una ricerca su questo" (with a URL), or any broad "analizza questo" pointed at a product/competitor. ALSO use it in QUERY MODE to answer questions about niches already studied ("il mercato X è valido?", "quanti competitor ci sono in X?", "che verdetto avevamo dato?") by reading RESEARCH_MEMORY_INDEX instead of re-running. When in doubt between "competitor question" and "niche question", this skill owns market-level answers.
---

# Niche Intelligence Run

Market validation + competitor census for any niche. Read-only research.
GO/NO-GO always stays with the owner.
**v1.1 (2026-06-13)** — adds: QUERY MODE discipline (canonical numbers,
answer template, freshness), universe separation in census + verdicts.
**v1.2 (2026-06-13)** — adopts ads-library-scan v1.2 evidence-cache +
KNOWN_WALLS rules (cache load-bearing fetches in `90_CACHE\fetches\`; check
the walls table in `00_SYSTEM_CONTROL\VAULT_CONVENTIONS.md` before retrying
blocked surfaces).
**v1.3 (cockpit auto-refresh)** — AUTO-REFRESH cockpit obbligatorio
al close-out (MASTER_DASHBOARD + NEXT_ACTIONS), stessa forza della regola
indice.

## MODE SELECTION (first decision, always)

- **QUERY MODE** — the request is a question answerable from past runs
  ("quanti competitor", "era PROVEN?", "che gap c'era?"):
  1. Open `RESEARCH_MEMORY_INDEX.md` (expected at `00_SYSTEM_CONTROL/`;
     if not there, search the vault by filename).
  2. Answer from the niche block + the linked report. Cite file + run date.
  3. If the data is >30 days old, say so and offer a refresh.
  4. NEVER launch a full run for a lookup.
  5. **Canonical numbers (v1.1):** counts come ONLY from the block's most
     recent registered run (`last_run` + its headline); older census lines in
     the same block are history — never quote them as current; on conflict
     the newest run wins, and say so.
  6. **Template (v1.1):** `<answer> — fonte: <report file>, run <date>`
     (+ refresh offer only if >30 days). Block updated within ~7 days →
     answer from the index directly; open reports only for detail.
- **RUN MODE** — new analysis requested, or no index entry exists → protocol
  below.

## STEP 0 — NICHE CLASSIFICATION (mandatory, before anything else)

From the anchor (URL / product / name), define and STATE at the top of the
output:

- niche label (this becomes the index key and the file slug)
- product class: digital / physical / hybrid · offer model (bundle, course,
  library, membership, single SKU, free-funnel)
- buyer profile + skill level (beginner/advanced)
- price band observed on the anchor
- adjacent niches (named, so future runs can link)
- anchor's languages/geos

Then check `RESEARCH_MEMORY_INDEX.md`:
- entry for this niche exists → load that report as prior dataset, say so,
  and run as an EXTENSION (vN+1), not a restart;
- no entry → this is a NEW niche: never inherit context, claims gates, or
  assumptions from other projects or previously studied niches.
- genuinely ambiguous anchor → ask the owner ONE question; otherwise proceed
  and label assumptions [INFERRED].

## RESEARCH QUESTIONS (the run must answer all four, with evidence)

Q1 Does the niche have real demand? · Q2 Who/how many advertise it (census +
tiers)? · Q3 What strategies/ads/funnels do they run, for how long? · Q4 Is
there room to enter, and where exactly (gap map)? → final recommendation +
confidence.

## FIXED VERDICT CRITERIA (declare BEFORE looking at data)

- **MARKET PROVEN** if ≥3 advertisers sustained ≥90 days within the last 12
  months AND demand trend stable or positive on proxies.
- **SPACE = YES** if proven AND ≥1 clear gap (angle / language / format /
  price band / quality / credibility) not held by a T1 player.
  **SPACE = TIGHT** if T1s cover all main angles+geos and only a price race
  remains.
- **Tiering defaults**: T1 = ≥30 active ads OR multi-language funnels OR
  ≥90d continuous OR high reach. T2 = 10–29 ads / 30–90d / 1–3 geos.
  T3 = <10 ads or <30d or throwaway pages.
- Adapting thresholds to the niche is allowed ONLY if declared up front with
  a one-line rationale.

## TASKS

- **TASK 0 — demand signals**: Google Trends 5y+12m (seeds incl. localized
  ones taken from the anchor's own slugs); marketplace proxies fit to the
  niche (marketplace review counts, affiliate-marketplace gravity, app stores — pick
  what applies, justify the pick); community sizes (Reddit growth, FB
  groups, YouTube subs). Output a DEMAND VERDICT
  (growing/stable/declining + seasonality) tagged [INFERRED] with evidence.
- **TASK 1 — anchor deep-dive**: run the `ads-library-scan` skill method on
  the anchor page (IDs, start dates, longevity, hooks, duplication,
  languages) + site teardown (offer ladder, prices, anchors, bonuses,
  guarantee/refund wording, proof audit, tech stack signals).
- **TASK 2 — census**: keyword scans incl. localized seeds; one row per
  distinct advertiser (page, #active ads as lower bound, oldest active start
  date, langs, destination domain, visible price); clone-network check
  (copy overlap, RDAP dates); tier every advertiser; collapse same-operator
  groups [INFERRED] when checkout/domains match.
  **Universe separation (v1.1):** structurally different markets
  (geo/price/funnel universes, e.g. WhatsApp-funnel LATAM vs EU/US web)
  get separate census numbers and separate verdict lines; the headline
  number is the core market, others named alongside, never silently summed.
  Library-ID collisions follow the `ads-library-scan` v1.1 protocol
  (flag, count once conservatively, report collision total).
- **TASK 3 — strategy extraction per tier**: angle taxonomy, funnel types,
  duplication/testing cadence, pricing & anchor patterns, proof tactics,
  localization sequencing.
- **TASK 4 — synthesis**: gap map (who holds what / UNHELD), verdicts per the
  fixed criteria, recommendation + confidence, rejected alternatives with
  reasons.

## METHOD & KNOWN WALLS

Direct `facebook.com/ads/library` is blocked (403/JS challenge). Working
route: prefix the full URL with `https://r.jina.ai/` (public rendering
proxy; ~1-in-3 calls fail with CAPTCHA/503 → retry ≤2, then [UNKNOWN]).
Renders ≈10–28 ad blocks per page → ALL counts are lower bounds; say so.
Known walls — do not burn retries, mark [UNKNOWN] + add to the owner-manual
checklist with exact URLs: EU-transparency reach/demo dropdowns · Page
Transparency box · ad formats/media · Etsy listing pages · Google Trends
(429). Absence claims ("zero advertisers in FR") always carry a LOW-SAMPLE
flag.

## EVIDENCE & SAFETY (binding)

Every claim labeled [OBSERVED — source + access date] / [INFERRED — basis]
/ [UNKNOWN]. Never estimate, never fill gaps. Read-only public sources only:
zero spend, logins, purchases, contact. Never modify other projects' launch
or decision files. Fabricated-proof tactics found in the market are recorded
as findings and anti-patterns, NEVER as recommendations.

## OUTPUT

One file:
`10_OUTPUTS/MARKET_RESEARCH_REPORTS/YYYY-MM-DD_<NICHE-SLUG>_NICHE_VALIDATION_vN.md`
Standard structure: Verdict · Confidence · Evidence basis · Dominant market
pattern · Demand signal · Recommended move · Why this move · Rejected
alternatives · Owner role · Measurement plan · Blockers/open items
(owner-manual checklist) · Files updated.

## MANDATORY CLOSE-OUT

Append or refresh this niche's block in `RESEARCH_MEMORY_INDEX.md` (schema
is in that file). **A run without index registration is INCOMPLETE — do not
report done until registered.** Then report: output file path + the index
entry written.

**AUTO-REFRESH cockpit (v1.3, stessa forza della regola indice):** after
index registration, update `00_SYSTEM_CONTROL\MASTER_DASHBOARD.md` (sections:
ultimi 3 run con verdetto · stato · KPI if moved) and the relevant lines of
`00_SYSTEM_CONTROL\NEXT_ACTIONS.md`; create/update task notes in
`00_SYSTEM_CONTROL\TASKS\` if the run produced new owner actions. **A run
without cockpit refresh is INCOMPLETE.**
