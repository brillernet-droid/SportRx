# Open Source Integration Backlog

This file converts the GitHub landscape scan into SportRx decisions.

## Adopted In Current Prototype

### OS-001: SportRx Benchmark Log Schema

- Inspiration: WODIS, local-first coach tools.
- Built: a small local JSON/CSV export path for benchmark sessions.
- Why: SportRx needs repeatable raw measurement records before any validation
  claim.
- Included:
  - benchmark date,
  - protocol version,
  - component results,
  - RPE,
  - equipment,
  - substitutions,
  - notes,
  - retest comparison.
- Still excluded:
  - full workout history,
  - wearable imports,
  - cloud sync.

### OS-002: Station Component Metadata

- Inspiration: ShredTrack station scaling detail, Free Exercise DB taxonomy.
- Built: a controlled station metadata and protocol layer for SportRx Hybrid Benchmark v1.
- Why: users must know exactly what version of a station test they completed.
- Included:
  - component ID,
  - display name,
  - standard equipment,
  - low-equipment alternative,
  - result fields,
  - safety stop notes,
  - setup and execution guidance,
  - retest notes,
  - markdown export.
- Still excluded:
  - 800-exercise database import,
  - exercise media library.

### OS-003: Export First

- Inspiration: WODIS, Claude Coach exports, data-portability projects.
- Built: local Markdown/JSON/CSV artifacts, one-click Review Pack ZIP, Artifact
  Catalog, Reviewer Handoff, and restorable Session Snapshot.
- Why: pilot data must be portable and inspectable before any external platform
  integration.
- Included:
  - one-user export,
  - full local session state,
  - restore from saved product-state JSON,
  - export-status dashboard in Export Center,
  - no account system,
  - no cloud storage.

### OS-004: Metric Source Labels

- Inspiration: physiology-lab style projects.
- Built: metadata labels that identify visible outputs as measured,
  self-reported, estimated, not tested, safety-screened, or ignored.
- Why: SportRx should feel like a testing product, not a questionnaire that
  guesses hidden scores.
- Included:
  - metric source,
  - output role,
  - whether the input affects an output,
  - Not tested preservation,
  - visible Input Ledger.
- Still excluded:
  - HRV,
  - wearable recovery scores,
  - opaque readiness scores.

### OS-005: Rule-Coded Plan-Actual Delta

- Inspiration: Domestique-style adaptive planning.
- Built: explicit reason codes for why a training block is held, progressed, or
  reduced after weekly feedback.
- Why: adaptation should be explainable before any LLM or friendly copy rewrites
  it.
- Included:
  - completion rate,
  - RPE pattern,
  - comparable retest result,
  - missed or non-comparable benchmark result,
  - safety-gate block.
- Still excluded:
  - acute/chronic workload ratios,
  - TSS,
  - cycling-specific load models,
  - injury-risk percentages.

### OS-006: Public Comparable-Product Page

- Inspiration: GitHub comparable-product scan.
- Built: an Open-Source Integration Console on the Workbench plus an exportable
  Markdown artifact.
- Why: GitHub visitors should understand why SportRx is a
  measurement-first prototype.
- Included:
  - positioning,
  - adopted patterns,
  - deferred integrations,
  - explicit rejection boundaries,
  - links to open-source inspiration.
- Still excluded:
  - marketing claims,
  - competitor teardown language.

### OS-007: Test Session Operator

- Inspiration: test-day worksheets, local-first coach tools, and structured
  workout operator views.
- Built: a Benchmark Protocol `Operator` tab plus exportable Markdown artifact.
- Why: SportRx should feel like a product that can run a real test day, not only
  describe one.
- Included:
  - safety preflight,
  - protocol lock,
  - warm-up step,
  - component order,
  - record-now fields,
  - stop rules,
  - Benchmark Log handoff,
  - retest anchor.
- Still excluded:
  - live timers,
  - automatic sensor capture,
  - scoring or validation.

### OS-008: Measurement Schema Registry

- Inspiration: WODIS/openweight-style explicit data contracts.
- Built: an Export Center schema registry console plus exportable Markdown
  artifact.
