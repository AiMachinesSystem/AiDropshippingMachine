#!/usr/bin/env python3
"""
read_ebay_demand.py — REAL eBay demand per query via the authenticated session (storage_state_ebay.json).
Reads SOLD/completed comps + ACTIVE competition and computes: sold-results count, recent-30d sold,
median sold price, sell-through proxy, and the max source cost to clear net >=$4 (owner formula).

WHY THIS EXISTS: Terapeak Product Research (/sh/research) is account-gated on this store (302 -> /sh, see
ERROR_REGISTRY E-018). The authenticated SOLD-search bypasses the 403 wall and gives the same demand signal.
eBay dropped the .s-item result classes (E-019), so this parses the rendered page TEXT by the "Sold <date>"
anchor pattern instead of DOM selectors (robust to layout churn).

SAFETY: READ-ONLY — GET navigation + read visible text. No listing/publish/price/order writes. No creds.
Caches every rendered page to 90_CACHE for the evidence trail. Run with PYTHONIOENCODING=utf-8.
GO scope: GO_EBAY_READ_SESSION (read-only).

Usage: read_ebay_demand.py "query one" "query two" ...   (defaults to the proven pool/water + kitchen cluster)
NOTE: pace sequential queries; rapid bursts can make eBay serve a thin ACTIVE page (active_listings=None).
"""
import os, re, sys, json
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "storage_state_ebay.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
MON = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
SOLD_RE = re.compile(r"^Sold\s+([A-Z][a-z]{2})\s+(\d{1,2}),\s+(\d{4})$")
PRICE_RE = re.compile(r"\$\s?([0-9][0-9,]*\.?[0-9]{0,2})")
RESULTS_RE = re.compile(r"([0-9][0-9,]*)\s+results?\s+for", re.I)
DEFAULT = ["deck jet pool fountain", "stock tank pool cover", "dog pool ramp", "ham maker meat press"]


def find_root(s):
    c = os.path.abspath(s)
    while c != os.path.dirname(c):
        if os.path.isdir(os.path.join(c, "10_OUTPUTS")):
            return c
        c = os.path.dirname(c)
    return s


def parse_sold(text, today):
    lines = [l.strip() for l in text.splitlines()]
    m = RESULTS_RE.search(text)
    total = int(m.group(1).replace(",", "")) if m else None
    comps = []
    for i, l in enumerate(lines):
        sm = SOLD_RE.match(l)
        if not sm or sm.group(1) not in MON:
            continue
        d = datetime(int(sm.group(3)), MON[sm.group(1)], int(sm.group(2)))
        title, price = "", None
        for j in range(i + 1, min(i + 12, len(lines))):
            if not title and lines[j] and lines[j] != "Opens in a new window or tab":
                title = lines[j][:70]
            pm = PRICE_RE.search(lines[j])
            if pm:
                try:
                    price = float(pm.group(1).replace(",", ""))
                except ValueError:
                    price = None
                break
        if price and 1 < price < 5000:
            comps.append({"date": d.strftime("%Y-%m-%d"), "title": title, "price": price,
                          "recent30": (today - d).days <= 30})
    return total, comps


def fetch(pg, query, active):
    sold = "" if active else "&LH_Sold=1&LH_Complete=1"
    url = "https://www.ebay.com/sch/i.html?_nkw=" + query.replace(" ", "+") + sold + "&_sop=13"
    pg.goto(url, wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(3500)
    try:
        return pg.locator("body").inner_text(timeout=8000)
    except Exception:
        return ""


def main():
    queries = sys.argv[1:] or DEFAULT
    if not os.path.exists(STATE):
        print("BLOCKED: storage_state_ebay.json not found. Run login_ebay_save_session.py first (owner login).")
        return 2
    from playwright.sync_api import sync_playwright
    today = datetime.now()
    root = find_root(HERE)
    ts = today.strftime("%Y-%m-%d_%H%M%S")
    cache = os.path.join(root, "90_CACHE", "fetches", "ebay", "demand_" + ts)
    os.makedirs(cache, exist_ok=True)
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000}, user_agent=UA)
        pg = ctx.new_page()
        for q in queries:
            st = fetch(pg, q, False)
            open(os.path.join(cache, "sold_%s.txt" % q.replace(" ", "_")), "w", encoding="utf-8").write(st)
            if "signin" in pg.url.lower():
                print("  [%s] SESSION EXPIRED -> re-run login_ebay_save_session.py" % q); break
            total, comps = parse_sold(st, today)
            at = fetch(pg, q, True)
            am = RESULTS_RE.search(at)
            active = int(am.group(1).replace(",", "")) if am else None
            prices = sorted(c["price"] for c in comps)
            n = len(prices)
            med = prices[n // 2] if n else None
            recent30 = sum(1 for c in comps if c["recent30"])
            max_cost4 = round(0.865 * med - 9.90, 2) if med else None
            stp = round(100 * total / (total + active), 1) if (total and active) else None
            rows.append({"query": q, "sold_results": total, "sold_parsed": n, "recent30_sold": recent30,
                         "median_sold_price": med, "active_listings": active,
                         "sell_through_proxy_pct": stp, "max_amazon_cost_net4": max_cost4})
            print("  [%s] sold=%s recent30=%s med=$%s active=%s ST~%s%% maxCost($4net)=%s" % (
                q, total, recent30, med, active, stp, max_cost4))
        b.close()
    json.dump(rows, open(os.path.join(cache, "_demand.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 70, "\nCACHE:", cache)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
