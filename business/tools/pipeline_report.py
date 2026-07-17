#!/usr/bin/env python3
"""Pipeline + unit-economics report from crm/leads.csv.

Reads the real leads you log and prints a funnel, conversion rates, MRR, and
CAC. Honest by construction: if you haven't logged real leads, it reports zero
rather than inventing a pipeline.

    python3 business/tools/pipeline_report.py [path/to/leads.csv]
"""
import csv
import os
import sys

STAGES = ["new", "contacted", "demo_booked", "demo_done", "proposal",
          "won", "lost"]


def load(path):
    rows = []
    with open(path, newline="") as f:
        for line in f:
            if line.lstrip().startswith("#") or not line.strip():
                continue
            # Re-feed non-comment lines through csv
            rows.append(line)
    reader = csv.DictReader(rows)
    return [r for r in reader if r.get("id")]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "crm", "leads.csv")
    if not os.path.exists(path):
        print(f"No leads file at {path}")
        return
    leads = load(path)

    print("=" * 50)
    print("  PIPELINE REPORT")
    print("=" * 50)
    if not leads:
        print("  No real leads logged yet. Add rows to crm/leads.csv as you")
        print("  work actual prospects, then re-run. (Reporting zero is the")
        print("  honest state — not a failure.)")
        print("=" * 50)
        return

    counts = {s: 0 for s in STAGES}
    mrr = 0.0
    for ld in leads:
        stage = (ld.get("stage") or "new").strip()
        counts[stage] = counts.get(stage, 0) + 1
        if stage == "won":
            try:
                mrr += float(ld.get("monthly_price") or 0)
            except ValueError:
                pass

    total = len(leads)
    print(f"  Total leads:        {total}")
    for s in STAGES:
        bar = "#" * counts.get(s, 0)
        print(f"  {s:<12} {counts.get(s,0):>3}  {bar}")
    print("-" * 50)
    contacted = sum(counts[s] for s in STAGES if s != "new")
    won = counts["won"]
    if contacted:
        print(f"  Contacted -> Won:   {won/contacted*100:>5.1f}%")
    print(f"  Won clients:        {won}")
    print(f"  MRR (won):          ${mrr:,.0f}")
    print(f"  ARR (run-rate):     ${mrr*12:,.0f}")
    print("=" * 50)
    print("  Tip: log every real touch. CAC = your outreach cost / won.")


if __name__ == "__main__":
    main()
