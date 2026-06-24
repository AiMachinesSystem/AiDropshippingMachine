#!/usr/bin/env python3
"""READ-ONLY: capture the AutoDS drafts list API JSON and print per-draft economics
(title, buy/sell price, profit, stock, supplier region) so the publish cost-gate (E-003)
runs on real data. No writes, no publish. GO scope: GO_AUTODS_READ_SESSION."""
import os, re, json, time
from datetime import datetime
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright

bodies=[]
def main():
    root=HERE
    while root and not os.path.isdir(os.path.join(root,"10_OUTPUTS")):
        root=os.path.dirname(root)
    ts=datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache=os.path.join(root,"90_CACHE","fetches","autods","draft_econ_"+ts); os.makedirs(cache,exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
        def cap(r):
            try:
                if "v2-api.autods.com/products/" in r.url and "/list/" in r.url and "application/json" in (r.headers or {}).get("content-type",""):
                    bodies.append((r.url, r.text()))
            except Exception: pass
        pg.on("response", cap)
        pg.goto(BASE+"/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(9000)
        try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(3000)
        except Exception: pass
        pg.wait_for_timeout(3000)
        b.close()
    # save + parse
    rows={}
    for i,(url,body) in enumerate(bodies):
        with open(os.path.join(cache,"list_%02d.json"%i),"w",encoding="utf-8") as f: f.write(body)
        try: data=json.loads(body)
        except Exception: continue
        items = data.get("results") or data.get("data") or (data if isinstance(data,list) else [])
        if isinstance(items,dict): items=items.get("results",[])
        for it in (items or []):
            if not isinstance(it,dict): continue
            pid=str(it.get("id") or it.get("_id") or "")
            title=(it.get("title") or "")[:60]
            vs=it.get("variation_statistics") or {}
            buy=vs.get("min_buy_price"); sell=vs.get("min_sell_price"); prof=vs.get("min_profit")
            stock=vs.get("in_stock"); region=vs.get("supplier_default_region") or vs.get("supplier_region")
            if pid: rows[pid]={"title":title,"buy":buy,"sell":sell,"profit":prof,"stock":stock,"region":region}
    print("captured list bodies:",len(bodies),"| parsed drafts:",len(rows),"| cache:",cache)
    print("-"*90)
    for pid,r in rows.items():
        print("%-26s buy=%-8s sell=%-8s profit=%-7s stock=%-5s reg=%-4s | %s" % (
            pid, r["buy"], r["sell"], r["profit"], r["stock"], r["region"], r["title"]))

if __name__=="__main__":
    main()
