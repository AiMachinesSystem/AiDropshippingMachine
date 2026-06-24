#!/usr/bin/env python3
"""
marketplace_filter_probe2.py — READ-ONLY. Capture the 3 missing filter shapes:
  (A) Ships-From = United States  (the US-warehouse constraint, owner's #1 requirement)
  (B) the categories taxonomy (name <-> autods_category_id)  [any marketplace/api/categories call]
  (C) the marketplace TITLE search (typed in the correct box: 'Search by product title…')

Captures every gw.autods.com/marketplace/api/* REQUEST (method/url/post_data) and saves taxonomy
RESPONSES. Read-only: navigation + dropdown select + typing a search query only. No writes.
GO scope: GO_AUTODS_READ_SESSION.
Usage: marketplace_filter_probe2.py [keyword]
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
    keyword = sys.argv[1] if len(sys.argv) > 1 else "meat tenderizer"
    from playwright.sync_api import sync_playwright
    root = find_repo_root(HERE)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root, "90_CACHE", "fetches", "autods", "mkt_probe2_" + ts)
    os.makedirs(cache, exist_ok=True)

    reqs, tax = [], []

    def on_request(req):
        try:
            u = req.url
            if "gw.autods.com/marketplace/api" not in u:
                return
            pd = None
            try:
                pd = req.post_data
            except Exception:
                pd = None
            reqs.append({"phase": PHASE[0], "method": req.method, "url": u, "post_data": pd})
        except Exception:
            pass

    def on_response(resp):
        try:
            u = resp.url
            if "gw.autods.com/marketplace/api" not in u:
                return
            if "categor" in u.lower() or "filter" in u.lower() or "taxonom" in u.lower() or "config" in u.lower():
                tax.append({"url": u, "body": resp.text()[:200000]})
        except Exception:
            pass

    PHASE = ["load"]

    print("MKT probe2. run:", ts, "| keyword:", repr(keyword))
    print("-" * 64)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000},
                            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        page = ctx.new_page()
        page.on("request", on_request)
        page.on("response", on_response)

        page.goto(BASE + "/marketplace", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(6000)

        # (A) Ships From -> United States. The 3rd ant-select is 'Select Ships From'.
        PHASE[0] = "ships_from_US"
        try:
            # find the select whose current text mentions 'Ships From'
            clicked = page.evaluate(r"""() => {
              const sels=[...document.querySelectorAll('.ant-select')];
              for(const s of sels){ if(/ships from/i.test(s.innerText||'')){ s.querySelector('.ant-select-selector')?.click(); return true; } }
              return false;
            }""")
            page.wait_for_timeout(1500)
            if clicked:
                # choose 'United States' option
                opt = page.locator(".ant-select-item-option", has_text=re.compile(r"^United States$", re.I)).first
                if not opt.count():
                    opt = page.get_by_text(re.compile(r"^United States$", re.I)).last
                opt.click(timeout=4000)
                page.wait_for_timeout(4000)
                print("  [A] Ships From -> United States selected")
            else:
                print("  [A] 'Ships From' select not found")
        except Exception as e:
            print("  [A] err:", type(e).__name__, e)

        # (C) title search in the MARKETPLACE box (placeholder 'Search by product title…')
        PHASE[0] = "title_search"
        try:
            box = page.get_by_placeholder(re.compile(r"product title", re.I)).first
            box.wait_for(state="visible", timeout=5000)
            box.click()
            box.fill(keyword)
            page.wait_for_timeout(800)
            box.press("Enter")
            page.wait_for_timeout(4500)
            print("  [C] title search submitted:", repr(keyword), "-> url:", page.url)
        except Exception as e:
            print("  [C] search err:", type(e).__name__, e)

        # (B) try to surface categories taxonomy: click a 'Categories' / filter entry if present
        PHASE[0] = "categories"
        try:
            cat = page.get_by_text(re.compile(r"^\s*Categories\s*$", re.I)).first
            if cat.count():
                cat.click(timeout=3000)
                page.wait_for_timeout(2500)
        except Exception:
            pass
        page.wait_for_timeout(1500)
        b.close()

    with open(os.path.join(cache, "_requests.jsonl"), "w", encoding="utf-8") as fh:
        for r in reqs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    for i, t in enumerate(tax):
        with open(os.path.join(cache, "taxonomy_%02d.json" % i), "w", encoding="utf-8") as fh:
            fh.write(t["body"])

    print("-" * 64)
    print("CACHE:", cache)
    print("requests captured:", len(reqs), "| taxonomy responses:", len(tax))
    print("=" * 64)
    for r in reqs:
        if r["post_data"] and "filters" in (r["post_data"] or ""):
            print("\n[%s] %s %s" % (r["phase"], r["method"], r["url"].split("?")[0]))
            try:
                body = json.loads(r["post_data"])
                print("  filters:", json.dumps(body.get("filters"), ensure_ascii=False))
                print("  order_by:", json.dumps(body.get("order_by"), ensure_ascii=False))
            except Exception:
                print("  BODY:", r["post_data"][:500])
    for t in tax:
        print("\nTAXONOMY:", t["url"])
        print("  ", t["body"][:300])
    return 0


if __name__ == "__main__":
    sys.exit(main())
