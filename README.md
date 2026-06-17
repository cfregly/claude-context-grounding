# claude-context-grounding

A runnable reference for **grounding Claude in fresh and document sources, with provenance**: one
small, correct demo of each grounding tool, in one repo. Grounding means putting real content into
the model's context and getting the source spans back, so the answer is cited rather than recalled.
Every demo runs offline by default and prints the exact request shape. Add `--live` to make the
real call.

```bash
pip install -r requirements.txt

python run.py                              # offline: every demo, as a dry run
python run.py citations                    # one demo, dry run
ANTHROPIC_API_KEY=... python run.py citations --live   # one demo, real call
```

## A note on honesty

This is a standalone reference repo, a bonus alongside the six `claude-startup-*` repos, not one
of them. Every demo uses a current, shipped request shape (the web tools are the `_20260209`
versions). The offline run prints `[dry]` on every line it simulates. `web_search`, `citations`,
and `files` have real `--live` paths. `web_fetch` is shown as a dry shape only, because a live
fetch needs a specific reachable URL, and the call shape is identical to `web_search`.

## The tools

| Tool | What the demo shows |
|---|---|
| `web_search` | server-side web search on Anthropic infra, with citations, `web_search_20260209` |
| `web_fetch` | server-side fetch of a specific URL, `web_fetch_20260209`, same dynamic filtering |
| `citations` | a document block with citations enabled, and the source spans returned on the answer |
| `files` | upload once with the Files API, reference by `file_id`, no re-upload across requests |

The repo also ships a `verify` skill and a Stop hook under `.claude/`, which is the skills and
hooks feature demonstrating itself.

## How the tools compose

The real pattern chains them: `web_search` finds the page, `web_fetch` reads it, or `files` brings
your own document in, and `citations` makes the answer point back at the exact span it used. That
chain is what turns a plausible answer into a sourced one.

## Layout

```
context_grounding/
  client.py    # the client, or None for the offline dry run, and model routing
  demos.py     # one function per tool, plus the registry
run.py         # one-command entry: all tools, or one, dry or --live
scripts/       # the self-contained deslop gate for CI
.claude/       # the verify skill and the Stop hook (skills + hooks, demonstrated)
```

## License

MIT.
