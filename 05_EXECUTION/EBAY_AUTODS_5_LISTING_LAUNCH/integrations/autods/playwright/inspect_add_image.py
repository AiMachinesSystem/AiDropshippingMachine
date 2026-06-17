#!/usr/bin/env python3
"""READ-ONLY: click 'Add Image' on the duck draft Images tab and dump the upload UI (file input / URL / options)."""
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception: pass
    # open duck Images tab
    pg.evaluate(r"""() => {
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>/duck/i.test(i.value));
      let el=inp; for(let k=0;k<16&&el.parentElement;k++){el=el.parentElement;
        const t=[...el.querySelectorAll('*')].find(e=>e.childElementCount<=1&&/^\s*Images\s*$/i.test(e.innerText||''));
        if(t){t.click();return;}}
    }"""); pg.wait_for_timeout(2000)
    # click 'Add Image' scoped to duck card
    res=pg.evaluate(r"""() => {
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>/duck/i.test(i.value));
      let el=inp; for(let k=0;k<16&&el.parentElement;k++){el=el.parentElement;
        const t=[...el.querySelectorAll('*')].find(e=>e.childElementCount<=1&&/^\s*Add Image\s*$/i.test(e.innerText||''));
        if(t){t.scrollIntoView({block:'center'});t.click();return 'clicked Add Image';}}
      return 'no-add-image';
    }""")
    print("Add Image:", res); pg.wait_for_timeout(2500)
    dump=pg.evaluate(r"""() => {
      const fi=[...document.querySelectorAll("input[type=file]")];
      const m=document.querySelector("[role=dialog],.ant-modal,.ant-dropdown,.ant-popover");
      return {
        fileInputs: fi.length,
        fileAccepts: fi.map(i=>i.accept||'(any)').slice(0,4),
        menu: m? (m.innerText||'').replace(/\s+/g,' ').slice(0,300):'(no modal/dropdown)',
        menuItems: m? [...m.querySelectorAll('*')].filter(e=>e.childElementCount<=1).map(e=>(e.innerText||'').trim()).filter(t=>t&&t.length<40 && /upload|url|computer|file|browse|marketplace|link|device/i.test(t)).slice(0,10) : []
      };
    }""")
    print("after Add Image:", json.dumps(dump,ensure_ascii=False)[:800])
    b.close()
