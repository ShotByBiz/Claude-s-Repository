# Fulfillment Engine — one command, order → finished deliverable

This is the machine, not another template. When an order comes in, you run **one
command** and get a finished deliverable ready to spot-check and send. Spinning up
a **brand-new gig-agent** is also one command. This is what turns the service
business from "you do every step" into "you approve and collect."

## What it does
- `status` — readiness doctor: LIVE vs OFFLINE, key/SDK, agents, orders, revenue.
- `list` — show the gig-agents you can fulfill (9 built in).
- `fulfill --gig <id> --intake <file|->` — produce the complete deliverable for an
  order and write it to `orders/<gig>-<n>.md`, logging it to `orders/ledger.csv`.
  Add `--price <amt> [--buyer name]` to log a **real** paid sale.
- `revenue` — total real sales logged (honest $0 until a real order is paid).
- `scaffold --id <id> --name <name>` — generate a new gig-agent entry to drop in.

## Built-in gig-agents (9)
prompt-pack · short-form-script · youtube-script · seo-blog · resume ·
ad-copy · product-descriptions · email-sequence · cold-email

## Quick start
```bash
python3 business/engine/fulfill.py list

# Fulfill an order (intake from a file or stdin)
python3 business/engine/fulfill.py fulfill --gig prompt-pack --intake order.txt
echo "topic: tankless heaters; length: 1200w; audience: homeowners" \
  | python3 business/engine/fulfill.py fulfill --gig seo-blog --intake -

# Add a brand-new service agent in one command
python3 business/engine/fulfill.py scaffold --id ad-copy --name "Ad Copy Pack"
```

## The loop it enables (your only touch points in **bold**)
1. Order arrives on Fiverr/Upwork/etc.
2. **You** paste the buyer's intake answers into a file (or stdin).
3. Engine generates the finished deliverable — minutes, or seconds.
4. **You** spot-check it and hit send; **you** collect payment.

That's the "here's the completed product, pay me" flow you asked for — automated
up to the two steps that must stay human (quality approval + your account/payment).

## Real vs. offline
- **With `ANTHROPIC_API_KEY` set** (and `pip install anthropic`): calls Claude
  (`claude-opus-4-8`, adaptive thinking, streaming) to produce the real deliverable.
- **Without a key**: produces a structured *offline draft* so the engine always
  runs and is demoable. It never fabricates a deliverable it didn't really make,
  and never invents facts about a buyer — gaps come back as `[NEEDS: ...]`.

## Add / edit agents
Each gig-agent lives in `agents/__init__.py` as one dict entry: an `id`, display
`name`, `price`, and a `system` production prompt that says exactly what to output
from an intake. Edit a prompt to tune quality; add an entry (or `scaffold`) to add
a service. That's the whole extension model.

## Honesty guardrails baked in
- No fabricated sales or revenue — `ledger.csv` only logs deliverables you
  actually generated for real orders.
- Generated deliverables and the ledger are git-ignored (they're your work
  product / client data, not source).
- Production prompts forbid inventing facts, stats, prices, or credentials.
