#!/usr/bin/env python3
"""
eBay login + session saver (Playwright) — UNBLOCK eBay sold-data (Terapeak/sold-listings).

WHAT IT DOES
- Opens a VISIBLE (non-headless) Chromium so the OWNER logs into eBay by hand (handles 2FA/captcha).
- Navigates to signin.ebay.com; the owner completes login in the window.
- On success (landed on an authenticated ebay.com page, NOT signin), saves the session to
  `ebay_storage_state.json` (gitignored) for reuse by read_ebay_sold.py — which then reads SOLD
  comps that are 403-walled to anonymous scraping.

SAFETY CONTRACT (do not weaken)
- MANUAL login only: this script types NO credentials. The owner logs in by hand. No secrets read/printed.
- Login ONLY: no listing, no offer, no order, no message, no write of any kind.
- The saved ebay_storage_state.json contains session cookies — gitignored, NEVER commit it.

GO scope: GO_EBAY_LOGIN (login + save session only). Run: python ebay_login_and_save_session.py
"""
import os, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STATE = os.path.join(HERE, "ebay_storage_state.json")
SIGNIN_URL = "https://signin.ebay.com/ws/eBayISAPI.dll?SignIn"


def _authed(u):
    # success = on an ebay.com page that is NOT the sign-in flow
    return ("ebay.com" in u) and ("signin.ebay.com" not in u) and ("/signin" not in u.lower())


def main():
    ap = argparse.ArgumentParser(description="eBay manual login + save session (visible browser).")
    ap.add_argument("--state", default=DEFAULT_STATE)
    ap.add_argument("--login-timeout", type=int, default=300000, help="Max ms to wait for login (default 5 min).")
    ap.add_argument("--slowmo", type=int, default=80)
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        print("FAIL: playwright not importable. Activate the venv first.")
        return 3

    print("eBay login + save session (VISIBLE browser) — MANUAL login by the owner.")
    print("  url        :", SIGNIN_URL)
    print("  save state :", args.state)
    print("  -> Log in to eBay in the window (complete any 2FA/captcha). Then wait for the save.")
    print("-" * 64)

    logged_in = False
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=False, slow_mo=args.slowmo)
            ctx = b.new_context(
                viewport={"width": 1366, "height": 900},
                user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
            )
            page = ctx.new_page()
            page.goto(SIGNIN_URL, wait_until="load", timeout=60000)
            print("  [..] waiting up to %ds for you to finish logging in..." % (args.login_timeout // 1000))
            try:
                page.wait_for_url(lambda u: _authed(u), timeout=args.login_timeout)
                logged_in = True
            except PWTimeout:
                logged_in = _authed(page.url)
            if logged_in:
                page.wait_for_timeout(2500)
                ctx.storage_state(path=args.state)
                print("  [ok] login detected — url:", page.url)
                print("  [ok] session saved to:", args.state)
            else:
                print("  [!!] still on sign-in — login not completed. Session NOT saved.")
            b.close()
    except Exception as e:  # noqa: BLE001
        print("  [ERR] %s: %s" % (type(e).__name__, e))
        print("RESULT: FAIL"); return 1

    print("-" * 64)
    if logged_in and os.path.exists(args.state):
        print("RESULT: PASS — eBay session saved (%d bytes). read_ebay_sold.py can now read sold comps." % os.path.getsize(args.state))
        return 0
    print("RESULT: FAIL — no session saved."); return 1


if __name__ == "__main__":
    sys.exit(main())
