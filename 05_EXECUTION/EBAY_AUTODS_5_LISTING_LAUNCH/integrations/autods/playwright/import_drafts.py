#!/usr/bin/env python3
"""
Import supplier products into AutoDS as DRAFTS (never publish).

SAFETY (do not weaken):
- Only ever clicks "Add as Draft (Simple page)". NEVER clicks "Publish to Store".
- Creates DRAFTS only (reversible). No publish, no pricing, no orders.
GO scope: owner GO 2026-06-17 to import the 2 mid-ticket AliExpress products as drafts.
Usage: import_drafts.py [--confirm]   (default = dry-run: opens modal, fills, does NOT submit)
"""
import os, re, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"

URLS = [
    ("dog_car_hammock", "https://www.aliexpress.com/item/4000283772703.html"),
    ("pc_temp_display", "https://www.aliexpress.com/item/4001179427755.html"),
]


def draft_count(page):
    try:
        txt = page.locator("body").inner_text(timeout=8000)
        m = re.search(r"Drafts\s*\(?\s*(\d+)\s*\)?", txt) or re.search(r"Upload\s*\(?\s*(\d+)\s*\)?", txt)
        return int(m.group(1)) if m else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--confirm", action="store_true"); args = ap.parse_args()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
        page = ctx.new_page()
        page.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); page.wait_for_timeout(6000)
        before = draft_count(page); print("drafts before:", before)

        for slug, url in URLS:
            try:
                page.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); page.wait_for_timeout(4000)
                page.get_by_text(re.compile(r"^\s*Add product with link\s*$", re.I)).first.click(timeout=6000)
                page.wait_for_timeout(1800)
                box = page.get_by_placeholder(re.compile(r"Enter URL or Product ID", re.I)).first
                box.wait_for(state="visible", timeout=6000)
                box.fill(url)
                page.wait_for_timeout(600)
                # SAFETY: only the draft button, never Publish
                draft_btn = page.get_by_role("button", name=re.compile(r"Add as Draft", re.I)).first
                draft_btn.wait_for(state="visible", timeout=6000)
                if args.confirm:
                    draft_btn.click(timeout=6000)
                    print("  [IMPORT] %s -> Add as Draft clicked (%s)" % (slug, url))
                    page.wait_for_timeout(18000)   # let AutoDS scrape + create the draft
                else:
                    print("  [DRY-RUN] %s filled, NOT submitted (%s)" % (slug, url))
                    page.keyboard.press("Escape"); page.wait_for_timeout(800)
            except Exception as e:
                print("  [ERR] %s: %s: %s" % (slug, type(e).__name__, e))

        page.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); page.wait_for_timeout(7000)
        after = draft_count(page); print("drafts after:", after)
        b.close()
    print("-" * 50)
    print(("IMPORT" if args.confirm else "DRY-RUN") + " complete. drafts %s -> %s" % (before, after))
    return 0


if __name__ == "__main__":
    sys.exit(main())
