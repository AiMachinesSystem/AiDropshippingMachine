#!/usr/bin/env python3
"""
delete_drafts_guarded.py — GUARDED, DRY-RUN-FIRST removal of dead-niche / unpublishable AutoDS DRAFTS.

Owner mandate 2026-06-24: build the tool but DRY-RUN ONLY. Mandatory keep-list (the 2 Kitchen drafts to
evaluate). Kill-list (the 5 proposed KILLs). Dry-run shows exactly which drafts WOULD be deleted, each with
ID, title, kill reason, risk, rollback possible/not. STOP before the real delete. Real delete = SEPARATE GO.

SAFETY (do not weaken):
- DEFAULT = --dry-run (READ-ONLY: pulls the live draft list, reconciles against kill/keep, reports; NO writes).
- HARD GUARD: ABORTS if any KEEP draft would ever be selected for deletion (keep always wins over kill).
- These are DRAFTS, not live listings: deleting a draft ends NO eBay listing and re-import recreates it
  (rollback = POSSIBLE via manage_draft.py import --url <source>). Risk = LOW. (Contrast remove_oos_listings.py
  which ends LIVE listings.)
- --confirm is intentionally HARD-BLOCKED: the real-delete UI flow is NOT wired in this tool, so it is
  IMPOSSIBLE to delete from here. Real delete is a separate, GO-gated, cold-tested step.

Reuses the saved authenticated session (storage_state.json). GO scope: GO_AUTODS_READ_SESSION (read-only dry-run).
Run with PYTHONIOENCODING=utf-8 on Windows.
Usage: delete_drafts_guarded.py [--dry-run] [--confirm]
"""
import os, re, sys, json, argparse
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "storage_state.json")
BASE = "https://platform.autods.com"

# ---- KILL-LIST (the 5 proposed KILLs) : distinctive title regex + reason + risk + rollback + source ----
KILL = [
    {"key": "dog_water_bowl", "rx": re.compile(r"no spill dog water bowl|dog water bowl", re.I),
     "reason": "eBay error EbayViolation (rule: EbayViolation -> kill+replace); niche Pet = 0 lifetime units (DEAD).",
     "risk": "LOW (draft only, never sold, not a live listing; deleting ends no eBay listing).",
     "rollback": "POSSIBLE — re-import the AliExpress source URL via manage_draft.py (title/desc edits would be lost).",
     "source": "AliExpress"},
    {"key": "water_bottle", "rx": re.compile(r"collapsible water bottle|foldable.*bottle", re.I),
     "reason": "eBay error EbayViolation,400 (rule: EbayViolation -> kill+replace); niche Outdoor = 0 units (DEAD).",
     "risk": "LOW (draft only, never sold).",
     "rollback": "POSSIBLE — re-import AliExpress source via manage_draft.py.",
     "source": "AliExpress"},
    {"key": "book_light", "rx": re.compile(r"clip on book light|book light", re.I),
     "reason": "eBay error EbayViolation (rule: EbayViolation -> kill+replace); lighting, no proven niche.",
     "risk": "LOW (draft only, never sold).",
     "rollback": "POSSIBLE — re-import AliExpress source via manage_draft.py.",
     "source": "AliExpress"},
    {"key": "pencil_case", "rx": re.compile(r"pencil case", re.I),
     "reason": "Broken economics: buy cost $133.13 on 0 stock -> never publishable; niche Home/Storage DEAD.",
     "risk": "LOW (draft only, OOS, never publishable).",
     "rollback": "POSSIBLE — re-import Amazon source via manage_draft.py (but item is broken/OOS; not worth it).",
     "source": "Amazon"},
    {"key": "mini_flat_iron", "rx": re.compile(r"mini flat iron|flat iron hair", re.I),
     "reason": "eBay error AnotherStoreImport (duplicate already uploaded); niche Beauty = 0 units (DEAD).",
     "risk": "LOW (draft only; the live copy already exists elsewhere in store).",
     "rollback": "POSSIBLE — re-import, but it is a duplicate; deletion is the correct dedup.",
     "source": "Amazon (duplicate)"},
]

# ---- KEEP-LIST (the 2 Kitchen drafts to evaluate) : MUST NEVER be deleted ----
KEEP = [
    {"key": "splatter_screen", "rx": re.compile(r"splatter screen|frying pan splatter", re.I),
     "note": "Kitchen [TOP niche]. Evaluate, do not delete. (Likely already PUBLISHED in amazon10 -> not a draft.)"},
    {"key": "microwave_cover", "rx": re.compile(r"microwave (splatter )?cover|splatter cover", re.I),
     "note": "Kitchen [TOP niche]. Evaluate, do not delete. (Likely already PUBLISHED in amazon10 -> not a draft.)"},
]


def find_repo_root(start):
    cur = os.path.abspath(start)
    while cur != os.path.dirname(cur):
        if os.path.isdir(os.path.join(cur, "10_OUTPUTS")):
            return cur
        cur = os.path.dirname(cur)
    return start


