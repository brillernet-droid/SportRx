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
- SportRX station circuit and fatigue-after-circuit running are experimental
  protocols. They are stored as raw context-rich records, not validated tests,
  aggregate scores, minimum-change thresholds or race predictors.

## Partial Evidence

- The 1 km record uses adult 1,000 m walk-run evidence as a constrained
  retest-reference only; it does not validate SportRX hard-running conditions,
  norms or score cutoffs.
- The low-equipment 6-minute option is informed by an adult continuous-run
  study. SportRX run/walk remains a broader partial-evidence protocol and does
  not use published reference equations.
- RowErg/SkiErg records are device-specific personal retest records. SportRX
  does not cross-convert RowErg and SkiErg, provide recreational norms, or
  assign an event prediction.
- Chinese national physical-fitness material is a local terminology/method
  reference only. SportRX does not import official grades, norms or composite
  scores.

## Not Validated

- SportRx Hybrid Benchmark v1 cutoffs.
- Race outcome prediction.
- Injury prediction.
- Population percentiles.

SportRx should collect real retest data before claiming benchmark norms,
predictive accuracy, or validated preparation thresholds.

## Knowledge Base Status

As of SportRX 2.2, the internal evidence base has structured source, claim,
rule, and protocol records with local internal SQLite FTS5 retrieval. It can
trace a product rule to its reviewed conclusion, source metadata, and stated
limits. It does not index copyrighted full text, collect participant data, or
generate answers.

The current validation task remains collecting repeatable Benchmark/retest data
and testing the product's own conservative rules. LLM-backed retrieval remains
out of scope until the evidence-note volume, retrieval evaluation set, data
governance and dose-control policy are substantially stronger.

See also:

- `evidence/evidence_appraisal.md`
- `evidence/evidence_questions.md`
- `evidence/validation_plan.md`
- `evidence/data_governance.md`
- `evidence/source_notes/006_benchmark_component_evidence.md`
