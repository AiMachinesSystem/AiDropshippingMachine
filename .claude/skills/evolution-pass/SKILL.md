---
name: evolution-pass
description: Heavy-reasoning reference for complex/strategic (L2) and machine-improvement (L3) tasks. Invoke when OPERATING_CORE classifies a task as L2/L3 — i.e. it touches architecture, workflows, automation, data, business strategy, external surfaces, connectors, repeated future execution, or the machine itself. Also invoke on explicit requests to improve/audit/restructure the machine, compare strategies, or validate a business move before committing. Provides the capability-discovery, strategy + value gate, simulation, measurement, learning, and pruning protocol. Do NOT use for L0 trivial tasks, L1 normal internal work, or query-mode lookups.
---

<evolution_pass version="3.1">

<when>
Load this only when OPERATING_CORE classified the task L2/L3, or the owner asked to improve
the machine. For L0 / L1 / query-mode, ignore this entirely.
</when>

<loop>
INTENT → DISCOVER capabilities → SHORTLIST → STRATEGY options → DRY-RUN on a real surface
(if possible) → SELECT on evidence → EXECUTE only what is allowed → MEASURE → LEARN (only
if real) → PRUNE / IMPROVE proposal (if warranted). Run only the steps the task needs.
</loop>

<discovery>
Recover the real capability set before choosing a strategy. Discover the machine's actual
skeleton, registries, skills, validators, templates, prior reports/lessons, and incidents
from what exists — do not assume folder paths or filenames. If the owner gave a list, start
there and verify it against reality before relying on it.
</discovery>

<capability_study>
For each shortlisted capability, capture only what changes the decision:
  name — why it fits this task — read-only or GO-gated — PRIMARY / SUPPORT / NOISE
Drop a capability explicitly with a one-line reason. Do not fill cost/risk/combination
fields unless you actually inspected it. Aim for the smallest effective set.
</capability_study>

<strategy>
Generate at most 3 candidate strategies; never default to the first. Choose by one
heuristic: the smallest safe strategy that produces the highest useful result. Score 1–5
ONLY as a tie-break when two strategies are genuinely close, and only on the deciding
dimensions (objective fit, safety/reversibility, cost).
</strategy>

<value_gate>
Applies when the task is business- or strategy-shaped. Each candidate strategy must state:
  1. value hypothesis — what revenue, saving, or owner-leverage it is meant to produce;
  2. economics sanity check — does the price/value plausibly clear the cost to acquire and
     serve, with margin headroom? Mark VIABLE / THIN / UNKNOWN with the basis;
  3. falsifier — what observation would prove the hypothesis wrong.
Reject any strategy with no credible path to value, or one that is THIN with no plan to
widen the margin, regardless of its other scores. "It works" is not sufficient — it must
pay. If the machine's mother objective is commercial, read "value" as profit; otherwise
read it as the machine's defined success measure and apply the same three-part test.
</value_gate>

<simulation>
Before any risky, structural, or external action, prefer a real dry-run over a
hypothetical. Use whatever genuine read / preview / sandbox surfaces the machine actually
has (read-only queries, previews, diffs, a test or validation run) — discover them, do not
assume. For GO-gated actions you cannot run yourself, do NOT narrate a long simulation:
write a 3-line GO request — what you will do, the risk, the rollback. Simulate only when it
produces evidence, reduces risk, or prevents a likely mistake.
</simulation>

<measurement>
Measure against a real signal available this session. If the machine has a verification /
regression / validation suite, run it for any task touching governance, registries,
validators, or structural files, and attach its PASS evidence before COMPLETE; on FAIL,
route to the machine's incident/rule mechanism and do not declare done. Where no live
signal exists, write "measurement: outcome-pending, deferred to owner action" rather than
self-grading. If the machine has pre-ship checks (constitution/gate check, output-contract
audit), run them before COMPLETE on any L2+ shipping or claiming output and cite their
verdicts.
</measurement>

<learning>
Capture a lesson only when you can name (a) a specific repeated or high-risk trigger and
(b) the exact rule/routing change it produces. If you cannot name both, write nothing. A
real lesson is one sentence plus the change it drives. Route durable lessons through the
machine's own rule/incident mechanism if one exists, so a lesson becomes an enforceable
rule rather than loose notes; otherwise propose where it should live. Never create
structural folders blindly.
</learning>

<pruning>
On L2/L3, judge whether existing artifacts should change. For REGISTERED / canonical
objects, use only the machine's canonical change verbs (e.g. ADD / DEPRECATE / REMOVE /
SUPERSEDE / ARCHIVE) through its registry — an "improvement" to a canonical rule is a new
superseding object, never an in-place edit. Use informal KEEP / IMPROVE / MERGE / SIMPLIFY
language only for non-canonical drafts and reports. Default: mark noisy items as
DEPRECATE_CANDIDATE and propose; never delete or archive automatically. Destructive pruning
requires OWNER GO. Pruning recommendations are proposals, not actions.
</pruning>

<utility_gate>
Before creating any new rule / skill / report / template / folder / workflow, confirm: it
solves a real, recurring or high-risk problem; no existing artifact can be improved
instead; it is reusable; it reduces future work; it earns its complexity. If the case is
weak, record it as IMPROVEMENT_CANDIDATE, not a permanent artifact. Produce only artifacts
that have a named consumer.
</utility_gate>

<l3_outputs>
For a full machine-improvement pass, produce only the subset that passes the utility gate
and has a reader — never a fixed file set by default: e.g. capability inventory, routing
map, strategy comparison, evolution plan, pruning review. Write each to the machine's
designated outputs location; if none exists, propose one before creating folders. The
minimum valid L3 output is a single decision note.
</l3_outputs>

<scorecard>
Use a short scorecard only when the run produced real learning, risk, or reusable output.
Score 1–5: output quality, safety, evidence strength, reusability, owner leverage, and
objective/strategic value. Then classify: USEFUL_OPERATIONAL_LEARNING /
TASK_COMPLETE_NO_SYSTEM_UPDATE_NEEDED / TOO_MUCH_NOISE. If the run created more complexity
than value, recommend simplification before adding anything.
</scorecard>

</evolution_pass>
