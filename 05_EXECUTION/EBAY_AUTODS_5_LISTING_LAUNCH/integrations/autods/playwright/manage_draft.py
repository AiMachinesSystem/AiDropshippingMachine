#!/usr/bin/env python3
"""manage_draft.py - single parametric CLI to manage AutoDS drafts end-to-end.

Consolidates: import_drafts.py, apply_titles_*.py, apply_desc_ckeditor_*.py,
discover_draft_ids.py, add_fabric_image_url.py.

SAFETY CONTRACT (do not weaken):
- Only ever clicks "Add as Draft" / "Save". NEVER clicks "Publish to Store" or "Save & Import".
- Title is hard-capped at 80 chars (refuses longer). Description is always set when provided.
- Reversible (draft edits only). No pricing/orders/publish. GO scope: drafts only.

Reuses the saved authenticated session (storage_state.json). Run with PYTHONIOENCODING=utf-8 on Windows.

Subcommands:
  status                                         show draft count
  import   --url URL [--dry]                     import a supplier URL as a DRAFT (default = real; --dry = no submit)
  find-id  --match REGEX                          print the dedicated /upload/<id> for the draft whose title matches
  set-title --match REGEX --title "T"            set title (<=80) on the draft whose CURRENT title matches REGEX
  set-desc  --id ID  (--desc-file F | --desc S)  set CKEditor description on the dedicated page of draft ID
  add-image --id ID  --image-url URL             add a custom image (via "Enter Image URL") on draft ID
  full     --url URL --match REGEX --title "T" (--desc-file F|--desc S) [--image-url URL] [--dry]
                                                 import -> set-title -> find-id -> set-desc -> add-image, with verify

Examples:
  python manage_draft.py status
  python manage_draft.py full --url https://www.amazon.com/dp/B0XXXX --match "dog bed|orthopedic" \
      --title "Orthopedic Dog Bed ..." --desc-file copy_dogbed.html --image-url https://.../main.png
"""
import os, re, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"


# ---------- shared playwright helpers ----------
def _expand_all(pg):
    try:
        pg.get_by_text(re.compile(r"^\s*Expand all\s*$", re.I)).first.click(timeout=4000); pg.wait_for_timeout(2500)
    except Exception:
        pass


def draft_count(pg):
    try:
        txt = pg.locator("body").inner_text(timeout=8000)
        m = re.search(r"Drafts\s*\(?\s*(\d+)\s*\)?", txt) or re.search(r"Upload\s*\(?\s*(\d+)\s*\)?", txt)
        return int(m.group(1)) if m else None
    except Exception:
        return None


def _titles(pg):
    out = []
    inputs = pg.locator("input[placeholder='Title']")
    for i in range(inputs.count()):
        try:
            out.append(inputs.nth(i).input_value())
        except Exception:
            pass
    return out


def _strip_tags(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


# ---------- operations (each takes a live page) ----------
def op_import(pg, url, dry):
    pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
    before = draft_count(pg); print("  drafts before:", before)
    pg.get_by_text(re.compile(r"^\s*Add product with link\s*$", re.I)).first.click(timeout=6000); pg.wait_for_timeout(1800)
    box = pg.get_by_placeholder(re.compile(r"Enter URL or Product ID", re.I)).first
    box.wait_for(state="visible", timeout=6000); box.fill(url); pg.wait_for_timeout(600)
    # SAFETY: only the draft button, never Publish
    draft_btn = pg.get_by_role("button", name=re.compile(r"Add as Draft", re.I)).first
    draft_btn.wait_for(state="visible", timeout=6000)
    if dry:
        print("  [DRY] filled, not submitted:", url); pg.keyboard.press("Escape"); pg.wait_for_timeout(600); return before, before
    draft_btn.click(timeout=6000); print("  [IMPORT] Add as Draft clicked:", url)
    pg.wait_for_timeout(18000)  # let AutoDS scrape + create the draft
    pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
    after = draft_count(pg); print("  drafts after:", after)
    return before, after


def op_set_title(pg, match, title):
    if len(title) > 80:
        print("  REFUSED: title is %d chars (>80): %s" % (len(title), title)); return False
    pat = re.compile(match, re.I)
    pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000); _expand_all(pg)
    inputs = pg.locator("input[placeholder='Title']"); fld = None; cur = None
    for i in range(inputs.count()):
        try:
            v = inputs.nth(i).input_value()
        except Exception:
            continue
        if v == title:
            print("  [skip] already applied"); return True
        if pat.search(v):
            fld = inputs.nth(i); cur = v; break
    if not fld:
        print("  [MISS] no draft title matches /%s/" % match); return False
    print("  match:", (cur or "")[:60])
    fld.scroll_into_view_if_needed(timeout=4000); fld.fill(title); pg.wait_for_timeout(800)
    res = pg.evaluate(r"""(nt)=>{const inp=[...document.querySelectorAll("input[placeholder='Title']")].find(i=>i.value===nt); if(!inp)return 'no-input'; let el=inp; for(let k=0;k<14&&el.parentElement;k++){el=el.parentElement; const btn=[...el.querySelectorAll('button')].find(b=>/^\s*save\s*$/i.test(b.innerText||'')); if(btn){btn.scrollIntoView({block:'center'});btn.click();return 'saved';}} return 'no-save';}""", title)
    print("  save:", res); pg.wait_for_timeout(4000)
    pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000); _expand_all(pg)
    ok = title in _titles(pg); print("  PERSISTED:", ok); return ok


