#!/usr/bin/env python3
"""Strategy simulator — model & rank the autonomous-income options.

Monte Carlo over a 90-day horizon for a solo beginner starting near-zero, part
time. It compares the streams in this repo on speed-to-first-dollar, chance of
being net-positive by day 90, projected profit, effort, and credit cost.

IMPORTANT: every number here is a MODELED PROJECTION from the documented
assumptions below — not real sales. It exists to rank feasibility, not to
promise income. Re-run with your own assumptions as reality comes in.

    python3 business/tools/simulate.py [--runs 5000] [--seed 7]
"""
import argparse
import random
import statistics as st

# ---- Assumptions (edit these; they are the whole model) --------------------
# Per strategy, per-month: (min,mode,max) triangular for orders/units, revenue
# per unit, variable cost fraction, monthly fixed cost, setup delay in months
# before any income is possible, and effort hours/week.
STRATEGIES = {
    "Fiverr AI-writing service (engine)": {
        # 'traction' = chance the channel gets ANY demand that month (the
        # cold-start reality: no reviews yet -> often nothing early on).
        "traction": [0.45, 0.70, 0.85],
        "orders": [(0, 1, 3), (1, 2, 8), (2, 5, 15)],   # ramps as reviews accrue
        "rev_per": (30, 55, 120), "fee": 0.20,
        "credit_per_order_opt": 0.05, "credit_per_order_base": 0.30,
        "fixed": 0.0, "setup_delay": 0, "hrs": 6,
        "recurring": False,
    },
    "Digital products (Gumroad)": {
        "traction": [0.28, 0.42, 0.55],                 # traffic-dependent; often zero
        "orders": [(0, 0, 4), (0, 1, 8), (0, 2, 12)],
        "rev_per": (19, 29, 59), "fee": 0.11,
        "credit_per_order_opt": 0.0, "credit_per_order_base": 0.0,
        "fixed": 0.0, "setup_delay": 0, "hrs": 3,
        "recurring": False,
    },
    "Clipping (pay-per-view)": {
        # 'orders' = $100 payout units/month; you post -> you get some views.
        "traction": [0.80, 0.90, 0.95],
        "orders": [(0, 1, 5), (0, 3, 12), (1, 6, 25)],
        "rev_per": (100, 100, 100), "fee": 0.0,
        "credit_per_order_opt": 0.0, "credit_per_order_base": 0.0,
        "fixed": 0.0, "setup_delay": 0, "hrs": 10,
        "recurring": False,
    },
    "Voice-receptionist bundle": {
        "traction": [0.15, 0.45, 0.60],                 # outreach is slow
        "orders": [(0, 0, 1), (0, 1, 2), (0, 1, 2)],
        "rev_per": (199, 297, 497), "fee": 0.0,
        "credit_per_order_opt": 25.0, "credit_per_order_base": 45.0,
        "fixed": 20.0, "setup_delay": 0, "hrs": 8,
        "recurring": True,
    },
    "Meta-agent / outbound (build last)": {
        "traction": [0.0, 0.25, 0.5],
        "orders": [(0, 0, 0), (0, 0, 1), (0, 1, 2)],
        "rev_per": (199, 297, 497), "fee": 0.0,
        "credit_per_order_opt": 25.0, "credit_per_order_base": 45.0,
        "fixed": 30.0, "setup_delay": 1, "hrs": 10,
        "recurring": True,
    },
}


def tri(t):
    return random.triangular(t[0], t[2], t[1])


def run_once(cfg, optimized=True):
    """Return (net_90d, first_income_month or None, credit_cost_90d)."""
    net = 0.0
    active_clients = 0  # for recurring
    first = None
    credit_total = 0.0
    ckey = "credit_per_order_opt" if optimized else "credit_per_order_base"
    for m in range(3):  # months 1..3
        if m < cfg["setup_delay"]:
            net -= cfg["fixed"]
            continue
        # Cold-start reality: many months the channel gets no traction at all.
        if random.random() > cfg["traction"][m]:
            net -= cfg["fixed"]
            if cfg["recurring"]:  # existing clients still pay/cost
                net += active_clients * (tri(cfg["rev_per"]) - cfg["credit_per_order_opt"]) \
                    if active_clients else 0
            continue
        units = max(0, round(tri(cfg["orders"][m])))
        gross = 0.0
        credit = 0.0
        if cfg["recurring"]:
            active_clients += units
            gross = active_clients * tri(cfg["rev_per"])
            credit = active_clients * cfg[ckey]
        else:
            gross = sum(tri(cfg["rev_per"]) for _ in range(units))
            credit = units * cfg[ckey]
        income = gross * (1 - cfg["fee"]) - credit - cfg["fixed"]
        credit_total += credit
        net += income
        if first is None and gross > 0:
            first = m + 1
    return net, first, credit_total


