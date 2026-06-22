#!/usr/bin/env python3
"""READ-ONLY: select the Ham Maker product, open Bulk Edit, and dump the modal's price/profit controls.
NO submit, NO save — observe only, then close."""
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
TARGET="406103214230"  # Ham Maker, sell 41.83
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    ctx=b.new_context(storage_state=STATE,viewport={"width":1500,"height":1000})
    pg=ctx.new_page()
    pg.goto(BASE+"/products",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(4500)
    if "offer" in pg.url:
        try: pg.get_by_text(re.compile(r"No Thanks",re.I)).first.click(timeout=5000)
        except Exception: pass
        pg.wait_for_timeout(3000); pg.goto(BASE+"/products",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(5000)
    try:
        box=pg.locator("input[placeholder]").first; box.fill(TARGET); box.press("Enter"); pg.wait_for_timeout(4500)
    except Exception as e: print("search fail",e)
    # tick first row checkbox
    try:
        cb=pg.locator("input.ant-checkbox-input").nth(1); cb.check(timeout=4000); pg.wait_for_timeout(1200)
        print("row checkbox ticked")
    except Exception as e: print("tick fail",type(e).__name__)
    # click Bulk Edit
    try:
        pg.get_by_text(re.compile(r"^\s*Bulk Edit\s*$",re.I)).first.click(timeout=5000); pg.wait_for_timeout(3000)
        print("Bulk Edit opened")
    except Exception as e: print("bulk edit click fail",type(e).__name__)
    # dump modal
    info=pg.evaluate(r"""() => {
      const opts=[...document.querySelectorAll('button,label,span,div,a')].map(e=>e.childElementCount<=1?(e.innerText||'').trim():'').filter(t=>t&&t.length<40&&/price|profit|fixed|margin|break|set|change|increase|decrease|%|amount/i.test(t));
      const inputs=[...document.querySelectorAll('input')].map(i=>({ph:i.placeholder||'',type:i.type,val:(i.value||'').slice(0,16)}));
      const radios=[...document.querySelectorAll('input[type=radio]')].length;
      const modalText=(document.querySelector('.ant-modal, [role=dialog]')||{}).innerText||'';
      return {opts:[...new Set(opts)].slice(0,25),inputs:inputs.slice(0,15),radios,modalSnippet:modalText.replace(/\s+/g,' ').slice(0,500)};
    }""")
    print("modal options:",info["opts"])
    print("modal inputs:",json.dumps(info["inputs"]))
    print("radios:",info["radios"])
    print("modal text:",info["modalSnippet"])
    pg.screenshot(path=os.path.join(HERE,"_bulk_edit_modal.png"))
    b.close()
