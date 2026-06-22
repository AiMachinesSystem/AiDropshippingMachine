"""
eBay/AutoDS — cycle 3 study: PRICE ELASTICITY + CAPITAL ALLOCATION (INTERNA).

Q1 (pricing): on a price-sorted commodity marketplace, what markup maximizes WEEKLY profit?
  Demand follows constant elasticity: orders(p) = base * (p/p0)^(-e).
  profit/order = p*(1-FVF) - per_order_fee - cost.  Sweep p, MC over (e, cost).
Q2 (allocation): given limited attention/fulfillment slots, does concentrating on the best
  SKUs beat spreading evenly? Greedy-by-(profit*velocity) vs uniform, on sampled archetypes.

Anchors: AOV/market ref p0=$106.67 (OBSERVED), FVF 13.6%+$0.40 (canon). Cost/elasticity sampled.
Outputs COMPUTED; [ESTIMATE] (elasticity not measured on our listings). Seed fixed.
"""
import random, statistics

random.seed(11)
N = 20000
P0 = 106.67          # market reference price (= current AOV)
FVF = 0.136
FEE = 0.40
BASE_ORDERS = 1.0    # per-listing weekly demand at p0 (relative)

def uni(a, b): return random.uniform(a, b)

# ---------- Q1: optimal markup under elasticity ----------
def weekly_profit(p, e, cost):
    demand = BASE_ORDERS * (p / P0) ** (-e)
    ppo = p * (1 - FVF) - FEE - cost
    return demand * ppo

opt_p, opt_markup_cost, opt_vs_p0 = [], [], []
grid = [P0 * m for m in [x / 100 for x in range(70, 181, 1)]]  # 0.70x..1.80x of market
for _ in range(N):
    e = uni(1.5, 3.0)             # commodity buyers are price-sensitive
    cost = P0 * uni(0.40, 0.60)   # landed cost = 40-60% of market (AliExpress band)
    best_p = max(grid, key=lambda p: weekly_profit(p, e, cost))
    opt_p.append(best_p)
    opt_markup_cost.append(best_p / cost)
    opt_vs_p0.append(best_p / P0)

def med(x): return statistics.median(x)
def pct(x, q): return sorted(x)[int(q * len(x))]

print("Q1 — PROFIT-MAXIMIZING PRICE (MC, elasticity 1.5-3.0, cost 40-60% of market):")
print(f"  optimal price            : ${med(opt_p):.2f}  [P10 ${pct(opt_p,.1):.2f} – P90 ${pct(opt_p,.9):.2f}]")
print(f"  optimal markup over COST : {med(opt_markup_cost):.2f}x  [{pct(opt_markup_cost,.1):.2f}–{pct(opt_markup_cost,.9):.2f}]")
print(f"  optimal price vs MARKET  : {med(opt_vs_p0)*100:.0f}% of market price  [{pct(opt_vs_p0,.1)*100:.0f}%–{pct(opt_vs_p0,.9)*100:.0f}%]")

# compare: profit at optimum vs profit at "match market" (p0) vs "current 27% markup on cost"
def avg_profit_at(strategy):
    tot = 0.0
    for _ in range(N):
        e = uni(1.5, 3.0); cost = P0 * uni(0.40, 0.60)
        if strategy == "opt":
            p = max(grid, key=lambda pp: weekly_profit(pp, e, cost))
        elif strategy == "match":
            p = P0
        elif strategy == "mk27":
            p = cost * 1.27
        tot += weekly_profit(p, e, cost)
    return tot / N
po, pm, pc = avg_profit_at("opt"), avg_profit_at("match"), avg_profit_at("mk27")
print(f"\n  avg weekly profit/listing — optimal ${po:.2f} · match-market ${pm:.2f} · current 27%-markup ${pc:.2f}")
print(f"  => pricing at optimum beats match-market by {(po/pm-1)*100:.0f}%, beats 27%-markup by {(po/pc-1)*100:.0f}%")

# ---------- Q2: concentrate vs spread ----------
print("\nQ2 — CAPITAL/ATTENTION ALLOCATION (10 archetype SKUs, 4 active slots):")
def trial_alloc():
    skus = []
    for _ in range(10):
        margin = uni(0.20, 0.55); vel = uni(0.2, 4.0)  # weekly orders potential
        skus.append(margin * P0 * vel)                 # weekly profit potential
    skus.sort(reverse=True)
    concentrate = sum(skus[:4])         # top 4 by potential
    uniform = sum(skus) * 4 / 10        # 4 slots' worth spread evenly across all 10
    return concentrate, uniform
con = [trial_alloc() for _ in range(N)]
mc = statistics.mean(c for c, _ in con); mu = statistics.mean(u for _, u in con)
print(f"  concentrate on top-4   : ${mc:.0f}/wk")
print(f"  spread across 10       : ${mu:.0f}/wk")
print(f"  => concentration beats spreading by {(mc/mu-1)*100:.0f}%")
