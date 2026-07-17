# Portfolio — "Try All, Keep What Works"

All five models from the operator brief are now built into deployable assets.
This is the honest verdict on which to run, why, and in what order. Re-run
`tools/evaluate_models.py` to reproduce the ranking; re-score it with real
numbers once `crm/leads.csv` has live leads.

## Ranking (weighted scorecard)

| Rank | Model | Score | Verdict |
|------|-------|-------|---------|
| 1 | **Appointment Reminders** | 4.52 | **Run now** — narrowest scope, lowest risk, fastest concrete ROI |
| 2 | **Voice Receptionist** | 4.46 | **Run now** — same buyer; bundle with #1 |
| 3 | Outbound Sales Agent | 3.12 | Build next — fills your own pipeline + a sellable service |
| 4 | Self-Demo Meta-Agent | 3.04 | Defer — highest ceiling, highest risk; build last on proven layers |
| 5 | Content + Lead Gen | 2.92 | Defer — slow ROI, commoditized, trust-sensitive |

Weights favor what matters at zero: time-to-first-revenue (28%), low startup
cost (18%), low delivery risk (16%).

## The keep decision

**Keep and run as one offer: Reminders + Voice Receptionist.**
They share a buyer (local service businesses), install on the same setup, and
each produces a hard ROI number (`roi_calculator.py`, `no_show_savings.py`). Sell
the receptionist as the headline and reminders as the no-show-killer add-on —
one sale, two revenue lines, both recurring.

**Build next: Outbound Sales Agent.** It does double duty — it's a sellable
service *and* the engine that finds clients for the offer above. That's leverage.

**Defer: Content and the Meta-Agent.** Content is slow and commoditized; the
meta-agent is powerful but should only automate a sales motion you've already
proven by hand. Building either first would burn the runway before first revenue.

## What "keep what works" means operationally
Nothing here is "working" until a real lead is logged and a real dollar changes
hands. The assets are sharp; the validation is yours to do (you hold the phone
line, the sending domain, the Stripe account). Log every real touch in
`crm/leads.csv`, run `pipeline_report.py` weekly, and let actual conversion data —
not these estimates — decide the final keep/kill.

## Why I did not "just make a profit"
This environment can't place calls, send outreach, or take payments, so any
reported revenue would be fake — worse than useless. The one real-money lever in
the session (a connected brokerage) I deliberately won't trade autonomously:
that's risking your capital on an irreversible action without your per-trade
say-so. The profit path here is real and unglamorous: take these assets live,
work the playbook, keep the winners.
