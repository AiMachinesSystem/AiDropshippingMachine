#!/usr/bin/env python3
"""
AutoDS MARKETPLACE read-only reader (product research). Reuses storage_state.json.
Navigates the AutoDS Marketplace discovery pages (and optional keyword searches), scrolls to load
more cards, and captures the marketplace product API JSON (gw.autods.com/marketplace/api/products/)
which contains: title, supplier, buy/sell price, profit, sold/order signals, category.

SAFETY CONTRACT: READ-ONLY research. Allowed interactions: navigation, scrolling, and typing a SEARCH
keyword (a read query, mutates nothing). FORBIDDEN: import, add-to-store, publish, any write control.
No credentials read/printed. Evidence cached to 90_CACHE (gitignored).
GO scope: GO_AUTODS_READ_SESSION + product-research mission (read-only).

Usage: read_marketplace.py [search1 "search 2" ...]   # no args = trending+hand-picked+best-sellers
"""
import os, re, sys, json
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
    searches = sys.argv[1:]
    from playwright.sync_api import sync_playwright
    root = find_repo_root(HERE) or HERE
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root, "90_CACHE", "fetches", "autods", "marketplace_" + ts)
    shots = os.path.join(root, "90_CACHE", "screenshots", "autods", "marketplace_" + ts)
    os.makedirs(cache, exist_ok=True)
    os.makedirs(shots, exist_ok=True)

    captured = []

    def on_response(resp):
        try:
            u = resp.url
            if "autods.com" not in u:
                return
            if "application/json" not in (resp.headers or {}).get("content-type", ""):
                return
            if "marketplace/api/products" not in u and "marketplace" not in u:
                # keep only marketplace-relevant payloads to stay focused
                if "products" not in u:
                    return
            body = resp.text()
            if len(body) > 600000:
                body = body[:600000] + "...(truncated)"
            captured.append({"url": u, "method": resp.request.method, "status": resp.status, "body": body})
        except Exception:
            pass

    def scroll_and_settle(page, rounds=6):
        for _ in range(rounds):
            try:
                page.mouse.wheel(0, 4000)
                page.wait_for_timeout(1800)
            except Exception:
                break

    def snap(page, slug):
        try:
            page.screenshot(path=os.path.join(shots, slug + ".png"), full_page=False)
        except Exception:
            pass
        try:
            txt = page.locator("body").inner_text(timeout=8000)
        except Exception:
            txt = ""
        with open(os.path.join(cache, slug + ".txt"), "w", encoding="utf-8") as fh:
            fh.write("URL: %s\nTITLE: %s\n%s\n%s\n" % (page.url, page.title(), "-" * 60, txt[:20000]))

    routes = [
        ("00_marketplace", BASE + "/marketplace"),
        ("01_trending", BASE + "/marketplace/trending-products"),
        ("02_hand_picked", BASE + "/marketplace/hand-picked-products"),
    ]

    print("AutoDS MARKETPLACE reader. run:", ts, "| searches:", searches or "(discovery pages)")
    print("-" * 64)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000},
                            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        page = ctx.new_page()
        page.on("response", on_response)
        for slug, url in routes:
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(5000)
                scroll_and_settle(page, rounds=5)
                snap(page, slug)
                print("  [ok]", url, "->", page.url)
            except Exception as e:
                print("  [ERR]", url, type(e).__name__, e)

        # optional keyword searches via the marketplace search box (read query only)
        for i, q in enumerate(searches):
            try:
                page.goto(BASE + "/marketplace", wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(3500)
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
                    box.fill(q)
                    box.press("Enter")
                    page.wait_for_timeout(5000)
                    scroll_and_settle(page, rounds=3)
                    snap(page, "search_%02d_%s" % (i, re.sub(r'[^a-z0-9]+', '_', q.lower())[:30]))
                    print("  [search] %r ->" % q, page.url)
                else:
                    print("  [search] box not found for %r" % q)
            except Exception as e:
                print("  [search ERR] %r" % q, type(e).__name__)
        b.close()

    with open(os.path.join(cache, "_api_bodies.jsonl"), "w", encoding="utf-8") as fh:
        for c in captured:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")

    # surface marketplace product payloads: print field keys + a few sample products
    print("-" * 64)
    print("CACHE:", cache)
    print("captured payloads:", len(captured))
    prod_payloads = [c for c in captured if "marketplace/api/products" in c["url"]]
    print("marketplace/api/products payloads:", len(prod_payloads))
    sample_done = False
    for c in prod_payloads:
        try:
            data = json.loads(c["body"])
        except Exception:
            continue
        items = data.get("results") or data.get("products") or data.get("data") or (data if isinstance(data, list) else None)
        if isinstance(items, dict):
            items = items.get("results") or items.get("items")
        if not items:
            continue
        if not sample_done and isinstance(items, list) and items:
            print("  sample product keys:", list(items[0].keys())[:40])
            sample_done = True
        print("  payload items:", len(items) if isinstance(items, list) else "n/a")
    return 0


if __name__ == "__main__":
    sys.exit(main())
