# Model 4 — Appointment Scheduling & Reminder Agent

A focused system that confirms appointments, sends multi-channel reminders,
handles rescheduling, and cuts no-shows. Sold to healthcare, clinics, salons,
consultants, home services.

## Why this is the sleeper pick
- **Narrowest scope = fastest to deliver and hardest to mess up.**
- **Directly tied to money the client already has** (a no-show is lost revenue
  on a slot they can't resell). The ROI is concrete and immediate.
- **Natural upsell to Model 1** clients — same buyer, more value, more MRR.
- No-show rates of 15–30% are common in healthcare/services; even a few points
  of reduction pays for the service many times over.

## Honest scope
The reminder logic, cadence, and reschedule flow are here. Sending needs the
client's SMS/email/voice provider and calendar (their accounts) — one-time wiring.
TCPA/consent rules apply to SMS and calls (see below).

## Contents
- `reminder-sequences.md` — the multi-channel cadence + reschedule branching
- `no_show_savings.py` — quantify recovered revenue from reduced no-shows

## Economics
- **$97–$297/mo** standalone, or a +$100/mo add-on to a Model 1 client.
- Cost is tiny (a few messages per appointment). Margin is excellent.

## Compliance
- TCPA: get consent for SMS/automated calls, honor STOP/opt-out, respect quiet
  hours and frequency. Appointment reminders to patients who provided their
  number generally qualify, but keep consent records and an easy opt-out.
- HIPAA if healthcare: minimum necessary info in messages (no diagnoses), use
  compliant providers, sign BAAs.
