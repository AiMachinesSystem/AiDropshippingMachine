---
tags:
  - machine
type: playbook
status: template
---

# VAULT_CONVENTIONS — nomi, cartelle, muri noti (template v1)

## CONVENZIONE NOMI OUTPUT

`10_OUTPUTS\<TIPO>\YYYY-MM-DD_<niche-or-project-slug>_<tipo>_vN.md`
- TIPO cartelle attive: MARKET_RESEARCH_REPORTS · COMPETITOR_ANALYSIS ·
  ADS_LIBRARY_SCANS · CREATIVE_BRIEFS · TEST_PLANS · STRATEGY_REPORTS ·
  SYSTEM_REPORTS · ANALYSIS_REPORTS.
- Un run = UN file. Appendici: `..._vN.M_APPENDIX.md` accanto al file base.
- Output execution di progetto: `05_EXECUTION\<project-slug>\YYYY-MM-DD_...`
  — mai nella cartella di un altro progetto.
- Registrazione indice OBBLIGATORIA a fine run (blocco nicchia in
  `00_SYSTEM_CONTROL\RESEARCH_MEMORY_INDEX.md`).
- REGOLA OROLOGIO: la data nel nome = output di `Get-Date` del momento; mai
  ereditata da nomi di missioni o file esistenti. File con data nel nome
  portano `created_real` (primo commit git) nel frontmatter; in conflitto fa
  fede `created_real`. Nomi già errati NON si rinominano (i riferimenti
  incrociati valgono più della data nel nome).

## CARTELLE DI SISTEMA

`00_SYSTEM_CONTROL\`: TEMPLATES\ (modelli output) · PLAYBOOKS\ (schede
install/integrazione + n8n_workflows\) · BASES\ (viste Obsidian) ·
MISSION_TEMPLATES\ (scheletri missione) · TASKS\ · DECISIONS\ · run
log/report missioni (`*_RUN_LOG.md`, `*_RUN_REPORT_*.md`). Se versioni le
skill nel repo, tieni `SKILL_SNAPSHOTS\` (`YYYY-MM-DD_<skill>_vX.md`, una a
ogni bump).

## 90_CACHE (non versionata — solo .gitkeep/README in git)

- `fetches\<dominio>\YYYY-MM-DD_<slug>.txt` — raw di ogni fetch load-bearing,
  salvato PRIMA della citazione; citazione: `[OBSERVED — url + data (cache:
  path)]`.
- `screenshots\<dominio>\YYYY-MM-DD_<slug>.png` — evidenze visive (solo pagine
  pubbliche, mai login).
- `tools\` — strumenti locali (es. Playwright: vedi playbook; attenzione allo
  shim npx se il path della vault contiene spazi o `&`).
- `selftests\` — output dei test a freddo (`claude -p`) come evidenza.

## REGISTRO MURI NOTI (non ri-tentare prima di 7 giorni dall'ultima verifica)

> Popola questa tabella man mano che incontri muri reali (siti che bloccano
> fetch/scraping, login wall, rate-limit). Aggiorna la riga quando un muro
> viene ri-testato; nuovo muro = nuova riga. Fallimento nuovo ≥2 retry →
> [UNKNOWN] + checklist owner, avanti.

| Muro | Ultima verifica | Esito |
|---|---|---|
| `amazon.com` product pages `/dp/<ASIN>` | 2026-06-28 (r.jina.ai proxy, 10+ tentativi) | CAPTCHA sistematico su tutte le pagine prodotto — prezzi non accessibili; search pages a volte 503. 3 fetch parziali (dati non-prezzo). Non riprovare prima di 2026-07-05. |
| `ebay.com/itm/<itemID>` | 2026-06-28 (r.jina.ai proxy) | 403 Forbidden su tutti i /itm/ singoli. Pagine /p/ (product catalog) funzionano parzialmente. Non riprovare prima di 2026-07-05. |
| `camelcamelcamel.com` | 2026-06-28 (r.jina.ai proxy) | Security verification block (Cloudflare). Dati prezzi non accessibili. |
| `walmart.com/search` | 2026-06-28 (r.jina.ai proxy) | CAPTCHA / robot check. Nessun dato prodotto. |

## VERSIONI SKILL

Bump di versione → changelog di 1 riga nell'header della skill (+ snapshot in
SKILL_SNAPSHOTS se versioni nel repo) + riga in MACHINE_STATE. QUERY MODE
risponde coi numeri dell'ultimo run registrato (regola "numeri canonici").

## REGOLA NUMERI CANONICI

Più run sulla stessa nicchia: vince SEMPRE l'ultimo registrato. Il blocco
nicchia in RESEARCH_MEMORY_INDEX con più run DEVE avere un'unica sezione
`### CANONE CORRENTE` in testa (QUERY MODE legge SOLO quella) e i numeri
superati sotto `### STORICO (superato da ...)`. VIETATO lasciare numeri
vecchi nei campi schema (`census:`, `leader:`, `key numbers:`) fuori dallo
STORICO.
