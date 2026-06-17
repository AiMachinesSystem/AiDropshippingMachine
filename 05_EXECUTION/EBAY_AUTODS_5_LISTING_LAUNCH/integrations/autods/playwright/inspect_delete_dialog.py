#!/usr/bin/env python3
"""SAFE inspection of the AutoDS Bulk Delete confirm dialog. Ticks ONE target row, opens Bulk Delete,
DUMPS the dialog text/buttons/checkboxes, then CANCELS (Escape) — NOTHING is deleted. Read-only outcome."""
import os, re, sys, json, glob
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
def root():
    c=os.path.abspath(HERE)
    while c!=os.path.dirname(c):
        if os.path.isdir(os.path.join(c,"10_OUTPUTS")): return c
        c=os.path.dirname(c)
    return HERE
R=root()
cands=sorted(glob.glob(os.path.join(R,"90_CACHE","fetches","autods","*","_removal_set_oos.json")))
targets={str(x["item_id"]) for x in json.load(open(cands[-1],encoding="utf-8"))}
pl=sorted(glob.glob(os.path.join(R,"90_CACHE","fetches","autods","audit_*","_products_list.json")))
keep={str(it.get("item_id_on_site")) for it in json.load(open(pl[-1],encoding="utf-8")) if it.get("status")==2 and (it.get("total_sold_count") or 0)>0}
from playwright.sync_api import sync_playwright
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
    rows=pg.evaluate(r"""() => {
      const cbs=Array.from(document.querySelectorAll("input.ant-checkbox-input, input[type=checkbox]"));
      return cbs.map((cb,i)=>{let el=cb;for(let k=0;k<7&&el.parentElement;k++){el=el.parentElement;if((el.innerText||'').length>60)break;}
        const t=(el.innerText||'').replace(/\s+/g,' ');return {i,ids:(t.match(/\b\d{11,13}\b/g)||[])};});
    }""")
    pick=None
    for r in rows:
        ids=set(r["ids"])
        if ids&keep: continue
        if ids&targets: pick=(r["i"],sorted(ids&targets)[0]); break
    print("picked checkbox idx",pick)
    if pick:
        pg.locator("input.ant-checkbox-input").nth(pick[0]).check(timeout=4000)
        pg.wait_for_timeout(800)
        try:
            pg.get_by_text(re.compile(r"^\s*Bulk Delete\s*$",re.I)).first.click(timeout=5000)
            pg.wait_for_timeout(2000)
        except Exception as e:
            print("bulk delete click fail",type(e).__name__)
        dlg=pg.evaluate(r"""() => {
          const m=document.querySelector("[role=dialog], .ant-modal, .ant-modal-confirm, .MuiDialog-root");
          if(!m) return {found:false};
          const btns=Array.from(m.querySelectorAll("button")).map(b=>(b.innerText||'').trim()).filter(Boolean);
          const cbs=Array.from(m.querySelectorAll("input[type=checkbox]")).map(c=>(c.closest('label')?.innerText||c.parentElement?.innerText||'').trim().slice(0,60));
          return {found:true, text:(m.innerText||'').replace(/\s+/g,' ').slice(0,600), buttons:btns, checkboxes:cbs};
        }""")
        print("DIALOG:",json.dumps(dlg,ensure_ascii=False,indent=1)[:1400])
        # CANCEL — never confirm
        try: pg.keyboard.press("Escape")
        except Exception: pass
        pg.wait_for_timeout(800)
        for mk in [lambda: pg.get_by_role("button",name=re.compile(r"^(cancel|close|no)$",re.I))]:
            try: mk().first.click(timeout=2000); break
            except Exception: pass
        pg.wait_for_timeout(1500)
        txt=pg.locator("body").inner_text(timeout=6000)
        m=re.search(r"out of (\d+)",txt.lower())
        print("after cancel, products count token:", m.group(0) if m else "n/a","(should still be 214 — nothing deleted)")
    b.close()
