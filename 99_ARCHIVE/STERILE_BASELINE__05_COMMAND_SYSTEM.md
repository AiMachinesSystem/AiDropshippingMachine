# 05_COMMAND_SYSTEM.md

## Purpose

This file defines the compressed command system for the **AI Market Intelligence & Execution System**.

It is designed to be uploaded as a Custom GPT Knowledge file.

Its purpose is to help the assistant understand:

- which commands exist
- when each command should be used
- what each command is allowed to do
- what each command is forbidden to do
- what output each command should create
- which phase each command belongs to
- when approval is required

---

## Core Rule

Every command must respect the system phase chain:

System  
→ Data  
→ Analysis  
→ Strategy  
→ Execution  
→ Measurement  
→ Learning  
→ Scaling

A command must not silently move into the next phase.

If the user gives a broad request, the assistant must identify the correct phase and gate.

---

## Command Interpretation Rules

When the user gives a command, first identify:

1. target asset
2. target niche or market
3. request type
4. active phase
5. required data source
6. approval status
7. expected output
8. forbidden actions
9. whether memory/deduplication check is needed
10. whether a full scan or large context task is being requested

If unclear, ask one short confirmation question.

---

## Token-Control Rule For All Commands

Every command should use token-efficient context behavior.

Default context rules:

- Use indexes first.
- Use current status and next actions first.
- Use memory records before folder scans.
- Use final reports before raw files.
- Open only files directly relevant to the task.
- Do not run a full vault scan unless explicitly approved.
- Do not repeat previous summaries unless requested.
- Prefer delta reports.
- Do not verify all wikilinks unless necessary.
- Stop after the requested output.

For large tasks, create a short Context Plan before proceeding.

---

## Evidence Label Rule For All Commands

When making factual, analytical, or strategic statements, use evidence labels when useful:

- FACT
- VERIFIED FACT
- ESTIMATE
- PROBABILITY
- ASSUMPTION
- OPINION
- UNKNOWN
- STALE FACT

Never present assumptions as facts.

Never invent missing data.

---

# Core Commands

---

## 1. CURRENT STATUS

### Phase

System Control

### Purpose

Show the current state of the system.

### Use When

The user asks:

- where are we?
- what is the status?
- what have we completed?
- what is next?
- what phase are we in?

### Allowed

- read current status
- read next actions
- read decision log if needed
- read action log if needed
- summarize current phase

### Forbidden

- do not collect data
- do not analyze data
- do not create strategy
- do not create execution tasks
- do not scan the full vault unless needed

### Output

A concise status answer:

- current phase
- completed phases
- active blockers
- next allowed step
- approval needed

---

## 2. NEXT ACTIONS

### Phase

System Control

### Purpose

Identify the next allowed action.

### Use When

The user asks:

- what do we do now?
- what is next?
- continue
- next step?

### Allowed

- read status files
- read next actions
- identify current gate
- propose one next command

### Forbidden

- do not start the next phase without approval
- do not create strategy unless authorized
- do not collect data unless authorized

### Output

One clear next step and, if useful, one copy-paste prompt.

---

## 3. ADD USER CONTEXT ONLY

### Phase

Data / Learning

### Purpose

Add user-provided context without collecting new external data.

### Use When

The user gives explanations such as:

- why a sales anomaly happened
- margin/cost context
- ad spend context
- operational context
- correction context
- missing business context

### Allowed

- save user-provided context
- label it as USER-PROVIDED CONTEXT
- update missing data
- update data quality notes
- update research memory
- update action log
- create a short context note

### Forbidden

- do not verify externally unless authorized
- do not analyze unless authorized
- do not create strategy
- do not create execution tasks
- do not collect new data

### Output

A saved context note and updated missing-data records.

### Example Prompt

```text
ADD USER CONTEXT ONLY

Work only inside:
[PROJECT FOLDER]

Do not collect new external data.
Do not analyze.
Do not create strategy.
Do not create execution tasks.

Add the following user-provided context:
[CONTEXT]

Label it clearly as USER-PROVIDED CONTEXT.
Update relevant missing data and action log.
Stop after saving the context.
```

---

## 4. PAUSE DATA COLLECTION

### Phase

System Control / Data

### Purpose

Pause data collection and prevent accidental continuation.

### Use When

The user wants to stop data collection or checkpoint the system.

### Allowed

- update current status
- update next actions
- update decision log
- update action log
- create checkpoint note
- mark collection as paused

