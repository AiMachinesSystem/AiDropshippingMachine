#!/usr/bin/env python3
"""READ-ONLY inspection of AutoDS 'Add product with link' flow (Drafts/upload). Opens it, dumps input+buttons, no submit."""
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(6000)
    print("url:",pg.url)
    # click "Add product with link" (or "Add product")
    clicked=None
    for label in ["Add product with link","Add product","Add Products","Add a product"]:
        try:
            pg.get_by_text(re.compile(r"^\s*"+re.escape(label)+r"\s*$",re.I)).first.click(timeout=4000)
            clicked=label; break
        except Exception: continue
    print("clicked:",clicked); pg.wait_for_timeout(2500)
    info=pg.evaluate(r"""() => {
      const scope=document.querySelector("[role=dialog],.ant-modal,.ant-drawer")||document.body;
      const inputs=Array.from(scope.querySelectorAll("input,textarea")).map(i=>(i.tagName+' ph="'+(i.placeholder||'')+'" type='+(i.type||'')+' name='+(i.name||'')).slice(0,100));
      const btns=Array.from(scope.querySelectorAll("button")).map(b=>(b.innerText||'').trim()).filter(Boolean).slice(0,15);
      const heads=Array.from(scope.querySelectorAll("h1,h2,h3,h4,label,.ant-modal-title")).map(e=>(e.innerText||'').trim()).filter(Boolean).slice(0,10);
      return {hasModal:!!document.querySelector("[role=dialog],.ant-modal,.ant-drawer"),heads,inputs:inputs.slice(0,12),buttons:btns};
    }""")
    print(json.dumps(info,ensure_ascii=False,indent=1)[:1800])
    b.close()
