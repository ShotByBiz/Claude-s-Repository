#!/usr/bin/env python3
"""Fulfillment engine CLI — turn an order into a finished deliverable.

    # See the gig-agents you can fulfill
    python3 business/engine/fulfill.py list

    # Fulfill an order: pass the intake as a file or on stdin
    python3 business/engine/fulfill.py fulfill --gig prompt-pack --intake order.txt
    echo "..." | python3 business/engine/fulfill.py fulfill --gig resume --intake -

    # Spin up a BRAND-NEW gig-agent in one command
    python3 business/engine/fulfill.py scaffold --id logo-brief --name "Logo Brief"

Writes the finished deliverable to engine/orders/<gig>-<n>.md and logs the order
so pipeline_report.py / the ledger can track it. Calls Claude (claude-opus-4-8)
when ANTHROPIC_API_KEY is set; produces an offline draft otherwise.
"""
import argparse
import datetime
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import agents  # noqa: E402
from generate import generate  # noqa: E402

ORDERS_DIR = os.path.join(HERE, "orders")
LEDGER = os.path.join(ORDERS_DIR, "ledger.csv")
SALES = os.path.join(ORDERS_DIR, "sales.csv")
# Rough per-order LLM cost estimate (claude-opus-4-8) for net-revenue math.
EST_COST_PER_ORDER = 0.15


def _read_intake(arg):
    if arg == "-" or arg is None:
        return sys.stdin.read()
    with open(arg, encoding="utf-8") as f:
        return f.read()


def _next_index(gig):
    os.makedirs(ORDERS_DIR, exist_ok=True)
    n = 1
    while os.path.exists(os.path.join(ORDERS_DIR, f"{gig}-{n}.md")):
        n += 1
    return n


def _log_order(gig, path, chars):
    os.makedirs(ORDERS_DIR, exist_ok=True)
    new = not os.path.exists(LEDGER)
    with open(LEDGER, "a", encoding="utf-8") as f:
        if new:
            f.write("timestamp,gig,output_file,chars,status\n")
        ts = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
        f.write(f"{ts},{gig},{os.path.basename(path)},{chars},delivered_draft\n")


def _log_sale(gig, buyer, price, path):
    os.makedirs(ORDERS_DIR, exist_ok=True)
    new = not os.path.exists(SALES)
    with open(SALES, "a", encoding="utf-8") as f:
        if new:
            f.write("timestamp,gig,buyer,price,output_file\n")
        ts = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
        safe_buyer = (buyer or "").replace(",", " ")
        f.write(f"{ts},{gig},{safe_buyer},{price},{os.path.basename(path)}\n")


def cmd_list(_):
    print("Available gig-agents:\n")
    for gid in agents.ids():
        a = agents.get(gid)
        print(f"  {gid:<22} {a['name']:<26} ${a['price']}/order")
    print("\nFulfill one:  fulfill.py fulfill --gig <id> --intake <file|->")


def cmd_fulfill(args):
    a = agents.get(args.gig)
    if not a:
        sys.exit(f"Unknown gig '{args.gig}'. Run `fulfill.py list`.")
    intake = _read_intake(args.intake)
    if not intake.strip():
        sys.exit("Empty intake. Pass a file or pipe the intake on stdin.")

    model = args.model or a.get("model", "claude-sonnet-4-6")
    print(f"Fulfilling '{a['name']}' via {model}…", file=sys.stderr)
    result = generate(a["system"], intake, a["name"],
                      model=model, max_tokens=args.max_tokens)
    deliverable = result.text

    n = _next_index(args.gig)
    out_path = os.path.join(ORDERS_DIR, f"{args.gig}-{n}.md")
    header = (f"# {a['name']} — order #{n}\n"
              f"_Generated {datetime.date.today().isoformat()}. "
              f"Spot-check before delivering._\n\n---\n\n")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header + deliverable + "\n")
    _log_order(args.gig, out_path, len(deliverable))
    print(f"\n✅ Deliverable written to {out_path}")
    if result.cost:
        print(f"   Cost this order: ~${result.cost:.4f} ({result.model})")
    print("   Review it, then deliver it to the buyer and collect payment.")
    if args.price:
        _log_sale(args.gig, args.buyer, args.price, out_path)
        print(f"   💰 Logged a ${args.price} sale"
              f"{' to ' + args.buyer if args.buyer else ''} in sales.csv. "
              f"(Only pass --price for a REAL paid order.)")
    else:
        print("   Tip: add --price <amt> [--buyer name] to log the sale once "
              "the buyer actually pays.")


SCAFFOLD_TMPL = '''    "{id}": {{
        "name": "{name}",
        "price": "TODO",
        "system": (
            "You are an expert producing a paid {name} deliverable. "
            "Describe exactly what to output from the buyer's intake here. "
            "Never fabricate facts; mark gaps with [NEEDS: ...]."
        ),
    }},'''


