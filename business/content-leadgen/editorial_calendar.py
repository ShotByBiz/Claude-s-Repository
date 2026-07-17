#!/usr/bin/env python3
"""Generate a dated editorial calendar for a content retainer.

Spreads N pieces/week across funnel stages so the calendar isn't all top-funnel
traffic bait with nothing that converts. No deps, no network.

    python3 editorial_calendar.py --weeks 8 --per-week 2 --start 2026-07-01 \
            --niche "tankless water heaters"
"""
import argparse
from datetime import date, timedelta

# Healthy mix: enough top-funnel for traffic, enough mid/bottom to convert.
STAGE_CYCLE = ["top", "top", "mid", "bottom", "mid"]

ANGLES = {
    "top": ["beginner guide to {n}", "common mistakes with {n}",
            "{n} explained for homeowners"],
    "mid": ["{n}: how to choose", "{n} vs alternatives compared",
            "what to look for in {n}"],
    "bottom": ["how much {n} costs in 2026", "is {n} worth it? honest breakdown",
               "{n}: when to call a pro"],
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--weeks", type=int, default=8)
    p.add_argument("--per-week", type=int, default=2)
    p.add_argument("--start", default=date.today().isoformat())
    p.add_argument("--niche", default="your niche")
    a = p.parse_args()

    y, m, d = map(int, a.start.split("-"))
    start = date(y, m, d)
    # snap to next Monday for clean weekly cadence
    start += timedelta(days=(7 - start.weekday()) % 7)

    print(f"Editorial calendar — {a.niche} — {a.weeks} weeks, "
          f"{a.per_week}/week\n")
    print(f"{'date':<12} {'stage':<7} working title")
    print("-" * 60)
    i = 0
    counts = {"top": 0, "mid": 0, "bottom": 0}
    for w in range(a.weeks):
        for s in range(a.per_week):
            day = start + timedelta(weeks=w, days=s * 2)
            stage = STAGE_CYCLE[i % len(STAGE_CYCLE)]
            angle = ANGLES[stage][i % len(ANGLES[stage])]
            title = angle.format(n=a.niche)
            counts[stage] += 1
            print(f"{day.isoformat():<12} {stage:<7} {title}")
            i += 1
    print("-" * 60)
    total = sum(counts.values())
    print(f"{total} pieces  |  top {counts['top']}  mid {counts['mid']}  "
          f"bottom {counts['bottom']}")
    print("Every bottom/mid piece must carry a lead magnet CTA (see brief).")


if __name__ == "__main__":
    main()
