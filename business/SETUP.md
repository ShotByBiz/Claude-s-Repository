# SETUP — go from repo to running in ~15 minutes

Everything in `business/` is built. This is the shortest path to actually
running it. The steps that need a human (you) are the ones that need *your*
accounts, *your* card, and *your* approval — by design.

## 0. Check engine readiness (30 seconds, no setup)
```bash
python3 business/engine/fulfill.py status
```
It tells you exactly what's set up and what's missing.

## 1. Turn the engine LIVE (~5 min)
The engine runs offline (draft mode) with zero setup. To make it produce real
deliverables with Claude:
```bash
pip install -r business/engine/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...        # your key from console.anthropic.com
python3 business/engine/fulfill.py status  # should now say LIVE
```

## 2. Stand up the storefront (~1 hour, one time — you do this)
These need *your* accounts:
1. **Gumroad** — list the ebook (`digital-products/ebook-clipping/`, open the
   HTML → Save as PDF) and the toolkit (`digital-products/PRODUCT-from-this-repo.md`).
2. **Fiverr** — post the gigs from `services/listings.md` (start with the
   🤖 AI-complete ones — those are what the engine fulfills).
3. **Stripe** — a payment link, for off-platform sales.

## 3. Run the loop (per order)
```bash
# 1. Buyer orders on Fiverr; you paste their intake answers into order.txt
# 2. Fulfill it (engine writes the finished deliverable):
python3 business/engine/fulfill.py fulfill --gig short-form-script --intake order.txt
# 3. Spot-check business/engine/orders/short-form-script-1.md, deliver, get paid
# 4. Log the real sale:
python3 business/engine/fulfill.py fulfill --gig short-form-script \
    --intake order.txt --price 45 --buyer "acme"
```
Track real money in:
```bash
python3 business/engine/fulfill.py revenue
```

## 4. The other streams (parallel, optional)
- **Clipping** (fastest first dollar): `clipping/starter-checklist.md` + `first-10-hooks.md`.
- **Recurring agent bundle** (highest LTV): `bundle/` + `docs/provider-setup.md`.

## What I (the AI) set up vs. what only you can
| Set up in the repo (done) | Only you can do (needs your accounts/approval) |
|---|---|
| Fulfillment engine + 9 gig-agents | Add your API key / install deps |
| Listings, ebook, landing pages, scripts | Create Gumroad/Fiverr/Stripe accounts |
| Revenue + pipeline tracking | Post listings, approve deliverables, collect payment |
| ROI/scorecard/report tools | Reply to real buyers |

The engine can't create accounts or move money on its own — and shouldn't. That
boundary is what keeps your accounts un-banned and your money safe.
