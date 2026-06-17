#!/usr/bin/env python3
"""READ-ONLY inspection of AutoDS 'Add Products' import-by-URL UI. Opens it, dumps inputs/buttons, no submit."""
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/products",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(4500)
    if "offer" in pg.url:
        try: pg.get_by_text(re.compile(r"No Thanks",re.I)).first.click(timeout=5000)
        except Exception: pass
        pg.wait_for_timeout(3000); pg.goto(BASE+"/products",wait_until="domcontentloaded",timeout=60000)
    pg.wait_for_timeout(5000)
    # click "Add Products" (sidebar/top)
    clicked=False
    for mk in [lambda: pg.get_by_role("button",name=re.compile(r"Add Products",re.I)),
               lambda: pg.get_by_text(re.compile(r"^\s*Add Products\s*$",re.I))]:
        try: mk().first.click(timeout=5000); clicked=True; break
        except Exception: continue
    print("clicked Add Products:",clicked); pg.wait_for_timeout(3000)
    print("url after click:",pg.url)
    info=pg.evaluate(r"""() => {
      const scope=document.querySelector("[role=dialog], .ant-modal, .ant-drawer") || document.body;
      const inputs=Array.from(scope.querySelectorAll("input,textarea")).map(i=>((i.tagName)+' ph="'+(i.placeholder||'')+'" type='+(i.type||'')).slice(0,90));
      const btns=Array.from(scope.querySelectorAll("button")).map(b=>(b.innerText||'').trim()).filter(Boolean).slice(0,20);
      const opts=Array.from(scope.querySelectorAll("*")).filter(e=>e.childElementCount<=1).map(e=>(e.innerText||'').trim()).filter(t=>/link|url|single|multiple|marketplace|amazon|aliexpress|import/i.test(t)).slice(0,15);
      return {hasModal: !!document.querySelector("[role=dialog],.ant-modal,.ant-drawer"), inputs:inputs.slice(0,15), buttons:btns, opts:[...new Set(opts)]};
    }""")
    print(json.dumps(info,ensure_ascii=False,indent=1)[:1600])
    b.close()
