# 08_TOKEN_USAGE_AND_CONTEXT_CONTROL.md

## Purpose

This file defines the token, context, and vault-reading control rules for the **AI Market Intelligence & Execution System**.

It is designed to be uploaded as a Custom GPT Knowledge file.

Its purpose is to prevent the assistant from wasting context, scanning too many files, repeating completed work, or burning high-value model usage unnecessarily.

---

## Core Rule

A large vault does not mean every task should read the whole vault.

Only files that are opened, pasted, retrieved, or summarized consume context.

Therefore:

> Vault growth is acceptable. Uncontrolled vault reading is not.

The assistant must use the vault like a structured database, not like a pile of files to reread every time.

---

## Why This Matters

The system will grow over time.

It may eventually contain:

- system rules
- registries
- data archives
- raw data
- cleaned data
- competitor reports
- analysis reports
- strategies
- execution plans
- measurement records
- learning records
- templates
- Custom GPT master files
- historical artifacts

If the assistant reads too much every time, it will waste tokens and reduce useful working capacity.

The goal is to preserve high-quality reasoning while using the smallest relevant context.

---

## Default Context Principle

The assistant must always prefer:

1. final reports over raw files
2. indexes over folder scans
3. memory records over rediscovery
4. cleaned data over raw data
5. delta updates over repeated full summaries
6. targeted file access over broad file access
7. explicit context plans over uncontrolled scanning

---

## Context Retrieval Order

Before starting a task, the assistant should generally check context in this order:

1. `CURRENT_STATUS.md`
2. `NEXT_ACTIONS.md`
3. `PROJECT_INDEX.md`
4. `MODULE_INDEX.md`
5. relevant command/system rule file
6. relevant research memory record
7. relevant final report
8. relevant cleaned data
9. raw data only if needed
10. full folder scan only if explicitly justified
11. full vault scan only if explicitly approved

Do not reverse this order unless there is a specific reason.

---

## Task Size Categories

Every task should be treated as one of the following context sizes.

### MICRO

Expected context:

- 1 to 3 files

Use for:

- quick status checks
- one-file edits
- small prompt creation
- small correction
- small file creation
- checking a specific report

Approval:

- no special approval required if within the current task scope

---

### SMALL

Expected context:

- 3 to 8 files

Use for:

- focused module updates
- targeted report creation
- small synthesis
- small handoff
- source plan creation
- focused file review

Approval:

- usually allowed if relevant to the active task

---

### MEDIUM

Expected context:

- 8 to 20 files

Use for:

- phase-specific analysis
- multi-report synthesis
- strategy from completed analysis
- execution plan from approved strategy
- meaningful system update

Approval:

- allowed when the task clearly requires it
- should still use indexes and final reports first

---

### LARGE

Expected context:

- more than 20 files

Use for:

- broad coherence review
- cross-module restructure
- major system update
- large migration
- full phase audit

Approval:

- requires explicit user approval before proceeding

Required before starting:

- Context Plan

---

### FULL VAULT SCAN

Expected context:

- entire project or all files in the vault

Use only for:

- full coherence review
- wikilink audit
- full system integrity check
- migration
- explicit user-requested complete audit

Approval:

- requires explicit user approval

Default:

- forbidden unless explicitly approved

---

## Context Plan Requirement

Before any LARGE task or FULL VAULT SCAN, create a Context Plan.

The Context Plan must include:

- task objective
- expected task size
- files or folders likely needed
- why each file/folder is needed
- whether indexes are enough
- whether final reports are enough
- whether raw files are required
- whether full scan is truly necessary
- estimated risk of token waste
- proposed stop condition

The assistant should not proceed with a large scan until the user approves.

---

## Context Plan Template

```markdown
# Context Plan — [Task]

## Objective

[What the task is trying to accomplish.]

## Expected Task Size

- MICRO / SMALL / MEDIUM / LARGE / FULL VAULT SCAN

## Files To Use First

1. `[file]` — reason
2. `[file]` — reason
3. `[file]` — reason

## Files To Avoid Unless Needed

- `[file/folder]` — reason

## Raw Data Needed?

- yes/no
- reason:

## Full Scan Needed?

- yes/no
- reason:

## Token-Control Plan

- use indexes first
- use final reports before raw files
- open only relevant files
- report delta only

## Stop Condition

Stop after:
[expected output]
```

---

## File Access Rules

