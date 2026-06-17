"""Anthropic client and model routing.

Demos default to Haiku for cheap calls and Opus where the feature wants a frontier model. Going
live is opt-in: `get_client` returns None unless a demo is run with `--live`, so no run spends a
token by accident.
"""

import os

FAST_MODEL = "claude-haiku-4-5"
MAIN_MODEL = "claude-opus-4-8"


def key_present() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def get_client(live: bool = False):
    if not live:
        return None
    if not key_present():
        raise RuntimeError("live mode needs ANTHROPIC_API_KEY in the environment")
    import anthropic

    return anthropic.Anthropic()