- Why: SportRx should make its local data objects reviewable before adding
  external integrations, cloud storage, or real pilot datasets.
- Included:
  - data object IDs,
  - owner modules,
  - required fields,
  - export artifact coverage,
  - not-tested policies,
  - claim boundaries.
- Still excluded:
  - formal interoperability certification,
  - cloud schemas,
  - validated norms or prediction labels.

### OS-009: Demo Scenario Matrix

- Inspiration: reviewer runbooks and mature demo-state libraries in local-first
  product prototypes.
- Built: a Workbench scenario matrix plus exportable Markdown artifact.
- Why: reviewers should understand what each synthetic state proves and does
  not prove before loading it.
- Included:
  - measurement depth,
  - benchmark session count,
  - feedback-week count,
  - Starter Path availability,
  - retest readiness,
  - recommended review pages,
  - claim boundary.
- Still excluded:
  - athlete norms,
  - validation labels,
  - fake benchmark percentiles.

### OS-010: Reviewer Session Plan

- Inspiration: release demo scripts, local-first review handoff flows, and
  productized reviewer tracks.
- Built: a Workbench reviewer session plan plus exportable Markdown artifact.
- Why: external reviewers should know whether they are doing a quick scan,
  guided measurement review, or full release review before judging SportRx.
- Included:
  - 3-minute quick scan,
  - 8-minute guided measurement review,
  - 12-minute full release review,
  - scenario IDs,
  - page sequences,
  - priority artifacts,
  - success criteria,
  - claim guardrails.
- Still excluded:
  - user accounts,
  - remote reviewer scheduling,
  - analytics tracking.

### OS-011: Evidence Library And Coverage Console

- Inspiration: claim-control dashboards in research-facing products and
  transparent evidence ledgers.
- Built: an Evidence Library page, Release QA evidence coverage console, and
  exportable Markdown artifacts.
- Why: reviewers should see which SportRx rules are allowed in the UI,
  explain-only, or blocked, and which saved sources support those boundaries,
  before trusting the prototype.
- Included:
  - source IDs,
  - evidence topics,
  - evidence tiers,
  - product use,
  - source limitations,
  - required evidence file coverage,
  - rule count,
  - evidence tier counts,
  - source ID count,
  - explain-only rules,
  - blocked rules,
  - forbidden claim policy.
- Still excluded:
  - formal validation,
  - automated literature grading,
  - RAG or LLM citation generation.

### OS-012: Review Pack Integrity Manifest

- Inspiration: local-first data-portability projects and release artifact
  manifests.
- Built: Review Pack checksum and leak checks plus a Markdown integrity report
  inside the downloadable ZIP.
- Why: reviewer handoff should be inspectable and reproducible before SportRx
  adds accounts, cloud sync, or pilot-data infrastructure.
- Included:
  - payload file count,
  - byte sizes,
  - SHA-256 hashes,
  - duplicate filename detection,
  - internal/cache path leak checks,
  - Release QA gate,
  - Export Center display.
- Still excluded:
  - signed releases,
  - remote provenance attestation,
  - cloud storage,
  - scientific validation claims.

### OS-013: Session Quality Review

- Inspiration: physiology-lab dashboards, local-first review handoff, and
  product-readiness gates.
- Built: a whole-session quality review on the Workbench plus exportable
  Markdown artifact and Release QA checks.
- Why: SportRx should tell reviewers when a session is interpretable, waiting
  for measurement, ready for training handoff, or ready for release review.
- Included:
  - Safety Gate state,
  - measured performance area count,
  - Benchmark Log count,
  - feedback-week count,
  - retest anchor state,
  - output-gate summary,
  - evidence source count,
  - next action.
- Still excluded:
  - data-confidence scores,
  - validated quality grading,
  - prediction,
  - medical clearance.

### OS-014: Protocol Deviation Review

- Inspiration: physiology-lab retest notes, local-first benchmark logs, and
  coach-facing test-day worksheets.
- Built: Benchmark Log protocol-deviation review plus exportable Markdown
  artifact and Release QA checks.
