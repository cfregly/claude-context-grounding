"""One function per grounding tool, online.

Grounding means putting fresh or document content into the model's context with provenance, so the
answer is sourced rather than recalled. Each function takes a real client and makes a real API
call, then reports what came back. There is no offline mode.
"""

import tempfile
from pathlib import Path

from .client import MAIN_MODEL


def web_search(client):
    """Server-side web search on Anthropic infra, with citations. The _20260209 version adds dynamic filtering."""
    r = client.messages.create(model=MAIN_MODEL, max_tokens=512,
                               tools=[{"type": "web_search_20260209", "name": "web_search"}],
                               messages=[{"role": "user", "content": "What is the latest Claude Opus model id?"}])
    used = any(getattr(b, "type", "") == "server_tool_use" for b in r.content)
    return f"web search server tool ran: {used}, stop_reason {r.stop_reason}"


def web_fetch(client):
    """Server-side fetch of a specific URL into context, on Anthropic infra, with the same dynamic filtering."""
    r = client.messages.create(model=MAIN_MODEL, max_tokens=512,
                               tools=[{"type": "web_fetch_20260209", "name": "web_fetch"}],
                               messages=[{"role": "user", "content": (
                                   "Fetch https://docs.claude.com/en/docs/about-claude/models and name "
                                   "one Claude model you find on that page.")}])
    used = any(getattr(b, "type", "") == "server_tool_use" for b in r.content)
    return f"web fetch server tool ran: {used}, stop_reason {r.stop_reason}"


def citations(client):
    """Attach a document with citations enabled, ask about it, get the exact source spans back."""
    doc_text = "The capital of France is Paris. The Eiffel Tower stands in Paris."
    doc = {"type": "document",
           "source": {"type": "text", "media_type": "text/plain", "data": doc_text},
           "title": "facts", "citations": {"enabled": True}}
    r = client.messages.create(model=MAIN_MODEL, max_tokens=256, messages=[{"role": "user", "content": [
        doc, {"type": "text", "text": "Where is the Eiffel Tower? Cite the document."}]}])
    cited = sum(len(getattr(b, "citations", None) or []) for b in r.content if getattr(b, "type", "") == "text")
    return f"response carried {cited} citation span(s) back into the source document"


def files(client):
    """Upload a file via the Files API, reference it by file_id, then delete it."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
        fh.write("hello from claude-context-grounding")
        path = fh.name
    try:
        uploaded = client.beta.files.upload(file=Path(path))
        client.beta.files.delete(uploaded.id)
        return f"uploaded file {uploaded.id}, referenced by file_id, then deleted it"
    finally:
        Path(path).unlink(missing_ok=True)


REGISTRY = {
    "web_search": ("server-side web search with citations", web_search),
    "web_fetch": ("server-side fetch of a specific URL", web_fetch),
    "citations": ("ground a response in a document, get the spans back", citations),
    "files": ("upload once, reference by file_id", files),
}
