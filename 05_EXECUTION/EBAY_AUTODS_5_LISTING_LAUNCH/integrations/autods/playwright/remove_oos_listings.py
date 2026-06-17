#!/usr/bin/env python3
"""
Targeted removal of the 37 OUT-OF-STOCK, never-sold AutoDS listings.

SAFETY (do not weaken):
- TARGET set = item_ids from _removal_set_oos.json (the 37). KEEP set = winners (total_sold_count>0) item_ids.
- HARD GUARD: the tool ABORTS if any KEEP id would ever be selected. It only ticks rows whose Item ID is in TARGET.
- DEFAULT = --dry-run (READ-ONLY: identifies/reports the rows to delete, NEVER clicks delete).
- --confirm performs deletion; --limit N caps how many (test batches). Bulk Delete ends the eBay listing.
GO scope: owner GO 2026-06-17 to remove the 37 OOS never-sold listings (winners protected).
"""
import os, re, sys, json, glob, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(HERE, "storage_state.json"); BASE = "https://platform.autods.com"


def find_repo_root(s):
    c = os.path.abspath(s)
    while True:
        if os.path.isdir(os.path.join(c, "10_OUTPUTS")): return c
        p = os.path.dirname(c)
        if p == c: return None
        c = p


def load_sets(root):
    # newest _removal_set_oos.json
    cands = glob.glob(os.path.join(root, "90_CACHE", "fetches", "autods", "*", "_removal_set_oos.json"))
    cands.sort()
    targets = {str(r["item_id"]) for r in json.load(open(cands[-1], encoding="utf-8"))}
    # winners (KEEP) from newest _products_list.json
    pl = glob.glob(os.path.join(root, "90_CACHE", "fetches", "autods", "audit_*", "_products_list.json")); pl.sort()
    keep = set()
    for it in json.load(open(pl[-1], encoding="utf-8")):
        if it.get("status") == 2 and (it.get("total_sold_count") or 0) > 0:
            keep.add(str(it.get("item_id_on_site")))
    return targets, keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--confirm", action="store_true", help="actually delete (default: dry-run)")
    ap.add_argument("--limit", type=int, default=0, help="max deletions (0 = all targets)")
    args = ap.parse_args()
    root = find_repo_root(HERE) or HERE
    targets, keep = load_sets(root)
    overlap = targets & keep
    print("TARGET (remove):", len(targets), "| KEEP/winners:", len(keep))
    if overlap:
        print("ABORT — target/keep overlap:", overlap); return 2
    from playwright.sync_api import sync_playwright

    def goto_products(page):
        page.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000); page.wait_for_timeout(4000)
        if "offer" in page.url:
            for mk in [lambda: page.get_by_role("link", name=re.compile(r"No Thanks", re.I)),
                       lambda: page.get_by_text(re.compile(r"No Thanks", re.I))]:
                try: mk().first.click(timeout=5000); break
                except Exception: continue
            page.wait_for_timeout(2500)
            page.goto(BASE + "/products", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(5500)

    def scan_page(page):
        rows = page.evaluate(r"""() => {
          const cbs = Array.from(document.querySelectorAll("input.ant-checkbox-input, input[type=checkbox]"));
          return cbs.map((cb,i) => {
            let el = cb; for (let k=0;k<7 && el.parentElement;k++){ el=el.parentElement; if((el.innerText||'').length>60) break; }
            const text=(el.innerText||'').replace(/\s+/g,' ');
            return {i, ids:(text.match(/\b\d{11,13}\b/g)||[])};
          });
        }""")
        out = []
        for r in rows:
            ids = set(r["ids"])
            if ids & keep:           # HARD GUARD: never a winner row
                continue
            hit = ids & targets
            if hit:
                out.append((r["i"], sorted(hit)[0]))
        return out

    found = set(); deleted = 0
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
        page = ctx.new_page()

        if not args.confirm:
            # DRY-RUN: paginate all pages once, report matches (no clicks)
            goto_products(page)
            for pageno in range(1, 16):
                pt = scan_page(page)
                for _, mid in pt: found.add(mid)
                print("  page %d: matched-this-page=%d  (cumulative %d/%d)" % (pageno, len(pt), len(found), len(targets)))
                nxt = page.locator("li.ant-pagination-next:not(.ant-pagination-disabled)")
                if nxt.count() == 0: break
                try: nxt.first.click(timeout=4000); page.wait_for_timeout(2200)
                except Exception: break
        else:
            # CONFIRM: reload-rescan loop (robust to post-delete reflow)
            for iteration in range(40):
                if args.limit and deleted >= args.limit:
                    print("  reached --limit", args.limit); break
                goto_products(page)
                # paginate to the first page that has a target
                pt = []
                for pageno in range(1, 16):
                    pt = scan_page(page)
                    if pt: break
                    nxt = page.locator("li.ant-pagination-next:not(.ant-pagination-disabled)")
                    if nxt.count() == 0: break
                    try: nxt.first.click(timeout=4000); page.wait_for_timeout(2200)
                    except Exception: break
                if not pt:
                    print("  no more targets located — DONE"); break
                # tick matched rows on this page (respect limit)
                cbs = page.locator("input.ant-checkbox-input")
                batch = []
                for idx, mid in pt:
                    if args.limit and (deleted + len(batch)) >= args.limit: break
                    try:
                        cbs.nth(idx).check(timeout=4000); batch.append(mid)
                    except Exception as e:
                        print("    tick fail", mid, type(e).__name__)
                if not batch:
                    print("  nothing ticked, stop"); break
                # Bulk Delete -> choose 'AutoDS and Selling Platform' -> Delete
                try:
                    page.get_by_text(re.compile(r"^\s*Bulk Delete\s*$", re.I)).first.click(timeout=5000)
                    page.wait_for_timeout(1500)
                    page.get_by_text(re.compile(r"AutoDS and Selling Platform", re.I)).first.click(timeout=5000)
                    page.wait_for_timeout(800)
                    page.get_by_role("button", name=re.compile(r"^\s*Delete\s*$", re.I)).first.click(timeout=5000)
                    page.wait_for_timeout(3500)
                    deleted += len(batch); found.update(batch)
                    print("  [DELETED] batch=%d ids=%s  (total %d)" % (len(batch), batch, deleted))
                except Exception as e:
                    print("  bulk-delete flow FAIL:", type(e).__name__, e); break
        b.close()

    print("-" * 60)
    print("DRY-RUN" if not args.confirm else "EXECUTION", "complete.")
    if not args.confirm:
        missing = targets - found
        print("targets identified on the grid: %d / %d" % (len(found), len(targets)))
        if missing: print("NOT located (%d):" % len(missing), sorted(missing)[:10])
    else:
        print("deletions performed:", deleted, "/", (args.limit or len(targets)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
