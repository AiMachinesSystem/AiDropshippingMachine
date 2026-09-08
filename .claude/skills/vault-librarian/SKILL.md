---
name: vault-librarian
description: Audit and upkeep of the vault's research-output tree, indexes, and machine-state files. Use when the owner asks to tidy, audit, reorganize, or check the vault ("riordina il vault", "audit dell'alberatura", "i file sono a posto?", "aggiorna lo stato della macchina", "manutenzione archivio"). Read/move/rename ONLY research outputs — never other projects' execution or decision files, never governance files without explicit owner scope.
---

# Vault Librarian

Keeps the research vault navigable. **v1.0 (2026-06-13).** Conservative by
design: reversibility beats tidiness.

## SCOPE (hard limits)

- Operates on `10_OUTPUTS\` (research outputs), `00_SYSTEM_CONTROL\
  RESEARCH_MEMORY_INDEX.md`, `MACHINE_STATE.md`, `BACKLOG.md`.
- NEVER touches: other projects' execution folders (e.g. 05_EXECUTION\*),
  governance/constitution files, `99_ARCHIVE` snapshots, `.git`.
- Every move/rename = git mv (or move + add) with a commit; never delete
  content — superseded files get a `> SUPERSEDED by <path>` header line
  ONLY if the owner authorized editing them.

## PROTOCOL

1. **Audit** — list `10_OUTPUTS` recursively; check each file against the
   convention `10_OUTPUTS\<TYPE>\YYYY-MM-DD_<slug>_<type>_vN.md`; check
   every path referenced by `RESEARCH_MEMORY_INDEX.md` actually exists.
2. **Cross-reference check BEFORE any rename** — grep the vault for the
   filename; if ≥1 reference exists outside the index, renaming requires
   updating every reference in the same commit, or (default) SKIP the
   rename and log why. Legacy files with many references stay as they are.
3. **Fix** — apply only safe moves/renames; update index links in the same
   commit.
4. **Refresh state** — update `MACHINE_STATE.md` (skills/integrations/
   project phases if changed) and `BACKLOG.md` (close done items with date,
   add newly discovered ones).
5. **Report** — what was moved/renamed/skipped and why; commit message
   prefix `LIBRARIAN:`.

## EVIDENCE & SAFETY

Read-only outside the scope above. No web. No installs. Every decision
logged. If anything is ambiguous (file ownership unclear, reference web too
tangled), do nothing and surface it to the owner instead.
