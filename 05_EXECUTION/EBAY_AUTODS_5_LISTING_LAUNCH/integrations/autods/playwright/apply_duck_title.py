#!/usr/bin/env python3
"""Apply the optimized, VeRO-safe TITLE to the duck-topper DRAFT only. Targets the Title input whose
current value contains 'duck'. Reversible (draft edit). Verifies the new value persisted after reload.
GO scope: owner GO 2026-06-17 to apply optimized title/description to the duck draft."""
import os, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
NEW_TITLE = "Rubber Duck Car Antenna Topper Aerial Ball Cute Yellow Dashboard Buddy Gift"
from playwright.sync_api import sync_playwright

def find_duck_title(pg):
    inputs = pg.locator("input[placeholder='Title']")
    n = inputs.count()
    for i in range(n):
        try:
            v = inputs.nth(i).input_value()
        except Exception:
            continue
        if re.search(r"duck", v, re.I) and not re.search(r"donald|daisy|disney", v, re.I):
            return inputs.nth(i), v
    return None, None

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception: pass
    fld,cur = find_duck_title(pg)
    if not fld:
        print("DUCK TITLE INPUT NOT FOUND"); b.close(); sys.exit(1)
    print("current duck title:", cur[:80])
    fld.scroll_into_view_if_needed(timeout=4000)
    fld.click()
    pg.keyboard.press("Control+A"); pg.keyboard.press("Delete")
    pg.wait_for_timeout(300)
    fld.press_sequentially(NEW_TITLE, delay=20)   # real keystrokes -> fire React onChange
    pg.wait_for_timeout(600)
    fld.press("Enter")
    pg.wait_for_timeout(500)
    fld.press("Tab")
    pg.wait_for_timeout(1500)
    # try an explicit Save/Update button if present
    for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*(Save|Update|Save changes)\s*$", re.I))]:
        try:
            mk().first.click(timeout=3000); print("clicked Save"); break
        except Exception: pass
    pg.wait_for_timeout(3500)
    print("set new title:", NEW_TITLE)
    # verify after reload
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception: pass
    fld2,cur2 = find_duck_title(pg)
    print("after reload, duck title:", (cur2 or "(not found)")[:90])
    print("PERSISTED:", (cur2 or "")==NEW_TITLE)
    b.close()
