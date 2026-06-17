#!/usr/bin/env python3
"""One-command entry for the grounding demos.

    python run.py                   # offline: every demo, as a dry run
    python run.py web_search        # one demo, dry run
    python run.py citations --live  # one demo, real call (needs ANTHROPIC_API_KEY)
    python run.py --live            # every demo, real call

Default is the offline dry run, so no run spends a token by accident. After a run it writes a
short receipt to data/last_run.md, which the Stop hook checks before it lets an agent stop.
"""

import sys
from pathlib import Path

from context_grounding.client import get_client, key_present
from context_grounding.demos import REGISTRY

RECEIPT = Path(__file__).resolve().parent / "data" / "last_run.md"


def _names(argv):
    return [a for a in argv if not a.startswith("-")]


def _write_receipt(selected, mode):
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# last run", "", f"mode: {mode}", f"demos: {len(selected)}", ""]
    lines += [f"- {name}" for name in selected]
    RECEIPT.write_text("\n".join(lines) + "\n")


def main(argv):
    live = "--live" in argv
    names = _names(argv)

    if names:
        unknown = [n for n in names if n not in REGISTRY]
        if unknown:
            print("unknown demo(s): " + ", ".join(unknown))
            print("available: " + ", ".join(REGISTRY))
            return 2
        selected = names
    else:
        selected = list(REGISTRY)

    if live and not key_present():
        print("--live needs ANTHROPIC_API_KEY in the environment. Running dry instead.")
        live = False

    client = get_client(live=live)
    mode = "live" if live else "dry"

    for name in selected:
        summary, fn = REGISTRY[name]
        print(f"\n=== {name}  ({summary})  [{mode}] ===")
        print(fn(client))

    _write_receipt(selected, mode)
    print(f"\nran {len(selected)} demo(s) in {mode} mode. receipt: data/last_run.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
