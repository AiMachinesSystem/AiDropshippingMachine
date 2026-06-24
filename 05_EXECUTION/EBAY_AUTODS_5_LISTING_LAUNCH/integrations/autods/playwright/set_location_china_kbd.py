#!/usr/bin/env python3
"""Set draft Country Location -> China via KEYBOARD (open combobox, type 'China', Enter) which is robust
vs the headless virtualized AntD dropdown that the click-the-option approach could not read. VERIFY the
change end-to-end via the products API (configuration.item_country_location flips to China) BEFORE any
publish (lesson E-008: AutoDS-saved != eBay-accepted; here we at least confirm the value persisted).
publish only runs if location verified == China. GO: owner 100% session GO 2026-06-23.

Usage: set_location_china_kbd.py <draft_id> <title_guard> <publish:0|1>
"""
import os, re, sys, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
DID=sys.argv[1]; GUARD=sys.argv[2].lower(); DO_PUB=(len(sys.argv)>3 and sys.argv[3]=="1")
URL=BASE+"/upload/"+DID+"&1"
from playwright.sync_api import sync_playwright

loc_val={"v":None}
def main():
    with sync_playwright() as p:
        HEADLESS = os.environ.get("HEADED","")!="1"
        b=p.chromium.launch(headless=HEADLESS); ctx=b.new_context(storage_state=STATE,viewport={"width":1500,"height":1100}); pg=ctx.new_page()
        def cap(r):
            try:
                if "v2-api.autods.com/products/" in r.url and "/list/" in r.url and "json" in (r.headers or {}).get("content-type",""):
                    data=json.loads(r.text())
                    for it in (data.get("results") or []):
                        if GUARD in (it.get("title","").lower()):
                            cfg=it.get("configuration") or {}
                            loc_val["v"]=cfg.get("item_country_location")
            except Exception: pass
        pg.on("response", cap)
        pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
        cur=pg.locator("input[placeholder='Title']").first.input_value()
        if GUARD not in cur.lower(): print("ABORT guard:",cur[:40]); b.close(); return
        print("draft:",cur[:55])
        # open Country Location combobox (the ant-select whose current item text is 'United States')
        opened=pg.evaluate(r"""()=>{
          const items=[...document.querySelectorAll('.ant-select-selection-item')];
          const it=items.find(e=>/united states/i.test(e.innerText||''));
          if(!it) return 'no-control';
          const sel=it.closest('.ant-select'); if(!sel) return 'no-wrap';
          sel.scrollIntoView({block:'center'});
          const ctl=sel.querySelector('.ant-select-selector'); if(ctl){ctl.click(); return 'opened';}
          return 'no-selector';
        }""")
        print("open country dd:",opened); pg.wait_for_timeout(1200)
        # type to filter, then CLICK the rendered option (fires AntD onChange so it persists; headed
        # renders the virtualized list reliably). Keyboard Enter is only a last-resort fallback.
        pg.keyboard.type("China", delay=60); pg.wait_for_timeout(1500)
        picked=False
        try:
            pg.locator(".ant-select-item-option, [role=option]").filter(has_text=re.compile(r"^\s*China\s*$", re.I)).first.click(timeout=5000); picked=True
        except Exception:
            try: pg.get_by_role("option", name=re.compile(r"^\s*China\s*$", re.I)).first.click(timeout=3000); picked=True
            except Exception: pass
        if not picked: pg.keyboard.press("Enter")
        print("clicked China option:", picked); pg.wait_for_timeout(900)
        seltext=pg.evaluate(r"""()=>{const items=[...document.querySelectorAll('.ant-select-selection-item')]; const it=items.find(e=>/china|united states/i.test(e.innerText||'')); return it?it.innerText.trim():null;}""")
        print("country selector now:",seltext)
        # Save
        try: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); print("saved")
        except Exception: print("save fail")
        pg.wait_for_timeout(4000)
        # verify via products API (reload upload list so the list/ call fires)
        loc_val["v"]=None
        pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
        pg.goto(BASE+"/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
        print("VERIFY item_country_location =",loc_val["v"],"(want China)")
        ok = bool(loc_val["v"]) and ("china" in str(loc_val["v"]).lower())
        if not ok:
            print("RESULT: LOCATION-NOT-SET (still",loc_val["v"],") - no publish"); b.close(); return
        if not DO_PUB:
            print("RESULT: LOCATION-SET-OK China (no publish requested)"); b.close(); return
        # publish from the dedicated single-draft page
        pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
        for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*&\s*Import\s*$", re.I)),
                   lambda: pg.get_by_text(re.compile(r"^\s*Save\s*&\s*Import\s*$", re.I))]:
            try: mk().first.click(timeout=6000); break
            except Exception: pass
        pg.wait_for_timeout(4000)
        for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*(Import|Publish|Confirm|Yes|OK)\s*$", re.I))]:
            try: mk().first.click(timeout=4000); break
            except Exception: pass
        pg.wait_for_timeout(9000)
        msgs=pg.evaluate(r"""()=>[...new Set([...document.querySelectorAll('.ant-message,.ant-notification,[role=alert]')].map(e=>(e.innerText||'').replace(/\s+/g,' ').trim()).filter(Boolean))].slice(0,6)""")
        print("MESSAGES:", json.dumps(msgs, ensure_ascii=False))
        pg.wait_for_timeout(11000)
        pg.goto(BASE+"/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
        still=pg.evaluate(r"""(g)=>!![...document.querySelectorAll("input[placeholder='Title']")].find(i=>i.value.toLowerCase().includes(g))""", GUARD)
        et=" ".join(msgs).lower()
        if not still: print("RESULT: PUBLISHED (left drafts)")
        elif any(k in et for k in ["restrict","policy","violation","not available","item location","cannot","can not"]): print("RESULT: BLOCKED -"," | ".join(msgs)[:200])
        else: print("RESULT: UNCONFIRMED still-in-drafts msgs=",json.dumps(msgs, ensure_ascii=False))
        b.close()
main()