def _read_sales():
    rows = []
    if not os.path.exists(SALES):
        return rows
    with open(SALES, encoding="utf-8") as f:
        next(f, None)  # header
        for line in f:
            parts = line.rstrip("\n").split(",")
            if len(parts) >= 4 and parts[3]:
                try:
                    rows.append((parts[1], parts[2], float(parts[3])))
                except ValueError:
                    pass
    return rows


def cmd_status(_):
    key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    try:
        import anthropic  # noqa: F401
        sdk = True
    except ImportError:
        sdk = False
    mode = "LIVE (Claude)" if (key and sdk) else "OFFLINE (draft mode)"
    orders = 0
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding="utf-8") as f:
            orders = max(0, sum(1 for _ in f) - 1)
    sales = _read_sales()
    revenue = sum(p for _, _, p in sales)
    print("=" * 46)
    print("  FULFILLMENT ENGINE — STATUS")
    print("=" * 46)
    print(f"  Mode:              {mode}")
    print(f"  ANTHROPIC_API_KEY: {'set' if key else 'NOT set'}")
    print(f"  anthropic SDK:     {'installed' if sdk else 'NOT installed'}")
    print(f"  Gig-agents:        {len(agents.ids())}")
    print(f"  Deliverables made: {orders}")
    print(f"  Paid sales logged: {len(sales)}")
    print(f"  Gross revenue:     ${revenue:,.2f}")
    print("-" * 46)
    if not (key and sdk):
        print("  To go LIVE:")
        if not sdk:
            print("    pip install -r business/engine/requirements.txt")
        if not key:
            print("    export ANTHROPIC_API_KEY=sk-ant-...")
    else:
        print("  Ready. Fulfill an order:")
        print("    fulfill.py fulfill --gig <id> --intake order.txt")
    print("=" * 46)


def cmd_revenue(_):
    sales = _read_sales()
    print("=" * 46)
    print("  FULFILLMENT REVENUE  (real sales only)")
    print("=" * 46)
    if not sales:
        print("  No paid sales logged yet. Log one when a buyer actually pays:")
        print("    fulfill.py fulfill --gig <id> --intake f --price 49 --buyer X")
        print("  (Reporting $0 is the honest state, not a failure.)")
        print("=" * 46)
        return
    by_gig = {}
    for gig, _buyer, price in sales:
        by_gig.setdefault(gig, [0, 0.0])
        by_gig[gig][0] += 1
        by_gig[gig][1] += price
    gross = sum(p for _, _, p in sales)
    est_cost = len(sales) * EST_COST_PER_ORDER
    print(f"  {'gig':<22}{'orders':>7}{'revenue':>12}")
    print("-" * 46)
    for gig, (n, rev) in sorted(by_gig.items(), key=lambda x: -x[1][1]):
        print(f"  {gig:<22}{n:>7}{('$' + format(rev, ',.0f')):>12}")
    print("-" * 46)
    print(f"  Orders:            {len(sales)}")
    print(f"  Gross revenue:     ${gross:,.2f}")
    print(f"  Est. LLM cost:     ${est_cost:,.2f}  (~${EST_COST_PER_ORDER}/order)")
    print(f"  Est. net:          ${gross - est_cost:,.2f}")
    print("=" * 46)


def cmd_scaffold(args):
    if agents.get(args.id):
        sys.exit(f"Gig '{args.id}' already exists.")
    snippet = SCAFFOLD_TMPL.format(id=args.id, name=args.name)
    print("New gig-agent scaffold. Paste this entry into "
          "engine/agents/__init__.py (inside AGENTS), then edit the system "
          "prompt:\n")
    print("{\n" + snippet + "\n}")
    print(f"\nThen: fulfill.py fulfill --gig {args.id} --intake <file>")


def main():
    p = argparse.ArgumentParser(description="Fulfillment engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list").set_defaults(func=cmd_list)
    sub.add_parser("status").set_defaults(func=cmd_status)
    sub.add_parser("revenue").set_defaults(func=cmd_revenue)

    f = sub.add_parser("fulfill")
    f.add_argument("--gig", required=True)
    f.add_argument("--intake", required=True, help="path or '-' for stdin")
    f.add_argument("--max-tokens", type=int, default=8000)
    f.add_argument("--model", help="override the gig's model (e.g. claude-opus-4-8)")
    f.add_argument("--price", type=float, help="log a REAL paid sale of this amount")
    f.add_argument("--buyer", help="buyer name for the sales log (optional)")
    f.set_defaults(func=cmd_fulfill)

    s = sub.add_parser("scaffold")
    s.add_argument("--id", required=True)
    s.add_argument("--name", required=True)
    s.set_defaults(func=cmd_scaffold)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
