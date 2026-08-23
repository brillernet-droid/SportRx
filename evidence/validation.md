# Validation Notes

SportRx 2.2 does not claim formal validation.

## Evidence-Backed

- General adult aerobic activity targets used by SportRx Core.
- RPE, talk-test, HRmax, and HRR intensity guidance used by SportRx Core.
- Exercise preparticipation screening principles behind the Safety Gate.
- Recent training behavior fields such as days/week, minutes/week, and recent
  session counts are treated as self-reported context, not validated
  performance tests.

## Expert-Informed

- Hybrid Race performance dimensions:
  - Running
  - Aerobic fitness
  - Strength endurance
  - Station experience
  - Work capacity
- Main-gap rules when at least two measured performance areas are available.
- 4-week starter path focus rules.
- Station circuit and Work capacity 1-100 fields are treated as
  protocol-derived review fields. They require a named protocol source or
  Benchmark Log provenance before they can count as measured performance.
- Protocol source fields document provenance and gate whether protocol-derived
  scores are usable for measured-profile comparison. They do not validate
  cutoffs or create norms.

## Experimental

- Quick Match fit categories.
- Training Profile labels.
- Internal aggregate scoring used for development and tests, hidden from the
  normal user experience.
- Public Beta Readiness status as a product-release gate, not a validation
  result.
- Phase 0 Self-Use Protocol as an operating checklist for builder self-use,
  not as proof that SportRx is validated.
- Legacy subjective background / comfort ratings are retained only as ignored
  compatibility fields in the Input Ledger.
- Lab Test Quality status is a protocol-provenance gate only. It does not
  change measured scores or validate benchmark cutoffs.
- Benchmark Log import compatibility is a data-handoff gate only. It identifies
  direct HYROX Check imports, missing RowErg/SkiErg modality details, and
  raw-only results without creating synthetic scores.

## Not Validated

- SportRx Hybrid Benchmark v1 cutoffs.
- Race outcome prediction.
- Injury prediction.
- Population percentiles.

SportRx should collect real retest data before claiming benchmark norms,
predictive accuracy, or validated preparation thresholds.

## Knowledge Base Status

As of SportRx 2.2, the internal evidence base is structured but not yet a RAG
system. The current validation task is to map each product rule to evidence and
collect repeatable benchmark/retest data before adding retrieval-augmented
generation.

See also:

- `evidence/evidence_appraisal.md`
- `evidence/evidence_questions.md`
- `evidence/validation_plan.md`
