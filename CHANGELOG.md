# Changelog

## 0.1.0 - Unreleased

- Initial SportRx Engine scaffold.
- Added rule-based safety, assessment, intensity, volume, prescription,
  progression, and explanation modules.
- Added examples, evidence notes, tests, and a Streamlit prototype.

## 2.0.0 - Unreleased

- Repositioned SportRx toward sport preparation and event testing.
- Added GREEN/YELLOW/RED safety gate.
- Added 60-second Quick Match.
- Added Hybrid Race Performance Lab.
- Added reusable race-check result object.
- Added Sport Match and Race Check share-card data objects.
- Added 4-week Starter Path based on the main gap.
- Updated Streamlit demo to Discover, Performance Lab, Race Check, Training, and
  Retest flow.

## 2.1.0 - Unreleased

- Reduced score-forward user experience.
- Preserved missing performance data as `Not tested` instead of midpoint scores.
- Split performance profile from training context.
- Renamed user-facing athlete type language to training profile.
- Added tie handling for balanced and tied-lowest performance dimensions.
- Removed age-alone YELLOW behavior from the 2.0 safety gate.
- Reworked Quick Match to show fit categories, reasons, and missing evidence.
- Reworked Hybrid Race result page around what is known, unknown, and useful next.
- Redesigned share cards with plainer sport language.
- Added SportRx Hybrid Benchmark v1 prototype specification.
- Expanded tests from 28 to 41.

## 2.2.0 - Unreleased

- Reworked Quick Match inputs from subjective background/adaptability sliders to concrete recent training behavior.
- Added a Quick Match Intake Contract console and Review Pack export so the
  first intake screen explains its direct numeric fields, excluded subjective
  ratings, and measured-test boundary before users interpret results.
- Added Benchmark Log engine for raw benchmark sessions, JSON export, CSV export, and retest summaries.
- Added a guided Benchmark Protocol layer for standard and low-equipment SportRx Hybrid Benchmark v1 testing.
- Added a `Benchmark Protocol` page to the Streamlit app with stop rules, component setup, recording principles, and markdown export.
- Upgraded Benchmark Protocol with a command console and component cards for
  test-day path, stop rules, worksheet readiness, brief readiness, and equipment
  state.
- Added a Test Session Operator engine, Benchmark Protocol tab, and Markdown
  export for step-by-step local benchmark execution without scoring.
- Added a `Workbench` home screen that summarizes the measurement pipeline, current boundary conditions, and next actions.
- Added a Demo Scenario Matrix console and export artifact to compare synthetic
  review states by measurement depth, retest readiness, Starter Path
  availability, and recommended pages.
- Added a Workbench Trial Mode Launcher for 3-minute full demo, 5-minute
  Quick Match self-intake, and 15-minute Benchmark-first trial paths.
- Added a Workbench Lab Workflow Board that separates intake contract,
  measurement layer, and training handoff in a lab-style first-screen view.
- Added a Page Health Matrix to the Workbench and Review Pack so each page has
  a visible responsibility, success signal, evidence source, and blocked claim.
- Added a Reviewer Session Plan console and export artifact with 3/8/12-minute
  review tracks, page sequences, artifacts, success criteria, and guardrails.
- Added an Open-Source Integration Console and export artifact showing which
  GitHub comparable-product patterns SportRx adopted, deferred, or explicitly
  rejected.
- Expanded the GitHub comparable-product scan into an Integration Map covering
  FitOntology-style decision traceability, benchmark log contracts, FITT-VP
  handoff boundaries, HYROX tooling later-scope, and platform integrations later.
- Refreshed the GitHub comparable-product scan with verified reference groups
  covering FitOntology, WODIS, Domestique, OpenAthlete, Fit Log Web App,
  Ballast, ShredTrack, Section 11, HYROX tooling, and data-format projects,
  while keeping AI coach, wearable readiness, race prediction, large exercise
  catalogs, and platform sync outside the current product scope.
- Added a Benchmark Log Entry Contract engine, UI panel, Review Pack export,
  and Release QA gate so each Benchmark component declares its raw-result
  fields, allowed units, companion context, HYROX import policy, and
  not-allowed inferences before users record data.
- Extended Benchmark Log component records with structured `result_fields`
  while preserving the existing raw `value`, `value_unit`, RPE, equipment,
  substitution, and notes export shape.
