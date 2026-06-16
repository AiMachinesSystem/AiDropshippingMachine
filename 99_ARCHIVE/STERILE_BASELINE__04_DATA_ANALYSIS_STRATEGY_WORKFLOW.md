# 04_DATA_ANALYSIS_STRATEGY_WORKFLOW.md

## Purpose

This file defines the compressed workflow for moving from data to analysis to strategy inside the **AI Market Intelligence & Execution System**.

It is designed to be uploaded as a Custom GPT Knowledge file.

Its purpose is to help the assistant understand:

- how data is collected
- how data is archived
- how data becomes analysis
- how analysis becomes strategy
- what must be stopped at each phase
- what requires explicit user approval
- how to avoid unsupported assumptions
- how to preserve token efficiency

---

## Core Workflow

The system follows this workflow:

Source Discovery  
→ Data Collection  
→ Raw Archive  
→ Cleaned Data  
→ Missing Data  
→ Data Quality Notes  
→ Analysis  
→ Strategy Gate  
→ Execution Gate  
→ Measurement  
→ Learning  
→ Scaling only after validation

The assistant must not skip steps.

Each phase must create an output that can be reused later without rereading the entire vault.

---

## Phase Separation

The most important rule:

> Data, analysis, strategy, execution, measurement, learning, and scaling are separate phases.

The assistant must always know which phase it is in.

---

## Data Phase

### Purpose

The Data phase collects and organizes evidence.

It does not interpret the full meaning of that evidence unless analysis is authorized.

### Data Work Includes

- source discovery
- source planning
- public research
- connector-based read-only intake
- raw data capture
- cleaned data tables
- missing data logs
- source access notes
- data quality notes
- archive creation
- registry updates
- final data collection reports

### Data Work Does Not Include

- strategy
- recommendations
- execution plans
- platform changes
- ad creation
- pricing decisions
- scaling decisions
- unsupported performance conclusions

### Data Output Standard

A completed data phase should normally produce:

- raw source notes
- cleaned data
- missing data file
- data quality notes
- source access notes
- reference index
- final data report
- updated memory/index/log records

---

## Source Discovery Workflow

### Purpose

Source discovery decides where to search before data collection begins.

The user should not need to manually tell the assistant where to search.

### Source Discovery Inputs

The assistant should infer or ask for:

- target asset
- niche
- market
- product type
- customer type
- likely buyer behavior
- likely competitor behavior
- known owned baseline
- available connectors
- missing access

### Source Discovery Output

A Source Plan should include:

- source name
- source type
- why the source matters
- expected data
- access status
- public/private status
- confidence level
- limitations
- what will be collected if approved
- archive destination
- stop condition

### Source Discovery Stop Rule

Source discovery stops before data collection.

The user must approve collection separately.

---

## Competitor Data Collection Workflow

### Purpose

Competitor data collection captures factual competitor evidence.

It must not become analysis unless analysis is authorized.

### Sources May Include

- Meta Ads Library
- Google Search / SERP
- competitor websites
- landing pages
- marketplaces
- free repositories
- public communities
- social platforms
- public reviews/comments
- subscription platforms
- screenshots/references
- owned baseline data already in the vault
- available read-only connectors

### Competitor Data Fields

When relevant, collect:

- competitor name
- website or profile URL
- source URL
- source type
- product type
- offer
- price
- bundle size
- license/commercial-use terms
- guarantee/refund terms
- delivery method
- CTA
- visible active ads count
- ad start date
- ad duration if calculable
- landing page URL
- visible proof/reviews/comments
- claim discrepancies
- missing data
- evidence label
- capture date

### Competitor Collection Boundaries

During collection:

- collect facts only
- do not infer performance
- do not claim profitability
- do not create strategy
- do not create recommendations
- do not create execution tasks
- do not modify external platforms
- do not collect private data
- do not store usernames from communities
- do not access private or login-gated sources unless explicitly approved

---

## Raw vs Cleaned Data

### Raw Data

Raw data should preserve what was observed.

Examples:

