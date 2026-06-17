---
name: verify
description: Use this skill to verify the demos whenever you add a tool, change a request shape, or touch the runner. Run it aggressively any time you touch relevant code.
---

Verify the repo with these tools, in order. Do not stop until they pass.

1. Run the offline dry run: `python run.py`. Every demo must run and the receipt at
   data/last_run.md must refresh.
2. Run the deslop gate on the docs: `python scripts/deslop_check.py`. It must be clean.
3. Read the README tool table against the code in `context_grounding/demos.py`. If a row and the
   code disagree, fix the row. The repo lists only what it actually runs, and labels a dry-only
   path instead of faking a call.
4. Check that no demo went live by accident: the dry path passes `client=None` and every line it
   prints starts with `[dry]`. Going live must stay opt-in behind `--live`.
5. If you touched a live path, sanity-check that one demo with `python run.py <demo> --live` and
   confirm the real response matches the shape the dry run prints. The files live path must still
   delete the file it uploads.

If you hit a blocker, find a solution and update this skill for the future, so the next change
verifies itself. This skill is meant to improve, not stay frozen.