- Added a Terminology Guide engine, Workbench expander, Review Pack export, and
  Release QA checks so Chinese-first copy keeps HYROX/RPE/Benchmark terms stable
  while blocking readiness-score, medical-clearance, and fake-norm language.
- Added a Demo Experience Console with Workbench cards, guided first-five-minute
  review path, trust anchors, blocked impressions, Review Pack export, and
  Release QA checks.
- Reworked the Workbench Demo Scenario Library into polished scenario cards with
  current-scenario highlighting, measured-depth signals, Starter Path state,
  retest state, recommended pages, and one-click loading.
- Added a Guided Review Console with walkthrough progress, recommended
  scenario, next-page guidance, quick actions, Review Pack export, and Release
  QA checks.
- Promoted Guided Review quick actions into a visible Workbench Action Rail so
  reviewers can load the complete demo, start Benchmark, inspect Training
  Profile, export the Review Pack, or check Release QA from the first screen.
- Added a Measurement Schema Registry console and export artifact for local
  data objects, required fields, export coverage, and not-tested policies.
- Added an Evidence Library page and export artifact for browsing saved source
  IDs, evidence tiers, product use, limitations, and required local evidence
  files.
- Added a Validation Readiness Matrix to separate product readiness, self-use
  data collection, tiny alpha, pilot dataset, and blocked validation claims.
- Added a Phase 0 Self-Use Protocol pack for a four-week
  baseline-feedback-retest workflow while keeping validation claims blocked.
- Reworked HYROX Check measured-test inputs to select `Not tested` or
  `Measured` before value entry, reducing accidental default-value capture.
- Added a Measurement Intake Matrix on HYROX Check to show measured status,
  provenance, gap-comparison eligibility, next measurement actions, and a
  Review Pack Markdown/CSV export.
- Added an Intake Precision Audit to Quick Match and the Review Pack so direct
  numeric, measured, safety-only, context, legacy, and unsupported inputs stay
  visibly separated.
- Added an Alpha Dataset Template pack with a data dictionary and header-only
  CSV templates for participants, benchmark sessions, weekly feedback, and
  pilot review capture without fake norms or validation claims.
- Added an Evidence Coverage console and export artifact that parses the
  rule-evidence map and summarizes allowed, explain-only, and blocked claims.
- Added Review Pack Integrity checks with SHA-256 payload hashes, byte sizes,
  duplicate filename detection, internal/cache path leak checks, ZIP manifest
  coverage, Export Center display, and Release QA gating.
- Added a Release Candidate Summary artifact and Release QA download so runtime,
  release gates, package state, review pack, run commands, and blocked claims
  fit on one page.
- Added Benchmark Log session-quality review before saving raw measurement records.
- Added Benchmark Log import-compatibility review before saving, so HYROX Check
  handoff, missing modality details, and raw-only records are visible before a
  session is saved.
- Added Protocol Deviation Review for Benchmark Log sessions to keep
  substitutions, missing RPE/equipment context, and retest protocol changes
  visible before interpreting raw change.
- Added Retest Interpretation Guard to combine raw benchmark deltas with
  protocol-context comparability before showing retest interpretation.
- Reworked the `Benchmark Log` page into Session Setup, Component Results, and Review & Save sections.
- Added a Training Profile report object and Markdown export.
- Reworked the `Training Profile` page into Report Overview, Performance Matrix, Known / Unknown, and Handoff sections.
- Added a 4-week Training Block object and Markdown export.
- Reworked the `训练` page into Block Overview, Weekly Plan, Session Detail, and Progression / Export sections.
- Added a Training Handoff Console to show blocked/available state, measured
  gap basis, block length, session count, weekly volume range, Safety Gate, and
  feedback-loop requirement.
- Added a Feedback Loop dashboard object and Markdown export.
- Reworked the `复测` page into Weekly Feedback, Progression Decision, Benchmark Retest, and Export sections.
- Added an Adaptive Loop Console to show adherence, weeks recorded, completion,
  latest rule-coded progression decision, dose change, retest state, and next
  action.
- Added synthetic demo seed data for reviewing the complete SportRx loop.
- Added Workbench and sidebar controls to load the full demo or reset the prototype state.
- Added Demo Scenario Library with Measure First, Benchmark Underway, and
  Complete Loop synthetic review states.
