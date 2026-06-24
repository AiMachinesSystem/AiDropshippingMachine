#!/usr/bin/env python3
"""
marketplace_filter_probe.py — READ-ONLY probe to crack the AutoDS Marketplace filter API.

The prior marketplace reader captured only RESPONSES, so it always saw the generic feed and
concluded "search doesn't filter". This probe captures the *REQUESTS* (method, full URL incl.
query string, and POST body) for every gw.autods.com marketplace/api/products call, while:
  1) loading the marketplace,
  2) dumping every visible filter control (category chips, dropdowns, search box, warehouse toggles),
  3) submitting one keyword search (a read query — mutates nothing).
Then it can SEE the exact filter shape (e.g. {"query":"pool"} or ?search=pool&warehouse=US) so a
follow-up replay can pull cluster-targeted, US-warehouse products directly via the authenticated API.

SAFETY CONTRACT: READ-ONLY research. Allowed: navigation, scrolling, dumping DOM, typing ONE search
keyword. FORBIDDEN: import, add-to-store, publish, any write. No credentials read/printed.
GO scope: GO_AUTODS_READ_SESSION + product-research mission (read-only).

Usage: marketplace_filter_probe.py [keyword]      # default keyword = "pool cover"
"""
import os, re, sys, json
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"


def find_repo_root(start):
    cur = os.path.abspath(start)
    while cur != os.path.dirname(cur):
        if os.path.isdir(os.path.join(cur, "10_OUTPUTS")):
            return cur
        cur = os.path.dirname(cur)
    return start


def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "pool cover"
    from playwright.sync_api import sync_playwright
    root = find_repo_root(HERE)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root, "90_CACHE", "fetches", "autods", "mkt_probe_" + ts)
    os.makedirs(cache, exist_ok=True)

    reqs = []          # captured marketplace API requests
    resp_counts = {}   # url -> item count (best-effort)

    def is_mkt(u):
        return "autods.com" in u and ("marketplace/api/products" in u or
                                      ("marketplace" in u and "products" in u))

    def on_request(req):
        try:
            u = req.url
            if not is_mkt(u):
                return
            pd = None
            try:
                pd = req.post_data
            except Exception:
                pd = None
            reqs.append({"method": req.method, "url": u, "post_data": pd,
                         "headers": {k: v for k, v in (req.headers or {}).items()
                                     if k.lower() in ("content-type", "x-store-id", "store-id", "authorization-store")}})
        except Exception:
            pass

    def on_response(resp):
        try:
            u = resp.url
            if not is_mkt(u):
                return
            if "application/json" not in (resp.headers or {}).get("content-type", ""):
                return
            body = resp.text()
            try:
                data = json.loads(body)
                items = data.get("results") or data.get("products") or data.get("data")
                if isinstance(items, dict):
                    items = items.get("results") or items.get("items")
                resp_counts[u] = len(items) if isinstance(items, list) else "n/a"
            except Exception:
                resp_counts[u] = "parse-err"
        except Exception:
            pass

    def dump_controls(page, slug):
        ctl = page.evaluate(r"""() => {
          const pick = (sel) => [...document.querySelectorAll(sel)]
              .map(e => (e.innerText||e.value||e.placeholder||'').replace(/\s+/g,' ').trim())
              .filter(t => t && t.length<=40);
          return {
            buttons: pick('button').slice(0,80),
            chips: pick('.ant-tag, .ant-select-selection-item, [class*=chip], [class*=Chip]').slice(0,60),
            selects: pick('.ant-select-selector, select').slice(0,40),
            placeholders: [...document.querySelectorAll('input')].map(i=>i.placeholder||'').filter(Boolean).slice(0,30),
            headings: pick('h1,h2,h3,h4,[class*=title],[class*=Title]').slice(0,40)
          };
        }""")
        with open(os.path.join(cache, "controls_" + slug + ".json"), "w", encoding="utf-8") as fh:
            json.dump(ctl, fh, ensure_ascii=False, indent=1)
        return ctl

    print("MKT filter probe. run:", ts, "| keyword:", repr(keyword))
    print("-" * 64)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000},
                            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        page = ctx.new_page()
        page.on("request", on_request)
        page.on("response", on_response)

        # 1) load marketplace + scroll
        page.goto(BASE + "/marketplace", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(6000)
        ctl = dump_controls(page, "00_marketplace")
        print("  [controls] buttons:", ctl["buttons"][:30])
        print("  [controls] selects:", ctl["selects"])
        print("  [controls] chips:", ctl["chips"][:30])
        print("  [controls] placeholders:", ctl["placeholders"])
        for _ in range(3):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(1500)

        n_before = len(reqs)

        # 2) submit ONE keyword search (read query)
        box = None
        for mk in [lambda: page.get_by_placeholder(re.compile(r"search", re.I)),
                   lambda: page.locator("input[type='search']"),
                   lambda: page.locator("input[placeholder*='Search' i]")]:
            try:
                cand = mk().first
                cand.wait_for(state="visible", timeout=4000)
                box = cand
                break
            except Exception:
                continue
        if box:
            box.fill(keyword)
            page.wait_for_timeout(500)
            box.press("Enter")
            page.wait_for_timeout(5000)
            for _ in range(2):
                page.mouse.wheel(0, 4000)
                page.wait_for_timeout(1500)
            dump_controls(page, "01_after_search")
            print("  [search] submitted %r -> url now: %s" % (keyword, page.url))
        else:
            print("  [search] search box NOT found")

        # 3) try clicking a category/filter dropdown to surface its options + the API it fires
        try:
            sel = page.locator(".ant-select-selector").first
            if sel.count():
                sel.click(timeout=3000)
                page.wait_for_timeout(1500)
                opts = page.evaluate(r"""() => [...document.querySelectorAll('.ant-select-item-option, [role=option]')]
                    .map(o=>(o.innerText||'').trim()).filter(Boolean).slice(0,60)""")
                with open(os.path.join(cache, "dropdown_options.json"), "w", encoding="utf-8") as fh:
                    json.dump(opts, fh, ensure_ascii=False, indent=1)
                print("  [dropdown] options:", opts[:30])
                page.keyboard.press("Escape")
        except Exception as e:
            print("  [dropdown] err:", type(e).__name__)

        print("  requests captured during search phase:", len(reqs) - n_before)
        b.close()

    # persist captured requests
    with open(os.path.join(cache, "_requests.jsonl"), "w", encoding="utf-8") as fh:
        for r in reqs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("-" * 64)
    print("CACHE:", cache)
    print("marketplace API requests captured:", len(reqs))
    print("=" * 64)
    seen = set()
    for r in reqs:
        key = (r["method"], r["url"].split("?")[0], (r["post_data"] or "")[:0])
        # print each distinct method+endpoint with its query + body
        qs = r["url"].split("?", 1)[1] if "?" in r["url"] else ""
        print("\n%s %s" % (r["method"], r["url"].split("?")[0]))
        if qs:
            print("  QUERY:", qs[:400])
        if r["post_data"]:
            print("  BODY :", r["post_data"][:600])
        print("  resp items:", resp_counts.get(r["url"], "?"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
