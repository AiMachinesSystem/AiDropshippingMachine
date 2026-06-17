#!/usr/bin/env python3
"""
AutoDS READ-ONLY status reader via Playwright (reuses storage_state.json).

SAFETY CONTRACT (do not weaken):
- READ-ONLY: navigates by URL and reads/screenshots. NO clicks on actionable controls, NO form submits,
  NO writes/imports/publishes/pricing/orders anywhere.
- Reuses the saved authenticated session (storage_state.json). No credentials are read or printed.
- Captures evidence to 90_CACHE (gitignored): screenshots, rendered page text, and the SPA's own
  API JSON responses (the app's GET calls — observing them is read-only).
- Never prints secrets to stdout (only metadata: endpoint paths, statuses, titles, counts).

GO scope: GO_AUTODS_READ_SESSION (read-only).

Usage:
  python read_autods_status.py                 # visits home only (discovery)
  python read_autods_status.py / /products /settings ...   # visits the given routes
"""
import os
import sys
import json
import re
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


def slugify(s):
    s = s.strip("/").replace("/", "_") or "home"
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", s)[:60]


def main():
    routes = sys.argv[1:] or ["/"]
    if not os.path.exists(STATE):
        print("FAIL: storage_state.json not found — run login_and_save_session.py first.")
        return 3
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("FAIL: playwright not installed in this venv.")
        return 3

    root = find_repo_root(HERE) or HERE
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    cache_fetch = os.path.join(root, "90_CACHE", "fetches", "autods", "run_" + ts)
    cache_shot = os.path.join(root, "90_CACHE", "screenshots", "autods", "run_" + ts)
    os.makedirs(cache_fetch, exist_ok=True)
    os.makedirs(cache_shot, exist_ok=True)

    captured = []
    seen_api = set()

    def on_response(resp):
        try:
            url = resp.url
            if "autods.com" not in url:
                return
            ct = (resp.headers or {}).get("content-type", "")
            if "application/json" not in ct:
                return
            try:
                body = resp.text()
            except Exception:
                return
            if len(body) > 300000:
                body = body[:300000] + "...(truncated)"
            captured.append({"method": resp.request.method, "url": url, "status": resp.status, "body": body})
            seen_api.add("%-4s %s [%s]" % (resp.request.method, url.split("?")[0], resp.status))
        except Exception:
            pass

    pages_info = []
    nav_links = []
    print("AutoDS READ-ONLY status reader (reusing saved session).")
    print("  run ts :", ts)
    print("  routes :", routes)
    print("-" * 70)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(
            storage_state=STATE,
            viewport={"width": 1440, "height": 1000},
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
        )
        page = ctx.new_page()
        page.on("response", on_response)
        for i, route in enumerate(routes):
            url = route if route.startswith("http") else BASE + (route if route.startswith("/") else "/" + route)
            slug = "%02d_%s" % (i, slugify(route))
            rec = {"route": route, "url": url, "slug": slug}
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(6500)
                rec["final_url"] = page.url
                try:
                    rec["title"] = page.title()
                except Exception:
                    rec["title"] = None
                try:
                    txt = page.locator("body").inner_text(timeout=8000)
                except Exception:
                    txt = ""
                rec["text_len"] = len(txt)
                shot = os.path.join(cache_shot, slug + ".png")
                try:
                    page.screenshot(path=shot, full_page=True)
                    rec["screenshot"] = shot
                except Exception as e:  # noqa: BLE001
                    rec["screenshot"] = "ERR:%s" % e
                with open(os.path.join(cache_fetch, slug + ".txt"), "w", encoding="utf-8") as fh:
                    fh.write("ROUTE: %s\nURL: %s\nFINAL_URL: %s\nTITLE: %s\n%s\n%s\n" % (
                        route, url, rec.get("final_url"), rec.get("title"), "-" * 60, txt))
                print("  [ok] %-24s -> %s | %s" % (route, rec.get("final_url"), rec.get("title")))
            except Exception as e:  # noqa: BLE001
                rec["error"] = "%s: %s" % (type(e).__name__, e)
                print("  [ERR] %-24s -> %s" % (route, rec["error"]))
            try:
                links = page.eval_on_selector_all(
                    "a[href]", "els => Array.from(new Set(els.map(e => e.href)))")
            except Exception:
                links = []
            rec["app_links"] = [l for l in links if l.startswith(BASE)]
            for l in rec["app_links"]:
                if l not in nav_links:
                    nav_links.append(l)
            pages_info.append(rec)
        b.close()

    with open(os.path.join(cache_fetch, "_api_bodies.jsonl"), "w", encoding="utf-8") as fh:
        for c in captured:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(os.path.join(cache_fetch, "_api_endpoints.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(sorted(seen_api)))
    with open(os.path.join(cache_fetch, "_nav_links.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(nav_links))
    with open(os.path.join(cache_fetch, "_pages.json"), "w", encoding="utf-8") as fh:
        json.dump(pages_info, fh, ensure_ascii=False, indent=2)

    print("-" * 70)
    print("CAPTURE DIR :", cache_fetch)
    print("SHOTS DIR   :", cache_shot)
    print("API resp    :", len(captured))
    print("Unique API endpoints hit:")
    for e in sorted(seen_api):
        print("   ", e)
    print("NAV links (same-origin app routes):")
    app_links = [l for l in nav_links if l.startswith(BASE)]
    for l in app_links:
        print("   ", l)
    if not app_links:
        print("    (none found as <a href> — SPA likely uses button-based nav; use URL routes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
