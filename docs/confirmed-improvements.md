# Confirmed Improvements

Checked on 2026-06-26.

Current status: candidate. No promoted grounding improvement is claimed yet.

The value bar is adversarially-confirmed to add value.

## Promotion Bar

A grounding improvement is promoted only when it clears the repo bar:

- same workload, same model family, baseline versus grounded path
- real source material, not remembered facts
- live model call, not only static review
- reproducible receipt with source ids, citation spans, or file ids
- skeptical check that tries the recall-only or uncited path
- value maps to accuracy, trust, auditability, lower review time, or lower risk

## Current Evidence

The repo is mechanically checked:

- `python scripts/deslop_check.py`
- `python -m compileall context_grounding run.py scripts`
- `python -m unittest discover -s tests -q`
- `env -u ANTHROPIC_API_KEY PYTHON_DOTENV_DISABLED=1 python run.py`

The live demos exercise web search, web fetch, citations, and files. Those demos prove request
shape and usage-object behavior for a run. They do not yet prove that a founder workflow improved
against a baseline.

## Candidate Workloads

Grounding should be evaluated on workloads where the cost of an uncited or stale answer is real:

- customer support answers that need exact policy or changelog citations
- diligence summaries that need source spans from uploaded documents
- regulatory or compliance checks that need record ids
- product research that combines fresh web sources with internal notes

## No Promoted Wins Yet

No row is promoted until a receipt shows:

- baseline answer quality or review time
- grounded answer quality or review time
- source evidence preserved in the final answer
- reviewer objection and outcome
- failure mode where grounding should not be used

Until then, this ledger records candidate evidence only.
