#!/usr/bin/env python3
"""Reprice ONE product via AutoDS Bulk Edit, SAFE: reveal the Price panel, and only set+Update if an
unambiguous fixed-price numeric field is found; else Cancel (no write). Verifies before/after.
GO: owner 'all go' this chat + 'usa AutoDS direttamente'."""
import os, re, json, sys
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
TARGET="406103214230"   # Ham Maker, current sell 41.83
NEW_PRICE="49.97"        # within market $25-69; +19%
from playwright.sync_api import sync_playwright

def read_price(pg):
    pg.goto(BASE+"/products",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(3500)
    if "offer" in pg.url:
        try: pg.get_by_text(re.compile(r"No Thanks",re.I)).first.click(timeout=4000)
        except Exception: pass
        pg.wait_for_timeout(2500); pg.goto(BASE+"/products",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(3500)
    pg.locator("input[placeholder]").first.fill(TARGET); pg.locator("input[placeholder]").first.press("Enter"); pg.wait_for_timeout(4000)
    txt=pg.locator("body").inner_text(timeout=6000)
    m=re.findall(r"\$?(\d{1,3}\.\d{2})", txt)
    return m

with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    ctx=b.new_context(storage_state=STATE,viewport={"width":1500,"height":1000})
    pg=ctx.new_page()
    before=read_price(pg); print("BEFORE prices on row page:",before[:8])
    # tick row + open Bulk Edit
    try: pg.locator("input.ant-checkbox-input").nth(1).check(timeout=4000); pg.wait_for_timeout(800)
    except Exception as e: print("tick fail",e); b.close(); sys.exit(1)
    try: pg.get_by_text(re.compile(r"^\s*Bulk Edit\s*$",re.I)).first.click(timeout=5000); pg.wait_for_timeout(2500)
    except Exception as e: print("bulkedit fail",e); b.close(); sys.exit(1)
    # click the Price option/tab inside modal
    try: pg.get_by_text(re.compile(r"^\s*Price\s*$",re.I)).last.click(timeout=4000); pg.wait_for_timeout(1800)
    except Exception: print("no Price tab")
    # dump the price panel
    panel=pg.evaluate(r"""() => {
      const dlg=document.querySelector('.ant-modal, [role=dialog]')||document.body;
      const opts=[...dlg.querySelectorAll('button,label,span,div,a,.ant-radio-wrapper,.ant-select')].map(e=>e.childElementCount<=1?(e.innerText||'').trim():'').filter(t=>t&&t.length<40&&/fixed|set|price|profit|increase|decrease|amount|%|margin|new/i.test(t));
      const inputs=[...dlg.querySelectorAll('input')].map(i=>({ph:i.placeholder||'',type:i.type,val:i.value||''}));
      return {opts:[...new Set(opts)].slice(0,30),inputs:inputs.slice(0,20),text:(dlg.innerText||'').replace(/\s+/g,' ').slice(0,600)};
    }""")
    print("PRICE PANEL opts:",panel["opts"])
    print("PRICE PANEL inputs:",json.dumps(panel["inputs"]))
    print("PRICE PANEL text:",panel["text"])
    # SAFETY: only proceed if there's a clear 'fixed'/'set price' affordance + a usable numeric input
    has_fixed=any(re.search(r"fixed|set price|set new|new price",o,re.I) for o in panel["opts"])
    print("\n[SAFETY] unambiguous fixed-price affordance found:",has_fixed)
    print("[DECISION] No write this run — observation only (cancel). Will execute once the fixed-price field is confirmed.")
    try: pg.get_by_role("button",name=re.compile(r"Cancel",re.I)).first.click(timeout=4000)
    except Exception: pass
    pg.screenshot(path=os.path.join(HERE,"_reprice_panel.png"))
    b.close()
