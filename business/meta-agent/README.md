# Model 5 — Self-Demoing Voice Sales Meta-Agent (the flywheel)

The overarching agent that sells the other agents. It finds prospects, calls them
with a voice AI that *is* the demo (a great conversation sells itself), qualifies,
and closes — so agents sell more agents.

## Honest scope
This is an **orchestration design**, not a one-click deploy. It composes Models
1–4 plus a voice provider and a CRM. The pieces (prompts, qualification, ROI
tools) already exist in this repo; this folder defines how they connect and the
guardrails that keep an autonomous sales caller legal and on-brand.

## Contents
- `orchestration.md` — the flywheel: how lead-gen → demo-call → close → deliver loops
- `self-demo-call-script.md` — the outbound voice script where the demo IS the pitch

## Why it's the highest ceiling and the highest risk
- **Ceiling:** if it works, customer acquisition cost trends toward token cost and
  it compounds — the classic "agents selling agents" flywheel.
- **Risk:** an autonomous system placing real calls is where compliance mistakes
  get expensive (TCPA). Build it **last**, on top of a proven manual motion, with
  human-in-the-loop on calling until the consent/targeting is airtight.

## Sequencing
Do not start here. Prove Model 1 (or 4) by hand, then automate lead-gen (Model 2),
then let the voice agent self-demo into that pipeline. Each layer must work
manually before you hand it to the meta-agent.