- Added a Workbench product tour that marks page-by-page review status and routes users to the next useful page.
- Added a visual Measurement Loop Timeline to the Workbench and export bundle.
- Added an Export Bundle object for local review artifacts.
- Added an `Export Center` page for Protocol, Benchmark Log, Training Profile, Training Block, Feedback Dashboard, and manifest downloads.
- Added Artifact Catalog to explain which export files reviewers should open first.
- Added Reviewer Handoff Markdown for run commands, demo scenarios, priority
  artifacts, and claim guardrails.
- Added Input Ledger for field units, source types, output roles, Not tested
  states, legacy compatibility fields, and ignored unsupported inputs.
- Added Benchmark Worksheet Markdown for test-day setup, safety checks,
  component results, RPE, equipment notes, substitutions, and retest anchors.
- Added local launch and smoke-check scripts for direct release-candidate
  verification before opening the Streamlit app.
- Added one-click Review Pack ZIP export for all current Export Center artifacts.
- Upgraded Export Center into a handoff dashboard for Review Pack, Artifact
  Catalog, Reviewer Handoff, Session Snapshot, raw Benchmark data, and Pilot
  Feedback.
- Added Release QA coverage for Review Pack ZIP generation.
- Added a Release QA object and Markdown export for product-readiness checks.
- Added a `Release QA` page for demo loop, export, claim-boundary, safety-boundary, measurement-gate, and evidence-file checks.
- Added a Public Release Package manifest and zip helper that excludes internal
  review notes, generated caches, and historical review archives.
- Added Public Package checks and manifest download to the `Release QA` page.
- Added a Metric Source Register that labels visible outputs as measured,
  self-reported, estimated, not tested, safety-screened, or ignored.
- Added Metric Sources views to HYROX Check and Training Profile.
- Added Release QA coverage for metric source labels.
- Added Plan-Actual reason codes for weekly progression decisions.
- Added reason-code tables to Feedback Loop and Markdown export.
- Added Release QA coverage for plan-actual feedback reasons.
- Added an Output Prerequisite Register that explains whether user-facing
  outputs are active, blocked, provisional, or waiting for retest.
- Added Output Gates views to Workbench and Training Profile.
- Added Release QA coverage for output prerequisite gates.
- Added Launch Readiness report for public demo review.
- Added Launch Readiness Markdown to the Export Center bundle.
- Added Launch Readiness checks to the Release QA page.
- Added Runtime Doctor for local Python, Streamlit, required runtime files, and
  run-command checks.
- Added Runtime Doctor to Release QA and Export Center.
- Added First Run Guide cards to the Workbench first screen with demo, personal
  measurement, and reviewer/export paths.
- Added First Run Guide Markdown to the Export Center bundle and Release QA checks.
- Added Lab Readiness Console for safety gate, equipment path, measurement
  depth, Benchmark Log, and retest state.
- Added Lab Readiness Console to HYROX Check, Benchmark Protocol, Benchmark Log,
  Export Center, Release QA, and the public package checks.
- Added Session Quality Review to summarize whole-session safety, measurement
  depth, Benchmark Log, feedback, retest, evidence context, and output gates
  before product interpretation or reviewer handoff.
- Added HYROX Check Measurement Review to separate measured tests, Not tested
  fields, self-reported context, Safety Gate boundary, and strongest/gap
  comparison readiness.
- Added Test-Day Brief for pre-test checks, component order, stop rules,
  after-test recording, and local Markdown export.
- Added Test-Day Brief to Benchmark Protocol, Export Center, Release QA, and
  public package checks.
- Added Demo Runbook with reviewer path, must-show pages, and claim guardrails.
- Added Demo Runbook Markdown to the Export Center bundle and Release QA page.
- Added Launch Command Center cards to the Workbench first screen.
- Added consent-first Pilot Feedback capture with local JSON/Markdown export.
- Added `Pilot Feedback` page and Release QA coverage for the feedback prompt.
- Added a Pilot Review Console for local alpha feedback status, average ratings,
  lowest-rated field, review flags, qualitative comments, and contact-consent
  count.
- Added Public Beta Readiness as a release gate that distinguishes local demo
  readiness, limited reviewer sessions, pilot-feedback depth, and public-beta
  candidacy without making validation claims.
