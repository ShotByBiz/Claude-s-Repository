# Strategy Simulation — verdict & method

Run it yourself: `python3 business/tools/simulate.py --runs 8000`

**What it is:** a Monte Carlo model (8,000 runs, 90-day horizon) ranking each
stream for a solo beginner starting near-zero, part-time. Every number is a
**modeled projection from documented assumptions** in `tools/simulate.py` — not
real sales. Edit the assumptions as reality comes in and re-run.

## Ranking (feasibility = speed + odds of being net-positive + low cost/effort)

| Rank | Strategy | Feas | P50 net (90d) | Net-positive by 90d | First $ |
|------|----------|------|---------------|---------------------|---------|
| 1 | Clipping (pay-per-view) | 0.93 | ~$1,600 | ~100% | mo 1 |
| 2 | **Fiverr AI-writing service (engine)** | 0.84 | ~$512 | ~98% | mo 2 |
| 3 | Digital products (Gumroad) | 0.76 | ~$113 | ~78% | mo 2 |
| 4 | Voice-receptionist bundle | 0.66 | ~$307 | ~72% | mo 2 |
| 5 | Meta-agent / outbound | 0.46 | ~-$90 | ~47% | mo 3 |

(P50 = median outcome. Numbers shift with the seed and your assumptions.)

## The two honest takeaways

1. **Most feasible overall: clipping.** Fastest to first dollar, ~zero cost, no
   reviews/audience barrier — you post, you get views. The catch is it's the
   most *effort* (≈10 hrs/wk) and it is **not** Claude-powered.
2. **Most feasible Claude-powered play: the Fiverr AI-writing service** (the
   engine in `engine/`). ~98% net-positive in the model, low effort, and now
   very cheap to run (see below). It's slower to *start* (needs a first review)
   but compounds and is the most hands-off per dollar.

**Recommended combo:** run clipping for fast cash *and* to build an audience,
point that audience at the Gumroad products, and let the Fiverr engine service
be the compounding, low-effort earner. The voice bundle is the high-LTV upgrade
later; the meta-agent is genuinely "build last" (negative median at 90 days).

## Credit optimization (backtested in the model)
The engine was re-tuned for credit usage: per-gig **model tiering** (Haiku/Sonnet
instead of Opus by default) + **prompt caching** on the system prompt + **no
extra thinking tokens** for straightforward writing. Modeled effect on the
service's 90-day credit cost:

- Before (Opus, no cache): ~$2.70
- After (tiered + cache): ~$0.50 → **~81% cheaper**, same revenue.

## Redundancy (added to the engine)
- SDK auto-retries transient errors (429/5xx/network), `max_retries=3`.
- On hard failure it **falls back to a cheaper model**, then to an offline draft
  — an order is never lost to a blip.
- Real per-order cost is measured and shown, so you always see what you spent.