def summarize(cfg, runs, optimized=True):
    nets, firsts, credits, pos = [], [], [], 0
    for _ in range(runs):
        net, first, credit = run_once(cfg, optimized)
        nets.append(net)
        credits.append(credit)
        if first:
            firsts.append(first)
        if net > 0:
            pos += 1
    nets.sort()
    p = lambda q: nets[int(q * (len(nets) - 1))]  # noqa: E731
    return {
        "p10": p(0.10), "p50": p(0.50), "p90": p(0.90),
        "prob_income": len(firsts) / runs,
        "prob_profit": pos / runs,
        "med_first_month": (st.median(firsts) if firsts else None),
        "credit_med": st.median(credits),
        "hrs": cfg["hrs"],
    }


def feasibility(s):
    """Composite for a beginner wanting real results, low friction, cheap."""
    speed = {1: 1.0, 2: 0.6, 3: 0.3, None: 0.0}[s["med_first_month"]]
    return round(
        0.34 * s["prob_profit"] + 0.26 * speed + 0.20 * s["prob_income"]
        + 0.12 * (1 - min(s["credit_med"] / 100, 1))     # cheaper = better
        + 0.08 * (1 - min(s["hrs"] / 12, 1)), 3)          # less effort = better


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    random.seed(a.seed)

    rows = []
    for name, cfg in STRATEGIES.items():
        s = summarize(cfg, a.runs, optimized=True)
        s["name"] = name
        s["score"] = feasibility(s)
        rows.append(s)
    rows.sort(key=lambda r: -r["score"])

    print("=" * 78)
    print(f"  STRATEGY SIMULATION  ({a.runs:,} runs, 90-day horizon, "
          f"credit-optimized)")
    print("  MODELED PROJECTIONS from stated assumptions — not real sales.")
    print("=" * 78)
    print(f"  {'strategy':<34}{'feas':>6}{'P50 net':>10}"
          f"{'profit%':>9}{'1st $':>8}")
    print("-" * 78)
    for r in rows:
        first = f"mo{int(r['med_first_month'])}" if r["med_first_month"] else "—"
        print(f"  {r['name']:<34}{r['score']:>6.2f}"
              f"{('$' + format(r['p50'], ',.0f')):>10}"
              f"{r['prob_profit'] * 100:>8.0f}%{first:>8}")
    print("-" * 78)
    top = rows[0]
    print(f"  P10/P50/P90 net for the winner ({top['name']}):")
    print(f"    ${top['p10']:,.0f}  /  ${top['p50']:,.0f}  /  ${top['p90']:,.0f}"
          f"   over 90 days")
    print(f"    Chance of any income by mo1: {top['prob_income']*100:.0f}%  |  "
          f"median credit spend: ${top['credit_med']:.2f}/90d")

    # Credit-optimization effect on the engine-backed service.
    key = "Fiverr AI-writing service (engine)"
    opt = summarize(STRATEGIES[key], a.runs, optimized=True)
    base = summarize(STRATEGIES[key], a.runs, optimized=True)  # nets same rev
    base_credit = st.median(
        [run_once(STRATEGIES[key], optimized=False)[2] for _ in range(a.runs)])
    print("-" * 78)
    print("  CREDIT OPTIMIZATION (engine service, median 90-day credit cost):")
    print(f"    Before (Opus, no cache):  ${base_credit:,.2f}")
    print(f"    After  (tiered + cache):  ${opt['credit_med']:,.2f}   "
          f"→ ~{(1 - opt['credit_med']/max(base_credit,1e-9))*100:.0f}% cheaper")
    print("=" * 78)
    print("  Verdict: rank is feasibility for a beginner (speed + odds of being")
    print("  net-positive + low cost/effort), NOT max theoretical upside.")


if __name__ == "__main__":
    main()
