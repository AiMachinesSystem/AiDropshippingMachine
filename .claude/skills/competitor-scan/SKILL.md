---
name: competitor-scan
description: Deep competitor teardown (single brand or batch) — positioning, offer structure, funnel, creative strategy, trust/compliance audit, 1–5 strength scores with a pre-declared rubric, and threat level to a new entrant. Use this skill whenever the owner asks to analyze, study, tear down, or compare competitors or a specific brand — triggers include "analizza questo competitor", "studia questi competitor", "chi è X e cosa fa", "competitor scan", "teardown di", "confronta questi brand", "come vende X", "che offerta ha X", or a competitor URL with a request like "guarda cosa fanno". ALSO use it in QUERY MODE to answer questions about competitors already studied ("chi è il leader", "quanti competitor attivi ci sono", "qual è il più debole", "chi dovremmo copiare/evitare") from RESEARCH_MEMORY_INDEX and existing reports, without re-running anything.
---

# Competitor Scan

Competitor intelligence inside a known or new niche. Read-only research.
**v1.1 (2026-06-13)** — adds: QUERY MODE discipline (canonical numbers,
answer template, freshness), universe separation in census deltas.
**v1.2 (2026-06-13)** — adopts ads-library-scan v1.2 evidence-cache +
KNOWN_WALLS rules (cache load-bearing fetches in `90_CACHE\fetches\`; check
the walls table in `00_SYSTEM_CONTROL\VAULT_CONVENTIONS.md` before retrying
blocked surfaces).
**v1.3 (cockpit auto-refresh)** — AUTO-REFRESH cockpit obbligatorio
al close-out (MASTER_DASHBOARD + NEXT_ACTIONS), stessa forza della regola
indice.

## MODE SELECTION (first decision, always)

- **QUERY MODE** — question answerable from past runs: open
  `RESEARCH_MEMORY_INDEX.md` (expected at `00_SYSTEM_CONTROL/`), answer from
  the niche block + linked reports, cite file + run date, offer a refresh if
  data is >30 days old. Never re-run for a lookup.
  **Discipline (v1.1):** counts/leaders come ONLY from the block's most
  recent registered run (`last_run` + headline); older lines in the block are
  history, never quoted as current. Answer template:
  `<answer> — fonte: <report file>, run <date>` (+ refresh offer only if
  >30 days). If the block was updated within ~7 days, answer from the index
  directly; open reports only for per-competitor detail.
- **RUN MODE** — new teardown requested → protocol below.

## STEP 0 — NICHE CONTEXT RESOLUTION (mandatory)

Classify the competitor's niche from its anchor product (label, buyer, price
band, offer model). Then check `RESEARCH_MEMORY_INDEX.md`:

- a niche run EXISTS → load it as the starting dataset; cite its findings by
  number instead of re-collecting them.
- NO niche run exists → say so explicitly, run a 10-minute
  mini-classification, RECOMMEND a full `niche-intelligence-run`, and
  proceed with the scan while marking all niche-level claims LOW-CONFIDENCE.
- NEVER silently borrow another niche's or another project's context,
  claim gates, or assumptions. If the owner's request mentions a different
  project, state that transferability is out of scope unless asked.

## DEPTH TIERING (declare before extracting)

- **FULL teardown** (site + ads, all sections A–F): the anchor competitor +
  any competitor where both data sources are reachable.
- **LIGHT card** (A + visible price + main hooks + trust flags only):
  thin-data competitors (dormant, few ads, walls).
- Do not pad LIGHT cards: **[UNKNOWN] beats filler.**

## EXTRACTION STRUCTURE (per competitor)

- **A Positioning** — what they sell, buyer, beginner vs advanced, sub-niche,
  model (bundle / course / library / membership / single plans / free-funnel).
- **B Offer** — main product, price, discount structure + anchor basis
  (declared or not), bonus stack, guarantee/refund if visible, upsells,
  delivery format.
- **C Funnel** — ad → landing → product → checkout; advertorial / quiz /
  lead magnet / email capture / affiliate bridge; multilingual funnels;
  page-follow or other warm-audience layers.
- **D Creative** — main hooks, pain points, dream outcomes,
  urgency/scarcity, proof mechanisms, visual patterns, long-form ads,
  duplicated-winner clusters (use `ads-library-scan` method).
- **E Trust & compliance** — real vs fabricated/staged proof, review
  quality, legal entity visibility, refund clarity, weak spots, claims that
  look risky / unsupported / fabricated.
- **F Scores** — see scoring discipline.

## SCORING DISCIPLINE (F)

Before scoring anything, declare a one-line 1↔5 rubric for EACH dimension:
offer strength · trust/credibility · ad sophistication · funnel
sophistication · localization · differentiation · threat level.
**Threat level = capacity to outspend/outrank a NEW entrant in the gap that
entrant would target** (not generic size). Every score cites evidence or is
[UNKNOWN — not scored]. End with an N×7 summary matrix.

## G — OPPORTUNITY GAPS · H — STRATEGIC ANSWERS

G: list what NO competitor owns (trust-proven aggregation, localized geos,
sub-niche authority, beginner pathway, real guarantee, verified proof,
premium curation, community/membership, creator-led authority — extend per
niche).
H: answer with evidence pointer (finding # or new source) + confidence tag
(HIGH/MEDIUM/LOW): 1 real leader · 2 most credible · 3 weakest-but-most-
aggressive · 4 model structurally · 5 explicitly avoid copying · 6 cleanest
entry angle · 7 sub-niche focus · 8 first hero offer · 9 safe vs risky
claims (substantiation standard: verifiable basis, EU/FTC consumer rules) ·
10 data still missing before GO/NO-GO (ranked).

## METHOD · EVIDENCE · SAFETY (binding, condensed)

Ad Library via `https://r.jina.ai/` prefix, retry ≤2, counts = lower
bounds, known walls → [UNKNOWN] + owner-manual list. Labels on every claim:
[OBSERVED — source + date] / [INFERRED — basis] / [UNKNOWN]. Read-only
public sources; zero spend/login/purchase/contact. Fabricated-proof tactics
are documented as weaknesses and anti-patterns, NEVER recommended. Never
modify other projects' files.

## OUTPUT

One file:
`10_OUTPUTS/COMPETITOR_ANALYSIS/YYYY-MM-DD_<NICHE-SLUG>_COMPETITOR_ANALYSIS_vN.md`
Standard structure: Verdict · Confidence · Evidence basis · Dominant
pattern · Recommended move · Why · Rejected alternatives · Owner role ·
Measurement plan · Blockers/open items · Files updated.

## MANDATORY CLOSE-OUT

Update the niche block in `RESEARCH_MEMORY_INDEX.md`: leader, credibility
leader, threat ranking, census deltas, report path. **No registration = run
INCOMPLETE.** Report file path + index entry written.
**AUTO-REFRESH cockpit (v1.3, stessa forza della regola indice):** after
index registration, update `00_SYSTEM_CONTROL\MASTER_DASHBOARD.md` (ultimi
run · stato · KPI) + `00_SYSTEM_CONTROL\NEXT_ACTIONS.md`; new owner actions
become task notes in `00_SYSTEM_CONTROL\TASKS\`. **No cockpit refresh = run
INCOMPLETE.**
**Universe separation (v1.1):** census deltas keep structurally different
markets (geo/price/funnel universes) as separate numbers — core market
headline first, other universes named alongside, never summed silently.
Library-ID collisions in ads data follow the `ads-library-scan` v1.1
collision protocol (count once, flag, report total).
