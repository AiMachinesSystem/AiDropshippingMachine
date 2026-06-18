---
tags:
  - machine
type: entity
status: active
date: 2026-06-18
description: "Playbook canonico per la gestione draft AutoDS (import + titolo + descrizione + immagine). Tool unico = manage_draft.py. Da qui in poi NIENTE script one-off per queste operazioni."
---

# AutoDS Draft Management (canonico)

Workflow canonico per creare/ottimizzare draft su AutoDS. **Un solo tool**, niente più script one-off.

## Tool canonico
`05_EXECUTION/EBAY_AUTODS_5_LISTING_LAUNCH/integrations/autods/playwright/manage_draft.py`
(eseguire con `PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe manage_draft.py <cmd>` su Windows).

Consolida e SOSTITUISCE: `import_drafts.py`, `apply_titles_*.py`, `apply_desc_ckeditor_*.py`, `discover_draft_ids.py`, `add_fabric_image_url.py` (restano per storia, ma non si usano più).

## Comandi
| Comando | Cosa fa |
|---|---|
| `status` | conta i draft |
| `import --url URL [--dry]` | importa una URL fornitore come DRAFT (solo "Add as Draft", mai publish) |
| `find-id --match REGEX` | stampa la pagina dedicata `/upload/<id>` del draft il cui titolo matcha |
| `set-title --match REGEX --title "T"` | imposta il titolo (≤80) sul draft il cui titolo CORRENTE matcha |
| `set-desc --id ID (--desc-file F \| --desc S) [--guard STR]` | imposta la descrizione (CKEditor) sulla pagina dedicata |
| `add-image --id ID --image-url URL` | aggiunge un'immagine custom via "Enter Image URL" |
| `full --url URL --match REGEX --title "T" (--desc-file F\|--desc S) [--image-url URL] [--dry]` | import → titolo → find-id → descrizione → immagine, con verifica |

Esempio end-to-end:
```
python manage_draft.py full --url https://www.amazon.com/dp/B0XXXX \
  --match "dog bed|orthopedic" --title "Titolo <=80" --desc-file copy.html --image-url https://.../main.png
```

## Sicurezza integrata (non indebolire)
- Mai "Publish to Store" / "Save & Import" — solo "Add as Draft" / "Save".
- Titolo **hard-cap a 80 char** (rifiuta se più lungo). Descrizione sempre verificata.
- Tutto reversibile (draft edit). Publish/prezzi/ordini = azione live separata GO-gated.

## Capability & muri noti (stato 2026-06-18)
- **Fonti importabili AutoDS:** SOLO AliExpress + Amazon (Temu non importabile → manuale; vedi [[temu-manual-sourcing]]).
- **Immagine custom:** si AGGIUNGE via "Add Image → Enter Image URL" (o upload file) e persiste. MA le immagini fornitore sono **bloccate** (no delete, badge "amazon") e il drag non persiste → l'immagine custom NON è promuovibile a principale dentro AutoDS. **La main image si imposta su eBay al publish.**
- **Descrizione:** editor = CKEditor → si scrive via `window.CKEDITOR.instances[0].setData(html)` sulla pagina dedicata `/upload/<id>` (single-draft = nessun rischio E-002).
- **Prezzo:** sul draft resta $0 finché non impostato (pricing rule o manuale) — si fa al publish.
- Regola copy: titolo ≤80, descrizione SEMPRE riscritta VeRO-safe → [[listing-title-description-rule]].

## Script effimeri (convenzione)
Probe/diagnostica usa e getta: **prefisso `_` nel nome** (`_probe.py`) nella cartella playwright → auto-ignorati da git; oppure usare la cartella scratch `/_tmp/` (gitignored). Mai committare script one-off di import/titolo/descrizione/immagine: usa `manage_draft.py`.

## Collegamenti
- Tool: `integrations/autods/playwright/manage_draft.py`
- Sessione/auth: `login_and_save_session.py` (storage_state.json, gitignored)
- Sourcing manuale Temu: [[temu-manual-sourcing]] · regola copy: [[listing-title-description-rule]]
