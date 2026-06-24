#!/usr/bin/env python3
"""Set Shipping Method -> 'Fastest with tracking' (preferred_shipping_type=4, the one 91/99 working
live listings use) on a draft, Save, VERIFY it persisted (reads products API type==4), then optionally
publish. publish only runs if the shipping change verified. GO: owner 100% session GO 2026-06-22.

Usage: set_shipping_and_publish.py <draft_id> <title_guard> <publish:0|1>
"""
import os, re, sys, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
DID=sys.argv[1]; GUARD=sys.argv[2].lower(); DO_PUB=(len(sys.argv)>3 and sys.argv[3]=="1")
URL=BASE+"/upload/"+DID+"&1"
from playwright.sync_api import sync_playwright

ship_type={"val":None}
def main():
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1500,"height":1100}); pg=ctx.new_page()
        def cap(r):
            try:
                if "v2-api.autods.com/products/" in r.url and "/list/" in r.url and "json" in (r.headers or {}).get("content-type",""):
                    data=json.loads(r.text())
                    for it in (data.get("results") or []):
                        if GUARD in (it.get("title","").lower()):
                            cfg=it.get("configuration") or {}
                            ship_type["val"]=cfg.get("preferred_shipping_type")
            except Exception: pass
        pg.on("response", cap)
        pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
        cur=pg.locator("input[placeholder='Title']").first.input_value()
        if GUARD not in cur.lower(): print("ABORT guard:",cur[:40]); b.close(); return
        print("draft:",cur[:55])
        # open shipping dropdown (the ant-select currently showing a shipping method)
        opened=False
        try:
            pg.get_by_text(re.compile(r"^\s*(Cheapest with tracking|Cheapest|Fastest with tracking)\s*$", re.I)).first.scroll_into_view_if_needed(timeout=4000)
            pg.get_by_text(re.compile(r"^\s*(Cheapest with tracking|Cheapest|Fastest with tracking)\s*$", re.I)).first.click(timeout=5000); opened=True
        except Exception as e: print("open dd err:",str(e)[:60])
        pg.wait_for_timeout(1500)
        # click the 'Fastest with tracking' option in the open dropdown
        picked=False
        try:
            pg.locator(".ant-select-item-option, [role=option]").filter(has_text=re.compile(r"Fastest with tracking", re.I)).first.click(timeout=5000); picked=True
        except Exception as e:
            # fallback: any visible element exactly 'Fastest with tracking'
            try: pg.get_by_text(re.compile(r"^\s*Fastest with tracking\s*$", re.I)).last.click(timeout=4000); picked=True
            except Exception as e2: print("pick err:",str(e2)[:60])
        print("opened dd:",opened,"| picked Fastest:",picked); pg.wait_for_timeout(1200)
        # Save
        saved=False
        try: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); saved=True
        except Exception: pass
        print("saved:",saved); pg.wait_for_timeout(4000)
        # reload + verify via API capture
        ship_type["val"]=None
        pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
        pg.goto(BASE+"/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
        print("VERIFY preferred_shipping_type =", ship_type["val"], "(want 4)")
        if ship_type["val"]!=4:
            print("RESULT: SHIPPING-NOT-SET (still", ship_type["val"],") - no publish"); b.close(); return
        if not DO_PUB:
            print("RESULT: SHIPPING-SET-OK type=4 (no publish requested)"); b.close(); return
        # publish from dedicated page
        pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
        clicked=False
        for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*&\s*Import\s*$", re.I)),
                   lambda: pg.get_by_text(re.compile(r"^\s*Save\s*&\s*Import\s*$", re.I))]:
            try: mk().first.click(timeout=6000); clicked=True; break
            except Exception: pass
        print("Save&Import:",clicked); pg.wait_for_timeout(4000)
        for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*(Import|Publish|Confirm|Yes|OK)\s*$", re.I))]:
            try: mk().first.click(timeout=4000); break
            except Exception: pass
        pg.wait_for_timeout(8000)
        msgs=pg.evaluate(r"""()=>[...new Set([...document.querySelectorAll('.ant-message,.ant-notification,[role=alert]')].map(e=>(e.innerText||'').replace(/\s+/g,' ').trim()).filter(Boolean))].slice(0,6)""")
        print("MESSAGES:", json.dumps(msgs, ensure_ascii=False))
        pg.wait_for_timeout(12000)
        pg.goto(BASE+"/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
        still=pg.evaluate(r"""(g)=>!![...document.querySelectorAll("input[placeholder='Title']")].find(i=>i.value.toLowerCase().includes(g))""", GUARD)
        et=" ".join(msgs).lower()
        if not still: print("RESULT: PUBLISHED (left drafts)")
        elif any(k in et for k in ["restrict","policy","violation","cannot","can not","not available","item location"]): print("RESULT: BLOCKED -", " | ".join(msgs)[:200])
        else: print("RESULT: UNCONFIRMED still-in-drafts")
        b.close()
main()
