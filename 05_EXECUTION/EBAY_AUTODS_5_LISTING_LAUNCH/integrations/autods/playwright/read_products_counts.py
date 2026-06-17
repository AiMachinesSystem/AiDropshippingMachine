#!/usr/bin/env python3
"""
AutoDS product COUNTS reader (drafts + published) — dismisses ONLY the trial UGC upsell, then reads.

SAFETY CONTRACT (do not weaken):
- Clicks allowed (read-only intent only): (a) dismiss the UGC upsell interstitial ("No Thanks, I'll Miss Out");
  (b) sidebar navigation links to LIST pages (e.g. "Drafts"). Both write NOTHING to the store.
- FORBIDDEN clicks: any data-mutating control — Bulk Edit/Delete/Relist/AI Rewrite, Save, Import, Add Product,
  publish, price changes, order actions, anything that creates/edits/deletes.
- Everything else is read-only navigation + screenshots + observing the SPA's own GET API responses.
- Reuses storage_state.json. No credentials read or printed. No secrets printed.

GO scope: GO_AUTODS_READ_SESSION + explicit owner GO to dismiss the upsell to read product counts.
"""
import os
import re
import sys
import json
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"


def find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "10_OUTPUTS")):
            return cur
        p = os.path.dirname(cur)
        if p == cur:
            return None
        cur = p


def main():
    if not os.path.exists(STATE):
        print("FAIL: storage_state.json not found.")
        return 3
    from playwright.sync_api import sync_playwright

    root = find_repo_root(HERE) or HERE
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache_fetch = os.path.join(root, "90_CACHE", "fetches", "autods", "products_" + ts)
    cache_shot = os.path.join(root, "90_CACHE", "screenshots", "autods", "products_" + ts)
    os.makedirs(cache_fetch, exist_ok=True)
    os.makedirs(cache_shot, exist_ok=True)

    captured = []

    def on_response(resp):
        try:
            url = resp.url
            if "autods.com" not in url:
                return
            if "application/json" not in (resp.headers or {}).get("content-type", ""):
                return
            body = resp.text()
            if len(body) > 300000:
                body = body[:300000] + "...(truncated)"
            captured.append({"method": resp.request.method, "url": url, "status": resp.status, "body": body})
        except Exception:
            pass

    def snap(page, slug):
        try:
            page.screenshot(path=os.path.join(cache_shot, slug + ".png"), full_page=True)
        except Exception:
            pass
        try:
            txt = page.locator("body").inner_text(timeout=8000)
        except Exception:
            txt = ""
        with open(os.path.join(cache_fetch, slug + ".txt"), "w", encoding="utf-8") as fh:
            fh.write("URL: %s\nTITLE: %s\n%s\n%s\n" % (page.url, page.title(), "-" * 60, txt))
        return txt

    print("AutoDS product counts reader.  run:", ts)
    print("-" * 64)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(
            storage_state=STATE, viewport={"width": 1440, "height": 1000},
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        page = ctx.new_page()
        page.on("response", on_response)

        # 1) go to products; expect the UGC upsell redirect
        page.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(5000)
        print("  after /products ->", page.url)
        snap(page, "00_before_dismiss")

        # 2) dismiss ONLY the upsell, if present
        dismissed = False
        if "ugc-offer" in page.url or "offer" in page.url:
            for make in [
                lambda: page.get_by_role("link", name=re.compile(r"No Thanks", re.I)),
                lambda: page.get_by_role("button", name=re.compile(r"No Thanks", re.I)),
                lambda: page.get_by_text(re.compile(r"No Thanks", re.I)),
            ]:
                try:
                    el = make().first
                    el.wait_for(state="visible", timeout=6000)
                    el.click()
                    dismissed = True
                    print("  [click] dismissed upsell via 'No Thanks'")
                    break
                except Exception:
                    continue
            page.wait_for_timeout(4000)
            print("  after dismiss ->", page.url)
        else:
            print("  no upsell detected on this load")

        # 3) load products (active/published) list
        page.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(6000)
        print("  products list ->", page.url)
        products_txt = snap(page, "01_products_list")
        try:
            links = page.eval_on_selector_all("a[href]", "els => Array.from(new Set(els.map(e => e.href)))")
        except Exception:
            links = []
        app_links = [l for l in links if l.startswith(BASE)]

        # 4) navigate to Drafts via the sidebar link (read-only navigation; no data-mutating clicks)
        draft_txt = ""
        for make in [
            lambda: page.get_by_role("link", name=re.compile(r"^\s*Drafts\s*$", re.I)),
            lambda: page.get_by_role("button", name=re.compile(r"^\s*Drafts\s*$", re.I)),
            lambda: page.get_by_text(re.compile(r"^Drafts$", re.I)),
        ]:
            try:
                el = make().first
                el.wait_for(state="visible", timeout=8000)
                el.click()
                page.wait_for_timeout(6500)
                print("  drafts ->", page.url)
                draft_txt = snap(page, "02_drafts")
                break
            except Exception:
                continue
        if not draft_txt:
            print("  drafts nav: could not locate the Drafts link")
        b.close()

    # dump captured API
    with open(os.path.join(cache_fetch, "_api_bodies.jsonl"), "w", encoding="utf-8") as fh:
        for c in captured:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")

    print("-" * 64)
    print("CAPTURE DIR:", cache_fetch)
    print("SHOTS DIR  :", cache_shot)
    print("App links  :", app_links)
    print("Product/count API bodies:")
    for c in captured:
        u = c["url"].split("?")[0]
        if re.search(r"product|count|draft|listing", u, re.I) and "marketplace/api/products" not in u:
            print("\n  === %s %s [%s] ===" % (c["method"], u, c["status"]))
            try:
                bd = json.loads(c["body"])
                s = json.dumps(bd, ensure_ascii=False)
                print("   ", s[:1500])
            except Exception:
                print("   ", c["body"][:800])
    return 0


if __name__ == "__main__":
    sys.exit(main())