def pull_live_drafts():
    """READ-ONLY: capture the AutoDS draft list API and return [{id,title,err,stock,region}]."""
    from playwright.sync_api import sync_playwright
    bodies = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(storage_state=STATE, viewport={"width": 1440, "height": 1000})
        pg = ctx.new_page()

        def cap(r):
            try:
                if "v2-api.autods.com/products/" in r.url and "/list/" in r.url and \
                   "json" in (r.headers or {}).get("content-type", ""):
                    bodies.append(r.text())
            except Exception:
                pass

        pg.on("response", cap)
        pg.goto(BASE + "/upload", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(9000)
        try:
            pg.get_by_text(re.compile(r"^\s*Expand all\s*$", re.I)).first.click(timeout=4000)
            pg.wait_for_timeout(3000)
        except Exception:
            pass
        pg.wait_for_timeout(2000)
        b.close()
    drafts = {}
    for body in bodies:
        try:
            data = json.loads(body)
        except Exception:
            continue
        for it in (data.get("results") or []):
            if not isinstance(it, dict):
                continue
            pid = str(it.get("id") or it.get("_id") or "")
            if not pid or pid in drafts:
                continue
            el = it.get("error_list") or []
            codes = ",".join((e.get("error_code") or "") for e in el) or "-"
            vs = it.get("variation_statistics") or {}
            drafts[pid] = {"id": pid, "title": it.get("title", ""), "err": codes,
                           "stock": vs.get("in_stock"), "region": vs.get("supplier_default_region")}
    return list(drafts.values())


def classify(drafts):
    rows = []
    for d in drafts:
        t = d["title"] or ""
        keep_hit = next((k for k in KEEP if k["rx"].search(t)), None)
        kill_hit = next((k for k in KILL if k["rx"].search(t)), None)
        if keep_hit and kill_hit:
            d["_conflict"] = (keep_hit["key"], kill_hit["key"])
        d["_keep"] = keep_hit
        d["_kill"] = kill_hit
        rows.append(d)
    return rows


def main():
    ap = argparse.ArgumentParser(description="Guarded dry-run draft delete (no real delete here).")
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--confirm", action="store_true", help="(BLOCKED) real delete needs separate GO + wired mechanism")
    args = ap.parse_args()

    if not os.path.exists(STATE):
        print("FAIL: storage_state.json not found."); return 3

    root = find_repo_root(HERE)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    print("=" * 92)
    print("GUARDED DRAFT-DELETE — DRY-RUN  | run:", ts)
    print("keep-list (protected):", [k["key"] for k in KEEP], "| kill-list (proposed):", [k["key"] for k in KILL])
    print("=" * 92)

    drafts = pull_live_drafts()
    rows = classify(drafts)

    # HARD GUARD: any keep draft also matched by a kill regex -> ABORT entirely
    conflicts = [d for d in rows if d.get("_conflict")]
    if conflicts:
        print("ABORT — keep/kill overlap on a live draft (keep must win):")
        for d in conflicts:
            print("   ", d["_conflict"], "->", d["title"][:60])
        return 2

    to_delete = [d for d in rows if d["_kill"] and not d["_keep"]]
    protected = [d for d in rows if d["_keep"]]
    retained = [d for d in rows if not d["_kill"] and not d["_keep"]]

    print("\nLIVE DRAFTS PULLED:", len(rows))
    print("-" * 92)
    print("WOULD DELETE (kill-list matches):", len(to_delete))
    for d in to_delete:
        k = d["_kill"]
        print("\n  • ID %s  err=%s  stock=%s  region=%s" % (d["id"], d["err"], d["stock"], d["region"]))
        print("    title   : %s" % d["title"][:78])
        print("    reason  : %s" % k["reason"])
        print("    risk    : %s" % k["risk"])
        print("    rollback: %s" % k["rollback"])
        print("    source  : %s" % k["source"])

    print("\n" + "-" * 92)
    print("PROTECTED (keep-list, never deleted):", len(protected))
    for d in protected:
        print("  • KEEP id %s | %s" % (d["id"], d["title"][:70]))
    not_present = [k for k in KEEP if not any(r.get("_keep", {}) and r["_keep"]["key"] == k["key"] for r in rows)]
    for k in not_present:
        print("  • KEEP '%s' — NOT a current draft (expected: published in amazon10). %s" % (k["key"], k["note"]))

    print("\nRETAINED (not in kill-list, left untouched):", len(retained))
    for d in retained:
        print("  • id %s  err=%s | %s" % (d["id"], d["err"], d["title"][:64]))

    # kill-list targets not found among live drafts (already gone?)
    matched_keys = {d["_kill"]["key"] for d in to_delete}
    missing = [k for k in KILL if k["key"] not in matched_keys]
    if missing:
        print("\nKILL targets NOT found among live drafts (already deleted/published?):",
              [k["key"] for k in missing])

    print("\n" + "=" * 92)
    if args.confirm:
        print("--confirm requested: BLOCKED. Real delete requires (a) a SEPARATE owner GO and (b) the")
        print("draft-delete UI flow wired + cold-tested. This tool performs DRY-RUN ONLY by design.")
        return 1
    print("DRY-RUN complete. NOTHING deleted. %d draft(s) would be removed on GO; %d retained; keep-list safe." %
          (len(to_delete), len(retained)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
