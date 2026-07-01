# Launch Playbook — Zero to First Paying Client

A realistic, sequenced plan. The slow part is real human steps (provider
signup, calls). This repo removes the *thinking* so you only do the *doing*.

## Phase 0 — Setup (≈2 hours, one time)
1. Create accounts: a voice provider (Retell/Vapi/Bland), Cal.com, Stripe.
2. Buy one phone number through the provider.
3. Paste `voice-receptionist/system-prompt.md` into the provider; fill a generic
   `{{...}}` config for one vertical (start with **dental** or **plumbing** —
   high job value, high missed-call pain).
4. Connect the calendar. Run 5 test calls against the QA list in
   `conversation-flows.md`. This is now your **demo agent**.

## Phase 1 — Pick a niche & build a list (Day 1)
- Choose ONE vertical + ONE city. Narrow beats broad for outreach.
- Build a list of 30–50 businesses from Google Maps/Yelp.
- **Pre-qualify the cheap way:** call each during business hours. The ones that
  hit voicemail are your hottest leads — they're losing money right now. Log
  them in `crm/leads.csv` with `source=google_maps`, `stage=new`.

## Phase 2 — Outreach (Days 1–10)
- For each lead, run `tools/roi_calculator.py` with rough numbers to get their
  `LOST_PER_MONTH`. Personalize Touch 1 of `outreach/cold-email.md`.
- Send the 5-touch sequence; for voicemail-droppers, also use the call script.
- Goal: **book 5 live demos.** Update `stage` in the CSV as leads progress.

## Phase 3 — Demo & close (Days 3–14)
- Re-skin the demo agent for the prospect's business (15 min using
  `configuration.md`).
- Have them call it and book a fake appointment. Then run the ROI math live.
- Quote Pro ($297, no contract, 14-day guarantee). Send the Stripe link on the
  call. Mark `stage=won` and set `monthly_price`.

## Phase 4 — Deliver & retain (ongoing)
- Provision their number, finalize KNOWN FACTS (get sign-off), go live.
- Send the **weekly value report** (calls answered, bookings made). This is the
  anti-churn lever — never skip it.
- Run `tools/pipeline_report.py` weekly to watch MRR and conversion.

## Phase 5 — Reinvest & scale
- First client's revenue funds your API credits and tools — the self-funding
  loop. Replicate the same vertical/city before expanding.
- Once 3–5 clients are stable, templatize onboarding and start Model #2
  (outbound) or #4 (reminders/no-show) as upsells to existing clients.

## Honest expectation-setting
First revenue depends on real-world response rates and your provider setup, not
on this repo. What's removed is the strategy/copy/config work — typically the
multi-week part. Treat every number in `crm/` as real or don't write it down.