- Why: SportRx should keep substitutions, missing RPE/equipment context, and
  retest protocol changes visible before interpreting raw change.
- Included:
  - completed-component record review,
  - missing unit/RPE/equipment flags,
  - substitution context,
  - repeated-component protocol comparison,
  - equipment and substitution change detection,
  - claim boundary.
- Still excluded:
  - automatic validity scoring,
  - minimal detectable change,
  - group norms,
  - race prediction.

### OS-015: Retest Interpretation Guard

- Inspiration: lab retest reporting, context-aware training logs, and
  local-first benchmark review.
- Built: Feedback Loop retest guard plus exportable Markdown artifact and
  Release QA checks.
- Why: raw changes should be shown together with protocol-context comparability
  before a reviewer treats them as meaningful.
- Included:
  - raw pre/post benchmark deltas,
  - comparable-context count,
  - context-changed count,
  - protocol deviation status,
  - component-level interpretation status,
  - claim boundary.
- Still excluded:
  - training-effect claims,
  - validated minimal detectable change,
  - statistical inference,
  - prediction.

### OS-016: Validation Readiness Matrix

- Inspiration: staged research protocols, public-beta release gates, and
  claim-control dashboards.
- Built: Evidence Library / Release QA validation-readiness matrix plus
  exportable Markdown artifact.
- Why: SportRx should say when it is ready to collect self-use or alpha data
  without implying the product is already validated.
- Included:
  - Phase 0 self-use,
  - Phase 1 tiny alpha,
  - Phase 2 pilot dataset,
  - current allowed validation claim,
  - capture checks,
  - blocked claims,
  - required validation files.
- Still excluded:
  - formal validation status,
  - statistical inference,
  - athlete norms,
  - prediction claims.

### OS-017: Phase 0 Self-Use Protocol Pack

- Inspiration: staged self-experiment protocols, lab test-retest workflows, and
  local-first product review packs.
- Built: Evidence Library / Release QA self-use protocol console plus
  exportable Markdown artifact.
- Why: SportRx needs a concrete next action after validation-readiness review:
  one builder, four weeks, baseline, weekly feedback, Week 4 retest, and
  guarded interpretation.
- Included:
  - pre-start checks,
  - Week 0 baseline setup,
  - Weeks 1-3 weekly feedback and friction notes,
  - Week 4 retest and Review Pack export,
  - minimum data fields,
  - stop-or-review rules,
  - success criteria,
  - blocked claims.
- Still excluded:
  - validation completion,
  - athlete norms,
  - injury-risk estimates,
  - medical clearance,
  - prediction claims.

### OS-018: Alpha Dataset Template Pack

- Inspiration: lightweight cohort data dictionaries, test-day spreadsheets, and
  local-first alpha review workflows.
- Built: Alpha Dataset Template engine, data dictionary, four header-only CSV
  templates, Export Center downloads, Artifact Catalog entries, Launch
  Readiness entries, Release QA checks, and public package manifest coverage.
- Why: SportRx needs clean real-user data capture before it can make stronger
  claims. The next milestone is baseline, weekly feedback, and retest data from
  real alpha users, not more AI-generated interpretation.
- Included:
  - anonymous participant table,
  - raw benchmark-session table,
  - weekly feedback table,
  - pilot-review table,
  - not-tested reason field,
  - Safety Gate separation,
  - no-imputation and no-fake-norm rules.
- Still excluded:
  - population norms,
  - percentiles,
  - validation claims,
  - prediction claims,
  - injury-risk estimates,
  - medical clearance.

### OS-019: Intake Precision Audit

- Inspiration: data-provenance panels, clinical intake field dictionaries, and
  sport-lab test sheets that separate self-report, measured tests, safety
  screening, and unsupported fields.
- Built: Intake Precision Audit engine, Quick Match console, Markdown export,
  Artifact Catalog entry, Launch Readiness entry, Release QA checks, and public
  package manifest coverage.
- Why: early users found vague labels such as background or adaptability hard
  to trust. SportRx should show whether each input is a direct number, measured
  test, safety-only field, context selector, legacy ignored value, or unsupported
  value before it asks users to believe any output.
