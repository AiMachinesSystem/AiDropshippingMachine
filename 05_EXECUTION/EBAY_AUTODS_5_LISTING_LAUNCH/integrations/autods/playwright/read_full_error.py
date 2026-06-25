#!/usr/bin/env python3
"""READ-ONLY: print the FULL error_list (untruncated) for drafts whose title matches a needle.
Usage: read_full_error.py <needle>   (default: chlorine)"""
import os, re, json, sys
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"
from playwright.sync_api import sync_playwright

needle = (sys.argv[1] if len(sys.argv) > 1 else "chlorine").lower()
bodies = []
with sync_playwright() as p:
    b = p.chromium.launch(headless=True); ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000}); pg = ctx.new_page()
    def cap(r):
        try:
            if "v2-api.autods.com/products/" in r.url and "/list/" in r.url and "json" in (r.headers or {}).get("content-type", ""):
                bodies.append(r.text())
        except Exception:
            pass
    pg.on("response", cap)
    pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(9000)
    try:
        pg.get_by_text(re.compile(r"^\s*Expand all\s*$", re.I)).first.click(timeout=4000); pg.wait_for_timeout(3000)
    except Exception:
        pass
    pg.wait_for_timeout(2000)
    b.close()

seen = set()
for body in bodies:
    try:
        data = json.loads(body)
    except Exception:
        continue
    for it in (data.get("results") or []):
        t = (it.get("title") or "")
        if needle in t.lower() and t not in seen:
            seen.add(t)
            print("TITLE:", t[:75])
            print("STATUS:", it.get("status"), "| pre_draft_status:", it.get("pre_draft_status"))
            print("ERROR_LIST:", json.dumps(it.get("error_list"), ensure_ascii=False))
            print("-" * 70)
if not seen:
    print("no draft matched needle:", needle)
