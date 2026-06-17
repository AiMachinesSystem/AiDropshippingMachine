---
machine: "eBay / AutoDS Dropshipping Machine"
project: EBAY_AUTODS_5_LISTING_LAUNCH
type: run_guide
status: active
date: 2026-06-16
created_real: 2026-06-16
---

# Playwright browser automation for AutoDS — Step 1 (connectivity smoke test)

> **Why this exists.** The AutoDS REST API is application-gated + paid (see `../AUTODS_API_READINESS.md`).
> Browser automation (Playwright driving the AutoDS web UI) is the alternative path to control AutoDS.
> This folder holds the isolated Playwright setup. **Step 1 = prove the headless browser works** — no login,
> no actions, just navigate + screenshot.

## Safety contract (do not weaken)
- `smoke_test.py` opens a HEADLESS browser, navigates to ONE public URL, takes ONE screenshot. Nothing else.
- NO login, NO credentials typed, NO clicks/forms/writes. NO secrets read or printed.
- Any login/import/publish/price/order via the UI remains behind its own GO gate — Step 1 does none of that.

## Setup (isolated, reversible)
Run from this folder (`integrations/autods/playwright/`):
```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m playwright install chromium
```
- `.venv/` is gitignored. **Rollback = delete this `.venv/` folder** (and optionally `pip uninstall playwright`).

## Run the smoke test
```
.venv\Scripts\python.exe smoke_test.py --out "..\..\..\..\..\10_OUTPUTS\playwright_test.png"
```
Or with an absolute `--out` path. Output: HTTP status, final URL, page title, screenshot path + byte size.
`RESULT: PASS` means the headless browser launched, the page rendered, and the screenshot was saved.

## Install log (§0.1 PROTOCOLLO INSTALLAZIONI)
- **Gap (class A):** no Playwright driver package present (browser binaries cached at `%LOCALAPPDATA%\ms-playwright`
  but `playwright` not importable in Python or resolvable in Node).
- **Command:** `python -m venv .venv` · `pip install -r requirements.txt` · `python -m playwright install chromium`
- **Version:** Python 3.12.10 · playwright **1.60.0** · chromium reused from `ms-playwright` cache.
- **Rollback:** delete `.venv/`. No global install, no service, no autostart, no network exposure.
- **State after mission:** no browser process left running (the script always closes the browser).

## Step-1 result (2026-06-16)
- `RESULT: PASS` — http_status **200**, final_url `https://platform.autods.com/login`, title `AutoDS - Login`.
- Screenshot: `10_OUTPUTS/playwright_test.png` (~102 KB, full AutoDS login page rendered).

## Next steps (NOT done here — each is GATED)
- Persistent authenticated session (login) → **GO required** (account access, credentials).
- Any UI write (import/publish/price/relist/order) → its existing GO gate.
