#!/usr/bin/env python3
"""Generation core — credit-efficient and redundant.

Design choices (per the explicit "optimize for credit usage + redundancy" ask):
- Per-gig model tiering: cheap models for simple work, stronger only where it
  pays. Overridable per order. (This is the biggest credit lever.)
- Prompt caching on the stable system prompt: repeat orders of the same gig
  within the cache window read the prefix at ~0.1x instead of full price.
- No extra thinking/effort tokens for straightforward content generation.
- Redundancy: SDK auto-retries transient errors; on hard failure we fall back to
  a cheaper model, then to an offline draft — an order is never lost to a blip.
- Real per-order cost is measured from usage and returned for the ledger.

If ANTHROPIC_API_KEY + the `anthropic` SDK are present it calls Claude; else it
returns an honest offline draft. Nothing here fabricates a sale.
"""
import os
from collections import namedtuple

Result = namedtuple("Result", "text model cost")

# $/1M tokens (input, output) — from the model catalog.
PRICES = {
    "claude-opus-4-8": (5.0, 25.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5": (1.0, 5.0),
}
DEFAULT_MODEL = "claude-opus-4-8"


def _offline_draft(intake, gig_name):
    return Result(
        f"[OFFLINE DRAFT — {gig_name}]\n"
        f"(Set ANTHROPIC_API_KEY and `pip install anthropic` to generate the "
        f"real deliverable.)\n\n"
        f"Structured shell built from your intake — the production prompt fills "
        f"in when a key is present.\n\n----- INTAKE -----\n{intake.strip()}\n",
        "offline", 0.0,
    )


def _cost(model, usage):
    pin, pout = PRICES.get(model, PRICES[DEFAULT_MODEL])
    g = lambda a: getattr(usage, a, 0) or 0  # noqa: E731
    return (g("input_tokens") * pin + g("output_tokens") * pout
            + g("cache_read_input_tokens") * pin * 0.1
            + g("cache_creation_input_tokens") * pin * 1.25) / 1_000_000


def _call(client, model, system_prompt, user_msg, max_tokens):
    # Cache the stable system prefix; stream so large outputs don't time out.
    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        system=[{"type": "text", "text": system_prompt,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        return stream.get_final_message()


def generate(system_prompt, intake, gig_name,
             model=DEFAULT_MODEL, max_tokens=8000,
             fallback_model="claude-haiku-4-5"):
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return _offline_draft(intake, gig_name)
    try:
        import anthropic
    except ImportError:
        return _offline_draft(intake, gig_name)

    client = anthropic.Anthropic(max_retries=3)  # auto-retry 429/5xx/network
    user_msg = (
        "Produce the complete, ready-to-deliver deliverable for this order. "
        "Use only what the intake provides; where something required is "
        "missing, insert a clearly marked [NEEDS: ...] placeholder rather than "
        "inventing facts.\n\n----- ORDER INTAKE -----\n" + intake.strip()
    )

    for attempt_model in (model, fallback_model):  # redundancy: try, then fall back
        try:
            msg = _call(client, attempt_model, system_prompt, user_msg, max_tokens)
        except Exception as e:  # noqa: BLE001 — any API/network failure
            last_err = e
            continue
        if msg.stop_reason == "refusal":
            return Result("[REFUSED] The model declined this order. Review the "
                          "intake for anything that tripped a safety filter, or "
                          "handle it manually.", attempt_model, _cost(attempt_model, msg.usage))
        text = "".join(b.text for b in msg.content if b.type == "text").strip()
        return Result(text, attempt_model, _cost(attempt_model, msg.usage))

    # Both models failed — never drop the order.
    draft = _offline_draft(intake, gig_name)
    return Result(draft.text + f"\n\n[NOTE: live generation failed ({last_err}); "
                  "offline draft returned so the order isn't lost.]",
                  "offline", 0.0)
