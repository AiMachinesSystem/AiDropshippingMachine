# 03_MODULE_MAP_AND_HANDOFFS.md

## Purpose

This file explains the module map and handoff logic for the **AI Market Intelligence & Execution System**.

It is designed to be uploaded as a Custom GPT Knowledge file.

Its purpose is to help the assistant understand:

- what each module/folder is for
- when each module should be used
- how work moves from one phase to the next
- what must happen before a phase handoff is allowed
- what each phase is forbidden to do
- how to keep the system universal, structured, and token-efficient

---

## Core Module Chain

The system follows this Level 2 chain:

System  
→ Data  
→ Analysis  
→ Strategy  
→ Execution  
→ Measurement  
→ Learning  
→ Scaling

The assistant must not skip phases.

Each phase has a different job.

---

## Folder Map

The main project folders are:

- `00_SYSTEM_CONTROL`
- `01_SYSTEM`
- `02_DATA`
- `03_ANALYSIS`
- `04_STRATEGY`
- `05_EXECUTION`
- `06_MEASUREMENT`
- `07_LEARNING`
- `08_SCALING`
- `09_TEMPLATES`
- `10_OUTPUTS`
- `99_ARCHIVE`

Each folder is a module.

The folder structure is part of the operating system, not just storage.

---

## 00_SYSTEM_CONTROL

### Purpose

Controls the current system state.

This is the first module to check before major work.

### Contains

- current status
- next actions
- decision log
- action log
- module index
- project index
- checkpoints
- readiness reports
- pause states
- approval status

### Use When

Use this module when the assistant needs to know:

- what phase the system is in
- what has already happened
- what is authorized
- what is paused
- what the next allowed step is
- what decisions have already been made
- whether work should continue, pause, or hand off

### Forbidden

Do not use this module to:

- store raw research data
- create analysis
- create strategy
- create execution tasks
- store final user-facing reports unless they are control reports

### Handoff Role

This module controls whether the system can move from one phase to the next.

Example:

If `CURRENT_STATUS` says data collection is paused, do not collect more data unless the user explicitly lifts the pause for a defined task.

---

## 01_SYSTEM

### Purpose

Defines how the system behaves.

This is the rules module.

### Contains

- command interpretation rules
- autonomy rules
- approval boundaries
- no unsupported assumptions rules
- evidence label rules
- language protocol
- index maintenance rules
- source discovery protocol
- deduplication behavior
- edit vs overwrite behavior
- context retrieval behavior

### Use When

Use this module when the assistant needs to know:

- how to interpret a user command
- whether approval is needed
- whether a task is data, analysis, strategy, execution, measurement, learning, or scaling
- how to classify evidence
- how to prevent unsupported assumptions
- how to avoid duplicate work
- how to manage context and token usage

### Forbidden

Do not use this module to:

- store raw competitor data
- store final analysis reports
- store execution plans
- store measurement results
- store temporary research notes

### Handoff Role

This module defines the gate rules for every handoff.

Example:

Analysis cannot hand off to strategy unless the user explicitly authorizes strategy.

---

## 02_DATA

### Purpose

Collects, stores, organizes, and preserves data.

Data is the evidence layer.

### Contains

- source discovery plans
- raw data
- cleaned data
- missing data notes
- data quality notes
- source access notes
- data source registry
- research memory index
- niche registry
- portfolio registry
- owned baseline data
- competitor data collection reports
- read-only intake records

### Use When

Use this module for:

- collecting data
- organizing facts
- archiving raw source notes
- creating cleaned tables
- logging missing data
- logging data quality limitations
- tracking source access
- registering a new niche, asset, competitor set, or data request

### Forbidden

Do not use this module to:

- create strategy
- create recommendations
- create execution tasks
- claim performance without evidence
- infer what should be done
- skip into analysis without authorization

### Handoff Role

Data may hand off to Analysis only when:

1. relevant data exists
2. raw and cleaned data are separated
3. missing data is logged
4. source quality is documented
5. the user authorizes analysis

### Data Handoff Output

Before handoff to Analysis, Data should produce:

- data summary
- source list
- cleaned tables
- missing data list
- data quality notes
- source access notes
- final data collection report

---

## 03_ANALYSIS

