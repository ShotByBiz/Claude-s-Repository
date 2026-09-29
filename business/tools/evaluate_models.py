#!/usr/bin/env python3
"""Score the five business models on weighted criteria and rank them.

This is the "try all, keep what works" decision tool. Scores (1-5) reflect a
grounded assessment for a solo operator starting from zero with limited capital;
edit them as real-world results come in. Higher weight = matters more early.

    python3 business/tools/evaluate_models.py
"""

# weight: how much this criterion matters for a zero-to-first-revenue operator
CRITERIA = {
    "time_to_first_revenue": 0.28,  # how fast can this realistically pay?
    "low_startup_cost":      0.18,  # cheap to start = survives the self-funding gap
    "low_delivery_risk":     0.16,  # hard to mess up / low blowup potential
    "margin":                0.14,
    "recurring_revenue":     0.14,
    "defensibility":         0.10,
}

# 1 (weak) .. 5 (strong), graded honestly per model
MODELS = {
    "1. Voice Receptionist": {
        "time_to_first_revenue": 5, "low_startup_cost": 4, "low_delivery_risk": 4,
        "margin": 5, "recurring_revenue": 5, "defensibility": 3,
    },
    "2. Outbound Sales Agent": {
        "time_to_first_revenue": 3, "low_startup_cost": 3, "low_delivery_risk": 2,
        "margin": 4, "recurring_revenue": 4, "defensibility": 3,
    },
    "3. Content + Lead Gen": {
        "time_to_first_revenue": 2, "low_startup_cost": 4, "low_delivery_risk": 2,
        "margin": 4, "recurring_revenue": 4, "defensibility": 2,
    },
    "4. Appointment Reminders": {
        "time_to_first_revenue": 4, "low_startup_cost": 5, "low_delivery_risk": 5,
        "margin": 5, "recurring_revenue": 5, "defensibility": 3,
    },
    "5. Self-Demo Meta-Agent": {
        "time_to_first_revenue": 2, "low_startup_cost": 2, "low_delivery_risk": 2,
        "margin": 5, "recurring_revenue": 5, "defensibility": 4,
    },
}


def score(model):
    return sum(MODELS[model][c] * w for c, w in CRITERIA.items())


def main():
    ranked = sorted(MODELS, key=score, reverse=True)
    print("=" * 60)
    print("  BUSINESS MODEL SCORECARD  (weighted, 1-5)")
    print("=" * 60)
    print("  Weights:")
    for c, w in CRITERIA.items():
        print(f"    {c:<24} {w:>4.0%}")
    print("-" * 60)
    print(f"  {'model':<28}{'score':>8}")
    print("-" * 60)
    for m in ranked:
        marker = "  <- START HERE" if m == ranked[0] else (
            "  <- fast add-on" if m.startswith("4") else "")
        print(f"  {m:<28}{score(m):>8.2f}{marker}")
    print("=" * 60)
    # Pair the top model with its best complement among the other top-tier
    # models (1 & 4 share a buyer and bundle well). Never pair a model with itself.
    bundle_pool = [m for m in ranked if m.startswith(("1.", "4."))]
    primary = ranked[0]
    complement = next((m for m in bundle_pool if m != primary), ranked[1])
    print("  Recommendation:")
    print(f"   KEEP & RUN NOW : {primary}")
    print(f"                    bundled with {complement}")
    print("                    (same buyer, fast, low risk -> sell together)")
    print("   BUILD NEXT     : 2. Outbound Sales Agent (fills the pipeline)")
    print("   DEFER          : 3. Content (slow ROI), 5. Meta-Agent (build last)")
    print("  Re-score with real numbers once leads are logged in crm/leads.csv.")


if __name__ == "__main__":
    main()
