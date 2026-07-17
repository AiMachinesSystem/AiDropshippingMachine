#!/usr/bin/env python3
"""set_brand_by_id.py — set Brand/Manufacturer item-specific = VALUE (default 'Unbranded') on ONE draft
via its own page (/upload/<id>), to clear AutoDS VeRO-word linter flags on manufacturer='Generic' or a
residual brand (see E-026). Mirrors set_title_by_id.py: direct nav, fill, Save (NOT Save&Import), verify.
READ/WRITE on one draft; NO publish.
Usage: set_brand_by_id.py <draft_id> ["Unbranded"]
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright

DID = sys.argv[1]
VAL = (sys.argv[2].strip() if len(sys.argv) > 2 else "Unbranded")
URL = BASE + "/upload/" + DID + "&1"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
    pg = ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
    # expand item-specifics if collapsed
    for lbl in ["Item Specifics", "Specifics", "Attributes"]:
        try:
            pg.get_by_text(re.compile(r"\b" + re.escape(lbl) + r"\b", re.I)).first.click(timeout=2000)
            pg.wait_for_timeout(1200)
        except Exception: pass
    filled = []
    for ph in ["Manufacturer", "Brand"]:
        loc = pg.locator("input[placeholder='%s']" % ph)
        try:
            cnt = loc.count()
        except Exception:
            cnt = 0
        for i in range(cnt):
            el = loc.nth(i)
            try:
                old = el.input_value()
            except Exception:
                continue
            el.click(); el.press("Control+A"); el.press("Delete"); el.fill(VAL); pg.wait_for_timeout(500)
            filled.append("%s[%d]:%r->%r" % (ph, i, old[:20], VAL))
    print("filled:", filled if filled else "NONE (no Manufacturer/Brand input found)")
    if not filled:
        print("RESULT: NO-FIELD"); b.close(); sys.exit(2)
    saved = False
    for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)),
               lambda: pg.get_by_text(re.compile(r"^\s*Save\s*$", re.I))]:
        try:
            mk().first.click(timeout=5000); saved = True; break
        except Exception: pass
    print("Save clicked:", saved); pg.wait_for_timeout(5000)
    # verify persistence
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
    for lbl in ["Item Specifics", "Specifics", "Attributes"]:
        try:
            pg.get_by_text(re.compile(r"\b" + re.escape(lbl) + r"\b", re.I)).first.click(timeout=2000)
            pg.wait_for_timeout(1000)
        except Exception: pass
    ok = False
    for ph in ["Manufacturer", "Brand"]:
        loc = pg.locator("input[placeholder='%s']" % ph)
        try:
            for i in range(loc.count()):
                if loc.nth(i).input_value().strip() == VAL:
                    ok = True
        except Exception: pass
    print("RESULT: PERSISTED %s" % ok)
    b.close()
    sys.exit(0 if ok else 1)
