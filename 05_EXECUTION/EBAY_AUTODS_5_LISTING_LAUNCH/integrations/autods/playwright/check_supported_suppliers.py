#!/usr/bin/env python3
"""READ-ONLY: open the 'Add product with link' modal and dump its text + any supplier logos/names,
to determine which suppliers (esp. Temu) are supported for import in THIS account. No writes/submits."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
    pg = ctx.new_page()
    pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(6000)
    try:
        pg.get_by_text(re.compile(r"^\s*Add product with link\s*$", re.I)).first.click(timeout=6000); pg.wait_for_timeout(2500)
    except Exception as e:
        print("could not open modal:", e)
    # dump modal text
    txt = pg.locator("body").inner_text(timeout=8000)
    # find the supplier mentions
    sup = re.findall(r"(AliExpress|Amazon|Walmart|Temu|Banggood|CJ\s*Dropshipping|Etsy|Costco|Wayfair|Alibaba|DHgate|Home Depot|eBay)", txt, re.I)
    print("Supplier names found on page:", sorted(set(s.title() for s in sup)))
    # alt/title of imgs in modal
    logos = pg.eval_on_selector_all("img", "els=>els.map(e=>e.alt||e.title||'').filter(Boolean)")
    sup_logos = [l for l in logos if re.search(r"alie|amazon|walmart|temu|bang|cj|etsy|costco|wayfair|alibaba|dhgate|depot|ebay", l, re.I)]
    print("Supplier logos (alt/title):", sup_logos)
    # placeholder hint
    try:
        ph = pg.get_by_placeholder(re.compile(r"Enter URL or Product ID", re.I)).first
        print("URL box present:", ph.is_visible())
    except Exception:
        print("URL box not found")
    # print a slice of modal text mentioning 'support'
    for line in txt.splitlines():
        if re.search(r"support|supplier|temu|paste|link|url", line, re.I) and len(line) < 120:
            print("  |", line.strip())
    b.close()
