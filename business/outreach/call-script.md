# Outbound Call & Voicemail Script

For *your* outbound prospecting calls (or an outbound AI agent you run). Follow
TCPA: call business lines during business hours, honor do-not-call, identify
yourself, no pre-recorded calls to mobiles without consent.

## Live answer

```
You:    Hi, is this {{BUSINESS_NAME}}? Great — I'll be quick. I actually called
        earlier and got voicemail, which is exactly what I help with. I set up
        AI receptionists that answer every call 24/7 and book appointments. Are
        you the right person to talk to about missed calls?

Them:   [gatekeeper] -> "Who handles new patient/customer calls or the front
        desk schedule? Could I grab 30 seconds with them?"
        [owner]      -> continue

You:    Most {{VERTICAL}} offices miss 5-10 calls a day — lunch, after hours,
        when the front desk is slammed. Each one's a potential {{AVG_JOB}}
        customer. Mine answers all of them and texts you the booking. Can I point
        a live demo at a test number so you can call it yourself? Takes 2 minutes.

Them:   [yes] -> book the demo / send the number now
        [objection] -> see objection-handling.md
```

## Voicemail (keep under 20 seconds)

```
Hi {{FIRST_NAME}}, it's {{YOUR_NAME}}. I called {{BUSINESS_NAME}} earlier and
got voicemail — and that's actually why I'm calling. I set up AI receptionists
that catch every missed call and book appointments 24/7. I'll text you a demo
number you can try yourself. No pressure — talk soon.
```

## The live demo (your strongest close)

The product sells itself the moment they hear it. Have a pre-built demo agent on
a spare number, configured for their vertical. Tell them: *"Call this number and
pretend you're a customer."* They book a fake appointment, hear a natural voice,
and the objection-to-close gap collapses. **Always demo. Never just describe.**

## After the demo

1. Ask: "How did that compare to what happens to your calls today?"
2. Quote the Pro tier ($297/mo, no contract, 14-day guarantee).
3. Offer to have *their* version live within 48 hours.
4. Send the Stripe link before you hang up. Log the lead in `crm/leads.csv`.
