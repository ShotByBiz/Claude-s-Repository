#!/usr/bin/env python3
"""ROI calculator for the AI Voice Receptionist pitch.

Estimates the revenue a prospect loses to unanswered calls, then compares it to
your subscription price. This is the number that closes deals: show the prospect
their own leak, then price well under it.

No dependencies, no network. Run with their real numbers during a sales call.

Example:
    python3 roi_calculator.py --calls-per-day 25 --missed-pct 0.30 \
            --avg-job-value 350 --close-rate 0.40 --price 297
"""
import argparse


def monthly_lost_revenue(calls_per_day, missed_pct, avg_job_value,
                         close_rate, business_days=22):
    missed_calls = calls_per_day * missed_pct * business_days
    lost_jobs = missed_calls * close_rate
    return missed_calls, lost_jobs, lost_jobs * avg_job_value


def main():
    p = argparse.ArgumentParser(description="Missed-call ROI for a prospect.")
    p.add_argument("--calls-per-day", type=float, default=20)
    p.add_argument("--missed-pct", type=float, default=0.27,
                   help="Fraction of calls that go unanswered (industry avg "
                        "for small service businesses is ~0.25-0.30).")
    p.add_argument("--avg-job-value", type=float, default=300,
                   help="Revenue from one converted caller (first job or LTV).")
    p.add_argument("--close-rate", type=float, default=0.40,
                   help="Fraction of answered new callers that become customers.")
    p.add_argument("--business-days", type=int, default=22)
    p.add_argument("--price", type=float, default=297,
                   help="Your monthly subscription price.")
    p.add_argument("--recapture", type=float, default=0.80,
                   help="Fraction of currently-missed calls the agent recovers.")
    a = p.parse_args()

    missed, lost_jobs, lost_rev = monthly_lost_revenue(
        a.calls_per_day, a.missed_pct, a.avg_job_value,
        a.close_rate, a.business_days)

    recovered_rev = lost_rev * a.recapture
    net_gain = recovered_rev - a.price
    roi_x = (recovered_rev / a.price) if a.price else float("inf")

    print("=" * 56)
    print("  AI VOICE RECEPTIONIST — MISSED-CALL ROI")
    print("=" * 56)
    print(f"  Calls/day:                 {a.calls_per_day:>10.0f}")
    print(f"  Missed (%):                {a.missed_pct*100:>9.0f}%")
    print(f"  Missed calls / month:      {missed:>10.0f}")
    print(f"  Avg job value:             ${a.avg_job_value:>9,.0f}")
    print(f"  Close rate on new callers: {a.close_rate*100:>9.0f}%")
    print("-" * 56)
    print(f"  Lost jobs / month:         {lost_jobs:>10.1f}")
    print(f"  Revenue lost / month:      ${lost_rev:>9,.0f}")
    print(f"  Agent recapture rate:      {a.recapture*100:>9.0f}%")
    print(f"  Revenue recovered / month: ${recovered_rev:>9,.0f}")
    print("-" * 56)
    print(f"  Your price / month:        ${a.price:>9,.0f}")
    print(f"  Client NET gain / month:   ${net_gain:>9,.0f}")
    print(f"  Client ROI:                {roi_x:>9.1f}x")
    print("=" * 56)
    if net_gain > 0:
        print(f"  PITCH: \"You're leaving ~${lost_rev:,.0f}/mo on the table. For")
        print(f"  ${a.price:,.0f}/mo we recover ~${recovered_rev:,.0f} of it — "
              f"that's {roi_x:.0f}x.\"")
    else:
        print("  This prospect's volume is low — sell on never-miss-a-call")
        print("  peace of mind and after-hours coverage, not raw ROI.")


if __name__ == "__main__":
    main()
