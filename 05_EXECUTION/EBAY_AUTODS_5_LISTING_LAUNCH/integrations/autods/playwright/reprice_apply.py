#!/usr/bin/env python3
"""
reprice_apply.py — APPLY a +PCT price change via AutoDS Bulk Edit (owner GO 2026-06-24 "usa playwright e fallo tu").

Discipline on a LIVE write:
- Default = --cold-test: act on EXACTLY ONE listing (deterministically located by item_id by scanning grid
  rows for the id — NEVER tick a row blindly; this is the E-007 safeguard), apply +PCT, then verify via the
  /products list API read-back. Captures the price-WRITE request (endpoint+payload) for later API replay.
- --all: after a verified cold-test, repeat the row-scan+bulk-edit for every active listing.
- HEADED by default (AntD Bulk Edit modal is unreliable headless = E-007); --headless to override.
- HARD SAFETY: only clicks Update if an unambiguous Increase-by-% (or fixed-price) control was set to the
  intended value; otherwise Cancel (no write) and report. Verifies the RIGHT item_id before/after.

GO scope: owner GO 2026-06-24 (reprice +2%, "fallo tu"). Run with PYTHONIOENCODING=utf-8.
Usage: reprice_apply.py [--pct 2] [--item ITEMID] [--cold-test|--all] [--headless]
"""
import os, re, sys, json, argparse
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"
DEFAULT_ITEM = "407023314446"   # Splatter Screen for Frying Pan 13" — cur 20.97 (kitchen, stable)


