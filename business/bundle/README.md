# Stream C — The "Never Miss" Bundle (Receptionist + Reminders)

The scorecard's two top models sold as **one offer to one buyer**. The
receptionist catches the calls you miss; the reminder system saves the
appointments you booked. Together they plug both leaks in a local business's
revenue — and it's one sale, two recurring revenue lines.

## The offer
> "We make sure you never miss a call and never lose a booked appointment."

| Tier | Price/mo | What's included |
|------|----------|-----------------|
| Core | $297 | 24/7 AI receptionist: answering, booking, FAQ, message capture |
| **Plus** ⭐ | $397 | Core + appointment reminders, reschedule handling, no-show recovery |
| Premium | $597 | Plus + SMS follow-up, waitlist auto-fill, 2 numbers, monthly report |

Lead with **Plus** — it's the full "never miss" promise and the best margin.

## The double ROI close
Run both calculators live in the sale; the two numbers stack:
- `tools/roi_calculator.py` → revenue recovered from answered calls
- `appointment-reminders/no_show_savings.py` → revenue saved from kept appointments

Combined recovered revenue typically dwarfs even the Premium price — that gap is
the pitch.

## What's reused (already built)
- Receptionist brain: `voice-receptionist/system-prompt.md` + flows + config
- Reminder logic: `appointment-reminders/reminder-sequences.md`
- Onboarding: `bundle/onboarding-flow.md` (one flow for both)
- Landing: `bundle/landing/index.html`
- Go-live: `docs/provider-setup.md`

## Why bundle instead of sell separately
Same buyer, same install, same calendar integration — selling them together
roughly doubles revenue per close with little extra delivery work, and the
combined promise ("never miss anything") is stickier and harder to cancel.
