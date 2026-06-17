#!/usr/bin/env python3
"""
Read the AutoDS DRAFTS count. Dismisses the UGC upsell, then navigates to the Drafts list via the
sidebar item (which is a React onClick element, not an <a href>) using a direct JS click — read-only
navigation to a list page. No data-mutating clicks. See read_products_counts.py for the full contract.
GO scope: GO_AUTODS_READ_SESSION + owner GO to read draft/published counts.
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
    from playwright.sync_api import sync_playwright
    root = find_repo_root(HERE) or HERE
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache_fetch = os.path.join(root, "90_CACHE", "fetches", "autods", "drafts_" + ts)
    cache_shot = os.path.join(root, "90_CACHE", "screenshots", "autods", "drafts_" + ts)
    os.makedirs(cache_fetch, exist_ok=True)
    os.makedirs(cache_shot, exist_ok=True)

    captured = []

    def on_response(resp):
        try:
            if "autods.com" not in resp.url:
                return
            if "application/json" not in (resp.headers or {}).get("content-type", ""):
                return
            captured.append({"url": resp.url, "status": resp.status, "body": resp.text()[:4000]})
        except Exception:
            pass

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000},
                            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        page = ctx.new_page()
        page.on("response", on_response)

        page.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4500)
        if "offer" in page.url:
            for make in [lambda: page.get_by_role("link", name=re.compile(r"No Thanks", re.I)),
                         lambda: page.get_by_text(re.compile(r"No Thanks", re.I))]:
                try:
                    make().first.click(timeout=5000)
                    break
                except Exception:
                    continue
            page.wait_for_timeout(3500)
        page.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(5000)

        # find the "Drafts" sidebar item (smallest element whose trimmed text == "Drafts") and JS-click it
        handle = page.evaluate_handle("""() => {
            const els = Array.from(document.querySelectorAll('a,button,span,div,li'));
            const hits = els.filter(e => (e.innerText||'').trim().toLowerCase() === 'drafts');
            hits.sort((a,b) => (a.innerText.length - b.innerText.length) || (a.children.length - b.children.length));
            return hits[0] || null;
        }""")
        info = page.evaluate("(el) => el ? {tag: el.tagName, cls: el.className, html: el.outerHTML.slice(0,200)} : null", handle)
        print("Drafts element:", info)
        if info:
            try:
                page.evaluate("(el) => el.click()", handle)
            except Exception as e:
                print("js click err:", e)
            page.wait_for_timeout(6500)
        print("after Drafts click ->", page.url)
        try:
            txt = page.locator("body").inner_text(timeout=8000)
        except Exception:
            txt = ""
        with open(os.path.join(cache_fetch, "drafts.txt"), "w", encoding="utf-8") as fh:
            fh.write("URL: %s\nTITLE: %s\n%s\n%s\n" % (page.url, page.title(), "-" * 60, txt))
        try:
            page.screenshot(path=os.path.join(cache_shot, "drafts.png"), full_page=True)
        except Exception:
            pass
        b.close()

    with open(os.path.join(cache_fetch, "_api_bodies.jsonl"), "w", encoding="utf-8") as fh:
        for c in captured:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")

    print("-" * 60)
    print("CAPTURE:", cache_fetch)
    print("count endpoints:")
    for c in captured:
        if re.search(r"count|draft", c["url"], re.I):
            print("  ", c["url"].split("?")[0], "->", c["body"][:200])
    # surface any "Drafts (N)" text
    m = re.findall(r"Drafts\s*\(?\s*(\d+)\s*\)?", txt) if 'txt' in dir() else []
    return 0


if __name__ == "__main__":
    sys.exit(main())
