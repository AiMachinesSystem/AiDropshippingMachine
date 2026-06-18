# _tmp — scratch effimero (NON versionato)

Cartella per **script e file usa-e-getta** (probe, diagnostica, esperimenti).
Tutto il contenuto è gitignored tranne questo README (vedi `.gitignore` root: `/_tmp/*` + `!/_tmp/README.md`).

Regole:
- Qui dentro vanno gli script effimeri che NON devono finire nel repo.
- Per i tool effimeri della cartella Playwright, in alternativa, usa il prefisso `_` nel nome
  (`_probe.py`) — sono auto-ignorati dal `.gitignore` di quella cartella.
- **Non** mettere qui tool canonici: la gestione draft AutoDS si fa SOLO con
  `05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/integrations/autods/playwright/manage_draft.py`
  (vedi playbook `00_SYSTEM_CONTROL/PLAYBOOKS/autods-draft-management.md`).
- Niente segreti qui (i segreti restano gestiti dai `.gitignore` dedicati).