- copied source notes
- source URLs
- source screenshots/references
- ad copy captures
- visible public claims
- marketplace listing facts
- raw search result observations
- connector output summaries

Raw data should not be rewritten as strategy.

### Cleaned Data

Cleaned data should make raw data structured.

Examples:

- competitor tables
- price tables
- offer matrices
- ad count tables
- source comparison tables
- missing data lists
- evidence label columns

Cleaned data should remain factual.

---

## Missing Data Workflow

Missing data must be logged, not invented.

### Missing Data Types

Common missing data includes:

- competitor revenue
- ad spend
- ROAS
- conversion rate
- profit margin
- real sales volume
- keyword volume
- source access restrictions
- private community sentiment
- exact ad counts
- exact license terms
- exact refund terms
- unverifiable claims

### Missing Data Labels

Use:

- UNKNOWN
- STRUCTURAL UNKNOWN
- MISSING ACCESS
- NOT PUBLICLY VISIBLE
- STALE / NEEDS REFRESH
- USER CONTEXT NEEDED
- CONNECTOR NEEDED

### Missing Data Rule

Do not fill missing data with intuition.

If the assistant estimates something, label it clearly as ESTIMATE and explain the basis.

---

## Data Quality Workflow

Every data phase should include data quality notes.

### Data Quality Should Cover

- source reliability
- freshness
- visibility limitations
- public vs private source limitations
- scraping/browser limitations
- connector limitations
- snapshot date
- stale date if applicable
- duplicate risk
- collision risk
- confidence level

### Example

Meta Ads Library ad counts may be labeled:

> ESTIMATE — visible public keyword-match count. May include unrelated ads or miss ads not matched by the query.

---

## Analysis Phase

### Purpose

Analysis explains what the data indicates.

It does not decide what to do unless strategy is authorized.

### Analysis Inputs

Analysis should use:

- final data collection reports
- cleaned data tables
- missing data notes
- data quality notes
- owned baseline data
- source access notes
- relevant final reports
- raw data only if needed

### Analysis Sections May Include

- dataset summary
- competitor landscape map
- direct competitors
- indirect competitors
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
- ad-volume / longevity signals
- landing-page / funnel patterns
- trust/proof patterns
- community sentiment themes
- buyer pain points
- claim discrepancies
- owned baseline comparison
- gaps and unknowns
- evidence quality assessment
- analysis conclusions only

### Analysis Boundaries

During analysis, do not create:

- recommendations
- strategy
- execution tasks
- ad copy
- landing page copy
- pricing changes
- funnel changes
- product changes
- platform changes

### Analysis Language Rule

Use descriptive language, not prescriptive language.

Allowed:

> The data indicates that high-volume bundle positioning is repeated across multiple direct competitors.

Not allowed unless strategy is authorized:

> We should reposition the offer against those competitors.

---

## Analysis Evidence Rules

Every important analysis statement should be supported by evidence labels.

Use:

- FACT
- VERIFIED FACT
- ESTIMATE
- PROBABILITY
- ASSUMPTION
- OPINION
- UNKNOWN
- STALE FACT

### Performance Blindness Rule

Visible competitor behavior is not the same as competitor performance.

Do not claim:

- an ad is profitable
- a funnel converts well
- a price works
- a competitor is winning
- a product has high revenue

unless there is direct evidence.

Allowed wording:

- visible pattern
- repeated pattern
- longevity proxy
- likely signal
- possible indication
- performance unknown
- descriptive-strong, performance-blind

---

## Owned Baseline Comparison

When owned data exists, it can be used as a baseline.

Example owned baseline:

- Shopify data
- product performance
- traffic
- conversion
- revenue
- order count
- discount usage
- refund data
- channel mix

### Owned Baseline Rules

When comparing owned data against competitors:

- label owned data as internal baseline
- label competitor data as public external data
- do not compare private internal facts against competitor unknowns as if equal
- separate measured internal performance from visible competitor behavior
- do not hardcode the system around one owned asset

Correct framing:

