# Conversation Flows

Reference flows the system prompt implements. Use these to script test calls and
to QA a new client's agent before go-live.

## 1. Inbound booking (happy path)

```
Agent:  Thanks for calling {{BUSINESS_NAME}}, this is {{AGENT_NAME}}. How can I help?
Caller: I need to book a cleaning.
Agent:  Happy to set that up. Can I get your full name?
Caller: Maria Gonzales.
Agent:  Thanks Maria. And the best number to reach you?
Caller: 555-204-8890.
Agent:  Let me read that back — 5-5-5, 2-0-4, 8-8-9-0. Correct?
Caller: Yes.
Agent:  Our soonest openings for a cleaning are Tuesday at 9am or Wednesday at
        2pm. Which works better?
Caller: Wednesday.
Agent:  Done — a cleaning Wednesday at 2pm for Maria Gonzales. You'll get a text
        confirmation shortly. Anything else?
Caller: No thanks.
Agent:  You're all set, Maria. See you Wednesday at 2 — thanks for calling.
```

## 2. FAQ deflection → soft booking

```
Caller: Do you take Delta Dental?
Agent:  We work with most major PPO plans including Delta Dental PPO — the front
        desk confirms exact coverage when you come in. Would you like me to get
        you on the schedule so they can verify your benefits?
```

## 3. After-hours urgent (the ROI call)

```
Caller: My water heater is leaking everywhere, it's 9pm.
Agent:  I'm sorry — let's get you help fast. What's the service address?
Caller: 1420 Oak Street.
Agent:  Got it. Your name and best number?  [reads back number]
Agent:  I'm flagging this as an emergency so the on-call tech is paged right now.
        Expect a callback within {{EMERGENCY_SLA}}. Shut the supply valve if you
        safely can. Anything else I should pass along?
```
> This single captured call typically exceeds a month of subscription cost. Lead
> with it in every plumbing/HVAC demo.

## 4. Can't-resolve → message capture

```
Caller: I want to dispute a charge on my last invoice.
Agent:  I want the right person on that. Let me take your details so billing
        calls you back. Your name? ... Best number? ... [reads back] ... And the
        invoice date or number if you have it? ... Thanks — billing will reach
        you by {{CALLBACK_SLA}}.
```

## 5. Caller asks "are you a robot?"

```
Agent:  I'm {{BUSINESS_NAME}}'s virtual assistant — I can book you in and answer
        questions right now, or take a message for the team. What works best?
```

## QA checklist before go-live (run as live test calls)

- [ ] Books into the real calendar and a confirmation actually fires
- [ ] Reads back name + number correctly under a noisy connection
- [ ] Refuses to quote a price not in KNOWN FACTS
- [ ] Correctly tags an emergency and routes per `EMERGENCY_INSTRUCTIONS`
- [ ] Discloses AI status when asked, without breaking flow
- [ ] Captures a full message when it can't resolve (no dead-ends)
- [ ] Handles two services in one call (e.g., reschedule + new question)
