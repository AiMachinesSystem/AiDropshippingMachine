#!/usr/bin/env python3
"""READ-ONLY: open the 'Shipping Methods' dropdown on the Book Light draft and list all options,
so we can pick the US-domestic service (type 4) that the 91 working live listings use. No save."""
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
ID="6a36f3e934ccb3112fdcf3a2"; URL=BASE+"/upload/"+ID+"&1"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
    # find the ant-select whose current text is 'Cheapest with tracking' and open it
    opened=pg.evaluate(r"""()=>{
      const items=[...document.querySelectorAll('.ant-select-selection-item')];
      const it=items.find(e=>/cheapest with tracking/i.test(e.innerText||''));
      if(!it) return 'no-control';
      let sel=it.closest('.ant-select'); if(!sel) return 'no-select-wrap';
      sel.scrollIntoView({block:'center'});
      const ctl=sel.querySelector('.ant-select-selector'); if(ctl){ctl.click(); return 'opened';}
      return 'no-selector';
    }""")
    print("open dropdown:", opened); pg.wait_for_timeout(3000)
    opts=pg.evaluate(r"""()=>{
      const sels=['.ant-select-item-option','[role=option]','.rc-virtual-list-holder-inner > div','.ant-select-item'];
      const out=new Set();
      for(const s of sels){ for(const o of document.querySelectorAll(s)){ const t=(o.innerText||'').trim(); if(t) out.add(t.slice(0,50)); } }
      return [...out];
    }""")
    print("OPTIONS:", json.dumps(opts, ensure_ascii=False, indent=1))
    b.close()
