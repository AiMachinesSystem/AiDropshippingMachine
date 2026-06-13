---
tags:
  - machine
type: playbook
status: template
description: "Procedura ufficiale di inizio sessione autonoma (forma PROCEDURALE — non hook). 10 passi, ~60 secondi: orientamento, stato, canone, missione aperta, gate, anti-contaminazione. Wiring come hook = GO owner separato."
---

# SESSION START PROTOCOL v0.1 — procedura ufficiale

> **Primo atto di OGNI sessione autonoma.** Forma PROCEDURALE: la macchina esegue questi
> passi come checklist — **niente hook automatici, niente node, niente auto-spawn, niente
> background agent, niente modifica automatica di note, niente intercettazione dei messaggi
> owner, niente auto-riscrittura, niente wiring automatico**. Il wiring come SessionStart hook
> vero è uno step separato con GO dedicato.

## LA PROCEDURA (~60 secondi, nell'ordine)

1. **Dove sono?** `Get-Location` + `git rev-parse --show-toplevel` — devono coincidere con la root della macchina. Da qui in poi: git SOLO con root verificata (`git -C "<root>"` o toplevel stampato nello stesso comando).
2. **Che ora è?** `Get-Date` — PRIMA di qualunque datazione (REGOLA OROLOGIO).
3. **Stato git?** `git status --short` + `git log --oneline -5`. Tree sporco non spiegato → STOP e segnala cosa è sporco prima di qualunque lavoro.
4. **C'è una missione aperta?** Cerca il run log più recente in `00_SYSTEM_CONTROL\*_RUN_LOG.md` SENZA riga `DONE` → se esiste: rileggi missione + log e riprendi dalla riga RECOVERY. Se non esiste: nessuna missione pendente.
5. **File di stato (in quest'ordine, solo le parti vive):** `MACHINE_STATE` → `BACKLOG` → `MASTER_DASHBOARD` §1–3 → `NEXT_ACTIONS` §⚡ → `ERROR_REGISTRY` (solo voci/regole nuove dall'ultima sessione: le regole del registro vincolano come la costituzione).
6. **Canone corrente?** `RESEARCH_MEMORY_INDEX`: solo righe `last_run` + headline delle sezioni CANONE CORRENTE — i numeri citabili vengono SOLO da lì (regola numeri canonici).
7. **Blocker veri?** Dashboard §2 (decisioni owner) + BACKLOG OWNER: distinguere "bloccato dall'owner" da "eseguibile ora dalla macchina".
8. **Modo operativo?** AUTONOMIA CONTROLLATA v0.1: interno → si esegue senza GO fino alla raccomandazione più forte; GO-CLASS → ci si ferma ESATTAMENTE al gate citandolo.
9. **Cosa posso fare / dove mi fermo?** Richiama la lista GO-CLASS (pubblicare, inviare, ads, spese, prezzi, piattaforme live, credenziali/account, push esterni, write esterni, impostazioni live).
10. **Anti-contaminazione:** dichiara il progetto in scope PRIMA di leggere file di progetto; firewall (ogni progetto sigillato; nessun travaso tra nicchie/sorgente/template/macchine future).

## OUTPUT DELLA PROCEDURA
5 righe di orientamento, poi si lavora: ① dove sono (root ok/anomala) ② missione aperta o no ③ 3 priorità correnti ④ blocker e di chi sono ⑤ modo operativo e gate rilevanti per il task.

## NOTE
- La procedura si ESEGUE, non si automatizza: ogni passo lascia evidenza leggibile nella sessione (auditabilità > comodità).
- Se un passo rivela un'anomalia (root sbagliata, tree sporco, log senza DONE inatteso) → si gestisce l'anomalia PRIMA del task richiesto.
- Promozione a hook: solo dopo che la procedura ha girato bene più volte, con GO owner dedicato.
