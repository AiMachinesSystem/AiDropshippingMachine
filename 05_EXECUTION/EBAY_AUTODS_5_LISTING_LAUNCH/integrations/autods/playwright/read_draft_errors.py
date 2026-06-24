#!/usr/bin/env python3
"""READ-ONLY: dump per-draft status + error_list (eBay error code/message) for all drafts.
Discriminates which drafts carry EbayViolation vs none. No writes. GO: GO_AUTODS_READ_SESSION."""
import os, re, json
from datetime import datetime
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
bodies=[]
def main():
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
        def cap(r):
            try:
                if "v2-api.autods.com/products/" in r.url and "/list/" in r.url and "json" in (r.headers or {}).get("content-type",""):
                    bodies.append(r.text())
            except Exception: pass
        pg.on("response", cap)
        pg.goto(BASE+"/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(9000)
        try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(3000)
        except Exception: pass
        pg.wait_for_timeout(2000)
        b.close()
    seen={}
    for body in bodies:
        try: data=json.loads(body)
        except Exception: continue
        for it in (data.get("results") or []):
            t=it.get("title","")[:50]
            if t in seen: continue
            el=it.get("error_list") or []
            codes=[e.get("error_code") for e in el]
            msg=(el[0].get("message","")[:70] if el else "")
            seen[t]={"status":it.get("status"),"pre":it.get("pre_draft_status"),"codes":codes,"msg":msg}
    print("captured bodies:",len(bodies),"| drafts:",len(seen))
    print("-"*100)
    for t,v in seen.items():
        print("status=%-3s pre=%-3s err=%-16s %s | %s"%(v["status"],v["pre"],",".join(c or "" for c in v["codes"]) or "-",t,v["msg"]))

if __name__=="__main__":
    main()
