#!/usr/bin/env python3
"""One-command entry for the grounding demos. Online only.

    ANTHROPIC_API_KEY=... python run.py                # every demo, real call
    ANTHROPIC_API_KEY=... python run.py citations      # one demo, real call

Requires ANTHROPIC_API_KEY. Every run calls the real Anthropic API. Without a key it fails fast
with a clear error and a non-zero exit. After a run it writes a receipt to data/last_run.md,
which the Stop hook checks before it lets an agent stop.
"""

import sys
from pathlib import Path

from context_grounding.client import get_client, require_key
from context_grounding.demos import REGISTRY

RECEIPT = Path(__file__).resolve().parent / "data" / "last_run.md"


def _names(argv):
    return [a for a in argv if not a.startswith("-")]


def _write_receipt(selected):
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# last run", "", f"demos: {len(selected)}", ""] + [f"- {n}" for n in selected]
    RECEIPT.write_text("\n".join(lines) + "\n")


def main(argv):
    try:
        require_key()
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    names = _names(argv)
    unknown = [n for n in names if n not in REGISTRY]
    if unknown:
        print("unknown demo(s): " + ", ".join(unknown))
        print("available: " + ", ".join(REGISTRY))
        return 2
    selected = names or list(REGISTRY)

    client = get_client()
    for name in selected:
        summary, fn = REGISTRY[name]
        print(f"\n=== {name}  ({summary}) ===")
        print(fn(client))

    _write_receipt(selected)
    print(f"\nran {len(selected)} demo(s) live. receipt: data/last_run.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