- Added local Session Snapshot JSON/Markdown export and restore for preserving a full prototype trial.
- Added Session Snapshot artifacts to the Export Center, Launch Readiness, Release QA, and public package checks.
- Added conservative Benchmark Log import into HYROX Check for unit-compatible measurements.
- Added raw retest comparison for repeated benchmark components.
- Added a `Benchmark Log` page to the Streamlit app.
- Upgraded Benchmark Log Review & Save with a session quality console, save
  gate, measured-area depth, interpretation readiness, issue/warning counts, and
  raw payload preview.
- Removed legacy subjective background / comfort rating fallback from Quick
  Match and HYROX Check context; current matching now uses direct recent
  behavior fields and session counts.
- Added Quick Match Intake Quality gate for Safety Gate state, behavior-field
  completeness, active signal count, time constraints, ignored legacy fields,
  and Benchmark-first routing.
- Added Lab Test Quality gate for raw timed fields, protocol-derived Station /
  Work capacity scores, protocol source completeness, and comparison readiness
  before those protocol scores can affect measured performance.
- Tightened protocol-derived Station / Work capacity scoring so values without
  a named protocol source are recorded as `measured_needs_protocol` and do not
  unlock measured-profile comparisons or Starter Path handoff.
- Replaced free-form HYROX Check protocol-source entry with conservative
  presets plus an optional documented-protocol note for clearer test provenance.
- Added an exportable Protocol Source Guide to HYROX Check, Review Pack,
  Artifact Catalog, and Release QA so protocol-score provenance presets are
  reviewable before testing.
- Extended Benchmark Log -> HYROX Check import so protocol-derived station
  scores carry Benchmark Log protocol provenance into `station_test_protocol`.
- Added protocol provenance fields to Input Ledger and Metric Sources so
  `station_test_protocol` and `work_capacity_test_protocol` have explicit
  output roles and claim boundaries.
- Upgraded the Streamlit app shell with a shared status strip and product-style page headers.
- Added GitHub open-source landscape scan, integration backlog, and positioning notes.
- Added a 2026 GitHub comparable-products scan covering assessment apps, adaptive
  planners, physiology labs, workout data standards, HYROX tools, and export
  patterns.
- Converted the scan into next-step integration decisions for metric source
  labels, plan-actual feedback reasons, and export-first architecture.
- Added a structured evidence knowledge base, literature matrix, and rule-to-evidence map.
- Added `evidence/library/` as a saved citation library for guidelines, safety screening, measurement/RPE, and HYROX/HIFT sources.
- Added evidence appraisal, open evidence questions, and a self-use/alpha/pilot validation plan.
- Added claim policy, controlled glossary, source-note templates, and topic-level evidence notes.
- Added an internal RAG decision note recommending a structured evidence base before retrieval.
- Removed measured run-test fields from Quick Match.
- Added a Quick Match input-review layer that explains which fields affect
  rough route matching, Safety Gate scope, or later prescription constraints.
- Added maximum session length to Quick Match because it affects downstream
  Training Block and prescription shape.
- Removed unused VO2max, HRmax, and resting-HR inputs from the Hybrid Race Check UI.
- Revised the Chinese demo copy to keep familiar sport terms such as HYROX, RPE,
  Benchmark, RowErg, and SkiErg in English.
- Added a Language Edition contract and Streamlit selector separating the
  Chinese user edition, English Lab Edition, and Internal Mixed Review surface
  so normal users do not see an undifferentiated mixed-language interface.
- Reworked the Streamlit shell toward a mobile-first prototype with a narrow
  app-style viewport, single-column cards, touch-sized buttons, and top quick
  navigation for phone-style trials.
- Split the Streamlit app into simplified public mobile pages and an
  internal-only mixed review surface so normal users no longer land in the
  Release QA / export / evidence dashboard.
- Required at least two measured performance dimensions before comparing strongest area and main gap.
- Blocked tailored Starter Path generation when measured data are insufficient.
- Routed insufficient-data users to SportRx Hybrid Benchmark v1.
- Hid the internal aggregate score from normal Streamlit screens.
- Kept Safety Gate separate from measured performance values.
- Moved internal audit, review, and strategy files into `docs/internal/`.
- Updated public sample output and validation notes.
