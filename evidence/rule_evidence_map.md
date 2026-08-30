# Rule Evidence Map

This map connects SportRx product rules to evidence. It should be updated before
new rules enter the app.

## Rule Status Labels

| Status | Meaning |
| --- | --- |
| `allowed_ui` | Can appear in normal product screens |
| `explain_only` | Can appear under "Why this result?" but should be caveated |
| `internal_only` | Can be used for development/testing, not normal UX |
| `blocked` | Should not be used until validated |

## Current Rules

| Rule ID | Product rule | Inputs | Evidence tier | Sources | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| SAFE-001 | Safety Gate must be separate from performance scoring | Symptoms, known conditions, injury flags, intended intensity | A/D | SAFE-EIM, SAFE-EIM-SCREEN, SAFE-PARQ, SAFE-ACSM-ALGO | allowed_ui | Safety can block training handoff; it must not change measured performance values |
| CORE-001 | General adult aerobic target can reference 150 min/week moderate activity | Weekly minutes, intensity category | A | PA-WHO-2020, PA-CDC-ADULT, PA-ACSM-CDC, PA-AHA | allowed_ui | Use as health target, not as a race-readiness threshold |
| CORE-002 | FITT-VP can structure basic aerobic prescription | Frequency, intensity, time, type, volume, progression | A | PA-ACSM-GETP12 | allowed_ui | Keep within apparently healthy adult scope |
| INT-001 | RPE can be used when HR devices are unavailable | Session RPE or target RPE range | B | MON-RPE-ACSM, MON-SRPE-FOSTER, MON-SRPE-REVIEW | allowed_ui | Explain subjectivity and need for consistent use |
| MEAS-001 | Missing performance tests remain `Not tested` | Empty benchmark fields | D | TEST-FIELD-ADULT, SportRx principle | allowed_ui | This is a measurement integrity rule, not a literature-derived threshold |
| MEAS-002 | At least two measured performance dimensions are required before comparing strongest area vs main gap | Measured running/station/strength/work-capacity scores | D/E | TEST-FIELD-ADULT, SportRx principle | explain_only | Plausible but not validated; should be tested with real users |
| HYB-001 | HYROX profile should include running, aerobic base, strength endurance, station experience, and work capacity | Hybrid check fields | C/D | HYROX-PHYS-2025, HIFT-HYBRID-REVIEW, HIFT-DEFINITION | explain_only | Direct HYROX evidence is young; keep claims conservative |
| QM-001 | Quick Match should use recent behavior inputs rather than subjective self-rating sliders | Age, training days, weekly minutes, running/walking minutes, longest continuous run/walk, strength days, recent high-intensity and loaded sessions | D/E | SportRx usability principle, MEAS-001 | allowed_ui | Reduces ambiguity; still a coarse profile match, not performance measurement |
| HYB-002 | SportRx Hybrid Benchmark v1 is a measurement layer, not a validated score | Benchmark result fields | D/E | TEST-6MWT-ATS, TEST-FIELD-ADULT, HYROX-PHYS-2025 | allowed_ui | Use raw results and retest change before norms |
| PROTOCOL-001 | Benchmark testing should declare component evidence status, setup, order, stop rules, recording fields, and retest notes before logs are interpreted | Equipment access, benchmark path, component protocol, protocol evidence status | B/D/E | TEST-1000M-ADULT-2000, TEST-6MRT-ADULT-2023, ERG-SKIERG-1000M-2025, ERG-ROWERG-ACCURACY-2022, CN-NPFS-2023 | allowed_ui | 1 km, 6-minute and erg records are partial evidence; station and compromised-run protocols remain experimental |
| LOG-001 | Benchmark sessions should store raw component results, RPE, equipment, substitutions, protocol version, context and notes before any scoring layer | Benchmark component fields and protocol context | D/E | TEST-FIELD-RELIABILITY, TEST-1000M-ADULT-2000, TEST-6MRT-ADULT-2023 | allowed_ui | Exportable logs support future validation; changed context is not directly comparable |
| LOG-002 | Benchmark logs may update HYROX Check only when the raw unit maps directly to an existing measured input | Benchmark session fields | D/E | MEAS-001, LOG-001 | allowed_ui | Do not convert rounds, distance, or mixed work into 0-100 scores unless a documented scoring rule exists |
| LOG-003 | Benchmark Log should show HYROX Check import compatibility before saving | Benchmark component fields, equipment/modality fields | D/E | LOG-001, LOG-002 | allowed_ui | Makes direct imports, missing modality details, and raw-only results visible without adding scoring |
| PATH-001 | If measured data are insufficient, do not generate tailored Starter Path | Measured dimension count, main gap | D/E | SportRx principle | allowed_ui | Route to benchmark first |
| PATH-002 | If station/strength is main gap, starter path emphasizes controlled station-specific strength endurance | Main gap | C/D | HIFT-HYBRID-REVIEW, HIFT-FITNESS, HYROX-PHYS-2025 | explain_only | Should be framed as a reasonable starting focus, not an outcome guarantee |
| PATH-003 | If running/aerobic is main gap, starter path emphasizes repeatable aerobic running volume | Main gap, training availability | A/C/D | PA-WHO-2020, PA-ACSM-GETP12, HYROX-PHYS-2025 | explain_only | Do not over-prescribe race-specific intensity without data |
| PRED-001 | Race finish prediction, injury-risk percentage, and fake percentiles are blocked | Any | E | None | blocked | Needs real SportRx dataset and validation |

## Promotion Rules

A rule can move from `explain_only` to `allowed_ui` only when:

- the input data are available in the app,
- the rule has a stable evidence citation,
- the user-facing claim is conservative,
- and the failure mode is acceptable.

A rule can move from `internal_only` or `blocked` only after a written validation
note is added to `evidence/validation.md`.

## Required Maintenance

When a rule changes, update:

- the rule row in this file,
- the relevant source note in `source_notes/`,
- the public claim boundary in `claim_policy.md` if the user-facing language
  changes,
- and `validation.md` if the validation status changes.
