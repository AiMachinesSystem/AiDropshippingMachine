#!/usr/bin/env python3
"""Read-only DOM inspection of the AutoDS /products pagination + page-size controls (to find selectors)."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(storage_state=STATE, viewport={"width":1440,"height":1000})
    pg = ctx.new_page()
    pg.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(4500)
    if "offer" in pg.url:
        try: pg.get_by_text(re.compile(r"No Thanks", re.I)).first.click(timeout=5000)
        except Exception: pass
        pg.wait_for_timeout(3000)
    pg.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
    info = pg.evaluate(r"""() => {
      const out = {selects:[], pag:[], showCtl:[], pageNums:[]};
      document.querySelectorAll('select').forEach(s => out.selects.push(s.outerHTML.slice(0,250)));
      document.querySelectorAll("[class*='pag' i],[class*='Pag']").forEach(e => { if(out.pag.length<8) out.pag.push((e.className||'')+' :: '+(e.outerHTML||'').slice(0,200)); });
      // elements whose text mentions Show / per page
      Array.from(document.querySelectorAll('*')).forEach(e => {
        const t=(e.childElementCount===0?(e.innerText||''):'').trim();
        if(/^show$/i.test(t) || /per page/i.test(t)) out.showCtl.push(e.tagName+'.'+(e.className||'')+' -> '+(e.parentElement?e.parentElement.outerHTML.slice(0,260):''));
        if(/^([0-9]{1,2})$/.test(t) && e.closest("[class*='pag' i]")) out.pageNums.push(e.tagName+'.'+(e.className||'')+' = '+t);
      });
      return out;
    }""")
    print("SELECTS:", info["selects"])
    print("\nPAG ELEMENTS:")
    for x in info["pag"]: print("  ", x)
    print("\nSHOW CONTROL:")
    for x in info["showCtl"][:6]: print("  ", x)
    print("\nPAGE NUMBER ELEMENTS:")
    for x in info["pageNums"][:20]: print("  ", x)
    b.close()