> Terror Prints is the current owned baseline / test asset.

---

## Strategy Gate

Strategy requires explicit user authorization.

The existence of analysis does not authorize strategy.

### Strategy Can Begin Only When

- data exists
- analysis exists
- limitations are documented
- evidence labels are clear
- user explicitly commands strategy

### Strategy Inputs

Strategy should use:

- final analysis report
- analysis limitations
- owned baseline comparison
- user goals
- business constraints
- evidence labels
- known unknowns

### Strategy Outputs May Include

- strategic direction
- positioning options
- pricing direction
- offer direction
- funnel direction
- creative direction
- channel direction
- product direction
- risk assessment
- decision options
- validation needs

### Strategy Must Not Automatically Include

- execution task lists
- platform changes
- ad launches
- budget scaling
- live edits
- publishing
- measurement claims

---

## Strategy Construction Workflow

When strategy is authorized, the assistant should:

1. confirm the strategy source analysis
2. confirm no new data is being collected unless authorized
3. summarize the evidence base
4. state limitations
5. identify strategic options
6. compare options
7. mark assumptions
8. identify risks
9. identify validation needs
10. ask for user decision if needed
11. stop before execution unless execution is authorized

---

## Execution Gate

Execution requires explicit approval after strategy.

### Execution Can Begin Only When

- strategy exists
- direction is approved
- user authorizes execution planning
- dependencies are known
- success criteria are defined or requested

### Execution Outputs May Include

- task list
- SOP
- checklist
- implementation plan
- content production plan
- campaign build plan
- landing page update plan
- measurement setup plan

### Execution Must Not Do

- external writes without approval
- product edits without approval
- price changes without approval
- ad creation without approval
- email sending without approval
- campaign publishing without approval
- scaling without approval

---

## Measurement Gate

Measurement happens after execution or when the user asks for performance review.

### Measurement Inputs

- executed action
- KPI baseline
- date range
- result data
- source of truth
- expected outcome
- actual outcome

### Measurement Outputs

- result summary
- KPI table
- confidence level
- limitations
- keep/fix/eliminate/scale classification
- next action recommendation if strategy/decision is authorized

### Measurement Rule

Do not scale without validation.

---

## Learning Loop

Learning can happen after any phase.

### Learning Inputs

- user corrections
- mistakes
- duplicate work
- bad assumptions
- successful workflows
- weak outputs
- measurement results
- strategy outcomes

### Learning Outputs

- correction record
- lesson learned
- prevention rule
- prompt improvement
- protocol update
- memory update

### Learning Rule

User corrections are high-priority system signals.

If the assistant uses a wrong target, wrong niche, wrong assumption, or wrong phase, record the correction and add a prevention rule.

---

## Scaling Gate

Scaling happens only after measurement and validation.

### Scaling Requires

- data
- analysis
- strategy
- execution
- measurement
- validation
- user approval

### Scaling Must Include

- risk controls
- monitoring plan
- stop-loss rules
- budget or resource boundaries
- learning feedback loop

Do not scale based only on competitor activity.

---

## Standard Workflow Example: Competitor Intelligence

### 1. Source Plan

Command:

`COMPETITOR DISCOVERY PLAN`

Output:

- sources to search
- why each source matters
- expected data
- access status
- confidence level
- limitations
- archive destination

Stop before collection.

### 2. Data Collection

Command:

`APPROVE COMPETITOR DATA COLLECTION`

Output:

- raw notes
- cleaned competitor table
- missing data
- data quality notes
- source access notes
- final data collection report

Stop before analysis.

### 3. Follow-Up Data Pass

Command:

`APPROVE SMALL FOLLOW-UP DATA PASS`

Output:

- targeted gap closure
- new raw/cleaned files
- updated missing data
- updated data quality notes
- final follow-up report

Stop before analysis.

### 4. Analysis

Command:

`ANALYZE DATA`

Output:

- competitor landscape analysis
- pricing/offer analysis
- ads pattern analysis
- funnel/trust analysis
- sentiment analysis
- owned baseline comparison
- limitations
- final analysis report

