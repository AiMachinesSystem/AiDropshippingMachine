#!/usr/bin/env python3
"""READ-ONLY: locate the duck draft's editable Title/Description fields + save mechanism. No edits."""
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    # try expand all
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception: pass
    info=pg.evaluate(r"""() => {
      // find the duck draft container by its title text
      const all=Array.from(document.querySelectorAll('*'));
      const titleEl=all.find(e=>/rubber duck/i.test(e.textContent||'') && (e.querySelector('input,textarea') || /title/i.test(e.textContent||'')) );
      // collect all text inputs/textareas + their current value + nearby label
      const fields=Array.from(document.querySelectorAll("input[type=text],textarea")).slice(0,30).map(i=>({
        tag:i.tagName, val:(i.value||'').slice(0,60), ph:(i.placeholder||''), maxlen:i.maxLength,
        near:(i.closest('[class]')?.className||'').slice(0,30)}));
      const saveBtns=Array.from(document.querySelectorAll('button')).map(b=>(b.innerText||'').trim()).filter(t=>/save|update|apply|done/i.test(t)).slice(0,8);
      return {fieldsCount:fields.length, fields, saveBtns:[...new Set(saveBtns)]};
    }""")
    print(json.dumps(info,ensure_ascii=False,indent=1)[:2200])
    b.close()
