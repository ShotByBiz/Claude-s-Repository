# Bundle Onboarding — One Flow, Both Services

From signed to live in ~48 hours. One intake covers receptionist + reminders.

## Step 0 — Payment (before any work)
- [ ] Stripe subscription / payment link active for the chosen tier.
- [ ] Add the client to `crm/leads.csv` as `stage=won` with `monthly_price`.

## Step 1 — Intake (client fills, ~10 min)
Send the questions in `voice-receptionist/configuration.md` plus these two for
reminders:
- [ ] What's your current no-show rate / how many appointments per week?
- [ ] What's a booked slot worth on average? (for the savings report)

## Step 2 — Build (you, ~30–45 min)
- [ ] Fill all `{{VARIABLES}}` in `voice-receptionist/system-prompt.md`.
- [ ] Confirm `KNOWN FACTS` with the client and get sign-off (their liability).
- [ ] Set the reminder cadence from `appointment-reminders/reminder-sequences.md`.
- [ ] Connect the calendar (booking + reschedule both write to it).

## Step 3 — Wire it up (one-time, see provider-setup.md)
- [ ] Provision/forward the phone number to the voice agent.
- [ ] Connect SMS/email for reminders (their provider, consent on file).
- [ ] Confirm bookings and reminders both read/write the same calendar.

## Step 4 — QA (run real test calls)
- [ ] Receptionist passes the QA list in `voice-receptionist/conversation-flows.md`.
- [ ] A test booking triggers a confirmation AND enters the reminder sequence.
- [ ] A "reschedule" reply moves the slot and frees the old one.
- [ ] "STOP" opts out of SMS correctly.

## Step 5 — Go live + set up retention
- [ ] Flip it on; tell the client what to expect.
- [ ] Schedule the **weekly value report**: calls answered + bookings made +
      no-shows prevented + slots refilled. This one email is your anti-churn.

## Step 6 — Week-2 check-in
- [ ] Review numbers with the client; capture a testimonial; ask for a referral.
- [ ] Log baseline vs. current no-show rate for the savings story.
