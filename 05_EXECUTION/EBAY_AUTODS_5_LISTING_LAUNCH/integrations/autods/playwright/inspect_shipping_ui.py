#!/usr/bin/env python3
"""READ-ONLY inspection: on the Book Light dedicated draft page, find the tabs and the shipping /
business-policy controls (selects, radios, dropdowns) so we can change preferred_shipping_type 2->4.
Dumps tab labels + any select/combobox text near 'shipping'/'policy'/'business'. No writes."""
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
ID="6a36f3e934ccb3112fdcf3a2"; URL=BASE+"/upload/"+ID+"&1"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
    tabs=pg.evaluate(r"""()=>[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].map(e=>(e.innerText||'').trim()).filter(Boolean)""")
    print("TABS:", json.dumps(tabs, ensure_ascii=False))
    # click any tab mentioning shipping/policy/business
    target=pg.evaluate(r"""()=>{const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/(ship|polic|business)/i.test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return (e.innerText||'').trim();} return null;}""")
    print("clicked tab:", target); pg.wait_for_timeout(3500)
    dump=pg.evaluate(r"""()=>{
      const out={selects:[],radios:[],labels:[],comboTexts:[]};
      for(const s of document.querySelectorAll('select')){ out.selects.push({name:s.name||'', val:s.value, opts:[...s.options].map(o=>o.text).slice(0,12)}); }
      for(const r of document.querySelectorAll('input[type=radio]')){ const lab=r.closest('label'); out.radios.push({checked:r.checked, lab:(lab?lab.innerText:'').slice(0,40)}); }
      for(const l of document.querySelectorAll('label,.ant-form-item-label')){ const t=(l.innerText||'').trim(); if(/ship|polic|business|location|handling|deliver/i.test(t)) out.labels.push(t.slice(0,60)); }
      for(const c of document.querySelectorAll('.ant-select-selector,.ant-select-selection-item')){ const t=(c.innerText||'').trim(); if(t) out.comboTexts.push(t.slice(0,60)); }
      return out;
    }""")
    print(json.dumps(dump, ensure_ascii=False, indent=1)[:2500])
    b.close()
