#!/usr/bin/env python3
"""Set the draft's Country Location -> China + postal 518001 (match the real AliExpress origin, the
AutoDS-recommended fix for 'shipping service not available for this item location'), Save, then publish.
GO: owner 100% session GO 2026-06-22. Usage: set_location_and_publish.py <id> <guard> <publish:0|1>"""
import os, re, sys, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
DID=sys.argv[1]; GUARD=sys.argv[2].lower(); DO_PUB=(len(sys.argv)>3 and sys.argv[3]=="1")
URL=BASE+"/upload/"+DID+"&1"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1500,"height":1100}); pg=ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
    cur=pg.locator("input[placeholder='Title']").first.input_value()
    if GUARD not in cur.lower(): print("ABORT guard:",cur[:40]); b.close(); sys.exit(1)
    print("draft:",cur[:55])
    # 1) Country Location combobox -> China
    locset=False
    try:
        loc=pg.get_by_text(re.compile(r"^\s*United States\s*$"), exact=False).last
        loc.scroll_into_view_if_needed(timeout=4000); loc.click(timeout=4000); pg.wait_for_timeout(800)
        # type to filter
        try: pg.keyboard.type("China", delay=40)
        except Exception: pass
        pg.wait_for_timeout(1200)
        pg.locator(".ant-select-item-option, [role=option]").filter(has_text=re.compile(r"^China$", re.I)).first.click(timeout=4000); locset=True
    except Exception as e: print("loc err:",str(e)[:70])
    pg.wait_for_timeout(1000)
    # 2) postal code -> 518001
    postset=False
    try:
        pc=pg.locator("input").filter(has=None)
        # find input whose value is the current zip
        cand=pg.evaluate(r"""()=>{const i=[...document.querySelectorAll('input')].find(x=>/^\d{4,6}$/.test(x.value)&&x.value!==''); return i?i.value:null;}""")
        if cand:
            inp=pg.locator("input").filter().nth(0)
            # use JS to set the zip input reliably
            pg.evaluate(r"""()=>{const i=[...document.querySelectorAll('input')].find(x=>/^\d{4,6}$/.test(x.value)); if(i){const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set; setter.call(i,'518001'); i.dispatchEvent(new Event('input',{bubbles:true})); i.dispatchEvent(new Event('change',{bubbles:true}));}}""")
            postset=True
    except Exception as e: print("postal err:",str(e)[:70])
    print("location set China:",locset,"| postal 518001:",postset); pg.wait_for_timeout(800)
    # Save
    try: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); print("saved")
    except Exception: print("save fail")
    pg.wait_for_timeout(4000)
    if not DO_PUB: print("RESULT: LOCATION-SET (no publish)"); b.close(); sys.exit(0)
    # publish
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
    elif any(k in et for k in ["restrict","policy","violation","not available","item location","cannot","can not"]): print("RESULT: BLOCKED -", " | ".join(msgs)[:200])
    else: print("RESULT: UNCONFIRMED still-in-drafts msgs=",msgs)
    b.close()
