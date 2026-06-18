#!/usr/bin/env python3
"""
AutoDS READ-ONLY connection test for eBay store divinit-92-us.

SAFETY CONTRACT (do not weaken):
- Python standard library ONLY (no pip installs).
- Loads secrets from a local .env ONLY (gitignored). NEVER prints the JWT/API key or any secret VALUE.
- Issues ONLY HTTP GET requests (read-only/idempotent). No POST/PUT/PATCH/DELETE anywhere in this file.
- Fails SAFELY (clear message, non-zero exit) if credentials are missing.
- Logs status code + endpoint path + a safe meta summary (key NAMES, match yes/no). Never dumps response VALUES.
- NEVER imports/publishes/updates/relists/deletes anything.

GO scope: GO_AUTODS_READ_SESSION (read-only). Base URL + user id are owner-provided via .env.
Updated 2026-06-16 for v2-api.autods.com + AUTODS_USER_ID.
"""
import json
import os
import sys
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ENV_CANDIDATES = [os.path.join(HERE, ".env"), os.path.join(os.getcwd(), ".env")]
DEFAULT_BASE_URL = "https://gw.autods.com"   # verified gateway; .env overrides (owner uses https://v2-api.autods.com)
TIMEOUT = 20
KEYS = ("AUTODS_API_BASE_URL", "AUTODS_API_KEY", "AUTODS_JWT",
        "AUTODS_STORE_NAME", "AUTODS_STORE_ID", "AUTODS_USER_ID")


def load_env():
    env = {}
    for path in ENV_CANDIDATES:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
            break
    for k in KEYS:
        if k not in env and os.environ.get(k):
            env[k] = os.environ[k]
    return env


def build_candidates(base, user_id):
    """Read-only GET candidates (no verified v2-api spec → probe a small ordered set)."""
    base = base.rstrip("/")
    c = []
    if user_id:
        c += ["%s/users/%s" % (base, user_id),
              "%s/user/%s" % (base, user_id),
              "%s/users/%s/details" % (base, user_id)]
    c += ["%s/v1/users/current" % base,
          "%s/auto-order-v3/users/external/user-details" % base]
    # de-dup, keep order
    seen, out = set(), []
    for u in c:
        if u not in seen:
            seen.add(u); out.append(u)
    return out


def get(url, token):
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", "Bearer " + token)   # token used, never printed
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.status, resp.read(300000)


def safe_summary(raw, store_name, user_id):
    try:
        data = json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        print("    response: non-JSON/unparseable (%d bytes)" % len(raw)); return
    if isinstance(data, dict):
        names = list(data.keys())
        print("    response: JSON object, %d top-level keys: %s" % (len(names), ", ".join(names[:40])))
        blob = json.dumps(data).lower()
        if user_id:
            print("    user_id %s present: %s" % (user_id, "yes" if str(user_id).lower() in blob else "no"))
        if store_name:
            print("    store '%s' present: %s" % (store_name, "yes" if store_name.lower() in blob else "no"))
    elif isinstance(data, list):
        print("    response: JSON array, %d items (values not shown)" % len(data))
    else:
        print("    response: JSON scalar (value not shown)")


def main():
    env = load_env()
    token = env.get("AUTODS_JWT") or env.get("AUTODS_API_KEY")
    base = env.get("AUTODS_API_BASE_URL") or DEFAULT_BASE_URL
    user_id = env.get("AUTODS_USER_ID", "")
    store_name = env.get("AUTODS_STORE_NAME", "")

    if not token:
        print("CREDENTIAL ACTION REQUIRED")
        print("Missing AUTODS_JWT (or AUTODS_API_KEY) in a local .env. Never paste secrets in chat.")
        return 2

    print("AutoDS READ-ONLY connection test (GET only — no writes).")
    print("  base_url   :", base)
    print("  jwt        : present (value hidden)")
    print("  user_id    :", user_id or "(not set)")
    print("  store_name :", store_name or "(not set)")
    print("  candidates : read-only GET probe (first 2xx wins)")

    any_response = False
    auth_fail = False
    ok = False
    for url in build_candidates(base, user_id):
        path = url[len(base.rstrip("/")):]
        try:
            status, raw = get(url, token)
        except urllib.error.HTTPError as e:
            any_response = True
            print("  [%s] GET %s" % (e.code, path))
            if e.code in (401, 403):
                auth_fail = True
            continue
        except Exception as e:  # noqa: BLE001
            print("  [ERR:%s] GET %s" % (type(e).__name__, path))
            continue
        any_response = True
        print("  [%s] GET %s   <-- OK" % (status, path))
        safe_summary(raw, store_name, user_id)
        ok = True
        break

    print("-" * 50)
    print("RESULT:")
    print("  autods_reachable :", "yes" if any_response else "NO (no server response)")
    if ok:
        print("  auth_valid       : yes (2xx on a read endpoint)")
    elif auth_fail:
        print("  auth_valid       : NO (401/403 — JWT invalid/expired or no API access)")
    elif any_response:
        print("  auth_valid       : uncertain (server responded but no 2xx; likely wrong v2-api path)")
    else:
        print("  auth_valid       : unknown (not reachable)")
    print("  safe_next_action :", "GO_IMPORT_5_DRAFTS prep" if ok else "fix base/endpoint or credentials")
    print("DONE — read-only test complete. Nothing was written.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
