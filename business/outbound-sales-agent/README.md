# Model 2 — Autonomous Sales Outreach Agent

A fleet of AI agents that find B2B leads, write personalized outreach, qualify
replies, and book meetings. Sold as a service or white-labeled to companies that
need outbound but hate doing it.

## Honest scope
The *thinking* assets are here (research rubric, personalization engine prompt,
qualification logic, sequence design). Going live needs an email-sending account
with proper domain war-up + an enrichment source — external, one-time setup.
**Deliverability and consent are the whole game** (see compliance below); copy is
secondary.

## Contents
- `agent-system-prompt.md` — the outreach SDR agent's brain
- `qualification-rubric.md` — BANT-style scoring so the agent only books real fits
- `sequence-framework.md` — multi-touch cadence with reply-branching

## Economics
- Sell at **$800–$2,500/mo** per client (or per-meeting: $150–$500/booked call).
- Your cost: enrichment + sending tools + tokens, typically $100–$400/mo/client.
- The pitch: "We fill your calendar with qualified calls; you only pay for
  pipeline." Higher ticket than Model 1, longer sales cycle.

## Compliance (non-negotiable)
- CAN-SPAM: real identity, physical address, honored opt-out, no deceptive
  subjects. CASL/GDPR if contacting Canada/EU (consent + legitimate interest).
- B2B cold email to business addresses is legal in the US with the above; it is
  **not** a license to spam. Low volume, high relevance, real value.
- Never scrape behind logins or violate a platform's ToS. Use public/business
  data and legitimate enrichment providers only.
