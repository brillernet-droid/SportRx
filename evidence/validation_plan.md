# SportRx Validation Plan

SportRx needs practice-based evidence, not just citations.

This file defines the first validation path for the prototype.

## Validation Principle

Do not validate the whole product at once.

Validate small claims:

- Can users complete the benchmark correctly?
- Are the tests repeatable enough for recreational use?
- Does SportRx correctly avoid giving tailored plans when measured data are
  missing?
- Do users understand `Not tested`, `Strongest Area`, and `Main Gap`?
- Does a 4-week Starter Path lead to usable retest data?

## Phase 0: Self-Use

Sample:

- 1 user: the builder.

Duration:

- 4 weeks.

Data to collect:

- Baseline SportRx Hybrid Benchmark v1.
- Weekly training completion.
- Session RPE.
- Notes on pain, unusual fatigue, or inability to complete.
- Week 4 retest using the same setup.

Goal:

- Find product friction and obvious nonsense before inviting others.
- Use the exportable `sportrx_phase_0_self_use_protocol.md` pack as the
  operating checklist for baseline, weekly notes, Week 4 retest, and claim
  boundaries.

Success criteria:

- The user can complete setup without external explanation.
- Benchmark instructions are clear enough to perform.
- Retest data can be compared without manual cleanup.

## Phase 1: Tiny Alpha

Sample:

- 5-10 recreational adults.
- Apparently healthy.
- Interested in HYROX / Hybrid Race or general hybrid training.

Duration:

- 4 weeks.

Data to collect:

- Baseline profile.
- Safety Gate result.
- Benchmark completion status.
- Raw test results.
- RPE for each test.
- Starter Path availability.
- Weekly adherence.
- Retest results.
- User confusion points.
- Consent status/version, anonymous ID, retention review date and deletion
  request status before any real participant record is stored.
- Protocol context: test variant, route or machine, surface, incline, timing,
  warm-up, familiarization, order, equipment setting and deviations.

Do not collect:

- Medical diagnoses beyond safety-screen boundary.
- Wearable data.
- Payment data.
- GPS.
- Nutrition.
- Sleep.

Data-governance requirements are defined in `data_governance.md`. The
repository ships only header-only templates; it does not itself recruit or
collect participant data.

Success criteria:

- At least 70% can complete onboarding without help.
- At least 70% understand whether they need benchmark data first.
- At least 60% complete at least two measured performance dimensions.
- No user believes SportRx provided medical clearance.

## Phase 2: Pilot Dataset

Sample:

- 30-50 users.

Purpose:

- Estimate test completion rates.
- Estimate test-retest variability.
- Identify which tests are too hard, unclear, or equipment-dependent.
- Decide whether low-equipment path should be the default.

Minimum fields:

| Field | Why needed |
| --- | --- |
| User ID | Longitudinal linkage |
| Date | Baseline/retest tracking |
| Safety Gate status | Training handoff boundary |
| Equipment access | Standard vs low-equipment path |
| 1 km run or 6-min run/walk | Running/aerobic measurement |
| Station circuit result | Strength-endurance measurement |
| RowErg/SkiErg result when available | Station-specific measurement |
| Compromised-run or mixed-work result | Work-capacity measurement |
| Test RPE | Effort/context |
| Session adherence | Training feasibility |
| Retest result | Change over time |
| Notes | Protocol deviations and usability issues |

## Claims Allowed After Each Phase

| Phase | Allowed claim |
| --- | --- |
| Before self-use | "Prototype; not validated." |
| After self-use | "Used internally for product testing." |
| After tiny alpha | "Early usability-tested prototype." |
| After pilot dataset | "Pilot-tested benchmark workflow; not population-normed." |

## Public Beta Gate

Public Beta Readiness is not a validation phase. It is a release-control layer
that checks whether the prototype can be shown to outside reviewers without
overclaiming.

Before public-beta messaging, SportRx should have:

- passing local Runtime Doctor checks;
- passing Release QA and Launch Readiness checks;
- a clean public package with internal notes excluded;
- required evidence files present;
- an Alpha Dataset Template ready for anonymous participant, benchmark,
  weekly feedback, and pilot-review capture;
- a ready demo runbook;
- at least five local pilot-feedback entries; and
- no unresolved low-rating pilot-feedback flags.

If the release gates pass but pilot-feedback depth is below five entries, the
allowed status is limited reviewer use only, not public-beta candidacy.

## Claims Still Blocked

Even after Phase 2, block:

- finish-time prediction,
- completion probability,
- injury-risk percentage,
- population percentile,
- medical clearance,
- validated readiness score.

These require a much larger dataset and a formal validation design.