Stop before strategy.

### 5. Strategy

Command:

`CREATE STRATEGY`

Output:

- strategic options
- recommended direction if authorized
- risks
- assumptions
- validation needs
- decisions needed

Stop before execution.

---

## Standard Workflow Example: Owned Store

### 1. Data Intake

Collect:

- products
- orders
- revenue
- traffic
- customer aggregates
- channels
- discounts
- refunds
- top products
- anomalies
- missing data

Stop before analysis.

### 2. Analysis

Analyze:

- revenue patterns
- product contribution
- discount behavior
- refund patterns
- channel performance
- traffic quality
- conversion
- anomalies
- owned baseline vs competitor landscape

Stop before strategy.

### 3. Strategy

Create:

- offer strategy
- pricing strategy
- funnel strategy
- retention strategy
- traffic strategy
- validation priorities

Stop before execution.

---

## Report Structure Standards

### Data Report

Should include:

- command executed
- data sources used
- data collected
- raw/cleaned archive locations
- missing data
- data quality notes
- access limitations
- no analysis confirmation
- no strategy confirmation
- exact next step

### Analysis Report

Should include:

- data sources used
- dataset summary
- analysis sections
- evidence labels
- findings
- limitations
- no strategy confirmation
- no recommendations confirmation
- no execution confirmation
- exact next step

### Strategy Report

Should include:

- analysis source
- strategic interpretation
- options
- selected or proposed direction
- assumptions
- risks
- validation needs
- decisions required
- no execution confirmation
- exact next step

### Execution Report

Should include:

- strategy source
- tasks
- priorities
- dependencies
- owners/status
- required approvals
- completion criteria
- measurement plan
- no external write confirmation unless approved

### Measurement Report

Should include:

- executed action
- KPI baseline
- KPI result
- date range
- source
- confidence level
- interpretation
- keep/fix/eliminate/scale classification
- limitations
- next step

---

## Token-Efficient Workflow

Every workflow should avoid unnecessary context usage.

### Default Context Order

1. current status
2. next actions
3. project index
4. module index
5. relevant memory record
6. relevant final report
7. relevant cleaned data
8. raw data only if needed

### Avoid

- full vault scans
- reading every file
- repeating long summaries
- verifying all wikilinks unless required
- reopening raw data when final reports are enough
- duplicate same-day collection

### Prefer

- final reports
- indexes
- memory records
- cleaned tables
- delta reports
- targeted file access
- explicit context plans for large tasks

---

## Freshness Rules

Data can become stale.

### Freshness Depends On Source

Fast-changing:

- Meta Ads Library
- ad counts
- landing pages
- competitor offers
- prices
- active campaigns
- marketplace listings

Slower-changing:

- system rules
- folder structure
- templates
- historical reports
- saved analysis
- learning records

### Freshness Labels

Use:

- CURRENT
- FRESH
- STALE
- NEEDS REFRESH
- SNAPSHOT ONLY
- HISTORICAL

### Refresh Rule

Do not refresh data automatically unless the user authorizes it.

If existing data is stale, say so and ask for refresh authorization.

---

## Current Known First Cycle

The first completed real workflow involved:

- owned Shopify data intake for Terror Prints
- STL competitor source discovery
- STL competitor data collection
- STL competitor follow-up data pass
- STL competitor analysis

The analysis was:

- descriptive-strong
- performance-blind

Meaning:

- visible competitor behavior is well described
- true competitor performance is unknown

This must constrain future strategy.

---

## What The Assistant Should Do When Asked “What Now?”

The assistant should answer by phase.

Example:

> We completed DATA and ANALYSIS for the STL competitor cycle.  
> The next possible phase is STRATEGY, but it requires explicit authorization.  
> Execution is not authorized yet.

Then provide one clear next prompt or action.

---

## Final Rule

Every workflow must end with:

- what was done
- where it was saved
- what was not done
- what remains unknown
- what the next allowed phase is
- whether approval is required

Do not continue automatically.
