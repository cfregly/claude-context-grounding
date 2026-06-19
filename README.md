# claude-grounding

[![ci](https://github.com/cfregly/claude-grounding/actions/workflows/ci.yml/badge.svg)](https://github.com/cfregly/claude-grounding/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A runnable reference for **grounding Claude in fresh and document sources, with provenance**: one
small, correct demo of each grounding tool, in one repo. Grounding means putting real content into
the model's context and getting the source spans back, so the answer is cited rather than recalled.
Every demo makes a real API call.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

ANTHROPIC_API_KEY=... python run.py                # every demo, real calls
ANTHROPIC_API_KEY=... python run.py citations      # one demo, real call
```

This is a real tool. Every run calls the Anthropic API, so `ANTHROPIC_API_KEY` is required. Without
a key it fails fast with a clear error and a non-zero exit. There is no offline mode and no fallback.

## Verify it

```bash
python scripts/deslop_check.py
python -m compileall context_grounding run.py scripts
env -u ANTHROPIC_API_KEY PYTHON_DOTENV_DISABLED=1 python run.py  # should fail fast, non-zero
```

## The tools

Every tool uses a current, shipped request shape (the web tools are the `_20260209` versions).

| Tool | What the demo does |
|---|---|
| `web_search` | runs server-side web search (`web_search_20260209`), reports the server tool fired |
| `web_fetch` | fetches a specific URL server-side (`web_fetch_20260209`), reports the server tool fired |
| `citations` | sends a document with citations enabled, reports the source spans returned on the answer |
| `files` | uploads a file with the Files API, references it by `file_id`, then deletes it |

The repo also ships a `verify` skill and a Stop hook under `.claude/`, which is the skills and
hooks feature demonstrating itself.

## How the tools compose

The real pattern chains them: `web_search` finds the page, `web_fetch` reads it, or `files` brings
your own document in, and `citations` makes the answer point back at the exact span it used. That
chain is what turns a plausible answer into a sourced one.

## Layout

```
context_grounding/
  client.py    # the real client, key required, and model routing
  demos.py     # one function per tool, plus the registry
run.py         # one-command entry: all tools, or one, all live
scripts/       # the self-contained deslop gate for CI
.claude/       # the verify skill and the Stop hook (skills + hooks, demonstrated)
```

## License

MIT.
