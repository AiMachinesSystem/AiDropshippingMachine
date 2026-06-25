#!/usr/bin/env python3
"""
ebay_demand_gate.py — pure offline logic: net-profit at REAL avg sold price (owner formula) + the 3-stage
demand funnel (permissive ENTRY -> balanced VALIDATE -> severe SCALE), per owner "3 -> 2 -> 1".
No network. Run directly for the self-test. Import `assess(...)` from the profit-engine.
"""

# net-profit formula (owner): price - cost - ship/tax - (FVF% + $0.40) - promoted - autods - return reserve
FEE_PCT, FEE_FIXED, SHIP_TAX, AUTODS, RETURN_RES = 0.135, 0.40, 3.00, 0.50, 2.00

# tunable funnel thresholds
STAGES = {
    "ENTRY":    {"sell_through": 25, "sold_per_mo": 3,  "net": 3.0},   # permissive — admit ~3 to test
    "VALIDATE": {"sell_through": 40, "sold_per_mo": 10, "net": 4.0},   # balanced — keep ~2 (after 7-day live data)
    "SCALE":    {"sell_through": 60, "sold_per_mo": 30, "net": 5.0},   # severe — keep ~1 winner to scale
}


def net_profit(price, amazon_cost, promoted=0.0):
    if not (isinstance(price, (int, float)) and isinstance(amazon_cost, (int, float))):
        return None
    return round(price - amazon_cost - SHIP_TAX - (FEE_PCT * price + FEE_FIXED) - promoted - AUTODS - RETURN_RES, 2)


def assess(avg_sold_price, sold_per_mo, sell_through_pct, amazon_cost, live_signal=False, sales_proven=False, account_clean=True):
    """Return funnel stage for a candidate. avg_sold_price = REAL Terapeak avg sold (the eBay selling price)."""
    net = net_profit(avg_sold_price, amazon_cost)
    nm = round(100 * net / avg_sold_price, 1) if (net is not None and avg_sold_price) else None
    st, sm = (sell_through_pct or 0), (sold_per_mo or 0)

    def meets(stage):
        s = STAGES[stage]
        return (st >= s["sell_through"]) and (sm >= s["sold_per_mo"]) and (net is not None and net >= s["net"])

    if meets("SCALE") and sales_proven and account_clean:
        stage = "SCALE"
    elif meets("VALIDATE") and live_signal:
        stage = "VALIDATE"
    elif meets("ENTRY"):
        stage = "ENTRY"
    else:
        stage = "REJECT"
    reason = "ST=%s%% sold=%s/mo net=$%s (%s%%)" % (st, sm, net, nm)
    return {"stage": stage, "net": net, "net_margin_pct": nm, "max_safe_ad": net, "reason": reason}


def _selftest():
    cases = [
        ("strong winner", dict(avg_sold_price=49.99, sold_per_mo=40, sell_through_pct=65, amazon_cost=29.99, live_signal=True, sales_proven=True), "SCALE"),
        ("validate-level", dict(avg_sold_price=49.99, sold_per_mo=15, sell_through_pct=45, amazon_cost=29.99, live_signal=True), "VALIDATE"),
        ("entry-only", dict(avg_sold_price=49.99, sold_per_mo=5, sell_through_pct=30, amazon_cost=29.99), "ENTRY"),
        ("thin-margin reject", dict(avg_sold_price=44.39, sold_per_mo=20, sell_through_pct=50, amazon_cost=39.99), "REJECT"),
        ("no-demand reject", dict(avg_sold_price=49.99, sold_per_mo=1, sell_through_pct=10, amazon_cost=29.99), "REJECT"),
    ]
    ok = True
    print("ebay_demand_gate self-test (owner formula + 3-stage funnel):")
    for name, kw, expect in cases:
        r = assess(**kw)
        passed = r["stage"] == expect
        ok = ok and passed
        print("  [%s] %-20s -> %-8s (exp %-8s) | %s" % ("PASS" if passed else "FAIL", name, r["stage"], expect, r["reason"]))
    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(_selftest())
