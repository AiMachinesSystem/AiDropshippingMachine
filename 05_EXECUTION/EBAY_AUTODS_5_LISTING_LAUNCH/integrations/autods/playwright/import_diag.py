#!/usr/bin/env python3
"""Diagnose AutoDS Add-as-Draft import for one URL: capture preview/toast/error + screenshot. Add-as-Draft only."""
import os, re, json, sys
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
url=sys.argv[1] if len(sys.argv)>1 else "https://www.aliexpress.com/item/4000283772703.html"
shot=os.path.join(HERE,"..","..","..","..","..","90_CACHE","screenshots","autods","import_diag.png")
os.makedirs(os.path.dirname(shot),exist_ok=True)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(5000)
    pg.get_by_text(re.compile(r"^\s*Add product with link\s*$",re.I)).first.click(timeout=6000); pg.wait_for_timeout(1500)
    box=pg.get_by_placeholder(re.compile(r"Enter URL or Product ID",re.I)).first
    box.fill(url); pg.wait_for_timeout(2500)
    # state after fill (does a preview/validation appear? is the draft button enabled?)
    st1=pg.evaluate(r"""() => {
      const m=document.querySelector("[role=dialog],.ant-modal")||document.body;
      const btns=Array.from(m.querySelectorAll("button")).map(b=>({t:(b.innerText||'').trim(),dis:b.disabled})).filter(x=>x.t);
      return {modalText:(m.innerText||'').replace(/\s+/g,' ').slice(0,400), buttons:btns};
    }""")
    print("AFTER FILL:",json.dumps(st1,ensure_ascii=False)[:700])
    try:
        pg.get_by_role("button",name=re.compile(r"Add as Draft",re.I)).first.click(timeout=6000)
        print("clicked Add as Draft")
    except Exception as e:
        print("draft click err:",type(e).__name__)
    pg.wait_for_timeout(8000)
    st2=pg.evaluate(r"""() => {
      const toast=Array.from(document.querySelectorAll(".ant-message, .ant-notification, [class*='toast' i], [class*='error' i]")).map(e=>(e.innerText||'').trim()).filter(Boolean).slice(0,8);
      const m=document.querySelector("[role=dialog],.ant-modal");
      return {toasts:[...new Set(toast)], modalStillOpen:!!m, modalText: m?(m.innerText||'').replace(/\s+/g,' ').slice(0,400):'(closed)', bodyHasError:/(could not|unable|failed|not supported|invalid|error|verify|unusual)/i.test(document.body.innerText||'')};
    }""")
    print("AFTER SUBMIT:",json.dumps(st2,ensure_ascii=False)[:900])
    try: pg.screenshot(path=shot,full_page=False); print("shot:",shot)
    except Exception: pass
    b.close()
