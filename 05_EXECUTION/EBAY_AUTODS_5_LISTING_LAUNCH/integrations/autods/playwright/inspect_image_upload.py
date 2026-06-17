#!/usr/bin/env python3
"""READ-ONLY deep probe for ANY custom-image-upload path on the duck draft (file inputs incl hidden, upload/replace/URL
buttons, drag zones, image-click editor). No uploads performed."""
import os, re, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(BASE+"/upload",wait_until="domcontentloaded",timeout=60000); pg.wait_for_timeout(7000)
    try: pg.get_by_text(re.compile(r"^\s*Expand all\s*$",re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception: pass
    # click duck Images tab (scoped to duck card)
    print("open duck Images tab:", pg.evaluate(r"""() => {
      const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>/duck/i.test(i.value));
      if(!inp) return 'no-duck'; let el=inp;
      for(let k=0;k<16&&el.parentElement;k++){el=el.parentElement;
        const t=[...el.querySelectorAll('*')].find(e=>e.childElementCount<=1&&/^\s*Images\s*$/i.test(e.innerText||''));
        if(t){t.scrollIntoView({block:'center'});t.click();return 'clicked';}}
      return 'no-tab';
    }"""))
    pg.wait_for_timeout(2500)
    probe=pg.evaluate(r"""() => {
      const all=[...document.querySelectorAll('*')];
      const fileInputs=document.querySelectorAll("input[type=file]").length;
      const fileInputsHidden=[...document.querySelectorAll("input[type=file]")].map(i=>({acc:i.accept||'',disp:getComputedStyle(i).display}));
      const txtHits=[...new Set(all.filter(e=>e.childElementCount<=2).map(e=>(e.innerText||'').trim()).filter(t=>t && t.length<40 && /upload|add image|replace|edit image|image url|from url|drag|drop|browse|\+ add|advanced|edit listing/i.test(t)))].slice(0,20);
      const dropZones=document.querySelectorAll("[class*='drop' i],[class*='upload' i],[class*='dropzone' i]").length;
      const urlInputs=[...document.querySelectorAll('input')].map(i=>i.placeholder||'').filter(ph=>/url|image link/i.test(ph)).slice(0,6);
      const imgs=document.querySelectorAll("img").length;
      return {fileInputs,fileInputsHidden:fileInputsHidden.slice(0,5),dropZones,urlInputs,textHits:txtHits,imgCount:imgs};
    }""")
    print("IMAGES-tab probe:", json.dumps(probe,ensure_ascii=False)[:900])
    # try clicking the first product image in the duck card to see if an editor/replace modal opens
    try:
        opened=pg.evaluate(r"""() => {
          const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>/duck/i.test(i.value));
          let el=inp; for(let k=0;k<16&&el.parentElement;k++){el=el.parentElement;
            const img=el.querySelector("img[src*='ebayimg'],img[src*='alicdn'],img[src*='aliexpress'],img[src*='media-amazon'],img[src]");
            if(img){img.scrollIntoView({block:'center'});img.click();return 'clicked-img:'+(img.src||'').slice(0,50);}}
          return 'no-img';
        }""")
        print("click image:", opened); pg.wait_for_timeout(2500)
        modal=pg.evaluate(r"""() => {const m=document.querySelector("[role=dialog],.ant-modal");
          if(!m) return {modal:false, fileInputs:document.querySelectorAll('input[type=file]').length};
          return {modal:true, text:(m.innerText||'').replace(/\s+/g,' ').slice(0,300),
            buttons:[...m.querySelectorAll('button')].map(b=>(b.innerText||'').trim()).filter(Boolean).slice(0,12),
            fileInputs:m.querySelectorAll('input[type=file]').length};}""")
        print("image-click modal:", json.dumps(modal,ensure_ascii=False)[:700])
    except Exception as e:
        print("image click err:", type(e).__name__)
    b.close()
