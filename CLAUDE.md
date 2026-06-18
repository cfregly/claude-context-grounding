# CLAUDE.md

Conventions for any agent working on `claude-grounding`. Read this first.

## What this is

A runnable reference for grounding Claude in fresh and document sources, with provenance: one
small, correct demo of each grounding tool, in one repo. Server-side web search, server-side web
fetch, document citations, and the Files API. Each demo makes a real API call.

This is a standalone platform deep-dive beside `claude-founder-kit`, not a stage module inside the
main kit. The web tools track the current `_20260209` versions.

## Run it

    pip install -r requirements.txt
    ANTHROPIC_API_KEY=... python run.py                # every demo, real calls
    ANTHROPIC_API_KEY=... python run.py citations      # one demo, real call

## Rules

- Key required, fail fast. Every run calls the real Anthropic API, so `ANTHROPIC_API_KEY` is
  required. Without a key the run fails fast with a clear error and a non-zero exit. There is no
  offline mode and no fallback.
- Shapes are current, not invented. The web tools are `web_search_20260209` and `web_fetch_20260209`.
  If a tool version moves, fix the shape rather than guess.
- Claim only what runs. Each demo reports what the real response carried (the server tool fired,
  the citation spans, the uploaded file id). The `files` demo deletes the file it uploads.
- Prose is deslop-clean: no em-dashes, no en-dashes, no semicolons, no buzzwords. CI runs the
  deslop gate on the README and this file, a compile check, and a fail-fast-without-a-key check.
- Never commit a key. `.env` stays git-ignored.
