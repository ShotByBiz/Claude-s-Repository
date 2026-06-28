# AI Agent Business Portfolio

Deployable starter kits for **all five** business models from the operator brief,
plus a scorecard that ranks them. Start with `PORTFOLIO.md` for the keep/kill
verdict, then dive into a model.

| Dir | Model | Status |
|-----|-------|--------|
| `voice-receptionist/` | 1. Voice Receptionist | **Run now** (bundle w/ #4) |
| `appointment-reminders/` | 4. Reminders / no-show killer | **Run now** (top-ranked) |
| `outbound-sales-agent/` | 2. Outbound sales agent | Build next |
| `content-leadgen/` | 3. Content + lead gen | Defer |
| `meta-agent/` | 5. Self-demo meta-agent flywheel | Build last |
| `tools/evaluate_models.py` | Weighted scorecard | `python3` it |

The Voice Receptionist kit below is the most fleshed-out (Model #1) and the
template for how each model is structured.

---

## Voice Receptionist — Business-in-a-Box

A complete, deployable starter kit for an **AI Voice Receptionist service** sold
to local service businesses (dentists, plumbers, HVAC, law firms, salons, real
estate). This is Model #1 from the operator brief — the fastest path to first
revenue because the buyer already loses money every time a call goes unanswered.

## ⚠️ What this is (and isn't)

This repository is built in an **offline sandbox** with access to a single
GitHub repo. It contains **real, reusable business assets** — agent prompts,
sales scripts, pricing, an ROI calculator, a lead tracker, and a sales landing
page. It does **not** contain (and cannot, from here) real customers, real
revenue, real call recordings, or live telephony. Nothing in `crm/` is a real
lead unless you put it there.

To go live you supply three external things (one-time setup, ~1–2 hours):

1. A voice provider — [Retell AI](https://retellai.com),
   [Vapi](https://vapi.ai), or [Bland](https://bland.ai). Paste
   `voice-receptionist/system-prompt.md` as the agent prompt.
2. A phone number — bought through that provider or ported via Twilio.
3. A calendar/CRM hook — Cal.com or Google Calendar for booking; a spreadsheet
   or CRM for leads (see `crm/`).

Everything else — the part that actually takes skill — is in this repo.

## Contents

| Path | What it is |
|------|------------|
| `voice-receptionist/system-prompt.md` | The agent's brain — production system prompt |
| `voice-receptionist/conversation-flows.md` | Booking, FAQ, lead-qualification, message-taking flows |
| `voice-receptionist/configuration.md` | Per-client config checklist (variables to fill per business) |
| `outreach/cold-email.md` | Cold email sequence (5 touches) with proven framing |
| `outreach/call-script.md` | Outbound call / voicemail script for live demos |
| `outreach/objection-handling.md` | Responses to the 8 objections you'll actually hear |
| `pricing.md` | Three-tier packaging + per-client unit economics |
| `tools/roi_calculator.py` | Real, runnable calculator: what unanswered calls cost a prospect |
| `tools/pipeline_report.py` | Reads `crm/leads.csv`, prints funnel + MRR/CAC metrics |
| `crm/leads.csv` | Lead pipeline tracker (starts empty — a schema, not fake data) |
| `landing/index.html` | A real, self-contained sales landing page |
| `docs/launch-playbook.md` | Day-by-day plan from zero to first paying client |
| `docs/metrics.md` | The KPIs to track and how to read them |

## Quick start

```bash
# See what a prospect loses to missed calls (drives every sales conversation)
python3 business/tools/roi_calculator.py --calls-per-day 25 --missed-pct 0.30 \
        --avg-job-value 350 --close-rate 0.4

# Once you start logging leads in crm/leads.csv:
python3 business/tools/pipeline_report.py
```

## The unit economics in one line

Charge **$297/mo**. A dental office missing ~6 calls/day at a ~$350 first-visit
value recovers far more than that in a single saved patient. That gap — their
recovered revenue vs. your price — is the entire pitch.
