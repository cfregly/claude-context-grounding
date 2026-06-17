# CLAUDE.md

Conventions for any agent working on `claude-context-grounding`. Read this first.

## What this is

A runnable reference for grounding Claude in fresh and document sources, with provenance: one
small, correct demo of each grounding tool, in one repo. Server-side web search, server-side web
fetch, document citations, and the Files API. Each demo runs offline as a dry run that prints the
mechanism and the exact request shape, and runs for real with `--live`.

This is a standalone reference repo, a bonus alongside the six `claude-startup-*` repos, not one of
them. The web tools track the current `_20260209` versions. Where a path is dry only, the docs say
so and never fake a call.

## Run it

    pip install -r requirements.txt
    python run.py                              # offline, runs every demo as a dry run
    python run.py citations                    # one demo, dry run
    ANTHROPIC_API_KEY=... python run.py citations --live    # one demo, real call

## Rules

- Runs in one command. `python run.py` works with no key and prints every tool's request shape.
- Going live is opt-in. Only `--live` constructs a real client, so no run spends a token by accident.
- Shapes are current, not invented. The web tools are `web_search_20260209` and `web_fetch_20260209`.
  If a tool version moves, fix the shape rather than guess.
- Claim only what runs. `web_search`, `citations`, and `files` run live. `web_fetch` is a dry shape
  only, because a live fetch needs a specific reachable URL. The dry run labels every line `[dry]`.
- The `files` live path cleans up after itself: it uploads a tiny file, references it, then deletes it.
- Prose is deslop-clean: no em-dashes, no en-dashes, no semicolons, no buzzwords. CI runs the
  deslop gate on the README and this file.
- Never commit a key. `.env` stays git-ignored.
