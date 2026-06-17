#!/usr/bin/env python3
"""Diagnose the duck draft 'Import'(publish) flow: click it, dump modal/buttons/required-fields/toast. No blind confirm."""
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception: pass
    res=pg.evaluate(r"""() => {
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>/duck/i.test(i.value));
      if(!inp) return 'no-duck';
      let el=inp;
      for(let k=0;k<16 && el.parentElement;k++){ el=el.parentElement;
        const btn=[...el.querySelectorAll('button')].find(b=>/^\s*import\s*$/i.test(b.innerText||''));
        if(btn){ btn.scrollIntoView({block:'center'}); btn.click(); return 'clicked'; } }
      return 'no-import';
    }""")
    print("import click:",res); pg.wait_for_timeout(3500)
    dump=pg.evaluate(r"""() => {
      const m=document.querySelector("[role=dialog],.ant-modal,.ant-drawer");
      const toasts=[...new Set([...document.querySelectorAll('.ant-message,.ant-notification,[class*=toast i]')].map(e=>(e.innerText||'').trim()).filter(Boolean))].slice(0,8);
      const out={modal:!!m, toasts};
      if(m){
        out.modalText=(m.innerText||'').replace(/\s+/g,' ').slice(0,500);
        out.buttons=[...m.querySelectorAll('button')].map(b=>({t:(b.innerText||'').trim(),dis:b.disabled})).filter(x=>x.t).slice(0,12);
        out.requiredEmpty=[...m.querySelectorAll('input,select,textarea')].filter(i=>!i.value).map(i=>i.placeholder||i.name||'(empty field)').slice(0,10);
      }
      return out;
    }""")
    print(json.dumps(dump,ensure_ascii=False,indent=1)[:1800])
    b.close()
