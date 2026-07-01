# Flywheel Orchestration

How the pieces in this repo connect into a self-reinforcing acquisition loop.

```
        +------------------ reinvest profit ------------------+
        v                                                     |
  [1] LEAD GEN  --->  [2] OUTREACH/RESEARCH  --->  [3] SELF-DEMO CALL
   public/business        Model 2 agent             voice AI that IS
   data, filtered         finds + qualifies         the product demo
        |                      |                          |
        |                      v                          v
        |                 [4] QUALIFY  --->  [5] CLOSE (Stripe link on call)
        |                  rubric gate         no contract, guarantee
        |                                            |
        +-----------<--- [7] DELIVER + REPORT <--- [6] ONBOARD
                          deploy client agent       configuration.md
                          (Model 1/4), weekly
                          value report = retention
```

## Component map (already in this repo)
- Lead gen + research → `outbound-sales-agent/agent-system-prompt.md`
- Qualify → `outbound-sales-agent/qualification-rubric.md`
- Self-demo call → `meta-agent/self-demo-call-script.md`
- ROI close → `tools/roi_calculator.py`, `appointment-reminders/no_show_savings.py`
- Onboard/deliver → `voice-receptionist/configuration.md` + `system-prompt.md`
- Retain → weekly value report (see `docs/metrics.md`)
- Track → `tools/pipeline_report.py`

## Guardrails (mandatory before autonomous calling)
1. **Consent + suppression list** checked before every call (TCPA, DNC).
2. **Human-in-the-loop** approves call batches until targeting is proven.
3. **Kill switch** + rate limits; log every call with outcome.
4. **Disclosure**: the voice agent states it's an AI when asked.
5. Start with **inbound/warm** demos before cold outbound calling.

## The compounding claim, stated honestly
The flywheel *can* drive CAC toward token cost — but only after each manual layer
is proven. Automating an unproven motion just scales the losses. Build the loop
one validated stage at a time.