### Purpose

Turns collected data into structured understanding.

Analysis explains what the data indicates.

### Contains

- competitor landscape analysis
- pricing analysis
- offer analysis
- ad pattern analysis
- funnel analysis
- trust/proof analysis
- community sentiment analysis
- owned baseline comparison
- limitations and unknowns
- evidence quality assessment
- final analysis reports

### Use When

Use this module when the user explicitly authorizes analysis.

Analysis may answer:

- what patterns exist?
- how do competitors cluster?
- what pricing structures are visible?
- what offers are repeated?
- what ad patterns are visible?
- what funnel structures are visible?
- what trust signals are used?
- what customer pain points appear?
- what claims are inconsistent?
- what is unknown?
- what does the data indicate?

### Forbidden

During analysis, do not create:

- strategy
- recommendations
- action plans
- tasks
- ads
- copy
- product changes
- price changes
- funnel changes
- execution plans

### Handoff Role

Analysis may hand off to Strategy only when:

1. analysis exists
2. limitations are documented
3. evidence quality is clear
4. the user explicitly authorizes strategy

### Analysis Handoff Output

Before handoff to Strategy, Analysis should produce:

- key findings
- evidence labels
- known limitations
- risks
- opportunities described as observations, not recommendations
- unknowns
- clear statement that strategy is not yet authorized

---

## 04_STRATEGY

### Purpose

Turns analysis into strategic direction.

Strategy decides what direction the user may choose.

### Contains

- strategic positioning options
- offer strategy
- pricing strategy
- funnel strategy
- creative direction
- product direction
- channel direction
- risk-adjusted priorities
- strategic decision records

### Use When

Use this module only when the user explicitly authorizes strategy.

Strategy may answer:

- what direction should the business consider?
- which opportunity is most attractive?
- what positioning could be stronger?
- what offer model could be tested?
- what pricing direction fits the evidence?
- what risks need to be managed?
- what should be prioritized?

### Forbidden

Strategy must not:

- create execution tasks unless authorized
- modify platforms
- launch campaigns
- create final ads for launch
- publish changes
- skip measurement requirements
- present assumptions as facts

### Handoff Role

Strategy may hand off to Execution only when:

1. strategy is approved by the user
2. required decisions are clear
3. risks and assumptions are documented
4. the user explicitly authorizes execution planning

### Strategy Handoff Output

Before handoff to Execution, Strategy should produce:

- strategic direction
- rationale
- assumptions
- risks
- required validation
- priority order
- user decisions needed
- execution readiness status

---

## 05_EXECUTION

### Purpose

Turns approved strategy into concrete implementation plans.

Execution makes the work actionable.

### Contains

- task lists
- SOPs
- checklists
- campaign build plans
- landing page update plans
- content production plans
- creative production plans
- workflow instructions
- implementation packages

### Use When

Use this module only when execution is explicitly authorized.

Execution may answer:

- what needs to be done?
- in what order?
- by whom?
- with what inputs?
- what approval is needed?
- what is the completion definition?
- what dependencies exist?

### Forbidden

Execution must not:

- modify live external platforms unless explicitly approved
- send emails unless explicitly approved
- publish changes unless explicitly approved
- change prices unless explicitly approved
- create or modify ads unless explicitly approved
- scale budgets unless explicitly approved

### Handoff Role

Execution may hand off to Measurement only when:

1. an execution package exists
2. implementation or test conditions are defined
3. KPIs are defined
4. the user authorizes measurement or a result review

### Execution Handoff Output

Before handoff to Measurement, Execution should produce:

- task list
- owner/status
- dependencies
- KPI targets
- expected outcome
- implementation date
- measurement window
- test conditions

---

## 06_MEASUREMENT

### Purpose

Measures whether execution worked.

Measurement validates or rejects outcomes.

### Contains

- KPI reports
- performance reviews
- before/after comparisons
- result validation
- keep/fix/eliminate/scale classifications
- measurement dashboards
- performance interpretation notes

### Use When

Use this module after execution or when the user asks for performance review.

Measurement may answer:

- what changed?
- did the test work?
- did KPIs improve?
- is the result reliable?
- should this be kept, fixed, eliminated, or considered for scaling?
- what remains unknown?

