"""One function per grounding tool.

Grounding means putting fresh or document content into the model's context with provenance, so the
answer is sourced rather than recalled. Each takes a client (None for the offline dry run) and
returns text. In dry mode it prints the mechanism and the exact, current request shape. Under
--live it makes the real call and reports what came back. The REGISTRY maps a name to a one-line
summary and its function.
"""

import tempfile
from pathlib import Path

from .client import MAIN_MODEL


def _dry(*lines):
    return "\n".join("[dry] " + line for line in lines)


def web_search(client):
    if client is None:
        return _dry(
            "Server-side web search, executed on Anthropic infra, with citations on the result.",
            "The _20260209 version adds dynamic filtering, which trims results before they hit context.",
            "Use it when the answer depends on something newer than the model's training cutoff.",
            'tools=[{"type":"web_search_20260209","name":"web_search"}]',
        )
    r = client.messages.create(model=MAIN_MODEL, max_tokens=512,
                               tools=[{"type": "web_search_20260209", "name": "web_search"}],
                               messages=[{"role": "user", "content": "What is the latest Claude Opus model id?"}])
    used = any(getattr(b, "type", "") == "server_tool_use" for b in r.content)
    return f"web search server tool ran: {used}, stop_reason {r.stop_reason}"


def web_fetch(client):
    return _dry(
        "Server-side web fetch pulls a specific URL into context, executed on Anthropic infra.",
        "Pair it with web search (search to find the URL, fetch to read it) or point it at a known page.",
        "The _20260209 version adds the same dynamic filtering, trimming the page before it hits context.",
        'tools=[{"type":"web_fetch_20260209","name":"web_fetch"}]',
        "Live use is the same call shape as web_search, with a URL in the prompt for the model to fetch.",
    )


def citations(client):
    doc_text = "The capital of France is Paris. The Eiffel Tower stands in Paris."
    if client is None:
        return _dry(
            "Citations ground a response in a document and return the exact source spans it used.",
            "Attach a document block with citations enabled, then ask a question about it.",
            "Each grounded text block comes back with a citations list pointing into the source.",
            '{"type":"document","source":{"type":"text","media_type":"text/plain","data":DOC},'
            '"title":"facts","citations":{"enabled":True}}',
        )
    doc = {"type": "document",
           "source": {"type": "text", "media_type": "text/plain", "data": doc_text},
           "title": "facts", "citations": {"enabled": True}}
    r = client.messages.create(model=MAIN_MODEL, max_tokens=256, messages=[{"role": "user", "content": [
        doc, {"type": "text", "text": "Where is the Eiffel Tower? Cite the document."}]}])
    cited = sum(len(getattr(b, "citations", None) or []) for b in r.content if getattr(b, "type", "") == "text")
    return f"response carried {cited} citation span(s) back into the source document"


def files(client):
    if client is None:
        return _dry(
            "Upload a file once, reference it by file_id across many requests, with no re-upload.",
            "Files persist until deleted, operations are free, content bills as input tokens.",
            "Pair with citations to ground answers in an uploaded document.",
            'uploaded = client.beta.files.upload(file=Path("report.pdf"))',
            'then {"type":"document","source":{"type":"file","file_id":uploaded.id}}',
        )
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
