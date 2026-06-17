# claude-context-grounding

A runnable reference for **grounding Claude in fresh and document sources, with provenance**: one
small, correct demo of each grounding tool, in one repo. Grounding means putting real content into
the model's context and getting the source spans back, so the answer is cited rather than recalled.
Every demo makes a real API call.

```bash
pip install -r requirements.txt

ANTHROPIC_API_KEY=... python run.py                # every demo, real calls
ANTHROPIC_API_KEY=... python run.py citations      # one demo, real call
```

This is a real tool. Every run calls the Anthropic API, so `ANTHROPIC_API_KEY` is required. Without
a key it fails fast with a clear error and a non-zero exit. There is no offline mode and no fallback.

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
