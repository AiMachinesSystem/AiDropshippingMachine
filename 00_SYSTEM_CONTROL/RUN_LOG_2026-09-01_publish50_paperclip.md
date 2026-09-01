---
run_id: RUN-2026-09-01-PUBLISH50-PAPERCLIP
created_real: 2026-09-01
type: run-log
status: active
risk_class: GO-CLASS (publish live eBay — GO owner received in chat 2026-09-01, "pubblicami 50 annunci" + "go ma agganciati alla paperclip personale")
---

# RUN LOG — Publish 50 listings via Paperclip BAY fleet

## Obiettivo
50 annunci live su eBay, eseguiti dalla flotta Paperclip (company `eBay`, prefix DIGA),
porte $0 (opencode_local / omniroute), gate VeRO + NET-margin rispettati.

## Stato step
- [x] 01:38-02:04 — Tentativi ricerca inline via subagent `claude-code-guide`: FALLITI tutti (API 400 ambiguous model). Nessuna ricerca persa: tutti falliti prima di produrre output.
- [x] 02:04 — Direzione owner: aggancio Paperclip personale http://127.0.0.1:3100/DIGA/dashboard
- [x] 02:10 — Probe Paperclip: UP (HTTP 200, v2026.824.1, local_trusted). Consulta /jarvis NON necessaria: il servizio funziona e i settaggi sono già i più free possibili (5 agent BAY tutti su adapter `opencode_local`, modelli omniroute, profile "cheap" disabilitato = nessuno spende).
- [x] 02:15 — Issue creato: `5415e55a-9153-4bb0-b9a7-87fb1df70e3d` (title "Publish 50 quality listings to eBay (batch via BAY fleet)"), status todo → assegnato a BAY-LEAD, project Operations, priority high.
- [x] 02:16 — Kickoff comment postato sull'issue.
- [x] 02:17 — BAY-LEAD running; issue → in_progress.
- [ ] Fine corsa — verifica item IDs live + report owner.

## Recovery
Se questa sessione si compatta: issue Paperclip `5415e55a-9153-4bb0-b9a7-87fb1df70e3d`,
company `9cadc9a2-2151-4db4-ac83-abe23a228e20`. Poll: GET /api/issues/{id}.
Monitor attivo in sessione (issue-status). Dashboard: http://127.0.0.1:3100/DIGA/dashboard

## Note
- I 3 subagent falliti hanno usato `claude-code-guide` con modello ambiguo: non rilanciare
  su quella porta; la ricerca ora vive dentro la flotta BAY (BAY-SOURCING/BAY-COMPETITOR).
- Verifica finale = item IDs eBay live contati, non dichiarati.
