# SportRX Knowledge Corpus

This folder is the public metadata and curated-summary layer for the internal
SportRX Knowledge Lab. It is separate from `evidence/records/`, which remains
the authoritative source for product rules and protocols.

## Records

- `cards.json`: reviewed bilingual Knowledge Cards eligible for retrieval.
- `packs/`: reviewed domain packs loaded alongside `cards.json`; new curation
  should be added here instead of expanding the base seed indefinitely.
- `candidates.json`: unreviewed discovery records; never eligible for search or
  model context.
- `discovery_queries.json`: repeatable PubMed, OpenAlex, and Crossref search
  intents for the ten topic lanes.

## Review And Access Rules

Every card must link to an existing source record, state population, evidence
tier, limitations, review status, access tier, and permitted question policy.
Only `reviewed` cards enter the local index.

GitHub stores metadata and concise curated summaries only. Open-access or
licensed full text belongs in ignored `evidence/private/` storage and is never
committed, exported, or sent to a model provider.

The `sports_medicine_injury_rehab` lane is `research_only`: it can support
internal literature review but never diagnosis, medical clearance,
rehabilitation instructions, or individual risk estimates.

## Readiness

Direct internal retrieval currently covers 78 reviewed cards. Reaching the
60-card count only opens the answer-evaluation stage: DeepSeek synthesis remains
disabled until at least 60 manually passed answer-quality cases, bilingual
retrieval checks, citation checks, and boundary checks all pass. The v1 corpus
target remains 300 reviewed cards. These are governance gates, not scientific
validation claims.

The first goal-directed prescription pack is documented in
`../prescription/README.md`. It adds research explanations but does not enable
an assessment-only program pack or change a training dose.

The reviewed hypertrophy movement layer is documented in
`../hypertrophy/README.md`. It adds muscle-region, movement-family, equipment,
range-of-motion and exercise-selection explanations. It remains a content layer
and does not activate hypertrophy dose or progression rules.