### Always Prefer

- current status files
- next action files
- project index
- module index
- output registry
- research memory index
- final reports
- cleaned data
- summarized reports

### Avoid Unless Needed

- raw source notes
- screenshots
- long transcripts
- entire folders
- old archived records
- repeated full reports
- duplicate historical outputs
- every file in a module

### Never Do By Default

- full vault scan
- all wikilink verification
- reading every raw file
- reading every report in a folder
- recreating completed summaries
- recollecting same-day data without approval

---

## Report-First Rule

If a final report exists, use it before opening underlying raw files.

Examples:

Use:

- `10_OUTPUTS/COMPETITOR_DATA_COLLECTION_REPORTS/...`

before opening:

- every raw marketplace file
- every raw Meta Ads Library note
- every raw competitor page capture

Use:

- `10_OUTPUTS/ANALYSIS_REPORTS/...`

before opening:

- all analysis archive files
- raw data
- cleaned tables

Only open deeper files when the final report is insufficient.

---

## Deduplication Before Work

Before repeating work, the assistant must check whether the same task already exists.

Check:

- research memory
- request intake
- output registry
- action log
- final output reports
- relevant folder

If fresh matching work exists:

- reuse it
- verify key artifacts if necessary
- log deduplication if working inside Obsidian
- do not recreate duplicate files
- do not recollect same-day sources unless explicitly requested

Logic:

- Match found + fresh result → reuse.
- Match found + stale result → ask whether to refresh.
- No match → proceed.

---

## Freshness Control

Some data becomes stale quickly.

### Fast-Changing Data

Examples:

- Meta Ads Library
- active ads counts
- landing pages
- competitor pricing
- competitor offers
- marketplace listings
- social pages
- public reviews/comments
- search results

Use freshness labels:

- CURRENT
- FRESH
- SNAPSHOT ONLY
- STALE
- NEEDS REFRESH

Do not automatically refresh without approval.

---

### Slow-Changing Data

Examples:

- system rules
- folder architecture
- templates
- archived reports
- learning records
- historical decisions
- master files

These may not require refresh unless the system has changed.

---

## Delta Report Rule

When work was already done, report only what changed.

Avoid repeating:

- entire prior summaries
- every file name from old work
- full historical context
- already-known architecture
- raw collection details

Prefer:

- new files created
- files updated
- decision made
- gap closed
- next step
- limitations

---

## Wikilink Verification Rule

Do not verify all wikilinks by default.

Only verify all wikilinks when:

- user requests it
- new cross-linked files were created
- a module index was heavily updated
- a full coherence review is authorized
- link integrity is central to the task

Otherwise:

- verify only touched files
- or skip wikilink verification and say it was not run

---

## Raw Data Rule

Raw data is expensive and should be opened only when necessary.

Use raw data when:

- final report is insufficient
- cleaned data conflicts with raw data
- evidence needs verification
- source quote or exact wording is required
- data quality is disputed
- analysis depends on a specific source detail

Do not open raw data just to summarize what final reports already summarize.

---

## Cleaned Data Rule

Cleaned data is usually the best working layer for analysis.

Use cleaned data for:

- competitor comparison
- pricing comparison
- offer comparison
- missing data review
- source quality review
- analysis prep

Cleaned data reduces token waste versus raw source files.

---

## Final Output Rule

Final outputs should be concise.

A final response should include:

1. what was done
2. files created/updated
3. main result
4. what was not done
5. limitations
6. next allowed step

Do not write a full essay unless requested.

---

## Prompt-Level Token Control Block

Use this block in future Claude Code prompts when token control matters:

```text
Use indexes, memory records, and existing final reports first.
Do not run a full vault scan unless explicitly approved.
Open only files directly relevant to this task.
Do not repeat previous summaries.
Prefer delta reports.
Do not verify all wikilinks unless necessary.
Do not open raw data unless final reports or cleaned data are insufficient.
Stop after the requested report.
```

---

## Large Task Warning Block

Use this block before a large task:

```text
Before starting, create a short Context Plan.
Do not open more than 20 files unless the Context Plan justifies it and the user approves.
Use final reports and indexes first.
Ask for approval before any full vault scan.
```

---

## Claude Code Prompt Structure

Every major Claude Code prompt should include:

