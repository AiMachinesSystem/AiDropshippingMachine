"""
eBay/AutoDS dropshipping — profitability Monte Carlo.

PURPOSE: practice/learn which strategic lever maximizes profit, by SIMULATING the
P&L under different strategies. All priors anchor on OBSERVED account data
(autods_status_report 2026-06-16) + margin canon (PROFITABILITY_VS_COMPETITION 2026-06-17).
Outputs are COMPUTED (not invented); they are still [ESTIMATE] because the base sample
is 1 week / 3 orders (LOW-SAMPLE). Seed fixed for reproducibility.

Model per strategy over a horizon of H weeks:
  orders/week follows logistic growth from baseline 3 toward a strategy ceiling K, rate r.
  profit/order = AOV * net_margin (both sampled per strategy).
  net profit/week = orders/wk * profit/order - AutoDS/wk - ad_cost (if promoted).
"""
import random, statistics

random.seed(42)

# --- OBSERVED baseline (hard numbers) ---
BASE_ORDERS_WK = 3.0          # last 7d
BASE_AOV = 106.67             # $320/3
BASE_MARGIN = 0.194           # $62/$320 net
AUTODS_WK = 29.90 / 4.33      # ~$6.90/wk subscription

N = 20000
HORIZONS = {"3mo": 13, "6mo": 26, "12mo": 52}

def tri(a, b, c):  # triangular: low, mode, high
    return random.triangular(a, c, b)

def uni(a, b):
    return random.uniform(a, b)

# Strategy = (ceiling K range, growth rate r range, margin range, AOV mult range, ad_rate range)
# K = sustainable orders/week ceiling. r = logistic rate (per week).
STRATEGIES = {
    "S0 status-quo (Amazon, broken fulfill)": dict(
        K=(2, 4, 6), r=(0.02, 0.06), margin=(0.15, 0.22), aovx=(0.95, 1.05), ad=(0.0, 0.0)),
    "S1 fix fulfill + clean catalog": dict(
        K=(7, 12, 20), r=(0.06, 0.14), margin=(0.17, 0.24), aovx=(0.95, 1.10), ad=(0.0, 0.0)),
    "S2 + AliExpress sourcing": dict(
        K=(8, 14, 24), r=(0.06, 0.14), margin=(0.35, 0.50), aovx=(1.00, 1.20), ad=(0.0, 0.0)),
    "S3 + promoted listings (scale winners)": dict(
        K=(18, 32, 60), r=(0.10, 0.20), margin=(0.33, 0.48), aovx=(1.00, 1.25), ad=(0.04, 0.12)),
    "S4 full stack (all levers)": dict(
        K=(25, 45, 90), r=(0.12, 0.24), margin=(0.38, 0.52), aovx=(1.05, 1.35), ad=(0.04, 0.12)),
}

def logistic(t, K, r, x0=BASE_ORDERS_WK):
    # closed-form logistic from x0 toward K
    if K <= x0:
        return K
    A = (K - x0) / x0
    import math
    return K / (1 + A * math.exp(-r * t))

def simulate(cfg, weeks):
    K = tri(*cfg["K"]); r = uni(*cfg["r"][0], ) if False else uni(*cfg["r"])
    margin = uni(*cfg["margin"]); aov = BASE_AOV * uni(*cfg["aovx"])
    ad = uni(*cfg["ad"])
    orders = logistic(weeks, K, r)
    rev_wk = orders * aov
    gross_wk = rev_wk * margin
    ad_cost = rev_wk * ad
    net_wk = gross_wk - AUTODS_WK - ad_cost
    return net_wk / 7.0  # net profit / day

print(f"Baseline OBSERVED: {BASE_ORDERS_WK:.0f} ord/wk · AOV ${BASE_AOV:.2f} · "
      f"margin {BASE_MARGIN*100:.1f}% · net/day ${BASE_ORDERS_WK*BASE_AOV*BASE_MARGIN/7:.2f}")
print(f"Monte Carlo N={N}, seed=42. Net profit/DAY (USD) — median [P10–P90]\n")

header = f"{'Strategy':42s} " + " ".join(f"{h:>20s}" for h in HORIZONS)
print(header)
print("-" * len(header))
for name, cfg in STRATEGIES.items():
    cells = []
    for h, wks in HORIZONS.items():
        vals = sorted(simulate(cfg, wks) for _ in range(N))
        med = statistics.median(vals)
        p10 = vals[int(0.10 * N)]; p90 = vals[int(0.90 * N)]
        cells.append(f"{med:6.0f} [{p10:4.0f}-{p90:4.0f}]")
    print(f"{name:42s} " + " ".join(f"{c:>20s}" for c in cells))

# Lever sensitivity: at 6mo, isolate the marginal effect of each lever vs S1.
print("\nLEVER SENSITIVITY @ 6mo (median net/day, holding others at S1 base):")
s1 = STRATEGIES["S1 fix fulfill + clean catalog"]
def med_of(cfg, wks=26):
    return statistics.median(sorted(simulate(cfg, wks) for _ in range(N)))
base = med_of(s1)
print(f"  S1 baseline                         : ${base:5.0f}/day")
v = dict(s1); v["margin"] = (0.35, 0.50)
print(f"  + AliExpress margin only            : ${med_of(v):5.0f}/day  (+{med_of(v)-base:.0f})")
v = dict(s1); v["K"] = (18, 32, 60); v["r"] = (0.10, 0.20)
print(f"  + volume/scale only                 : ${med_of(v):5.0f}/day  (+{med_of(v)-base:.0f})")
v = dict(s1); v["aovx"] = (1.05, 1.35)
print(f"  + bundling AOV only                 : ${med_of(v):5.0f}/day  (+{med_of(v)-base:.0f})")
