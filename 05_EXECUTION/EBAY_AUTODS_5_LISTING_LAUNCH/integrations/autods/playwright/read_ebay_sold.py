#!/usr/bin/env python3
"""
READ-ONLY: read eBay SOLD/completed listing comps for a query, using the authenticated eBay session
(ebay_storage_state.json from ebay_login_and_save_session.py). This bypasses the 403 that blocks
anonymous scraping of sold listings -> gives real demand/price evidence for NET-margin validation.

SAFETY: read-only. Navigates the sold-search URL and reads visible prices/titles/sold-counts. No writes.
Caches the rendered text to 90_CACHE for the evidence trail. Run with PYTHONIOENCODING=utf-8 on Windows.

Usage: read_ebay_sold.py "search query"   [--active]   (default = SOLD/completed; --active = active listings)
"""
import os, re, sys, json
from datetime import datetime
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "ebay_storage_state.json")


def main():
    args = [a for a in sys.argv[1:] if a != "--active"]
    active = "--active" in sys.argv
    if not args:
        print("usage: read_ebay_sold.py \"query\" [--active]"); return 2
    query = args[0]
    if not os.path.exists(STATE):
        print("FAIL: ebay_storage_state.json not found — run ebay_login_and_save_session.py first."); return 3
    from playwright.sync_api import sync_playwright
    sold = "" if active else "&LH_Sold=1&LH_Complete=1"
    url = "https://www.ebay.com/sch/i.html?_nkw=" + query.replace(" ", "+") + sold + "&_sop=13"

    root = HERE
    while root and not os.path.isdir(os.path.join(root, "10_OUTPUTS")):
        root = os.path.dirname(root)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root or HERE, "90_CACHE", "fetches", "ebay", "sold_" + ts)
    os.makedirs(cache, exist_ok=True)

    print("eBay %s comps for: %s" % ("ACTIVE" if active else "SOLD", query))
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000},
                            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        pg = ctx.new_page()
        pg.goto(url, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(5000)
        try:
            txt = pg.locator("body").inner_text(timeout=8000)
        except Exception:
            txt = ""
        with open(os.path.join(cache, "page.txt"), "w", encoding="utf-8") as fh:
            fh.write("URL: %s\n%s\n%s" % (url, "-" * 60, txt))
        rows = pg.evaluate(r"""() => {
          const out=[]; const items=document.querySelectorAll('li.s-item, .s-item');
          for(const it of items){
            const t=(it.querySelector('.s-item__title')||{}).innerText||'';
            const pr=(it.querySelector('.s-item__price')||{}).innerText||'';
            const sold=(it.querySelector('.s-item__quantitySold, .s-item__hotness, .s-item__caption')||{}).innerText||'';
            if(t && pr && !/Shop on eBay/i.test(t)) out.push({title:t.slice(0,70), price:pr.trim(), sold:sold.trim().slice(0,40)});
          }
          return out.slice(0,25);
        }""")
        b.close()

    print("  cache:", cache)
    print("-" * 90)
    if not rows:
        print("  (no parsed rows — check page.txt; eBay may have challenged the session or layout changed)")
    nums = []
    for r in rows:
        print("  %-10s %-30s %s" % (r["price"], r["sold"], r["title"]))
        for m in re.findall(r"\$([0-9]+(?:\.[0-9]{2})?)", r["price"]):
            nums.append(float(m))
    if nums:
        nums.sort()
        n = len(nums)
        med = nums[n // 2]
        print("-" * 90)
        print("  parsed %d prices | min $%.2f | median $%.2f | max $%.2f" % (n, nums[0], med, nums[-1]))
    with open(os.path.join(cache, "rows.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