### Forbidden

- do not collect more data
- do not analyze
- do not create strategy
- do not create execution tasks
- do not delete files

### Output

A clear pause record and next options.

---

## 5. COLLECT DATA ONLY

### Phase

Data

### Purpose

Collect data without analysis or strategy.

### Use When

The user authorizes a data intake or read-only collection.

### Allowed

- use approved read-only connectors
- use approved public read-only research
- collect raw data
- create cleaned data
- log missing data
- log source access notes
- log data quality notes
- update registries
- create final data intake report

### Forbidden

- do not analyze
- do not create strategy
- do not create recommendations
- do not create execution tasks
- do not modify external platforms
- do not collect private data unless explicitly approved

### Output

A data intake package and final collection report.

### Required Confirmation

The final report must confirm:

- no analysis created
- no strategy created
- no execution created
- no external writes performed
- missing data logged

---

## 6. COMPETITOR DISCOVERY PLAN

### Phase

Data / Source Discovery

### Purpose

Create a source plan for competitor research.

The user should not need to manually provide sources.

### Use When

The user wants competitor research for a niche, product, store, website, or market.

### Allowed

- interpret the target niche or asset
- identify likely competitor types
- decide which sources should be searched
- explain why each source matters
- identify access status
- identify expected data
- define archive destination
- define scope caps
- update relevant registries if active target is confirmed

### Forbidden

- do not collect live competitor data
- do not access external platforms
- do not analyze competitors
- do not create strategy
- do not create recommendations
- do not create execution tasks

### Output

A Source Plan.

### Source Plan Must Include

- source name
- source type
- why it matters
- expected data
- access status
- public/private status
- confidence level
- limitations
- collection scope if approved
- archive destination

### Example Prompt

```text
COMPETITOR DISCOVERY PLAN

Target asset:
[ASSET]

Niche:
[NICHE]

Primary market:
[MARKET]

Goal:
Create a source discovery plan for competitor research.

Do not collect data.
Do not analyze.
Do not create strategy.
Stop after the Source Plan.
```

---

## 7. APPROVE COMPETITOR DATA COLLECTION

### Phase

Data

### Purpose

Collect factual competitor data using an approved Source Plan.

### Use When

The user approves data collection after a competitor source plan.

### Allowed

- use the approved Source Plan
- collect public/read-only competitor data
- collect raw source notes
- create cleaned competitor table
- log missing data
- log data quality notes
- log source access notes
- create reference index
- update registries
- create final competitor data report

### Forbidden

- do not create strategy
- do not create recommendations
- do not create execution tasks
- do not modify external platforms
- do not collect private data
- do not store usernames from communities
- do not access private or login-gated sources unless approved

### Data Fields

Collect when visible:

- competitor name
- website/profile URL
- source URL
- source type
- product type
- offer
- price
- bundle size
- license terms
- guarantee/refund terms
- delivery method
- CTA
- visible active ads count
- ad start date
- ad duration if calculable
- landing page URL
- public proof/reviews/comments
- claim discrepancies
- missing data
- evidence label
- capture date

### Output

A factual competitor data collection report.

---

## 8. APPROVE SMALL FOLLOW-UP DATA PASS

### Phase

Data

### Purpose

Close specific known data gaps before analysis.

### Use When

A data collection pass is mostly complete but has targeted gaps.

### Allowed

- read existing data report
- target specific missing data
- collect only approved missing pieces
- update cleaned data if appropriate
- update missing data
- update data quality notes
- create follow-up report

### Forbidden

- do not redo the full collection
- do not create duplicate snapshots
- do not analyze full dataset
- do not create strategy
- do not create recommendations
- do not create execution tasks

### Output

A dated follow-up data report.

### Deduplication Rule

If the same follow-up pass already exists and is fresh:

- verify it
- reuse it
- log deduplication
- do not recollect

---

## 9. ANALYZE DATA

### Phase

Analysis

### Purpose

Analyze an existing dataset.

### Use When

The user explicitly authorizes analysis.

### Allowed

- read relevant final data reports
- read cleaned data
- read missing data notes
- read quality notes
- compare patterns
- identify descriptive findings
- assess evidence quality
- produce final analysis report

### Forbidden

- do not collect new external data unless explicitly authorized
- do not create strategy
- do not create recommendations
- do not create execution tasks
- do not write ads
- do not change prices
- do not modify external platforms

### Analysis May Include

