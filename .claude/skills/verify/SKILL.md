---
name: verify
description: Use this skill to verify the demos whenever you add a tool, change a request shape, or touch the runner. Run it aggressively any time you touch relevant code.
---

Verify the repo with these tools, in order. Do not stop until they pass.

1. Run the demos: `ANTHROPIC_API_KEY=... python run.py`. Every demo needs a key, calls the real
   API, and must finish and refresh the receipt at data/last_run.md. Without a key the run must
   fail fast with a clear key-required message and a non-zero exit.
2. Run the deslop gate on the docs: `python scripts/deslop_check.py`. It must be clean. Offline.
3. Run the compile check: `python -m compileall context_grounding run.py scripts`. It must succeed. Offline.
4. Read the README tool table against the code in `context_grounding/demos.py`. If a row and the
   code disagree, fix the row. The repo lists only what it actually runs.
5. Confirm each demo reports a real result: the web tools report the server tool fired, citations
   reports the span count, and the files demo still deletes the file it uploads.

If no key is available, run the offline gates (steps 2 and 3) and confirm step 1 fails fast with
the key-required message under `env -u ANTHROPIC_API_KEY PYTHON_DOTENV_DISABLED=1 python run.py`.
Do not fake a run.

If you hit a blocker, find a solution and update this skill for the future, so the next change
verifies itself. This skill is meant to improve, not stay frozen.