def op_find_id(pg, match):
    pat = re.compile(match, re.I)
    pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(8000); _expand_all(pg)
    pairs = pg.evaluate(r"""() => {
      const out=[]; const inputs=[...document.querySelectorAll("input[placeholder='Title']")];
      for(const inp of inputs){ let el=inp, ref=null;
        for(let k=0;k<18&&el.parentElement;k++){el=el.parentElement; const a=el.querySelector("a[href*='/upload/']"); if(a){ref=a.getAttribute('href');break;}}
        out.push({title:inp.value, ref}); }
      return out;
    }""")
    for pr in pairs:
        if pat.search(pr["title"] or "") and pr["ref"]:
            rid = pr["ref"].split("/upload/")[-1]
            return rid, pr["title"]
    return None, None


def _click_desc_tab(pg):
    return pg.evaluate(r"""()=>{const e=[...document.querySelectorAll('.ant-tabs-tab,[role=tab]')].find(x=>/^\s*Description\s*$/i.test(x.innerText||'')); if(e){e.scrollIntoView({block:'center'});e.click();return true;}return false;}""")


def op_set_desc(pg, draft_id, html, guard=None):
    url = BASE + "/upload/" + draft_id + ("&1" if "&" not in draft_id else "")
    pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
    cur = pg.locator("input[placeholder='Title']").first.input_value()
    print("  draft:", cur[:55])
    if guard and guard.lower() not in cur.lower():
        print("  GUARD FAIL (expected '%s' in title) — aborting" % guard); return False
    print("  desc tab:", _click_desc_tab(pg)); pg.wait_for_timeout(3500)
    setres = pg.evaluate("""(h)=>{if(!window.CKEDITOR||!window.CKEDITOR.instances)return 'no-ckeditor';const ins=Object.values(window.CKEDITOR.instances);if(!ins.length)return 'no-instance';ins[0].setData(h);return 'set';}""", html)
    print("  setData:", setres); pg.wait_for_timeout(1500)
    if setres != "set":
        return False
    try:
        pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); print("  save: ok")
    except Exception as e:
        print("  save err:", type(e).__name__)
    pg.wait_for_timeout(3500)
    marker = _strip_tags(html)[:25].lower()
    pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000); _click_desc_tab(pg); pg.wait_for_timeout(4000)
    got = pg.evaluate("""()=>{if(!window.CKEDITOR||!window.CKEDITOR.instances)return '';const ins=Object.values(window.CKEDITOR.instances);return ins.length?ins[0].getData():'';}""")
    ok = marker in _strip_tags(got).lower(); print("  PERSISTED:", ok); return ok


def op_add_image(pg, draft_id, image_url):
    url = BASE + "/upload/" + draft_id + ("&1" if "&" not in draft_id else "")
    pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
    pg.evaluate(r"""()=>{const e=[...document.querySelectorAll('*')].find(x=>x.childElementCount<=1 && /^\s*Images\s*$/i.test(x.innerText||'')); if(e)e.click();}"""); pg.wait_for_timeout(2500)
    pg.evaluate(r"""()=>{const e=[...document.querySelectorAll('*')].find(x=>x.childElementCount<=1 && /^\s*Add Image\s*$/i.test(x.innerText||'')); if(e)e.click();}"""); pg.wait_for_timeout(1500)
    try:
        bx = pg.get_by_placeholder(re.compile(r"Enter Image URL", re.I)).first
        bx.wait_for(state="visible", timeout=6000); bx.fill(image_url); pg.wait_for_timeout(600)
    except Exception as e:
        print("  URL field err:", type(e).__name__); return False
    res = pg.evaluate(r"""()=>{const inp=[...document.querySelectorAll('input')].find(i=>/enter image url/i.test(i.placeholder||'')); if(!inp)return 'no-input'; let el=inp; for(let k=0;k<8&&el.parentElement;k++){el=el.parentElement; const btn=[...el.querySelectorAll('button')].find(b=>/^\s*(add|add image|ok|confirm|insert|apply|upload)\s*$/i.test(b.innerText||'')); if(btn){btn.scrollIntoView({block:'center'});btn.click();return 'clicked:'+btn.innerText.trim();}} inp.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true})); return 'enter';}""")
    print("  add-image:", res); pg.wait_for_timeout(6000)
    try:
        pg.get_by_role("button", name=re.compile(r"^\s*Save\s*$", re.I)).first.click(timeout=5000); print("  save: ok")
    except Exception:
        pass
    pg.wait_for_timeout(3500)
    needle = image_url.split("/")[-1][:20]
    pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
    pg.evaluate(r"""()=>{const e=[...document.querySelectorAll('*')].find(x=>x.childElementCount<=1 && /^\s*Images\s*$/i.test(x.innerText||'')); if(e)e.click();}"""); pg.wait_for_timeout(3000)
    present = pg.evaluate("""(n)=>[...document.querySelectorAll('img')].some(i=>(i.src||'').includes(n))""", needle)
    print("  image present:", present); return present


