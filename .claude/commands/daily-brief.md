---
description: Brief del giorno - legge MASTER_DASHBOARD, TASKS/DECISIONS, git log e produce nella lingua dell'owner cosa e cambiato ieri, cosa tocca all'owner oggi (con minuti), cosa e bloccato e da chi
---
Produci il brief del giorno per l'owner, in `<OWNER_LANGUAGE>`. SOLO lettura — nessuna
ricerca nuova, nessuna azione live. (Legge il cockpit + le note atomiche TASKS/DECISIONS.)

1. Fonti (in quest'ordine):
   - `00_SYSTEM_CONTROL\MASTER_DASHBOARD.md` (cockpit: stato, decisioni
     pendenti, top 5 azioni, KPI)
   - le note in `00_SYSTEM_CONTROL\TASKS\` (frontmatter: owner, priority,
     minutes, blocked_by, status) e `00_SYSTEM_CONTROL\DECISIONS\`
     (status: pending)
   - `git log --since=yesterday --oneline` nella cartella della macchina
     (+ eventuali run report di missione se <48h)
   - `00_SYSTEM_CONTROL\RESEARCH_MEMORY_INDEX.md` solo per i numeri canonici
2. Output (max ~30 righe), TRE sezioni fisse:
   - **COSA È CAMBIATO IERI** — dai commit git e dai run report recenti:
     file nuovi/modificati che contano, verdetti nuovi, KPI mossi.
   - **COSA TOCCA A TE OGGI** — le task `owner == "owner"` e
     `status == "open"` NON bloccate, in ordine di priority: una riga
     ciascuna con **minuti stimati** e link alla nota; totale minuti in
     fondo. Decisioni pending in testa se sbloccano altro.
   - **COSA È BLOCCATO E DA CHI** — task con `blocked_by` valorizzato:
     riga = task → bloccata da → chi deve muoversi (owner o macchina).
     Includi le scadenze hard (es. STALE/due date) anche se non bloccate.
3. Numeri SOLO canonici (ultimo run registrato nell'indice); ogni numero con
   fonte file + data run. Niente numeri inventati.
4. Chiudi con UNA raccomandazione di priorità per oggi, con il perché.
5. Se MASTER_DASHBOARD risulta più vecchio dell'ultimo run nell'indice,
   segnalalo come anomalia AUTO-REFRESH (la regola impone l'aggiornamento a
   fine run).

$ARGUMENTS
