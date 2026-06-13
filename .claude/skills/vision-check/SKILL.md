---
name: vision-check
description: Rapid realignment check of any plan, output, or pending action against the machine's constitution and vision. Use when the owner asks "vision check", "siamo allineati alla vision?", "questo rispetta le regole?", or before delivering any strategy/launch output if there is doubt about gates. Read-only — produces a verdict, never fixes silently.
---

# Vision Check

**v1.0 (2026-06-13).** Verifica di allineamento in ≤5 minuti. Read-only.

## SOURCES (in quest'ordine)
1. `00_SYSTEM_CONTROL\VISION_ALIGNMENT.md` (costituzione)
2. `CLAUDE.md` di progetto (regole operative)
3. `00_SYSTEM_CONTROL\VISION_SCHEMA.md` (stack/architettura)
4. `MACHINE_STATE.md` (stato corrente)

## CHECKLIST (applicare al target indicato dall'owner)
- **GO gates:** il target contiene azioni live/esterne senza GO esplicito
  per-azione? (pubblicare, spendere, inviare, registrare, login, write su
  piattaforme) → FLAG bloccante.
- **Evidenze:** ogni claim ha etichetta [OBSERVED/INFERRED/UNKNOWN]? numeri
  inventati o stime non marcate? → FLAG.
- **Firewall progetti:** travasi non autorizzati tra progetti (es. tra
  `<PROJECT_NAME>` e altre nicchie)? → FLAG bloccante.
- **Owner-only data:** il target presuppone dati dietro mura owner senza
  averli chiesti? → FLAG.
- **Forma output:** finisce con raccomandazione + confidenza + alternative
  scartate (mai solo lista opzioni)? struttura §8 dello schema rispettata?
- **Integrità:** claim non sostanziabili, prove fabbricate, anchor non
  dichiarati in QUALSIASI bozza? → FLAG bloccante (mai replicare anti-pattern).

## OUTPUT (inline, niente file salvo richiesta)
`ALLINEATO` oppure `DISALLINEATO + lista flag (bloccanti vs minori) + fix
minimo per ciascuno`. Una riga di fonte per ogni flag (file + sezione).
