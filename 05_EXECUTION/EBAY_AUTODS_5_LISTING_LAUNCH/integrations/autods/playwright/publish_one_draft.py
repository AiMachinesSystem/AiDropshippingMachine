#!/usr/bin/env python3
"""Publish ONE draft from its dedicated single-draft page (/upload/<id>&1) = no cross-draft risk (E-002).
Pre-flight: verify title<=80 and title matches the expected guard substring. Then click Save & Import,
wait, and CAPTURE the eBay response (success = left drafts; failure = policy/restriction toast/modal text).
Prints a machine-readable RESULT line. One draft per run so we stop on the first eBay restriction (does not
hammer a restricted account). GO scope: owner GO 2026-06-22 'PUBBLICA 5 PRODOTTI'.

Usage: publish_one_draft.py <draft_id> <title_guard_substring>
"""
import os, re, sys, json
HERE=os.path.dirname(os.path.abspath(__file__)); STATE=os.path.join(HERE,"storage_state.json"); BASE="https://platform.autods.com"
from playwright.sync_api import sync_playwright

DRAFT_ID=sys.argv[1]; GUARD=sys.argv[2].lower()
URL=BASE+"/upload/"+DRAFT_ID+"&1"

def grab_msgs(pg):
    return pg.evaluate(r"""() => {
      const sels=['.ant-message','.ant-notification','.ant-notification-notice','[class*=toast i]','[role=alert]'];
      const out=new Set();
      for(const s of sels){ for(const e of document.querySelectorAll(s)){ const t=(e.innerText||'').trim(); if(t) out.add(t.replace(/\s+/g,' ').slice(0,400)); } }
      const m=document.querySelector('[role=dialog],.ant-modal-body');
      if(m){ const t=(m.innerText||'').trim(); if(t) out.add('MODAL: '+t.replace(/\s+/g,' ').slice(0,400)); }
      return [...out].slice(0,10);
    }""")

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); ctx=b.new_context(storage_state=STATE,viewport={"width":1440,"height":1000}); pg=ctx.new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000)
    ti=pg.locator("input[placeholder='Title']").first
    try: cur=ti.input_value()
    except Exception:
        print("RESULT: ABORT no-title-input"); b.close(); sys.exit(1)
    print("draft title:", cur[:75], "| len", len(cur))
    if GUARD not in cur.lower():
        print("RESULT: ABORT guard-mismatch (expected '%s')"%GUARD); b.close(); sys.exit(1)
    if len(cur)>80:
        print("RESULT: ABORT title-over-80 len=%d"%len(cur)); b.close(); sys.exit(1)

    # PUBLISH via Save & Import on this single-draft page
    clicked=False
    for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*Save\s*&\s*Import\s*$", re.I)),
               lambda: pg.get_by_text(re.compile(r"^\s*Save\s*&\s*Import\s*$", re.I)),
               lambda: pg.get_by_role("button", name=re.compile(r"^\s*Import\s*$", re.I))]:
        try: mk().first.click(timeout=6000); clicked=True; break
        except Exception: pass
    print("Save&Import clicked:", clicked); pg.wait_for_timeout(3500)
    # confirm dialog if present
    for mk in [lambda: pg.get_by_role("button", name=re.compile(r"^\s*(Import|Publish|Confirm|Yes|OK)\s*$", re.I))]:
        try: mk().first.click(timeout=4000); print("confirmed dialog"); break
        except Exception: pass
    pg.wait_for_timeout(6000)
    msgs=grab_msgs(pg)
    print("MESSAGES:", json.dumps(msgs, ensure_ascii=False))
    pg.wait_for_timeout(16000)

    # VERIFY via the PAGINATED products/list API, never via the visible UI page (E-027):
    # with 2000+ drafts an item absent from the first page is NOT proof of publish.
    # If it is still a draft, its error_list carries the REAL eBay error (the toast is usually gone).
    cap={}
    pg.on("request", lambda r: cap.update({"url":r.url,"headers":dict(r.headers),"body":r.post_data})
          if ("/products/" in r.url and "/list/" in r.url and r.method=="POST" and not cap) else None)
    pg.goto(BASE+"/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(9000)
    item=None; scanned=False
    if cap:
        hdr={k:v for k,v in cap["headers"].items()
             if k.lower() in ("authorization","content-type","accept","origin","referer")}
        body=json.loads(cap["body"]); scanned=True
        for off in range(0,3000,300):
            body["limit"]=300; body["offset"]=off
            try: data=pg.request.post(cap["url"], data=json.dumps(body), headers=hdr).json()
            except Exception: scanned=False; break
            items=data.get("results") or []
            if isinstance(items,dict): items=items.get("results",[])
            if not items: break
            for it in items:
                if str(it.get("id"))==DRAFT_ID: item=it; break
            if item or len(items)<300: break
    errs=(item or {}).get("error_list") or []
    err_text=(" ".join(msgs)+" "+" ".join(e.get("message","") for e in errs)).lower()
    restricted = ("restriction on your ebay account" in err_text or "selling policy" in err_text
                  or "cannot be listed" in err_text or "can not be listed" in err_text)
    if not scanned:
        print("RESULT: UNVERIFIED (products/list API not captured — do NOT count as published)")
    elif item is None:
        print("RESULT: PUBLISHED (id no longer in drafts, API-verified)")
    elif restricted:
        print("RESULT: BLOCKED-EBAY-RESTRICTION | %s" % json.dumps(errs, ensure_ascii=False)[:300])
    else:
        print("RESULT: NOT-PUBLISHED (still a draft) | %s" % (json.dumps(errs, ensure_ascii=False)[:300] or "no error_list"))
    b.close()
