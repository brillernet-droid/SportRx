# SportRx Evidence Knowledge Base

This folder is the working evidence base for SportRx. It is not a RAG system yet.
Its job is to keep the product honest:

- what SportRx can claim,
- what SportRx can measure,
- what SportRx only infers,
- and what still needs real user data.

## Evidence Tiers

SportRx uses five evidence tiers.

| Tier | Label | Meaning | Product use |
| --- | --- | --- | --- |
| A | Guideline-backed | Major public-health, clinical exercise, or sport-science guideline | Can support product rules and user-facing explanations |
| B | Validated field-test evidence | A test or monitoring method has reliability, validity, or standardized protocol support | Can support measurement protocols and retesting logic |
| C | Peer-reviewed sport-specific evidence | Direct evidence in HYROX, HIFT, hybrid competition, or closely related formats | Can support sport-specific emphasis, with caveats |
| D | Expert-informed | Plausible rule based on exercise science and coaching logic, but not directly validated for SportRx | Can be used if labelled clearly |
| E | Experimental SportRx rule | Internal prototype rule or hypothesis | Must not be presented as validated |

## Current Evidence Position

Stable enough for v0.2:

- General adult aerobic and muscle-strengthening activity targets.
- Basic FITT-VP aerobic prescription for apparently healthy adults.
- Safety gate separation from performance scoring.
- RPE as a practical intensity and training-load input.
- Repeatable field testing as a measurement layer.

Not stable enough yet:

- HYROX completion prediction.
- Injury-risk percentages.
- Population percentiles.
- Validated SportRx readiness score.
- Validated HYROX-specific benchmark cutoffs.

## Knowledge Base Workflow

Every new SportRx rule should have:

1. A `rule_id`.
2. A user-facing claim.
3. Required input data.
4. Evidence tier.
5. Source references.
6. Known limits.
7. Whether the rule is allowed in the normal UI.

Rules without this mapping should stay out of product output.

## Operating Documents

- `README.md`: directory map and update rule.
- `claim_policy.md`: allowed and forbidden user-facing claims.
- `glossary.md`: controlled product vocabulary.
- `library/`: saved citation records grouped by topic.
- `literature_matrix.md`: source registry.
- `evidence_appraisal.md`: product-area evidence strength and current decision.
- `evidence_questions.md`: unanswered evidence questions.
- `rule_evidence_map.md`: rule-to-evidence traceability.
- `validation_plan.md`: self-use, alpha, and pilot evidence plan.
- `data_governance.md`: future participant-data boundary; the repository does not collect real participant data.
- `source_notes/`: topic-level notes that translate literature into product
  constraints.
- `intake_queue.md`: sources to review before inclusion.
- `templates/`: repeatable forms for source and rule review.

## Source Note Standard

Each source note should state:

- what the evidence supports,
- what it does not support,
- which SportRx rules it affects,
- what user-facing language is allowed,
- and what language is not allowed.

This prevents citation inflation: a source only matters if it changes or
constrains a product rule.

## Retrieval Status

SportRX now has a structured evidence-record layer and local internal SQLite
FTS5 retrieval. It indexes reviewed source metadata, claims, rules, and
protocols; it does not index copyrighted full text or generate answers.

The retrieval layer may support internal rule review and a future bounded
"Why this result?" explanation surface. It must not decide:

- Safety Gate status,
- exercise intensity, weekly volume, or progression,
- medical clearance,
- race prediction, injury risk, or athlete percentiles.

LLM-backed RAG remains deferred until SportRX has 50-100 curated evidence notes,
real measurement/retest data, a larger retrieval evaluation set, and a written
policy proving generated text cannot change exercise dose.
