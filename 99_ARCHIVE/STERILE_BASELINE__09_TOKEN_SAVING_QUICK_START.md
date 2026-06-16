# 09_TOKEN_SAVING_QUICK_START.md

## Purpose

This file is a compact token-saving guide for the **AI Market Intelligence & Execution System**.

Use it as a quick instruction layer for Claude Code, Custom GPT, ChatGPT Projects, or any future AI session.

The goal is simple:

> Preserve reasoning quality while using the smallest useful context.

---

## Core Rule

Do not read the whole vault unless the user explicitly approves it.

A large Obsidian vault is not a problem.

Uncontrolled reading is the problem.

Use the vault like a database:

1. check the index
2. check current status
3. check memory
4. check final reports
5. check cleaned data
6. open raw files only if needed

---

## Default Context Order

For almost every task, use this order:

1. `CURRENT_STATUS.md`
2. `NEXT_ACTIONS.md`
3. `PROJECT_INDEX.md`
4. `MODULE_INDEX.md`
5. relevant command/rule file
6. relevant research memory record
7. relevant final report
8. relevant cleaned data
9. raw data only if necessary

Do not start from raw data unless the task specifically requires it.

---

## Token Budget Categories

### MICRO

Use for small questions or edits.

Limit:

- 1 to 3 files

Examples:

- create one prompt
- check one report
- update one note
- answer “what now?”

---

### SMALL

Use for focused work.

Limit:

- 3 to 8 files

Examples:

- create a source plan
- update one protocol
- summarize one completed phase
- create one master file

---

### MEDIUM

Use for serious but bounded work.

Limit:

- 8 to 20 files

Examples:

- analyze one completed dataset
- create strategy from one analysis report
- create an execution plan from one approved strategy

---

### LARGE

Requires explicit user approval.

Limit:

- more than 20 files

Examples:

- broad system review
- cross-module rewrite
- architecture audit
- major restructuring

---

### FULL VAULT SCAN

Requires explicit user approval every time.

Use only for:

- full coherence review
- full wikilink audit
- migration
- complete system integrity check

---

## Mandatory Context Plan For Large Tasks

Before any LARGE task or FULL VAULT SCAN, create this first:

```text
CONTEXT PLAN

Task:
[task]

Expected size:
MICRO / SMALL / MEDIUM / LARGE / FULL VAULT SCAN

Files I will check first:
1. [file] — why
2. [file] — why
3. [file] — why

Files I will avoid unless needed:
- [file/folder] — why

Raw data needed?
Yes/No — reason

Full scan needed?
Yes/No — reason

Stop condition:
[what output ends the task]
```

Do not proceed with a large scan until the user approves.

---

## Default Token-Saving Block For Claude Code

Paste this into most Claude Code prompts:

```text
TOKEN CONTROL

Use indexes, memory records, and existing final reports first.
Do not run a full vault scan unless explicitly approved.
Open only files directly relevant to this task.
Do not repeat previous summaries.
Prefer delta reports.
Do not verify all wikilinks unless necessary.
Do not open raw data unless final reports or cleaned data are insufficient.
Stop after the requested output.
```

---

## Stronger Token-Saving Block

Use this when the task may grow too large:

```text
STRICT TOKEN CONTROL

Before reading files, identify the minimum context needed.
Use CURRENT_STATUS, NEXT_ACTIONS, PROJECT_INDEX, MODULE_INDEX, and the most relevant final report first.
Do not open more than 8 files without explaining why.
Do not open more than 20 files without explicit approval.
Do not run full vault scans.
Do not re-summarize old work.
Report only:
- what changed
- what was created
- what remains missing
- what the next allowed step is
```

---

## Anti-Duplicate Rule

Before doing work, check if the same task was already completed.

Use:

- research memory
- output registry
- action log
- final reports
- request intake

If the same task is fresh:

- reuse it
- verify only the necessary files
- do not recreate duplicate files
- do not recollect same-day data
- report the existing artifact

---

## Report-First Rule

If a final report exists, read it before raw data.

Example:

Use:

- `10_OUTPUTS/ANALYSIS_REPORTS/...`

before opening:

- all files in `03_ANALYSIS/...`
- raw files in `02_DATA/...`

Raw data is for verification, not default reading.

---

## Delta-Only Reporting

When continuing from completed work, do not repeat the full history.

Report only:

- new action taken
- files created
- files updated
- decision made
- limitations
- next step

Avoid:

- listing every historical file again
- repeating the full project architecture
- restating all previous findings
- summarizing old reports unless asked

---

## Wikilink Rule

Do not verify all wikilinks by default.

Verify all links only if:

- new cross-linked files were created
- index files were heavily changed
- the user asks for a link check
- a full coherence review is authorized

Otherwise:

- verify touched files only
- or state that full wikilink verification was not run

---

## Raw Data Rule

Open raw data only when:

- the final report is insufficient
- cleaned data conflicts with raw data
- exact wording is required
- evidence is disputed
- the analysis depends on a source detail

Do not open raw data just to repeat what final reports already say.

---

## Phase Gate Reminder

Saving tokens also means avoiding unauthorized phases.

Do not continue automatically.

Stop at the current phase:

- Data stops before analysis.
- Analysis stops before strategy.
- Strategy stops before execution.
- Execution stops before measurement.
- Measurement stops before scaling.

---

## Model Usage Rule

Use the strongest model only when the reasoning requires it.

Use advanced models for:

- system architecture
- multi-file analysis
- strategy
- cross-module reasoning
- complex corrections
- major decisions

Use faster/cheaper models for:

- small edits
- markdown formatting
- simple file creation
- link checks
- short summaries
- one-off prompts

Do not waste premium model usage on routine formatting.

---

## Short Prompt To Control Any AI Session

Use this at the top of a new session:

```text
Use minimal context.
Check memory/index/final reports before raw files.
Do not scan the full vault unless I explicitly approve.
Do not repeat old summaries.
Do not move phases without approval.
Give me one clear next step.
```

---

## Short Prompt For Claude Code

```text
Work only inside the project folder.
Use the smallest relevant context.
Use indexes and final reports first.
Open only files needed for this task.
No full vault scan.
No repeated summaries.
No next phase without approval.
Stop after the requested report.
```

---

## Emergency Stop Phrase

If token usage is getting too high, the user may say:

```text
TOKEN STOP
```

When the user says this, the assistant must:

1. stop expanding context
2. summarize current progress in 5 lines or less
3. list files already touched
4. list the minimum next action
5. wait

---

## Final Rule

The assistant should not try to know everything all at once.

The assistant should retrieve the right context at the right moment.

Small context.
High precision.
No duplicate work.
No phase skipping.
