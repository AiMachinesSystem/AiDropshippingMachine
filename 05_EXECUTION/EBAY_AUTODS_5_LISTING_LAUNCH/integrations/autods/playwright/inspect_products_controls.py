#!/usr/bin/env python3
"""READ-ONLY inspection of AutoDS /products controls: search box, Add Filter, bulk-action bar, row checkbox,
and whether searching an eBay item_id filters to that product. NO deletes, NO writes — only opens/reads."""
import os, re, sys, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
# load one target item id to test search
root=HERE
test_id=None
for r,_,fs in os.walk(os.path.join(HERE,"..","..","..","..","..","90_CACHE","fetches","autods")):
    if "_removal_set_oos.json" in fs:
        data=json.load(open(os.path.join(r,"_removal_set_oos.json"),encoding="utf-8")); test_id=data[0]["item_id"]; break
print("test item_id:",test_id)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000})
    pg=ctx.new_page()
    pg.goto(BASE+"/products",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(4500)
    if "offer" in pg.url:
        try: pg.get_by_text(re.compile(r"No Thanks",re.I)).first.click(timeout=5000)
        except Exception: pass
        pg.wait_for_timeout(3000)
    pg.goto(BASE+"/products",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(6000)
    info=pg.evaluate(r"""() => {
      const out={searchInputs:[],filterBtns:[],bulkBtns:[],checkboxes:0,rowText:''};
      document.querySelectorAll("input").forEach(i=>{ const ph=(i.placeholder||'')+' type='+i.type+' '+(i.className||'').slice(0,40); if(/search|sku|item|title/i.test(i.placeholder||'')||i.type==='search') out.searchInputs.push(ph); });
      Array.from(document.querySelectorAll('button,div,span')).forEach(e=>{ const t=(e.childElementCount<=1?(e.innerText||''):'').trim(); if(/^add filter$/i.test(t)) out.filterBtns.push(e.tagName+'.'+(e.className||'').slice(0,40)); if(/^(bulk edit|bulk delete|bulk relist|remove from list|delete)$/i.test(t)) out.bulkBtns.push(t); });
      out.checkboxes=document.querySelectorAll("input[type=checkbox]").length;
      return out;
    }""")
    print("search inputs:",info["searchInputs"][:8])
    print("Add Filter btns:",info["filterBtns"][:4])
    print("bulk/delete btns visible:",info["bulkBtns"])
    print("checkboxes on page:",info["checkboxes"])
    # try searching the test item id
    if test_id:
        box=None
        for mk in [lambda: pg.get_by_placeholder(re.compile(r"search|sku|item|title",re.I)),
                   lambda: pg.locator("input[type='search']"),
                   lambda: pg.locator("header input, input[placeholder]")]:
            try:
                c=mk().first; c.wait_for(state="visible",timeout=4000); box=c; break
            except Exception: continue
        if box:
            try:
                box.fill(str(test_id)); box.press("Enter"); pg.wait_for_timeout(4000)
                txt=pg.locator("body").inner_text(timeout=6000)
                print("\nafter searching item_id, page mentions id:", str(test_id) in txt, "| 'out of 1'? ", "out of 1" in txt.lower() or "1 result" in txt.lower())
                import re as _re
                m=_re.search(r"out of (\d+)", txt.lower())
                print("  results count token:", m.group(0) if m else "n/a")
            except Exception as e:
                print("search test failed:",type(e).__name__)
        else:
            print("no search box found")
    b.close()