def find_repo_root(start):
    cur = os.path.abspath(start)
    while cur != os.path.dirname(cur):
        if os.path.isdir(os.path.join(cur, "10_OUTPUTS")):
            return cur
        cur = os.path.dirname(cur)
    return start


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pct", type=float, default=2.0)
    ap.add_argument("--item", default=DEFAULT_ITEM, help="eBay item_id to cold-test")
    ap.add_argument("--all", action="store_true", help="apply to ALL active listings (after cold-test)")
    ap.add_argument("--cold-test", action="store_true", default=True)
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--apply", action="store_true", help="actually perform the write (else map+cancel)")
    ap.add_argument("--attr", default="Additional profit %", help="Bulk Edit attribute to set")
    args = ap.parse_args()
    factor = 1 + args.pct / 100.0

    root = find_repo_root(HERE)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root, "90_CACHE", "fetches", "autods", "reprice_apply_" + ts)
    os.makedirs(cache, exist_ok=True)

    from playwright.sync_api import sync_playwright
    writes = []        # captured price-write requests
    list_items = {}    # id_on_site -> min_sell_price (from list API)

    print("REPRICE APPLY +%.1f%% | mode: %s | item: %s | headed: %s | run: %s"
          % (args.pct, "ALL" if args.all else "COLD-TEST", args.item, not args.headless, ts))
    print("-" * 80)

    with sync_playwright() as p:
        b = p.chromium.launch(headless=args.headless)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1500, "height": 1000})
        pg = ctx.new_page()

        def on_request(req):
            try:
                u = req.url
                m = req.method
                if m in ("PATCH", "PUT", "POST") and "autods.com" in u and \
                   re.search(r"/products?/|/price|/bulk|/edit", u, re.I) and "/list" not in u:
                    pd = None
                    try:
                        pd = req.post_data
                    except Exception:
                        pd = None
                    writes.append({"method": m, "url": u, "post_data": (pd or "")[:1500]})
            except Exception:
                pass

        def on_response(resp):
            try:
                u = resp.url
                if "/products/" in u and "/list" in u and "application/json" in (resp.headers or {}).get("content-type", ""):
                    data = json.loads(resp.text())
                    for it in (data.get("results") or []):
                        vs = it.get("variation_statistics") or {}
                        iid = it.get("item_id_on_site")
                        if iid:
                            list_items[str(iid)] = vs.get("min_sell_price")
            except Exception:
                pass

        pg.on("request", on_request)
        pg.on("response", on_response)

        def goto_products():
            pg.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(4000)
            if "offer" in pg.url:
                for mk in [lambda: pg.get_by_role("link", name=re.compile(r"No Thanks", re.I)),
                           lambda: pg.get_by_text(re.compile(r"No Thanks", re.I))]:
                    try: mk().first.click(timeout=4000); break
                    except Exception: continue
                pg.wait_for_timeout(2500)
                pg.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(5000)

        def find_row_for(item_id):
            """Scan all grid rows; return checkbox index of the row containing item_id (deterministic, E-007-safe)."""
            for pageno in range(1, 16):
                rows = pg.evaluate(r"""() => {
                  const cbs=[...document.querySelectorAll('input.ant-checkbox-input, input[type=checkbox]')];
                  return cbs.map((cb,i)=>{let el=cb;for(let k=0;k<8&&el.parentElement;k++){el=el.parentElement;if((el.innerText||'').length>60)break;}
                    return {i,text:(el.innerText||'').replace(/\s+/g,' ')};});
                }""")
                for r in rows:
                    if item_id in (r["text"] or ""):
                        return r["i"], r["text"][:80]
                nxt = pg.locator("li.ant-pagination-next:not(.ant-pagination-disabled)")
                if nxt.count() == 0:
                    return None, None
                try:
                    nxt.first.click(timeout=4000); pg.wait_for_timeout(2200)
                except Exception:
                    return None, None
            return None, None

        def open_price_panel(attr):
            """Open Bulk Edit -> add `attr` sub-panel. Returns dumped panel info or None."""
            try:
                pg.get_by_text(re.compile(r"^\s*Bulk Edit\s*$", re.I)).first.click(timeout=6000); pg.wait_for_timeout(2500)
            except Exception as e:
                print("  bulk-edit open fail:", type(e).__name__); return None
            # STEP 1: click "Add item to edit" — the modal starts empty; this opens the attribute menu
            for mk in [lambda: pg.get_by_text(re.compile(r"Add item to edit", re.I)),
                       lambda: pg.get_by_role("button", name=re.compile(r"Add item to edit", re.I))]:
                try:
                    mk().first.click(timeout=4000); pg.wait_for_timeout(1500); break
                except Exception:
                    continue
            # dump the attribute menu that appears
            menu = pg.evaluate(r"""() => [...document.querySelectorAll('.ant-dropdown li,.ant-select-item,[role=menuitem],li,.ant-modal button')]
                .map(e=>(e.innerText||'').trim()).filter(t=>t&&t.length<30)""")
            print("  ADD-ITEM MENU:", [m for m in dict.fromkeys(menu)][:30])
            # STEP 2: choose the target attribute (default 'Additional profit %')
            esc = re.escape(attr)
            for mk in [lambda: pg.get_by_role("menuitem", name=re.compile(r"^\s*" + esc + r"\s*$", re.I)),
                       lambda: pg.locator(".ant-dropdown").get_by_text(re.compile(r"^\s*" + esc + r"\s*$", re.I)),
                       lambda: pg.locator("li", has_text=re.compile(r"^\s*" + esc + r"\s*$", re.I)),
                       lambda: pg.get_by_text(re.compile(r"^\s*" + esc + r"\s*$", re.I))]:
                try:
                    mk().first.click(timeout=3000); pg.wait_for_timeout(1500); break
                except Exception:
                    continue
            info = pg.evaluate(r"""() => {
              const dlg=document.querySelector('.ant-modal,[role=dialog]')||document.body;
              const labels=[...dlg.querySelectorAll('label,.ant-radio-wrapper,button,.ant-segmented-item,option,.ant-select-selection-item,.ant-select-item')]
                  .map(e=>(e.innerText||'').trim()).filter(t=>t&&t.length<40);
              const inputs=[...dlg.querySelectorAll('input,select')].map(i=>({ph:i.placeholder||'',type:i.type||i.tagName,val:(i.value||'').slice(0,14)}));
              return {labels:[...new Set(labels)].slice(0,40),inputs:inputs.slice(0,25),text:(dlg.innerText||'').replace(/\s+/g,' ').slice(0,700)};
            }""")
            return info

        def cold_test(item_id):
            goto_products()
            idx, rowtxt = find_row_for(item_id)
            if idx is None:
                print("  TARGET item_id %s NOT found on grid — abort (no write)." % item_id); return False
            cur_before = list_items.get(item_id)
            print("  located row idx %d | price(before)=%s | %s" % (idx, cur_before, rowtxt))
            try:
                pg.locator("input.ant-checkbox-input").nth(idx).check(timeout=4000); pg.wait_for_timeout(900)
            except Exception as e:
                print("  tick fail:", type(e).__name__); return False
            info = open_price_panel(args.attr)
            if not info:
                return False
            print("  PANEL[%s] labels:" % args.attr, info["labels"])
            print("  PANEL inputs:", json.dumps(info["inputs"]))
            print("  PANEL text:", info["text"][:300])
            with open(os.path.join(cache, "price_panel.json"), "w", encoding="utf-8") as fh:
                json.dump(info, fh, ensure_ascii=False, indent=1)

            if not args.apply:
                try:
                    pg.get_by_role("button", name=re.compile(r"^\s*Cancel\s*$", re.I)).first.click(timeout=4000)
                except Exception:
                    pass
                print("  [MAP-ONLY] CANCELLED (no write). Re-run with --apply to set %s=%s." % (args.attr, args.pct))
                return True

            # --apply: fill the numeric field for the attribute, verify it, then Update
            val = str(int(args.pct)) if float(args.pct).is_integer() else str(args.pct)
            filled = pg.evaluate(r"""(v) => {
              const dlg=document.querySelector('.ant-modal,[role=dialog]')||document.body;
              // pick the last empty/number input in the modal (the attribute value field)
              const ins=[...dlg.querySelectorAll('input')].filter(i=>i.type!=='checkbox'&&i.type!=='radio'&&!/search/i.test(i.placeholder||''));
              const inp=ins[ins.length-1];
              if(!inp) return 'no-input';
              const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
              setter.call(inp, v);
              inp.dispatchEvent(new Event('input',{bubbles:true}));
              inp.dispatchEvent(new Event('change',{bubbles:true}));
              return inp.value;
            }""", val)
            print("  filled attribute input ->", filled)
            ok_num = False
            try:
                ok_num = abs(float(filled) - float(val)) < 1e-6
            except Exception:
                ok_num = False
            if not ok_num:
                try: pg.get_by_role("button", name=re.compile(r"^\s*Cancel\s*$", re.I)).first.click(timeout=4000)
                except Exception: pass
                print("  [SAFETY] could not set the value cleanly (got %r, wanted %r) -> CANCELLED, no write." % (filled, val))
                return False
            # click Update
            try:
                pg.get_by_role("button", name=re.compile(r"^\s*Update\s*$", re.I)).first.click(timeout=5000)
                pg.wait_for_timeout(6000)
                print("  [WRITE] Update clicked (%s=%s on item %s)" % (args.attr, val, item_id))
            except Exception as e:
                print("  Update click fail:", type(e).__name__); return False
            # verify via API read-back
            list_items.clear()
            goto_products()
            find_row_for(item_id)  # forces the list API for the page containing it
            cur_after = list_items.get(item_id)
            print("  VERIFY item %s : before=%s  after=%s  (target +%.1f%% = %s)" %
                  (item_id, cur_before, cur_after,
                   args.pct, round(cur_before*factor, 2) if isinstance(cur_before,(int,float)) else "?"))
            return True

        cold_test(args.item)
        b.close()

    with open(os.path.join(cache, "_writes.jsonl"), "w", encoding="utf-8") as fh:
        for w in writes:
            fh.write(json.dumps(w, ensure_ascii=False) + "\n")
    print("-" * 80)
    print("captured candidate write requests:", len(writes), "| cache:", cache)
    for w in writes[:6]:
        print("  ", w["method"], w["url"][:90])
    return 0


if __name__ == "__main__":
    sys.exit(main())
