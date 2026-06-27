#!/usr/bin/env python3
"""READ-ONLY: scroll the AutoDS drafts list to load ALL drafts, capture list API JSON,
print per-draft economics deduped by id. No writes."""
import os, re, json
from datetime import datetime
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
bodies=[]
def main():
    root=HERE
    while root and not os.path.isdir(os.path.join(root,"10_OUTPUTS")): root=os.path.dirname(root)
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
        def cap(r):
            try:
                if "v2-api.autods.com/products/" in r.url and "/list/" in r.url and "application/json" in (r.headers or {}).get("content-type",""):
                    bodies.append((r.url, r.text()))
            except Exception: pass
        pg.on("response", cap)
        pg.goto(BASE+"/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(9000)
        # scroll repeatedly to force lazy load of all drafts
        for _ in range(40):
            pg.mouse.wheel(0, 4000); pg.wait_for_timeout(1200)
            try: pg.get_by_text(re.compile(r"^\s*Load more\s*$",re.I)).first.click(timeout=1000)
            except Exception: pass
        pg.wait_for_timeout(3000); b.close()
    rows={}
    for url,body in bodies:
        try: data=json.loads(body)
        except Exception: continue
        items = data.get("results") or data.get("data") or (data if isinstance(data,list) else [])
        if isinstance(items,dict): items=items.get("results",[])
        for it in (items or []):
            if not isinstance(it,dict): continue
            pid=str(it.get("id") or it.get("_id") or "")
            title=(it.get("title") or "")[:55]
            vs=it.get("variation_statistics") or {}
            buy=vs.get("min_buy_price"); sell=vs.get("min_sell_price"); prof=vs.get("min_profit")
            stock=(vs.get("in_stock") or {}).get("total") if isinstance(vs.get("in_stock"),dict) else vs.get("in_stock")
            reg=vs.get("supplier_default_region") or vs.get("supplier_region")
            asin=""
            if isinstance(reg,list) and reg: asin=reg[0].get("item_id_on_site",""); regn=reg[0].get("region")
            else: regn=reg
            if pid: rows[pid]={"title":title,"buy":buy,"sell":sell,"profit":prof,"stock":stock,"reg":regn,"asin":asin}
    print("bodies:",len(bodies),"| drafts:",len(rows))
    # classify
    clean=[]
    for pid,r in rows.items():
        b_=r["buy"]; st=r["stock"]; rg=r["reg"]
        sentinel = (b_ is not None and abs(float(b_)-133.13)<0.5)
        ok = (rg==1) and (st and float(st)>0) and not sentinel
        tag = "CLEAN" if ok else ("SENT" if sentinel else ("OOS" if not st or float(st or 0)==0 else ("REG%s"%rg)))
        print("%-26s %-6s prof=%-7s stock=%-4s reg=%-3s %-12s | %s"%(pid,tag,r["profit"],st,rg,r["asin"],r["title"]))
        if ok: clean.append(pid)
    print("CLEAN_COUNT:",len(clean))
    print("CLEAN_IDS:",",".join(clean))
main()
