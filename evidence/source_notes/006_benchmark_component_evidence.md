# Benchmark Component Evidence Ledger

## Scope

This note connects reviewed sources to the five SportRX Hybrid Benchmark v1
component families. It is a protocol-evidence ledger, not a validation claim.
The machine-readable records are in `evidence/records/`.

| Component | SportRX status | What can be said | What cannot be said |
| --- | --- | --- | --- |
| 1 km run | `partial_evidence` | Keep route, surface, incline, warm-up and timing consistent for a raw personal retest | It is a validated SportRX hard-run score, norm or equivalent to a 6-minute test |
| 6-minute run/walk | `partial_evidence` | Keep the variant and setup consistent for a raw personal retest | A run/walk has the same validation/reference values as continuous running or converts to 1 km time |
| RowErg / SkiErg 1 km | `partial_evidence` | Keep erg type, model, setting, familiarization, order, raw time and RPE consistent | RowErg and SkiErg are interchangeable or yield a recreational percentile |
| Station circuit | `experimental` | Preserve movement, load, sequence, rest, result and RPE for a protocol-consistent personal record | It is a validated circuit, score, meaningful-change test or HYROX predictor |
| Compromised run / transition | `experimental` | Preserve preceding work, route, surface, time and RPE as a contextual raw record | It is a validated fatigue index, change threshold or event predictor |

## Reviewed Sources

- `TEST-1000M-ADULT-2000`: a 51-person healthy-adult 1,000 m walk-run study;
  it does not validate SportRX hard-running conditions.
- `TEST-6MRT-ADULT-2023`: standardized 6-minute **run** in healthy adults;
  SportRX does not import reference equations and keeps run/walk partial.
- `ERG-SKIERG-1000M-2025`: small national-level skier study; device and
  population scope do not generalize to recreational hybrid users.
- `ERG-ROWERG-ACCURACY-2022`: monitor/device accuracy under controlled rig
  conditions, not human-performance validation.
- `ERG-ROWERG-RELIABILITY-1999`: trained-rower 2,000 m reliability, not a
  1,000 m recreational SportRX standard.
- `CN-NPFS-2023`: China-local terminology/method boundary only; no official
  grades, norms or composite scores are imported.

## Future Evidence Needed

- direct recreational-adult reliability for the exact RowErg/SkiErg 1 km
  protocol;
- direct reliability/feasibility for the SportRX station and compromised-run
  protocols; and
- consented, de-identified SportRX test-retest data collected under a separate
  Phase 0 / Alpha process.