- Included:
  - direct numeric field count,
  - measured test count,
  - Not tested count,
  - safety-only boundary,
  - legacy and unsupported ignored-field boundary,
  - downloadable intake audit.
- Still excluded:
  - new scoring rules,
  - validation claims,
  - risk estimates,
  - medical clearance.

### OS-020: Comparable Product Integration Map

- Inspiration: FitOntology, WODIS, Domestique, ShredTrack, HYROX-Pace, Hybrid
  Training App, REGmon, AthleteLoadMonitor, Athlete Report Generator, and
  exercise-prescription-recommendation.
- Built: Open-Source Integration Console now groups reference projects into
  integration lanes instead of only listing examples.
- Why: SportRx should learn from adjacent GitHub products without drifting into
  AI coaching, wearable dashboards, generic ACSM/FITT-VP generators, or HYROX
  race prediction.
- Included:
  - decision-support traceability,
  - benchmark-log data contract,
  - FITT-VP as a training handoff layer,
  - event-specific tooling as later scope,
  - external platform integrations as later scope,
  - pilot-data capture as an architecture lane,
  - rejected boundary list for AI coach, wearable readiness, fake percentiles,
    and official event-readiness labels.
- Still excluded:
  - imported competitor code,
  - training-platform connectors,
  - race predictions,
  - wearable signals,
  - fake norms,
  - new sport packs.

### OS-021: Pilot Data Capture Lane

- Inspiration: REGmon, AthleteLoadMonitor, and Athlete Report Generator.
- Built: Open-Source Integration Console now includes pilot-data capture as a
  lane for turning SportRx forms, benchmark logs, RPE feedback, protocol
  deviations, and reports into future alpha-dataset objects.
- Why: SportRx should become more realistic by collecting cleaner practice data,
  not by adding more questionnaire labels or unsupported AI claims.
- Included:
  - Safety Gate remains separate from performance scoring,
  - Quick Match self-report remains separate from measured benchmark data,
  - weekly RPE feedback remains separate from sensor-derived or benchmark
    measurements,
  - protocol deviations stay visible before retest interpretation,
  - report/export handoff is treated as part of the data pipeline.
- Still excluded:
  - team accounts,
  - permission systems,
  - predictive risk models,
  - sensor imports,
  - youth-athlete profiling,
  - FMS/Y-balance scoring,
  - batch dashboards,
  - PDF automation.

## Later

### OS-022: WODIS Compatibility Review

- Decide whether SportRx benchmark logs should map to WODIS fields.
- Only after SportRx's own benchmark log stabilizes.

### OS-023: Exercise Taxonomy Mapping

- Review Free Exercise DB for station exercise names and equipment categories.
- Only after station metadata is stable.

### OS-024: External Calendar / Workout Export

- Review Claude Coach and TrainingPeaks-style structured workouts.
- Only after Starter Path becomes more structured.

## Explicitly Deferred

### OS-D01: Wearables

Do not add Garmin, Apple Watch, COROS, WHOOP, Strava, or TrainingPeaks in the
next milestone.

Reason:

- SportRx does not yet have a validated measurement layer.
- Wearables would move the product toward AI coach/readiness dashboards.

### OS-D02: AI Coach

Do not add chat coaching.

Reason:

- The market is crowded.
- SportRx's differentiation is rule-based, measured, and explainable.

### OS-D03: Medical / Health Risk Expansion

Do not add blood pressure, glucose, cholesterol, BMI risk scoring, VO2max
estimation, or medical-risk percentages.

Reason:

- FitLog-style broad assessment is useful but out of scope.
- SportRx should keep Safety Gate separate from performance scoring.

## Recommended Next Integration Milestone

The next open-source-inspired work package should be:

```text
SportRx 2.5 - Measurement Schema Hardening
```

The goal is not more assessment labels. The goal is to make the benchmark log,
input ledger, artifact catalog, and export bundle boringly stable enough that
real self-use and small-group pilot data can be collected without rewriting the
data model every week.