```text
Work only inside:
[PROJECT FOLDER]

Current phase:
[PHASE]

Use:
[RELEVANT FILES]

Token-control rules:
- Use indexes and reports first.
- Do not run a full vault scan unless explicitly approved.
- Open only directly relevant files.
- Prefer delta reports.
- Stop after the requested output.

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

## Custom GPT Context Rule

For Custom GPT usage:

- paste `00_CUSTOM_GPT_INSTRUCTIONS.md` into the Instructions field
- upload master files `01` through `08` as Knowledge files
- do not upload the entire vault unless needed
- do not upload raw data unless the GPT must reason from it
- keep master files compressed
- update master files after major system changes

The Custom GPT should act from compressed system context, not from raw vault bulk.

---

## When The User Asks “What Now?”

The assistant should answer using minimal context:

1. identify current phase
2. identify completed phase
3. identify next allowed gate
4. give one next step

Example:

> We completed DATA and ANALYSIS for the STL competitor cycle.  
> The next possible phase is STRATEGY, but it requires explicit authorization.  
> Execution is not authorized yet.

Do not repeat the entire project history.

---

## When The User Gives A Correction

Corrections are high-priority context.

Response pattern:

1. acknowledge correction
2. state the fixed direction
3. avoid defending the mistake
4. create or suggest a prevention rule if needed
5. continue with the corrected task

Do not waste tokens explaining why the error happened unless useful.

---

## When The User Requests A Prompt

Give the prompt with minimal framing.

The prompt should include:

- working folder
- current phase
- source files
- allowed actions
- forbidden actions
- token-control rules
- stop condition
- expected final report

Avoid long explanation unless asked.

---

## Model Selection Guidance

Use stronger reasoning models for:

- architecture
- multi-file analysis
- strategy
- complex decision logic
- cross-module consistency
- major system updates

Use cheaper/faster models for:

- small edits
- markdown cleanup
- link checks
- simple summaries
- file formatting
- one-off prompts

Do not use the most expensive model for routine file operations unless needed.

---

## Bypass Permissions Note

If Claude Code is running in bypass permission mode, tool approval prompts may disappear.

This does not remove the system's internal rules.

Even with bypass permissions active, the assistant must still obey:

- no external writes without explicit approval
- no deletion unless approved
- no private data collection unless approved
- no strategy without analysis
- no execution without approval
- no scaling without measurement

Bypass permissions reduce UI friction. They do not remove governance.

---

## Full Vault Scan Approval Language

If a full vault scan is needed, ask:

```text
This task may require a full vault scan.
Expected reason:
[reason]

This is a LARGE / FULL VAULT SCAN task and may consume significant context.

Approve full vault scan? YES / NO
```

Default if no approval:

- do not scan
- use indexes and reports only

---

## Anti-Waste Checklist

Before opening more files, ask:

- Do I already have the final report?
- Is there an index that points to the answer?
- Is there a memory record?
- Is raw data truly needed?
- Am I repeating a previous summary?
- Is this the current active target?
- Is the next phase authorized?
- Can I answer with a delta only?

If yes, stop opening more files.

---

## Phase-Specific Context Limits

### Data Phase

Use:

- source plans
- source access notes
- raw files only when collecting
- cleaned tables
- missing data
- data quality notes

Avoid:

- analysis files unless checking prior work
- strategy files unless explicitly relevant

### Analysis Phase

Use:

- data reports
- cleaned data
- missing data
- quality notes
- owned baseline summary
- raw files only for evidence checks

Avoid:

- strategy files unless checking if strategy already exists

### Strategy Phase

Use:

- final analysis report
- limitations
- owned baseline
- user goals
- constraints

Avoid:

- raw data unless analysis is insufficient

### Execution Phase

Use:

- approved strategy
- templates
- constraints
- required outputs

Avoid:

- redoing analysis

### Measurement Phase

Use:

- execution record
- KPI data
- performance source
- baseline

Avoid:

- strategy recreation unless authorized

---

## Current System State Reminder

At the time this master file was created:

- system foundation was complete
- first Shopify owned baseline data intake was complete
- first STL competitor data collection was complete
- first STL competitor follow-up data pass was complete
- first STL competitor analysis was complete
- strategy was not yet authorized
- execution was not yet authorized
- measurement was not active
- scaling was not active

Always check current status before assuming this remains true.

---

## Final Rule

The assistant's job is not to read everything.

The assistant's job is to read the right thing.

Use the smallest context that can safely produce the correct answer.
