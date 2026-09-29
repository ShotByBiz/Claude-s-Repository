#!/usr/bin/env python3
"""Quantify revenue recovered by cutting no-shows. The renewal-justifying number.

    python3 no_show_savings.py --appts-per-week 120 --slot-value 180 \
            --no-show-before 0.20 --no-show-after 0.08 --price 199
"""
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--appts-per-week", type=float, default=100)
    p.add_argument("--slot-value", type=float, default=150,
                   help="Revenue from one kept appointment.")
    p.add_argument("--no-show-before", type=float, default=0.20)
    p.add_argument("--no-show-after", type=float, default=0.08,
                   help="Realistic with confirm+reschedule reminders.")
    p.add_argument("--price", type=float, default=199, help="Your monthly fee.")
    p.add_argument("--weeks-per-month", type=float, default=4.33)
    a = p.parse_args()

    monthly_appts = a.appts_per_week * a.weeks_per_month
    recovered_appts = monthly_appts * (a.no_show_before - a.no_show_after)
    recovered_rev = recovered_appts * a.slot_value
    net = recovered_rev - a.price
    roi = recovered_rev / a.price if a.price else float("inf")

    print("=" * 50)
    print("  NO-SHOW REDUCTION — RECOVERED REVENUE")
    print("=" * 50)
    print(f"  Appointments / month:   {monthly_appts:>10.0f}")
    print(f"  No-show before -> after:{a.no_show_before*100:>6.0f}% -> "
          f"{a.no_show_after*100:.0f}%")
    print(f"  Slots saved / month:    {recovered_appts:>10.1f}")
    print(f"  Value per slot:         ${a.slot_value:>9,.0f}")
    print("-" * 50)
    print(f"  Revenue recovered/mo:   ${recovered_rev:>9,.0f}")
    print(f"  Your fee:               ${a.price:>9,.0f}")
    print(f"  Client net gain/mo:     ${net:>9,.0f}")
    print(f"  Client ROI:             {roi:>9.1f}x")
    print("=" * 50)


if __name__ == "__main__":
    main()