# ---------- CLI ----------
def _read_desc(args):
    if args.desc_file:
        with open(args.desc_file, "r", encoding="utf-8") as fh:
            return fh.read()
    return args.desc


def main():
    ap = argparse.ArgumentParser(description="Manage AutoDS drafts (import/title/description/image). Drafts only, never publish.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    pi = sub.add_parser("import"); pi.add_argument("--url", required=True); pi.add_argument("--dry", action="store_true")
    pf = sub.add_parser("find-id"); pf.add_argument("--match", required=True)
    pt = sub.add_parser("set-title"); pt.add_argument("--match", required=True); pt.add_argument("--title", required=True)
    pd = sub.add_parser("set-desc"); pd.add_argument("--id", required=True); pd.add_argument("--desc-file"); pd.add_argument("--desc"); pd.add_argument("--guard")
    pa = sub.add_parser("add-image"); pa.add_argument("--id", required=True); pa.add_argument("--image-url", required=True)
    pfu = sub.add_parser("full")
    pfu.add_argument("--url", required=True); pfu.add_argument("--match", required=True); pfu.add_argument("--title", required=True)
    pfu.add_argument("--desc-file"); pfu.add_argument("--desc"); pfu.add_argument("--image-url"); pfu.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    if args.cmd in ("set-title", "full") and len(args.title) > 80:
        print("REFUSED: title is %d chars (>80)." % len(args.title)); return 2
    if not os.path.exists(STATE):
        print("FAIL: storage_state.json not found - run login_and_save_session.py first."); return 3
    from playwright.sync_api import sync_playwright

    rc = 0
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1100})
        pg = ctx.new_page()
        if args.cmd == "status":
            pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(7000)
            print("drafts:", draft_count(pg))
        elif args.cmd == "import":
            op_import(pg, args.url, args.dry)
        elif args.cmd == "find-id":
            rid, t = op_find_id(pg, args.match)
            print("ID:", rid, "| title:", (t or "")[:60]) if rid else print("not found")
            rc = 0 if rid else 1
        elif args.cmd == "set-title":
            rc = 0 if op_set_title(pg, args.match, args.title) else 1
        elif args.cmd == "set-desc":
            rc = 0 if op_set_desc(pg, args.id, _read_desc(args), args.guard) else 1
        elif args.cmd == "add-image":
            rc = 0 if op_add_image(pg, args.id, args.image_url) else 1
        elif args.cmd == "full":
            print("== IMPORT =="); before, after = op_import(pg, args.url, args.dry)
            if args.dry:
                print("dry-run: stopping after import preview"); b.close(); return 0
            if after is not None and before is not None and after <= before:
                print("WARN: draft count did not increase - import may have failed; continuing to try title match")
            print("== SET TITLE =="); ok_t = op_set_title(pg, args.match, args.title)
            print("== FIND ID =="); rid, _ = op_find_id(pg, re.escape(args.title))
            print("  id:", rid)
            ok_d = ok_i = None
            desc = _read_desc(args)
            if rid and desc:
                print("== SET DESC =="); ok_d = op_set_desc(pg, rid, desc)
            if rid and args.image_url:
                print("== ADD IMAGE =="); ok_i = op_add_image(pg, rid, args.image_url)
            print("-" * 50)
            print("RESULT: title=%s id=%s desc=%s image=%s" % (ok_t, rid, ok_d, ok_i))
            rc = 0 if (ok_t and rid and (desc is None or ok_d)) else 1
        b.close()
    return rc


if __name__ == "__main__":
    sys.exit(main())
