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


def cmd_list(_):
    print("Available gig-agents:\n")
    for gid in agents.ids():
        a = agents.get(gid)
        print(f"  {gid:<20} {a['name']:<28} ${a['price']}/order")
    print("\nFulfill one:  fulfill.py fulfill --gig <id> --intake <file|->")


def cmd_fulfill(args):
    a = agents.get(args.gig)
    if not a:
        sys.exit(f"Unknown gig '{args.gig}'. Run `fulfill.py list`.")
    intake = _read_intake(args.intake)
    if not intake.strip():
        sys.exit("Empty intake. Pass a file or pipe the intake on stdin.")

    print(f"Fulfilling '{a['name']}'…", file=sys.stderr)
    deliverable = generate(a["system"], intake, a["name"],
                           max_tokens=args.max_tokens)

    n = _next_index(args.gig)
    out_path = os.path.join(ORDERS_DIR, f"{args.gig}-{n}.md")
    header = (f"# {a['name']} — order #{n}\n"
              f"_Generated {datetime.date.today().isoformat()}. "
              f"Spot-check before delivering._\n\n---\n\n")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header + deliverable + "\n")
    _log_order(args.gig, out_path, len(deliverable))
    print(f"\n✅ Deliverable written to {out_path}")
    print("   Review it, then deliver it to the buyer and collect payment.")


SCAFFOLD_TMPL = '''    "{id}": {{
        "name": "{name}",
        "price": "TODO",
        "system": (
            "You are an expert producing a paid {name} deliverable. "
            "Describe exactly what to output from the buyer's intake here. "
            "Never fabricate facts; mark gaps with [NEEDS: ...]."
        ),
    }},'''


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

    f = sub.add_parser("fulfill")
    f.add_argument("--gig", required=True)
    f.add_argument("--intake", required=True, help="path or '-' for stdin")
    f.add_argument("--max-tokens", type=int, default=8000)
    f.set_defaults(func=cmd_fulfill)

    s = sub.add_parser("scaffold")
    s.add_argument("--id", required=True)
    s.add_argument("--name", required=True)
    s.set_defaults(func=cmd_scaffold)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