### Forbidden

Measurement must not:

- scale automatically
- create new strategy without authorization
- invent causality
- overclaim results
- ignore data quality limitations

### Handoff Role

Measurement may hand off to Learning and Scaling.

Learning can happen after any result.

Scaling requires validation.

### Measurement Handoff Output

Before handoff to Scaling, Measurement should produce:

- KPI result
- baseline
- comparison period
- confidence level
- limitations
- result classification
- validation status
- scale readiness

---

## 07_LEARNING

### Purpose

Captures system learning.

Learning improves future behavior.

### Contains

- user corrections
- lessons learned
- mistake records
- prevention rules
- system improvements
- prompt improvements
- reusable insights
- correction intake records
- learning maps

### Use When

Use this module when:

- the user corrects the system
- the assistant makes a wrong assumption
- duplicate work is detected
- a workflow succeeds
- a workflow fails
- measurement reveals a lesson
- a prevention rule is needed
- behavior should change in future sessions

### Forbidden

Learning must not:

- overwrite historical truth
- erase mistakes without audit trail
- turn lessons into strategy unless strategy is authorized
- collect unrelated private information

### Handoff Role

Learning feeds back into System.

Important user corrections should update:

- operating rules
- protocols
- prevention rules
- command behavior
- future prompt patterns

### Learning Handoff Output

Learning should produce:

- what happened
- correction
- cause
- prevention rule
- affected modules
- future behavior change

---

## 08_SCALING

### Purpose

Controls scaling decisions.

Scaling increases resources only after proof.

### Contains

- scale readiness reports
- scale decision rules
- risk controls
- scaling plans
- budget escalation logic
- replication plans
- validated growth paths

### Use When

Use this module only after:

1. data exists
2. analysis exists
3. strategy exists
4. execution occurred
5. measurement validated the result
6. user authorizes scaling

### Forbidden

Scaling must not:

- happen based only on analysis
- happen based only on competitor behavior
- happen based only on assumptions
- happen without measurement
- happen without user approval
- modify budgets or platforms without explicit approval

### Handoff Role

Scaling may feed back into Measurement and Learning.

Scaling should create stricter monitoring, not remove controls.

---

## 09_TEMPLATES

### Purpose

Stores reusable formats.

Templates keep outputs consistent.

### Contains

- source plan templates
- data intake templates
- competitor table templates
- analysis templates
- strategy templates
- execution templates
- measurement templates
- learning templates
- decision templates

### Use When

Use templates when creating repeatable outputs.

### Forbidden

Templates should not contain live raw data unless they are examples.

Do not confuse templates with completed reports.

---

## 10_OUTPUTS

### Purpose

Stores final outputs.

Outputs are clean, readable, and user-facing.

### Contains

- final data collection reports
- final analysis reports
- final strategy reports
- final execution packages
- final measurement reports
- Custom GPT master files
- summaries
- handoff documents

### Use When

Use this module when a phase creates a final report or user-facing deliverable.

### Forbidden

Do not store messy raw data here.

Raw data belongs in `02_DATA`.

Detailed analysis archives belong in `03_ANALYSIS`.

### Handoff Role

Outputs are usually the best context source for future tasks.

When saving tokens, read final output reports before raw files.

---

## 99_ARCHIVE

### Purpose

Stores inactive, historical, deprecated, accidental, or preserved materials.

### Contains

- inactive plans
- deprecated files
- accidental artifacts
- historical records
- archived versions
- paused work

### Use When

Use this module when something should be preserved but no longer active.

### Forbidden

Do not delete historical records unless explicitly requested.

### Handoff Role

Archived materials can still inform learning, but they should not be treated as active unless reactivated by the user.

---

## Standard Handoff Logic

The system should move through phases like this:

### System to Data

Allowed when:

- system rules exist
- command is understood
- asset/request type is identified
- data source or source discovery is needed
- user authorizes data work

Output:

- source plan or data collection scope

---

### Data to Analysis

Allowed when:

- data has been collected or organized
- raw and cleaned data are separated
- missing data is logged
- source access notes exist
- data quality is documented
- user authorizes analysis

Output:

- analysis report

---

### Analysis to Strategy

Allowed when:

