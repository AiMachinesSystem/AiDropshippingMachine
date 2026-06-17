#!/usr/bin/env python3
"""READ-ONLY: open the duck draft, find its Images tab + file-upload input + any Save mechanism. No uploads."""
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception: pass
    # locate the duck draft card via its title input value
    inputs=pg.locator("input[placeholder='Title']"); n=inputs.count(); duck_idx=None
    for i in range(n):
        try:
            if re.search(r"duck",inputs.nth(i).input_value(),re.I): duck_idx=i; break
        except Exception: pass
    print("duck title input idx:",duck_idx,"of",n)
    # click the Images tab nearest the duck title (try clicking any 'Images' tab text in the duck card region)
    # Strategy: click all 'Images' tabs is risky; instead just report file inputs + tabs globally + save buttons
    info=pg.evaluate(r"""() => {
      const fileInputs=document.querySelectorAll("input[type=file]").length;
      const tabs=[...new Set(Array.from(document.querySelectorAll('*')).filter(e=>e.childElementCount<=1).map(e=>(e.innerText||'').trim()).filter(t=>/^(Product|Description|Variants|Images|Item Specifications)$/i.test(t)))];
      const saveBtns=[...new Set(Array.from(document.querySelectorAll('button')).map(b=>(b.innerText||'').trim()).filter(t=>/save|update|apply|done|upload|add image/i.test(t)))];
      return {fileInputs,tabs,saveBtns:saveBtns.slice(0,12)};
    }""")
    print(json.dumps(info,ensure_ascii=False,indent=1)[:1200])
    # try clicking an 'Images' tab to reveal upload UI (first one), then re-count file inputs
    try:
        pg.get_by_text(re.compile(r"^\s*Images\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
        after=pg.evaluate("""() => ({fileInputs:document.querySelectorAll('input[type=file]').length,
          uploadBtns:[...new Set(Array.from(document.querySelectorAll('button')).map(b=>(b.innerText||'').trim()).filter(t=>/upload|add image|browse|choose/i.test(t)))]})""")
        print("after clicking Images tab:",json.dumps(after,ensure_ascii=False))
    except Exception as e:
        print("images tab click err:",type(e).__name__)
    b.close()
