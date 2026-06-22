"""
eBay/AutoDS dropshipping — RISK-ADJUSTED Monte Carlo (cycle 2, "studia").

Extends profit_montecarlo.py with the risks the first sim ignored:
  1. Returns/refunds  — each return wipes the order profit + return shipping.
  2. Ad-cost variance — promoted-listing ACoS uncertain.
  3. ACCOUNT SUSPENSION (ruin) — monthly hazard; once suspended, profit -> 0 forever.
     Amazon-arbitrage sourcing carries HIGH hazard (policy violation); AliExpress LOW.

Anchors: OBSERVED baseline (autods_status_report 2026-06-16) + canon (2026-06-17).
Suspension hazards = DECLARED ASSUMPTIONS [ESTIMATE] (we have no measured suspension rate);
ranges chosen to be conservative and varied in MC. Outputs are COMPUTED. Seed fixed.

Metric = EXPECTED CUMULATIVE NET PROFIT over 52 weeks (sums weekly, zeroed after suspension),
plus P(survive 12mo) and P10 (downside).
"""
import random, statistics, math

random.seed(7)
N = 20000
WEEKS = 52

BASE_AOV = 106.67
AUTODS_WK = 29.90 / 4.33

def uni(a, b): return random.uniform(a, b)
def tri(a, b, c): return random.triangular(a, c, b)

# Two engines compared at an equal SCALE ceiling, differing only in sourcing risk profile.
ENGINES = {
    "Amazon-sourced (high policy risk)": dict(
        K=(20, 35, 60), r=(0.10, 0.20), margin=(0.30, 0.42), aovx=(1.00, 1.20),
        ad=(0.05, 0.12), return_rate=(0.04, 0.10),
        suspend_monthly=(0.04, 0.10)),   # high hazard: retail-arbitrage policy
    "AliExpress-sourced (low policy risk)": dict(
        K=(20, 35, 60), r=(0.10, 0.20), margin=(0.42, 0.55), aovx=(1.00, 1.25),
        ad=(0.05, 0.12), return_rate=(0.04, 0.10),
        suspend_monthly=(0.005, 0.02)),  # low hazard: compliant sourcing
}

def logistic(t, K, r, x0=3.0):
    if K <= x0: return K
    A = (K - x0) / x0
    return K / (1 + A * math.exp(-r * t))

def run(cfg):
    K = tri(*cfg["K"]); r = uni(*cfg["r"]); margin = uni(*cfg["margin"])
    aov = BASE_AOV * uni(*cfg["aovx"]); ad = uni(*cfg["ad"])
    ret = uni(*cfg["return_rate"]); haz_m = uni(*cfg["suspend_monthly"])
    haz_w = 1 - (1 - haz_m) ** (1/4.33)   # convert monthly hazard to weekly
    cum = 0.0; alive_weeks = 0
    for w in range(1, WEEKS + 1):
        if random.random() < haz_w:        # suspended this week -> dead forever
            break
        orders = logistic(w, K, r)
        rev = orders * aov
        gross = rev * margin
        # returns: lose profit on returned orders + ~ $8 return ship each
        returned = orders * ret
        gross -= returned * (aov * margin) + returned * 8.0
        net = gross - AUTODS_WK - rev * ad
        cum += net; alive_weeks = w
    return cum, alive_weeks

print(f"RISK-ADJUSTED MC  N={N}, seed=7, horizon=52wk. [ESTIMATE — suspension hazard = declared assumption]\n")
print(f"{'Engine':40s} {'E[cum 12mo]':>13s} {'median':>9s} {'P10 down':>10s} {'P(survive)':>11s}")
print("-" * 86)
for name, cfg in ENGINES.items():
    res = [run(cfg) for _ in range(N)]
    cums = sorted(c for c, _ in res)
    surv = sum(1 for _, a in res if a == WEEKS) / N
    mean = statistics.mean(cums)
    med = statistics.median(cums)
    p10 = cums[int(0.10 * N)]
    print(f"{name:40s} {mean:12,.0f}$ {med:8,.0f}$ {p10:9,.0f}$ {surv*100:9.1f}%")

# Isolate the cost of the suspension risk alone (Amazon engine with hazard zeroed).
print("\nWHAT THE SUSPENSION RISK ALONE COSTS (Amazon engine):")
amz = ENGINES["Amazon-sourced (high policy risk)"]
def emean(cfg):
    return statistics.mean(run(cfg)[0] for _ in range(N))
base = emean(amz)
nohaz = dict(amz); nohaz["suspend_monthly"] = (0.0, 0.0)
print(f"  Amazon E[cum] WITH suspension risk : {base:12,.0f}$")
print(f"  Amazon E[cum] if risk = 0          : {emean(nohaz):12,.0f}$")
print(f"  => expected $ destroyed by ruin risk: {emean(nohaz)-base:12,.0f}$")
