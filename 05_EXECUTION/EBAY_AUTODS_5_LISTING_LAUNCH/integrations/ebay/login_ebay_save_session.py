#!/usr/bin/env python3
"""
eBay login + session saver (Playwright) — activates the Terapeak demand reader.

WHAT IT DOES
- Opens a VISIBLE (non-headless) Chromium. The OWNER signs into eBay by hand (incl. 2FA/passkey/captcha).
- Waits until you land on the authenticated eBay site (Seller Hub / signed-in), then saves the session to
  `storage_state_ebay.json` (gitignored) and closes.

SAFETY CONTRACT (do not weaken)
- Manual login only — the script NEVER types credentials. No secrets read or printed.
- Login ONLY: no listing edit, no publish, no pricing, no orders, no other writes.
- The saved storage_state_ebay.json holds session cookies — gitignored, never committed.
GO scope: GO_EBAY_LOGIN (owner account login + save session only). Mirrors the AutoDS login contract.

Usage: login_ebay_save_session.py [--url https://www.ebay.com/sh/research] [--login-timeout 300000]
Then I (the machine) run read_terapeak.py against the saved session.
"""
import os, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STATE = os.path.join(HERE, "storage_state_ebay.json")
# Land directly on Terapeak research (redirects through sign-in if not authed)
DEFAULT_URL = "https://www.ebay.com/sh/research"


def main():
    ap = argparse.ArgumentParser(description="eBay login + save session (manual, visible browser).")
    ap.add_argument("--state", default=DEFAULT_STATE)
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--login-timeout", type=int, default=300000, help="max ms to wait for sign-in (default 5 min)")
    ap.add_argument("--slowmo", type=int, default=80)
    args = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        print("FAIL: playwright not importable. Activate the venv first."); return 3

    print("eBay login + save session (VISIBLE browser). Sign in by hand; I never type your password.")
    print("  url        :", args.url, "\n  save state :", args.state)
    print("-" * 64)
    logged_in = False
    with sync_playwright() as p:
        b = p.chromium.launch(headless=False, slow_mo=args.slowmo)
        ctx = b.new_context(viewport={"width": 1366, "height": 900},
                            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
        pg = ctx.new_page()
        print("  [..] opening", args.url, "— please sign in to eBay in the window now.")
        pg.goto(args.url, wait_until="load", timeout=60000)
        print("  [..] waiting up to %ds for sign-in (complete any 2FA/passkey/captcha)" % (args.login_timeout // 1000))

        # SUCCESS = on ebay.com and NOT on a signin/login page
        def authed(u):
            return ("ebay.com" in u) and ("signin" not in u.lower()) and ("/login" not in u.lower())
        try:
            pg.wait_for_url(lambda u: authed(u), timeout=args.login_timeout)
            logged_in = True
        except PWTimeout:
            logged_in = authed(pg.url)
        if logged_in:
            pg.wait_for_timeout(3000)
            ctx.storage_state(path=args.state)
            print("  [ok] signed-in url:", pg.url)
            print("  [ok] session saved to:", args.state)
        else:
            print("  [!!] still on a sign-in page — login NOT completed; session NOT saved.")
        b.close()
    print("-" * 64)
    if logged_in and os.path.exists(args.state):
        print("RESULT: PASS — eBay session saved (%d bytes). Next: I run read_terapeak.py." % os.path.getsize(args.state))
        return 0
    print("RESULT: FAIL — no session saved."); return 1


if __name__ == "__main__":
    sys.exit(main())
