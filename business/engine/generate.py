#!/usr/bin/env python3
"""Generation core for the fulfillment engine.

If ANTHROPIC_API_KEY is set and the `anthropic` SDK is installed, this calls
Claude (claude-opus-4-8, adaptive thinking, streaming) to produce the real
deliverable. Otherwise it returns a structured offline draft so the engine
always runs, is demoable, and never blocks on a missing key.

Nothing here fabricates a *sale* — it produces the *work product* for an order
you actually received.
"""
import os

MODEL = "claude-opus-4-8"


def _offline_draft(system_prompt, intake, gig_name):
    """Deterministic, honest fallback when no API access is available."""
    return (
        f"[OFFLINE DRAFT — {gig_name}]\n"
        f"(Set ANTHROPIC_API_KEY and `pip install anthropic` to generate the "
        f"real deliverable via {MODEL}.)\n\n"
        f"This is the structured shell the engine produced from your intake. "
        f"The production prompt below is what gets sent to Claude when a key is "
        f"present; the intake is what fills it.\n\n"
        f"----- INTAKE RECEIVED -----\n{intake.strip()}\n\n"
        f"----- WHAT WILL BE PRODUCED -----\n"
        f"A finished {gig_name} deliverable built to the spec in the production "
        f"prompt, ready for your final spot-check before delivery.\n"
    )


def generate(system_prompt, intake, gig_name, max_tokens=8000):
    """Return a finished deliverable string for one order."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _offline_draft(system_prompt, intake, gig_name)
    try:
        import anthropic
    except ImportError:
        return _offline_draft(system_prompt, intake, gig_name)

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    user_msg = (
        "Produce the complete, ready-to-deliver deliverable for this order. "
        "Use only what the intake provides; where the intake is missing "
        "something required, insert a clearly marked [NEEDS: ...] placeholder "
        "rather than inventing facts.\n\n"
        f"----- ORDER INTAKE -----\n{intake.strip()}"
    )
    # Streaming per the API guidance for potentially long outputs.
    with client.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        message = stream.get_final_message()

    if message.stop_reason == "refusal":
        return ("[REFUSED] The model declined this request. Review the intake "
                "for anything that tripped a safety classifier, or handle it "
                "manually.")
    return "".join(b.text for b in message.content if b.type == "text").strip()