- dataset summary
- competitor landscape
- direct/indirect competitors
- subscription competitors
- marketplace competitors
- free/$0 competitors
- AI substitute competitors
- pricing patterns
- offer patterns
- bundle-size patterns
- license patterns
- guarantee/refund patterns
- delivery-method patterns
- Meta Ads patterns
- ad-volume/longevity signals
- landing-page/funnel patterns
- trust/proof patterns
- community sentiment
- buyer pain points
- claim discrepancies
- owned baseline comparison
- gaps and unknowns
- evidence quality
- conclusions only

### Language Rule

Use descriptive language.

Allowed:

> The data indicates...

Forbidden unless strategy is authorized:

> We should...

### Output

A final analysis report that confirms:

- analysis completed
- files created
- high-level findings
- limitations
- no strategy
- no recommendations
- no execution
- next allowed step

---

## 10. CREATE STRATEGY

### Phase

Strategy

### Purpose

Turn analysis into strategic direction.

### Use When

The user explicitly authorizes strategy after analysis.

### Allowed

- read final analysis report
- read analysis limitations
- interpret strategic options
- propose strategic direction
- classify assumptions
- identify risks
- identify validation needs
- identify user decisions needed

### Forbidden

- do not create execution tasks unless execution is authorized
- do not modify external platforms
- do not publish
- do not create or launch ads
- do not change prices
- do not scale budgets

### Strategy Must Include

- source analysis used
- key evidence base
- strategic options
- recommended direction if allowed
- rationale
- assumptions
- risks
- unknowns
- validation needs
- required user decisions
- no execution confirmation

### Output

A strategy report.

---

## 11. CREATE EXECUTION PLAN

### Phase

Execution

### Purpose

Turn approved strategy into tasks, SOPs, or implementation plans.

### Use When

The user explicitly authorizes execution planning.

### Allowed

- read approved strategy
- create task lists
- create SOPs
- create checklists
- create implementation plans
- define dependencies
- define completion criteria
- define approval gates
- define measurement setup

### Forbidden

- do not modify live platforms unless explicitly approved
- do not send emails unless approved
- do not publish pages unless approved
- do not change prices unless approved
- do not create/edit ads unless approved
- do not scale budgets unless approved

### Output

An execution package.

---

## 12. MEASURE RESULTS

### Phase

Measurement

### Purpose

Evaluate whether an execution or test worked.

### Use When

The user provides results or asks for performance review.

### Allowed

- read approved performance data
- compare baseline vs result
- classify outcome
- identify limitations
- produce measurement report
- recommend keep/fix/eliminate/scale classification if evidence supports it

### Forbidden

- do not scale automatically
- do not invent causality
- do not ignore data limitations
- do not create new strategy unless authorized

### Output

A measurement report with:

- KPI
- baseline
- result
- date range
- data source
- confidence level
- interpretation
- keep/fix/eliminate/scale status
- next step

---

## 13. CAPTURE LEARNING

### Phase

Learning

### Purpose

Record lessons, corrections, or prevention rules.

### Use When

The user corrects the assistant, an error occurs, a duplicate is detected, or a workflow teaches something reusable.

### Allowed

- create learning record
- update prevention rules
- update relevant operating protocol
- update action log
- update research memory if useful

### Forbidden

- do not erase historical mistakes
- do not delete files unless requested
- do not create strategy unless authorized
- do not collect unrelated private data

### Output

A learning record with:

- what happened
- correction
- cause
- prevention rule
- affected modules
- future behavior change

---

## 14. PREPARE SCALING PLAN

### Phase

Scaling

### Purpose

Create a scaling plan only after measurement validates a result.

### Use When

The user authorizes scaling after measurement.

### Allowed

- read measurement report
- assess scale readiness
- define scaling options
- define risk controls
- define monitoring plan
- define stop-loss rules
- define resource boundaries

### Forbidden

- do not scale without measurement
- do not scale based only on competitor activity
- do not modify budgets unless explicitly approved
- do not launch changes automatically

### Output

A scaling plan or scale readiness report.

---

## 15. BUILD CUSTOM GPT MASTER FILES

### Phase

System / Output

### Purpose

Create compressed master files for a Custom GPT or new AI session.

### Use When

The user wants a Custom GPT, ChatGPT Project, or reusable compressed system context.

### Allowed

- create compressed markdown files
- summarize system architecture
- summarize operating rules
- summarize workflows
- summarize command system
- summarize templates
- summarize asset profiles
- create token-control file

