#!/usr/bin/env python3
"""set_title_by_id.py — set an eBay title (<=80) on a draft via its OWN page (/upload/<id>) BY ID.
Bloat-immune: navigates directly to the draft (no /upload list DOM search -> avoids the brand/match + page-1
failure of manage_draft set-title, see E-020). Fills input[placeholder=Title], clicks Save (NOT Save&Import),
re-reads the input to confirm persistence. READ/WRITE on ONE draft only; no publish.
Usage: set_title_by_id.py <draft_id> "<new title <=80>"
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright

DID = sys.argv[1]; NEW = sys.argv[2].strip()
if len(NEW) > 80:
    print("RESULT: ABORT title-over-80 len=%d" % len(NEW)); sys.exit(1)
URL = BASE + "/upload/" + DID + "&1"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True); ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
    pg = ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
    ti = pg.locator("input[placeholder='Title']").first
    try:
        old = ti.input_value()
    except Exception:
        print("RESULT: ABORT no-title-input"); b.close(); sys.exit(1)
    print("old title:", old[:70], "| len", len(old))
    ti.click(); ti.press("Control+A"); ti.press("Delete"); ti.fill(NEW); pg.wait_for_timeout(800)
    # Save (the per-card Save button; NOT Save & Import which would publish)
    saved = False
    for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)),
               lambda: pg.get_by_text(re.compile(r"^\s*Save\s*$", re.I))]:
        try:
            mk().first.click(timeout=5000); saved = True; break
        except Exception:
            pass
    print("Save clicked:", saved); pg.wait_for_timeout(5000)
    # re-read to verify persistence (reload the page fresh)
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
    cur = pg.locator("input[placeholder='Title']").first.input_value()
    ok = cur.strip() == NEW
    print("new title:", cur[:70], "| len", len(cur))
    print("RESULT: PERSISTED %s" % ok)
    b.close()
    sys.exit(0 if ok else 1)
