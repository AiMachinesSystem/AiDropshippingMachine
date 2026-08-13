#!/usr/bin/env python3
"""TITLE FIXER v1 — repairs eBay titles that were truncated mid-word by a fixed-length cut.
DRAFT ONLY: writes a review CSV. Publishes nothing, touches no live listing.

Repair chain, deterministic and reversible:
  1. strip trailing punctuation / connector words ("... with", "... for", "... and", "... ,")
  2. drop a trailing word fragment (1-2 letters, or a token that is a prefix of nothing)
  3. collapse duplicated phrases ("Power Strip ... Power Strip")
  4. re-fill the free space up to 80 with category keywords not already present
  5. hard cap 80, always cut on a word boundary
"""
import os, re, csv, sqlite3
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "catalog.db")
MAXLEN = 80

CONNECTORS = {"with","for","and","the","a","an","of","in","on","to","by","or","w","is","are",
              "non","anti","ultra","super","multi","pro","plus","up","from","that","this","your","&"}

def strip_tail(t):
    """remove trailing punctuation and dangling connector/fragment tokens, repeatedly"""
    changed = True
    while changed and t:
        changed = False
        t2 = t.rstrip(" ,-–—&/|(:;.")
        if t2 != t: t, changed = t2, True
        toks = t.split()
        if not toks: break
        last = re.sub(r"[^A-Za-z0-9]", "", toks[-1])
        # dangling connector, or a 1-2 letter alphabetic fragment, or a lone number+unit start
        if last.lower() in CONNECTORS or (len(last) <= 2 and last.isalpha()):
            t = " ".join(toks[:-1]); changed = True
    return t.strip()

def collapse_adjacent(t):
    """collapse only an IMMEDIATELY repeated 2-4 word phrase — safe, never reorders meaning"""
    toks = t.split()
    for n in (4, 3, 2):
        i, out = 0, []
        while i < len(toks):
            if i + 2*n <= len(toks) and [w.lower() for w in toks[i:i+n]] == [w.lower() for w in toks[i+n:i+2*n]]:
                out.extend(toks[i:i+n]); i += 2*n
            else:
                out.append(toks[i]); i += 1
        toks = out
    return " ".join(toks)


def dedupe_phrases(t):
    """collapse an immediately repeated 2-3 word phrase, and repeated single words"""
    toks = t.split()
    for n in (3, 2):
        i = 0; out = []
        while i < len(toks):
            if i + 2*n <= len(toks) and [w.lower() for w in toks[i:i+n]] == [w.lower() for w in toks[i+n:i+2*n]]:
                out.extend(toks[i:i+n]); i += 2*n
            else:
                out.append(toks[i]); i += 1
        toks = out
    seen = OrderedDict(); out = []
    for w in toks:
        k = re.sub(r"[^a-z0-9]", "", w.lower())
        if k and len(k) > 3 and seen.get(k):
            continue
        seen[k] = True; out.append(w)
    return " ".join(out)

def cut80(t, limit=MAXLEN):
    if len(t) <= limit: return t
    cut = t[:limit]
    if " " in cut: cut = cut[:cut.rfind(" ")]
    return strip_tail(cut)

def enrich(t, category):
    """append category words that add search coverage, only if they fit"""
    if not category or category.startswith("Other") or category == "(vuota)":
        return t
    have = set(re.sub(r"[^a-z0-9 ]", " ", t.lower()).split())
    add = [w for w in re.split(r"[\s,&/]+", category)
           if w and len(w) > 2 and w.lower() not in have and w.lower() not in CONNECTORS]
    for w in add:
        cand = f"{t} {w}"
        if len(cand) <= MAXLEN: t = cand; have.add(w.lower())
        else: break
    return t

con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
rows = con.execute("SELECT * FROM listing WHERE trunc=1 OR over80=1 ORDER BY sold DESC, title_len DESC").fetchall()

out = []
for r in rows:
    old = r["title"]
    # v2 CONSERVATIVE: only remove what is broken. No keyword enrichment, no cross-phrase
    # dedupe — both produced ungrammatical output ("Groom like Brushes Combs") on real data.
    # Adjacent exact repeats are still collapsed; that failure mode is safe.
    t = strip_tail(old)
    t = collapse_adjacent(t)
    t = cut80(t)
    t = strip_tail(t)
    out.append({
        "item_id": r["item_id"], "id": r["id"], "category": r["category"], "sold": r["sold"],
        "old_len": len(old), "new_len": len(t), "changed": int(t != old),
        "old_title": old, "new_title": t, "url": r["url"],
    })
con.close()

changed = [o for o in out if o["changed"]]
bad = [o for o in out if o["new_len"] > MAXLEN or not o["new_title"]]
print(f"candidati: {len(out)}   riscritti: {len(changed)}   invariati: {len(out)-len(changed)}")
print(f"lunghezza nuova: min {min(o['new_len'] for o in out)} / max {max(o['new_len'] for o in out)}")
print(f"violazioni residue (>80 o vuoti): {len(bad)}")
print("\n--- 12 esempi PRIMA / DOPO ---")
for o in changed[:12]:
    print(f"  [{o['old_len']:>3}] {o['old_title']}")
    print(f"  [{o['new_len']:>3}] {o['new_title']}")
    print()

p = os.path.join(HERE, "title_fix_review.csv")
with open(p, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print("CSV:", p)
