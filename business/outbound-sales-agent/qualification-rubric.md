# Qualification Rubric (BANT+)

Agent scores each prospect 0–100 before booking. Book only if ≥ `BOOK_THRESHOLD`
(default 60). Tune per client.

| Dimension | Weight | What to look for |
|-----------|--------|------------------|
| **Fit (ICP)** | 30 | Industry, size, geography match the client's best customers |
| **Pain signal** | 25 | Public evidence of the problem the offer solves (hiring, reviews, news, stack) |
| **Authority** | 20 | Contact can influence or make the buying decision |
| **Timing trigger** | 15 | Something makes *now* the right moment (funding, new hire, expansion) |
| **Budget proxy** | 10 | Company can plausibly afford the offer (size/funding as proxy) |

## Scoring guide
- **80–100** — book immediately, flag as hot.
- **60–79** — book; standard discovery.
- **40–59** — nurture; follow up on a real future trigger.
- **< 40** — NOT_A_FIT; do not consume sending reputation on it.

## Anti-patterns (auto-disqualify)
- No identifiable pain → not a fit, no matter the company size.
- Wrong-level contact with no path to authority → find the right person first.
- Generic "everyone could use this" reasoning → that's the tell you have no
  trigger. Stop and move on.

The rubric exists so the agent optimizes for **qualified pipeline**, not message
count. Track booked→qualified→closed downstream and re-weight from real outcomes.
