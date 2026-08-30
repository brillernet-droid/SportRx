# SportRX Phase 0 / Alpha Data Governance

## Current Scope

This repository does not recruit participants or collect real participant data.
The header-only Alpha Dataset Template is preparation for a future Phase 0 or
Alpha workflow. Any collection requires a separate approved consent and local
operating process first.

## Minimum Data Rules

- Assign an anonymous `participant_id`; do not place names, phone numbers or
  direct identifiers in the Benchmark export.
- Record explicit `consent_status` and `consent_version` before entering a real
  participant record.
- Capture only fields needed for protocol consistency, completion, RPE,
  retest-error and usability review.
- Keep Safety Gate status separate from performance measurements.
- Keep missing tests as `Not tested` with `not_tested_reason`; do not impute.
- Record a retention review date and a deletion request status. Define the
  local retention window and deletion contact before recruiting.

## Venue Entry Routing

- Venue Entry stores only age, consent, screening-provider ID/version,
  member-reported completion route, and whether a relevant change was reported
  since screening.
- Do not store screening answers, symptoms, diagnoses, names, phone numbers,
  contact information, or a copy of the external screening tool.
- A `screening_follow_up_needed` or `stop_automation` route is assessment-only:
  it cannot open Benchmark, Training Profile handoff, Starter Path, or automatic
  exercise advice.
- The default Chinese venue pathway is `research_required`. No real venue pilot
  may begin until a lawful local pathway, consent process, retention window,
  deletion route, and staff escalation process have been documented.

## De-identification And Export

- Keep any linking file between a person and `participant_id` outside this
  repository and outside public exports.
- Export only de-identified rows for internal analysis.
- Never commit real session logs, consent records, private PDFs or linking
  files to GitHub.
- Knowledge Lab sends only the research question and approved public card
  summaries to DeepSeek. Do not include a participant profile, health details,
  identifiers, Benchmark sessions, or private full-text PDFs in a query.

## Allowed Future Analysis

- onboarding and Benchmark completion;
- protocol consistency and documented deviations;
- test-retest raw error and feasibility; and
- usability, comprehension and adherence.

## Prohibited Claims

The data must not be used to generate medical clearance, injury-risk
percentages, race predictions, population norms, fake percentiles, or a
validated SportRX score. A small feasibility sample cannot establish those
claims.
