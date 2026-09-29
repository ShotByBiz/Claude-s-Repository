# Per-Client Configuration Checklist

Fill this once per client. These values replace the `{{VARIABLES}}` in
`system-prompt.md`. Keep a copy per client (e.g. `crm/clients/acme-dental.md`).

## Identity
- `AGENT_NAME`: receptionist name (e.g. "Ava")
- `BUSINESS_NAME`:
- `BUSINESS_TYPE`: e.g. dental office, plumbing company
- `CITY_STATE`:

## Facts (source of truth)
- `ADDRESS`:
- `HOURS`:
- `SERVICE_LIST`: services the agent can book
- `SERVICES_AND_PRICING`: only prices the agent may state aloud
- `INSURANCE_PAYMENT`:
- `PARKING`:
- `EMERGENCY_INSTRUCTIONS`: what to do for emergencies
- `EMERGENCY_SLA`: e.g. "15 minutes"

## Routing & booking
- `CALENDAR_SYSTEM`: Cal.com / Google Calendar / etc.
- `CONFIRMATION_CHANNEL`: text / email
- `CALLBACK_SLA`: e.g. "the next business hour"
- `TRANSFER_NUMBER`: live human fallback (optional)

## Go-live checklist
- [ ] All variables above filled — no `{{...}}` left in the deployed prompt
- [ ] Calendar integration connected and a test booking lands
- [ ] Phone number provisioned and forwarded (or ported)
- [ ] 5 test calls run against `conversation-flows.md` QA list
- [ ] Client signed off on the KNOWN FACTS block (their liability surface)
- [ ] Daily/weekly call summary email configured to client
- [ ] Billing started ({{see pricing.md}})

## Client intake questions (send before build — 10 min to answer)
1. What are your hours, and what happens to calls after hours today?
2. Which services should the assistant be able to book?
3. How many calls a day roughly, and how many go unanswered?
4. What counts as an emergency, and who should be paged?
5. What questions do callers ask most? (this seeds KNOWN FACTS)
6. What should it NEVER say or do?
7. Where do bookings go today — what calendar?
