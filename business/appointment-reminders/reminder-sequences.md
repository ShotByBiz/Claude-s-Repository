# Reminder & Reschedule Sequences

Goal: every booked slot is either kept or proactively refilled. A silent no-show
is the only failure.

## Default cadence (tune per vertical)

| When | Channel | Message intent |
|------|---------|----------------|
| On booking | SMS/email | Confirm details + add-to-calendar link |
| 3 days before | email | Reminder + easy reschedule link |
| 1 day before | SMS | "Reply C to confirm, R to reschedule" |
| 2 hours before | SMS | Final nudge + directions/prep |
| After a no-show | SMS | Warm re-book offer (don't shame) |

## Reschedule branching
```
Reply "R" / "reschedule":
  -> offer next 2 open slots from {{CALENDAR}}
  -> on pick: move booking, send new confirmation
  -> free the old slot and flag it as newly-open for waitlist fill
Reply "C" / "confirm":
  -> mark confirmed, stop further reminders
No reply by 2h-before:
  -> send final SMS; flag slot as at-risk for staff
Reply "STOP":
  -> opt out of SMS immediately and permanently; fall back to email only
```

## Waitlist fill (the extra-revenue lever)
When a slot frees up from a reschedule/cancel, auto-offer it to a waitlist
contact. Turning a cancellation into a filled slot is pure recovered revenue and
a strong reason to charge more.

## Message rules
- Minimum necessary info (HIPAA): time, place, "your appointment" — never the
  service/diagnosis in plain text.
- Always include opt-out. Respect quiet hours (no 6am texts).
- Confirm-or-reschedule beats reminder-only — give them a one-tap action.

## Metric that sells renewals
Track **no-show rate before vs. after** and **slots refilled from waitlist**.
Put both in a monthly one-pager. That number is why they keep paying.
