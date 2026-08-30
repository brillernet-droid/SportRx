# SportRX

> **A standardized measurement creates an explainable training start point, then retest makes change visible.**

SportRX is a measurement-first exercise decision prototype for gyms, running
clubs, and training groups. It is not an AI fitness coach and does not turn a
short questionnaire into a performance assessment.

The venue-entry core loop is:

```text
external screening pathway → Safety Gate → Hybrid Benchmark → Training Profile → Starter Path → RPE / Completion → Retest
```

SportRX keeps Safety Gate separate from measured performance. It records raw
benchmark results, protocol context, RPE, equipment and deviations; preserves
missing tests as `Not tested`; and only creates a conservative Starter Path
when its measurement requirements are met.

## Current status

This is a measurement-first prototype. Current work focuses on self-use,
small-sample usability testing, and institution pilots. SportRX does not claim
medical clearance, injury-risk percentages, race predictions, population
percentiles, validated readiness scores, or official event certification.

AI does not decide safety, exercise dose, weekly volume, or progression.

## Venue Entry status

Venue Entry keeps screening separate from measurement. SportRX records only
minimal routing metadata from a configured external screening pathway; it does
not reproduce, translate, score, or store screening answers. Only an explicit
`eligible_for_benchmark` route can open Benchmark. The default Chinese
deployment is `research_required`, so it is internal/demo-only until a lawful,
locally applicable pathway, consent process, retention window, deletion route,
and staff escalation process are documented.

## Internal Knowledge RAG

The repository also contains an internal, Chinese-answer research layer under
[`evidence/knowledge/`](evidence/knowledge/README.md). It indexes only
human-reviewed bilingual knowledge cards and stays separate from the
deterministic rule-evidence store. The optional DeepSeek synthesis path remains
disabled until the corpus and citation, boundary, and answer-quality gates pass.

## Run locally

```bash
python3 -m pip install -e ".[dev,app]"
python3 scripts/smoke_check.py
bash scripts/run_local.sh
```

The primary early-testing interface is Chinese. Select `中文版` in the local
demo. English Lab Edition is available for copy review.

## Chinese documentation

- [Quick start](docs/zh-CN/quickstart.md)
- [Product guide](docs/zh-CN/product-guide.md)
- [Claim boundaries](docs/zh-CN/claim-boundaries.md)
- [Terminology](docs/zh-CN/terminology.md)
- [Venue Entry (Chinese)](docs/zh-CN/venue-entry.md)

Technical evidence, rule IDs, schemas, and source documents remain in English
under [`evidence/`](evidence/).