- analysis is complete
- findings are evidence-labeled
- limitations are documented
- no recommendations were prematurely created
- user authorizes strategy

Output:

- strategy document or decision options

---

### Strategy to Execution

Allowed when:

- strategy is complete
- direction is approved
- user authorizes execution planning
- risks and dependencies are clear

Output:

- execution plan, SOP, or task package

---

### Execution to Measurement

Allowed when:

- execution or test plan exists
- KPIs are defined
- baseline or expected outcome exists
- user authorizes measurement or results review

Output:

- measurement report

---

### Measurement to Learning

Allowed when:

- results exist
- mistakes or wins are identified
- user corrections occur
- process improvements are needed

Output:

- learning record or prevention rule

---

### Measurement to Scaling

Allowed only when:

- measurement validates the result
- confidence level is acceptable
- risks are documented
- user authorizes scaling

Output:

- scale readiness report or scaling plan

---

## Handoff Stop Conditions

Each phase should stop after its own output.

Data stops after data report.  
Analysis stops after analysis report.  
Strategy stops after strategy report.  
Execution stops after execution package.  
Measurement stops after measurement report.  
Learning stops after learning record.  
Scaling stops after scaling plan.

Do not automatically continue to the next phase.

---

## Example: Competitor Research Handoff

### Step 1 — Source Discovery

Command:

`COMPETITOR DISCOVERY PLAN`

Output:

- source plan
- source priority
- expected data
- access limitations
- archive destination

Stops before collection.

---

### Step 2 — Data Collection

Command:

`APPROVE COMPETITOR DATA COLLECTION`

Output:

- raw source notes
- cleaned competitor table
- missing data
- data quality notes
- source access notes
- final collection report

Stops before analysis.

---

### Step 3 — Analysis

Command:

`ANALYZE DATA`

Output:

- competitor landscape analysis
- pricing and offer analysis
- ad pattern analysis
- funnel and trust analysis
- sentiment analysis
- owned baseline comparison
- limitations and unknowns
- final analysis report

Stops before strategy.

---

### Step 4 — Strategy

Command:

`CREATE STRATEGY`

Output:

- strategy options
- priority decisions
- risk-adjusted direction
- assumptions
- validation needs

Stops before execution.

---

## Example: Owned Store Data Handoff

### Data Intake

Collects:

- sales
- orders
- revenue
- products
- customers aggregate
- traffic
- discounts
- refunds
- channel performance
- owned baseline

Stops before analysis.

### Analysis

May examine:

- revenue patterns
- top products
- pricing
- conversion
- anomalies
- owned baseline vs market
- performance limitations

Stops before strategy.

### Strategy

May define:

- product direction
- offer direction
- funnel direction
- positioning direction

Stops before execution.

---

## Token-Efficient Handoff Rule

Every handoff should use final reports before raw files.

Preferred context order:

1. current status
2. next actions
3. project index
4. module index
5. relevant final report
6. relevant memory record
7. relevant cleaned data
8. raw data only if needed

Do not read all files by default.

---

## Current First Real Cycle

The first real cycle completed:

1. Shopify owned baseline data intake for Terror Prints
2. STL competitor source plan
3. STL competitor data collection
4. STL competitor follow-up data pass
5. STL competitor analysis

Current result:

- `02_DATA` completed for the first STL cycle
- `03_ANALYSIS` completed for the first STL cycle
- `04_STRATEGY` not yet authorized
- `05_EXECUTION` not yet authorized
- `06_MEASUREMENT` not yet active
- `08_SCALING` not yet active

The assistant must verify current status before assuming this remains unchanged.

---

## Handoff Quality Checklist

Before moving to the next phase, check:

- Is the current phase complete?
- Is the output saved?
- Are limitations documented?
- Are evidence labels used?
- Is the next phase explicitly authorized?
- Are external writes avoided unless approved?
- Are indexes/logs updated?
- Is duplicate work avoided?
- Is token usage controlled?
- Is the system still asset-agnostic?

If any answer is no, do not hand off yet.

---

## Final Rule

A phase handoff is a controlled transition, not an automatic continuation.

The assistant must always know:

- what phase it is in
- what phase it is not allowed to enter yet
- what output is required
- what evidence exists
- what is missing
- what approval is required next
