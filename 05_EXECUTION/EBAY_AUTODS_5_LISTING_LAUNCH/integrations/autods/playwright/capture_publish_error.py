#!/usr/bin/env python3
"""INVESTIGATION: capture the FULL eBay/AutoDS import error, not just the toast.
On the Book Light dedicated page, hook all network responses, click Save & Import, and dump:
 - the import/publish API request URL + response BODY (real error code/detail)
 - the toast text + the 'Click to view' article href
 - the product's error_list / status from the products API
Saves raw bodies to cache. One item only. GO scope: owner 2026-06-22 'vedi l'errore su autods'.
"""
import os, re, json
from datetime import datetime
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
ID="6a36f3e934ccb3112fdcf3a2"; URL=BASE+"/upload/"+ID+"&1"
from playwright.sync_api import sync_playwright

root=HERE
while root and not os.path.isdir(os.path.join(root,"10_OUTPUTS")): root=os.path.dirname(root)
ts=datetime.now().strftime("%Y-%m-%d_%H%M%S")
cache=os.path.join(root,"90_CACHE","fetches","autods","publish_err_"+ts); os.makedirs(cache,exist_ok=True)

resp_log=[]
def main():
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
        def on_resp(r):
            try:
                u=r.url
                if "autods.com" in u and any(k in u.lower() for k in ["import","publish","upload","product","store","error","list"]):
                    ct=(r.headers or {}).get("content-type","")
                    body=""
                    if "json" in ct or "text" in ct:
                        try: body=r.text()
                        except Exception: body=""
                    resp_log.append({"status":r.status,"url":u,"ct":ct,"body":body[:4000]})
            except Exception: pass
        pg.on("response", on_resp)
        pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
        cur=pg.locator("input[placeholder='Title']").first.input_value()
        print("draft:", cur[:60])
        # trigger publish
        clicked=False
        for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*&\s*Import\s*$", re.I)),
                   lambda: pg.get_by_text(re.compile(r"^\s*Save\s*&\s*Import\s*$", re.I))]:
            try: mk().first.click(timeout=6000); clicked=True; break
            except Exception: pass
        print("Save&Import:", clicked); pg.wait_for_timeout(4000)
        for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*(Import|Publish|Confirm|Yes|OK)\s*$", re.I))]:
            try: mk().first.click(timeout=4000); break
            except Exception: pass
        pg.wait_for_timeout(9000)
        # toast + article link
        detail=pg.evaluate(r"""() => {
          const out={toasts:[],links:[]};
          for(const e of document.querySelectorAll('.ant-message,.ant-notification,.ant-notification-notice,[role=alert]')){
            const t=(e.innerText||'').trim(); if(t) out.toasts.push(t.replace(/\s+/g,' ').slice(0,500));
            for(const a of e.querySelectorAll('a')){ if(a.href) out.links.push(a.href); }
          }
          return out;
        }""")
        print("TOASTS:", json.dumps(detail["toasts"], ensure_ascii=False))
        print("ARTICLE LINKS:", json.dumps(detail["links"], ensure_ascii=False))
        b.close()
    # dump responses
    with open(os.path.join(cache,"responses.json"),"w",encoding="utf-8") as f:
        json.dump(resp_log,f,ensure_ascii=False,indent=1)
    print("="*80); print("captured responses:", len(resp_log), "| cache:", cache)
    # surface anything mentioning error / restriction / ebay
    for r in resp_log:
        bl=(r["body"] or "").lower()
        if any(k in bl for k in ["error","restrict","policy","violation","cannot","can not","limit","suspend"]) or r["status"]>=400:
            print("-"*70)
            print("STATUS",r["status"],r["url"][:90])
            print((r["body"] or "")[:1500])

if __name__=="__main__":
    main()
