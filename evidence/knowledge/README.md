# SportRX Knowledge Corpus

This folder is the public metadata and curated-summary layer for the internal
SportRX Knowledge Lab. It is separate from `evidence/records/`, which remains
the authoritative source for product rules and protocols.

## Records

- `cards.json`: reviewed bilingual Knowledge Cards eligible for retrieval.
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

Direct internal retrieval begins with reviewed cards. DeepSeek synthesis stays
disabled below 60 reviewed cards; the v1 corpus target is 300 reviewed cards.
Those thresholds are corpus-governance gates, not scientific validation claims.
