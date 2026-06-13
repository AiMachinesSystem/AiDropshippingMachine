---
tags:
  - machine
type: playbook
status: active
date: 2026-06-12
---

# PLAYBOOK — Playwright + Chromium headless (studiato 2026-06-12)

**Gap che chiude:** Layer 7 (intelligence esterna: screenshot/visual QA di
landing page come evidenza). Classe A piena: open-source, zero account, zero
servizi, locale, reversibile, dentro budget.

- **Stato pre-install [OBSERVED 2026-06-12]:** CLI v1.60.0 risolvibile via
  npx, ma NESSUN browser in `%LOCALAPPDATA%\ms-playwright`.
- **Install scelta (locale, repo-pulita):** cartella dedicata
  `90_CACHE\tools\playwright\` con `package.json` proprio →
  `npm install playwright` (lì dentro) + `npx playwright install chromium
  --only-shell` (solo headless shell, più piccola del Chromium pieno ~281 MB
  [OBSERVED — playwright.dev/docs/browsers]). node_modules NON versionato
  (.gitignore).
- **Verifica:** `npx playwright --version` + smoke test headless (script
  `smoke.js`: apre example.com, salva screenshot, chiude browser) — nessun
  processo residuo dopo `browser.close()`.
- **Percorso browser Windows:** `%LOCALAPPDATA%\ms-playwright`.
- **Uninstall pulito:** `npx playwright uninstall --all` (binari browser) +
  cancellare `90_CACHE\tools\playwright\node_modules`.
- **Esposizione rete/servizi:** nessuna — il browser vive solo durante lo
  script [OBSERVED — omissione docs + architettura library mode].
- **Script minimo (dai docs, library mode):** vedi `smoke.js` nella cartella
  tools (goto → screenshot → close).
- **Regole d'uso nella macchina:** solo pagine pubbliche; screenshot salvati
  in `90_CACHE\screenshots\<dominio>\<data>_<slug>.png` come evidenza
  [OBSERVED-class]; mai login automation; mai lasciare processi attivi.
- **Shim npx — ATTENZIONE (lezione di metodo):** se il percorso della vault
  contiene spazi o `&`, lo shim cmd di npx si rompe — il path viene troncato al
  primo spazio e il resto interpretato come comando [OBSERVED — `Cannot find
  module ...cli.js` + `'<parola>' is not recognized`]. Non è riparabile senza
  rinominare il percorso. Workaround PERMANENTE (non temporaneo): invocare
  Playwright via
  `node "<VAULT_ROOT>\90_CACHE\tools\playwright\node_modules\playwright\cli.js" …`
  oppure script library-mode via `node`.