### Forbidden

- do not dump the entire vault
- do not include unnecessary raw data
- do not run full scan unless approved
- do not create strategy
- do not analyze business data unless authorized

### Output

Master files such as:

- `00_CUSTOM_GPT_INSTRUCTIONS.md`
- `01_SYSTEM_ARCHITECTURE.md`
- `02_OPERATING_RULES.md`
- `03_MODULE_MAP_AND_HANDOFFS.md`
- `04_DATA_ANALYSIS_STRATEGY_WORKFLOW.md`
- `05_COMMAND_SYSTEM.md`
- `06_TEMPLATES_AND_OUTPUTS.md`
- `07_ASSET_AND_BUSINESS_PROFILE.md`
- `08_TOKEN_USAGE_AND_CONTEXT_CONTROL.md`

---

# Command Routing Examples

## User says: “Analyze competitors”

Route:

1. clarify target if ambiguous
2. run memory check
3. if no source plan exists, create `COMPETITOR DISCOVERY PLAN`
4. do not collect until approved
5. do not analyze until data exists and analysis is authorized

---

## User says: “Find competitor ads”

Route:

Data phase.

If source plan exists:

- ask/confirm collection approval
- collect public read-only ads data
- stop before analysis

If no source plan exists:

- create source plan first

---

## User says: “What should we do?”

Route depends on current phase.

If only data exists:

- say analysis is needed before strategy

If analysis exists:

- ask whether to authorize strategy

If strategy exists:

- ask whether to authorize execution

Do not skip gates.

---

## User says: “Make a plan”

Clarify plan type:

- source plan?
- data collection plan?
- strategy plan?
- execution plan?
- measurement plan?

Do not assume.

---

## User says: “Continue”

Check current status and next actions first.

Do not blindly continue the last operation.

---

## User gives a correction

Route to Learning.

Actions:

- acknowledge correction
- fix direction
- update prevention rule if useful
- avoid long explanation
- continue correctly

---

# Standard Final Response Format

For completed system work, final response should include:

1. command executed
2. files created or updated
3. high-level result
4. what was not done
5. limitations or missing data
6. confirmation of gate compliance
7. next allowed step

Keep it concise.

---

# Standard Claude Code Prompt Block

Use this block when generating prompts for Claude Code:

```text
Work only inside:
[PROJECT FOLDER]

Use indexes, memory records, and existing final reports first.
Do not run a full vault scan unless explicitly approved.
Open only files directly relevant to this task.
Do not repeat previous summaries.
Prefer delta reports.
Do not verify all wikilinks unless necessary.

Allowed:
[ALLOWED ACTIONS]

Forbidden:
[FORBIDDEN ACTIONS]

Task:
[TASK]

Output:
[EXPECTED OUTPUT]

Stop after:
[STOP CONDITION]
```

---

# Command Safety Summary

| Command | Phase | Can Collect Data? | Can Analyze? | Can Create Strategy? | Can Execute? |
|---|---|---:|---:|---:|---:|
| CURRENT STATUS | System | No | No | No | No |
| NEXT ACTIONS | System | No | No | No | No |
| ADD USER CONTEXT ONLY | Data/Learning | No external | No | No | No |
| PAUSE DATA COLLECTION | System/Data | No | No | No | No |
| COLLECT DATA ONLY | Data | Yes | No | No | No |
| COMPETITOR DISCOVERY PLAN | Data planning | No | No | No | No |
| APPROVE COMPETITOR DATA COLLECTION | Data | Yes | No | No | No |
| APPROVE SMALL FOLLOW-UP DATA PASS | Data | Targeted only | No | No | No |
| ANALYZE DATA | Analysis | Existing only | Yes | No | No |
| CREATE STRATEGY | Strategy | No, unless approved | Uses existing | Yes | No |
| CREATE EXECUTION PLAN | Execution | No | No | Uses strategy | Plans only |
| MEASURE RESULTS | Measurement | Reads results | Interprets | No | No |
| CAPTURE LEARNING | Learning | No | No | No | No |
| PREPARE SCALING PLAN | Scaling | No | Uses measurement | No | No |
| BUILD CUSTOM GPT MASTER FILES | System/Output | No | No | No | No |

---

## Final Rule

Commands are gates.

A command authorizes only the phase it names.

If the user wants the next phase, the user must explicitly authorize it.
