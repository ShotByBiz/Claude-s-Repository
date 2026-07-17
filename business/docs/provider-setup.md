# Go-Live Provider Setup Walkthrough

The one-time external wiring that turns the prompts/scripts in this repo into a
running service. Budget ~1–2 hours. Do it once for a generic demo agent, then
re-skin per client via `configuration.md`.

## What you need (accounts)
1. **Voice provider** — pick one: [Retell AI](https://retellai.com),
   [Vapi](https://vapi.ai), or [Bland](https://bland.ai).
2. **Calendar** — [Cal.com](https://cal.com) (free, API-friendly) or Google
   Calendar.
3. **Payments** — [Stripe](https://stripe.com) (payment links or subscriptions).
4. **SMS/email for reminders** — Twilio (SMS) + any email sender, or the voice
   provider's messaging if it has one.

## Step-by-step

### A. Voice agent (the receptionist)
1. Create the voice-provider account; add billing (per-minute, usually
   ~$0.07–$0.15/min — that's your main variable cost).
2. Create a new agent. Paste `voice-receptionist/system-prompt.md` as the prompt.
3. Fill every `{{VARIABLE}}` from `configuration.md` (start with a generic
   demo config for one niche, e.g. dental or plumbing).
4. Pick a natural voice; set the greeting; keep latency low (short prompt helps).

### B. Phone number
1. Buy a number in the provider (or port the client's via Twilio later).
2. For real clients: forward their existing line to the agent number (so their
   published number is unchanged).

### C. Calendar / booking
1. Connect Cal.com or Google Calendar to the agent (most providers have a native
   integration or you wire it via a webhook/function call).
2. Define bookable event types matching the client's services.
3. Test: have the agent create a booking; confirm it lands on the calendar and a
   confirmation fires.

### D. Reminders (for the bundle)
1. Connect SMS (Twilio) + email. Store consent for each contact (TCPA).
2. Implement the cadence from `appointment-reminders/reminder-sequences.md`
   (a no-code tool like n8n/Make/Zapier can trigger reminders off calendar
   events without custom code).
3. Test confirm / reschedule / STOP branches end to end.

### E. Payments
1. Create a Stripe product per tier (Core / Plus / Premium).
2. Generate a payment link or subscription checkout you can send on a sales call.

### F. Final QA before selling
- Run the QA checklist in `voice-receptionist/conversation-flows.md`.
- Make 5 real test calls (book, FAQ, emergency, message, "are you AI?").
- Confirm a booking triggers a reminder sequence.

## Cost sanity check
Per client, expect ~$15–$60/mo in voice + tokens + number + messaging. At
$397/mo (Plus) that's ~85%+ gross margin. Track real per-client cost so a
high-volume client gets moved to Premium or a usage tier.

## Compliance quick-list
- Disclose AI when asked (built into the prompt).
- Follow your state's call-recording consent laws.
- TCPA for SMS/automated calls: consent, opt-out, quiet hours.
- HIPAA if healthcare: minimum-necessary info, compliant providers, BAAs.
