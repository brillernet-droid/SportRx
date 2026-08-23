# SportRx

SportRx helps recreational athletes understand where they are, what they are
ready for, and what to train next.

The current demo is built around a measurement-first flow:

```text
Workbench -> Quick Match -> HYROX Check -> Benchmark Protocol -> Benchmark Log -> Training Profile -> Starter Path -> Retest -> Export Center -> Release QA
```

SportRx Labs currently supports:

- Product workbench for the current measurement loop
- Mobile-first Streamlit shell with a narrow app-style viewport and top quick
  navigation for first-time phone trials
- User-facing language editions now open into simplified mobile pages for Home,
  Quick Match, Benchmark testing, Training Profile, Training, and Retest, while
  internal QA/export/evidence consoles stay inside Internal Mixed Review
- Measurement Loop Timeline for visualizing the full demo path from Quick Match
  through export and Release QA
- Demo Scenario Library with Measure First, Benchmark Underway, and Complete
  Loop synthetic review states, including polished Workbench scenario cards for
  one-click trial switching
- Demo Scenario Matrix for comparing those synthetic states by measurement
  depth, retest readiness, Starter Path availability, and recommended pages
- Hybrid Race Check
- Quick Match for challenge fit, with an input-review panel that shows which
  fields affect route matching, safety boundaries, or later prescription
  constraints
- Quick Match Lab Intake Sheet that presents age, past-4-week behavior, and
  next-4-week constraints as a direct-number record before any route matching
  and is included in the Review Pack export
- Quick Match Intake Contract that explains why the entry screen asks direct
  numeric behavior fields and keeps subjective adaptability or measured tests
  out of Quick Match
- Quick Match now uses direct recent-behavior fields such as weekly minutes,
  run/walk minutes, longest continuous run/walk, strength days, and recent
  high-intensity / loaded-movement session counts. Legacy subjective
  background / comfort ratings are ignored by current matching rules.
- Quick Match Intake Quality gate that shows whether the self-reported record
  is usable for rough routing, blocked by Safety Gate, too sparse, or should be
  routed to SportRx Hybrid Benchmark v1 before interpretation
- Intake Precision Audit for separating direct numeric fields, measured tests,
  safety-only fields, context selections, and ignored legacy / unsupported
  values before users trust any output
- 4-week starter path
- Prototype Hybrid Benchmark v1
- Guided Benchmark Protocol for standard and low-equipment paths
- Benchmark Protocol command console and component cards for test-day setup,
  stop rules, worksheet readiness, and repeatable raw-data capture
- Test-Day Command Board for turning the protocol into a visible preflight,
  component-test, raw-recording, log-handoff, and retest-anchor workflow
- Test Session Operator for step-by-step benchmark execution during a local
  test day
- Test-Day Brief for pre-test checks, component order, stop rules, and after-test
  recording
- Language Edition selector that separates the Chinese user edition, English
  Lab Edition, and Internal Mixed Review surface before public testing
- Local Benchmark Log with JSON/CSV export
- Protocol Deviation Review for substitutions, missing RPE/equipment context,
  and retest protocol consistency
- Session quality console before benchmark logs are saved, including save gate,
  measured-area depth, interpretation readiness, issues, warnings, and raw
  payload preview
- HYROX import compatibility console before benchmark logs are saved, separating
  directly importable fields, missing modality details, and raw-only records
- Training Profile report with Markdown export
- 4-week Training Block view with Markdown export
- Training Handoff Console for showing whether the Starter Path is blocked or
  available, what measured gap it is based on, session count, weekly volume, and
  feedback-loop requirements
- Feedback Loop dashboard for weekly RPE feedback and raw benchmark retest comparison
- Retest Interpretation Guard for showing whether raw retest changes have
  comparable protocol context before interpretation
- Adaptive Loop Console for showing adherence, weeks recorded, completion rate,
  latest rule-coded progression decision, dose change, retest state, and next
  action
- Plan-Actual reason codes for explaining weekly progression decisions
- One-click synthetic demo seed for reviewing the full loop
- Workbench product tour that guides reviewers through the full loop
- Lab Workflow Board on the Workbench for showing intake contract, measurement
  layer, and training handoff as separate lab-style lanes
- Page Health Matrix for documenting each page's responsibility, success
  signal, primary evidence, and blocked claims
- Trial Mode Launcher on the Workbench for choosing a 3-minute full demo,
  5-minute self-reported Quick Match intake, or 15-minute measured Benchmark
  start without changing scoring rules
- Launch Command Center cards for first-screen demo readiness
- Demo Experience Console for making the first five minutes of Workbench review
  feel guided, credible, and measurement-first
- Guided Review Console for showing scenario choice, walkthrough progress, next
  page, quick actions, exports, and Release QA handoff in one place
- Guided Action Rail for visible one-click reviewer actions from the Workbench
  first screen
- Open-Source Integration Console for showing which GitHub comparable-product
  patterns were adopted, deferred, or explicitly rejected, now organized as an
  integration map across decision traceability, benchmark logs, FITT-VP handoff,
  protocol documents, pilot-data capture, event-specific tooling, and future
  platform connections
- Terminology Guide for keeping the Chinese-first UI consistent while preserving
  HYROX, RPE, Benchmark, Safety Gate, Training Profile, Starter Path, and other
  precise product terms in English
- First Run Guide cards for complete demo, personal measurement trial, and
  reviewer/export paths
- Lab Readiness Console for safety gate, equipment path, measurement depth,
  benchmark log, and retest state
- Session Quality Review for summarizing whether the current local trial has
  enough safety, measurement, benchmark, feedback, retest, and evidence context
  for product interpretation
- HYROX Check Measurement Review for separating measured tests, not-tested
  tests, self-reported context, safety boundaries, and comparison gates
- HYROX Check measured-test entry uses explicit `Not tested` versus `Measured`
  status before allowing a value, so default numbers do not imply hidden data
- HYROX Check protocol-derived scores use protocol-source presets plus an
  optional documented note, so Station / Work capacity values are not accepted
  as measured performance without provenance
- Protocol Source Guide on HYROX Check and in the Review Pack, documenting
  protocol-source presets and boundaries for protocol-derived scores, accepted
  provenance presets, when an `Other documented protocol` note is required,
  and what those sources still cannot claim
- Benchmark Log Entry Contract on the Benchmark Log page and in the Review
  Pack, documenting component-specific raw-result fields, allowed units,
  companion fields, HYROX import policy, and not-allowed inferences
- Measurement Intake Matrix for showing each HYROX Check component's measured
  status, value, provenance, gap-comparison eligibility, and next measurement
  action, with Markdown and CSV Review Pack exports
- Lab Test Quality console for checking raw timed fields, protocol-derived
  Station / Work capacity scores, protocol source completeness, and comparison
  readiness before protocol scores can affect measured performance
- Input Ledger and Metric Sources now track `station_test_protocol` and
  `work_capacity_test_protocol` as protocol provenance fields required before
  protocol-derived scores count as measured performance
- Input Ledger for showing each collected, missing, legacy, and ignored field,
  including its unit, source type, and output role
- Intake Precision Audit for showing whether each input is direct numeric,
  measured, safety-only, context, legacy, or unsupported, and what it can and
  cannot affect
- Measurement Schema Registry for documenting local data objects, required
  fields, export coverage, and not-tested policies
- Evidence Library page for browsing saved source IDs, evidence tiers, product
  use, limitations, and required local evidence files
- Validation Readiness Matrix for separating product-readiness, self-use data
  collection, tiny alpha, pilot dataset, and still-blocked validation claims
- Phase 0 Self-Use Protocol for turning the next step into a four-week
  baseline-feedback-retest workflow without claiming validation
- Printable Benchmark Worksheet for test-day setup, safety checks, component
  results, RPE, equipment notes, substitutions, and retest anchors
- Export Center dashboard for local Markdown/JSON/CSV review artifacts, Artifact
  Catalog, Reviewer Handoff, Session Snapshot, raw Benchmark data, Pilot
  Feedback, and one-click Review Pack ZIP download
- Release Candidate Summary for a one-page handoff of runtime, Release QA,
  launch, public package, review pack, run commands, and blocked claims
- Review Pack Integrity checks with SHA-256 file hashes, byte sizes, duplicate
  filename detection, and internal/cache path leak checks
- Reviewer Handoff one-pager for run commands, demo scenarios, priority
  artifacts, and claim guardrails
- Reviewer Session Plan for 3/8/12-minute review tracks with scenarios, page
  sequences, artifacts, and guardrails
- Release QA page for local demo-readiness checks
- Evidence Coverage console for rule-evidence status, allowed/explain-only/
  blocked rules, forbidden claims, and required evidence files
- Launch Readiness report for public demo review
- Public Beta Readiness gate that separates local demo readiness, limited
  reviewer sessions, pilot-feedback depth, and public-beta candidacy
- Runtime Doctor for local Python, Streamlit, runtime files, and run-command checks
- Demo Runbook for guiding first-time reviewers through the product loop
- Consent-first Pilot Feedback capture with local JSON/Markdown export
- Pilot Review Console for alpha feedback status, average ratings, lowest-rated
  field, review flags, comment count, and contact-consent count
- Alpha Dataset Template with a data dictionary and header-only CSV templates
  for participants, benchmark sessions, weekly feedback, and pilot review
  capture; it does not create norms, percentiles, validation claims, or
  predictions
- Local Session Snapshot export/restore for preserving a full prototype trial
- Public release package manifest that excludes internal notes, generated
  cache, and review archives
- Metric Source Register for showing whether each output is measured,
  self-reported, estimated, not tested, or ignored
- Output Prerequisite Register for showing which product outputs are active,
  blocked, provisional, or waiting for retest
- Preserved SportRx Core aerobic FITT-VP prescription engine

The web demo now separates language editions instead of exposing one mixed
interface:

- `中文版`: the primary early-testing edition. Normal controls, page titles, and
  explanations should be Chinese, while shared product terms such as SportRx,
  HYROX, RPE, Benchmark, Safety Gate, Training Profile, Starter Path, RowErg,
  and SkiErg can remain stable.
- `English Lab Edition`: the English user-facing edition. Normal controls,
  page titles, and explanations should be English.
- `Internal Mixed Review`: an internal-only review surface for development,
  QA, and reviewer handoff. It should not be treated as the normal user
  experience.

The product language is governed by the exportable Terminology Guide. Until
formal validation exists, SportRx prefers `current measured picture`, `training
profile`, `strongest area`, and `what needs work` over readiness-score language,
and blocks medical clearance, risk percentage, fake percentile, and official
event-readiness claims.

5K/10K Running exists only as a registry-ready card. It is not a full sport pack
yet.

## Product Principle

Measure what we know.
Show what we do not know.
Explain what matters.
Recommend the next useful action.

SportRx maintains a structured evidence base in `evidence/`. Product rules are
linked to source IDs and claim boundaries before they are promoted into the UI.

Open-source product research is tracked in `docs/research/`. SportRx uses those
projects for positioning and architecture lessons, not as code to copy.
The current comparable-product scan is saved at
`docs/research/github_comparable_products_2026.md`.

## What Users See

Instead of leading with a prototype score, the demo shows:

- Where you are now
- What looks good
- What needs work
- Your training context
- What we know
- What we do not know
- What to measure next
- Raw benchmark logs that can be exported and retested
- Unit-compatible benchmark results that can update HYROX Check without re-entry
- Metric source and prerequisite labels as the product matures

Numeric prototype scores may still exist internally for ranking or tests. They
are not presented as validated probabilities, clinical measurements, race
predictions, or injury-risk estimates.

## Safety Boundary

SportRx is a prototype. It does not diagnose disease, replace medical care, give
medical clearance, or handle emergencies.

The safety gate outputs only:

- `GREEN`: no major automated stop flag identified
- `YELLOW`: professional assessment or clarification is recommended before
  high-intensity participation
- `RED`: stop automated training handoff and recommend appropriate professional
  assessment

Performance cannot override safety. A RED safety gate blocks automated training.

## Project Structure

```text
SportRx/
├── app/
│   └── streamlit_app.py
├── scripts/
│   ├── run_local.sh
│   └── smoke_check.py
├── sportrx/
│   ├── artifact_catalog.py
│   ├── benchmark_worksheet.py
│   ├── safety_gate.py
│   ├── quick_match.py
│   ├── performance_lab.py
│   ├── benchmark.py
│   ├── benchmark_protocol.py
│   ├── benchmark_log.py
│   ├── demo_runbook.py
│   ├── demo_scenarios.py
│   ├── demo_seed.py
│   ├── export_archive.py
│   ├── export_bundle.py
│   ├── evidence_library.py
│   ├── feedback_loop.py
│   ├── first_run_guide.py
│   ├── input_ledger.py
│   ├── lab_readiness.py
│   ├── launch_command_center.py
│   ├── launch_readiness.py
│   ├── measurement_timeline.py
│   ├── metric_sources.py
│   ├── output_prerequisites.py
│   ├── plan_actual.py
│   ├── protocol_deviation.py
│   ├── release_package.py
│   ├── release_qa.py
│   ├── reviewer_handoff.py
│   ├── retest_interpretation.py
│   ├── review_pack_integrity.py
│   ├── report.py
│   ├── runtime_doctor.py
│   ├── self_use_protocol.py
│   ├── session_snapshot.py
│   ├── session_quality_review.py
│   ├── test_day_brief.py
│   ├── validation_readiness.py
│   ├── training_block.py
│   ├── walkthrough.py
│   ├── passport.py
│   ├── pilot_feedback.py
│   ├── share_card.py
│   ├── starter_path.py
│   ├── screening.py
│   ├── assessment.py
│   ├── readiness.py
│   ├── intensity.py
│   ├── volume.py
│   ├── prescription.py
│   ├── progression.py
│   ├── events.py
│   └── explanation.py
├── evidence/
├── examples/
└── tests/
```

## Quick Start

```bash
python3 -m pip install -e ".[dev,app]"
python3 scripts/smoke_check.py
bash scripts/run_local.sh
```

Optional full test suite:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider
```

Run a Hybrid Race Check from Python:

```python
from sportrx.performance_lab import assess_hybrid_performance

profile = {
    "age": 35,
    "training_days": 3,
    "weekly_training_minutes": 120,
    "running_minutes_per_week": 60,
    "available_days_per_week": 3,
    "max_minutes_per_session": 45,
    "symptoms": [],
    "known_conditions": [],
}

check = assess_hybrid_performance(profile)
```

Create a raw Benchmark Log record and derive a HYROX Check patch:

```python
from sportrx.benchmark_log import (
    benchmark_profile_patch,
    build_benchmark_import_compatibility,
    build_component_result,
    create_benchmark_session,
    evaluate_benchmark_session_quality,
)

components = [
    build_component_result("run_1km", value=360, value_unit="seconds", rpe_0_10=7),
    build_component_result("station_circuit", value=72, value_unit="score", rpe_0_10=7),
]

quality = evaluate_benchmark_session_quality(components)
compatibility = build_benchmark_import_compatibility(components)

session = create_benchmark_session(
    profile,
    components,
)

patch = benchmark_profile_patch([session])
```

When a protocol-derived station score is imported, the patch also carries
`station_test_protocol` so HYROX Check can show the Benchmark Log provenance.
Rounds, distances, or mixed raw fields that do not match an existing HYROX
Check field stay in the raw Benchmark Log.

`build_benchmark_import_compatibility()` is shown before saving a Benchmark Log.
It is a data-handoff check only: it can flag direct imports, missing RowErg /
SkiErg modality details, or raw-only components, but it does not normalize raw
results into scores.

Build an exportable Training Profile report:

```python
from sportrx.passport import build_readiness_passport
from sportrx.report import build_training_profile_report, report_markdown

passport = build_readiness_passport(profile)
report = build_training_profile_report(passport)
markdown = report_markdown(report)
```

Inspect metric source labels:

```python
from sportrx.metric_sources import build_metric_source_register

register = report["metric_sources"]
```

Metric source labels document provenance only. They do not validate SportRx,
create athlete norms, or turn self-reported training context into measured
performance.

Inspect output prerequisite gates:

```python
from sportrx.output_prerequisites import build_output_prerequisites

gates = build_output_prerequisites(passport)
```

Output prerequisite gates explain why a SportRx output is available, blocked,
provisional, or waiting for retest. They do not add new scoring.

Build an exportable 4-week Training Block:

```python
from sportrx.prescription import generate_prescription
from sportrx.training_block import build_training_block, training_block_markdown

passport = build_readiness_passport(profile)
core_plan = generate_prescription(profile)
block = build_training_block(passport, core_plan)
markdown = training_block_markdown(block)
```

Build an exportable Feedback Loop dashboard:

```python
from sportrx.feedback_loop import build_feedback_dashboard, feedback_dashboard_markdown

dashboard = build_feedback_dashboard(core_plan, feedback_by_week={}, benchmark_sessions=[])
markdown = feedback_dashboard_markdown(dashboard)
```

Inspect plan-actual reason codes:

```python
from sportrx.plan_actual import classify_plan_actual

reason = classify_plan_actual(
    planned_sessions=3,
    completed_sessions=3,
    average_rpe=5,
)
```

Plan-actual reason codes explain rule-based weekly adjustment only. They are
not recovery scores, risk predictions, or medical advice.

Build a launch readiness report:

```python
from sportrx.launch_readiness import build_launch_readiness

launch = build_launch_readiness(
    profile,
    passport,
    core_plan,
    benchmark_sessions=[],
    feedback_by_week={},
    evidence_files_present={},
)
```

Launch readiness checks whether the local prototype is ready for demo review.
It is not scientific validation.

Build a demo runbook:

```python
from sportrx.demo_runbook import build_demo_runbook

runbook = build_demo_runbook(launch)
```

Capture local pilot feedback:

```python
from sportrx.pilot_feedback import create_pilot_feedback_entry, export_pilot_feedback_json

entry = create_pilot_feedback_entry(
    reviewer_role="coach",
    ratings={"setup_clarity": 4, "measurement_realism": 4, "trust": 4, "actionability": 4, "visual_polish": 4},
    comments={"first_impression": "Feels measurement-first."},
)
payload = export_pilot_feedback_json([entry])
```

Save and restore a local prototype session:

```python
from sportrx.session_snapshot import (
    build_session_snapshot,
    restore_session_snapshot,
    session_snapshot_json,
)

snapshot = build_session_snapshot(profile, benchmark_sessions=[], feedback_by_week={})
payload = session_snapshot_json(snapshot)
restored_state = restore_session_snapshot(snapshot)
```

Session snapshots preserve user-owned local product state. Restoring a snapshot
recalculates SportRx outputs from saved inputs; it does not create validation
data, athlete norms, or outcome evidence.

Inspect Review Pack integrity before handoff:

```python
from sportrx.export_bundle import build_export_bundle
from sportrx.review_pack_integrity import build_review_pack_integrity

bundle = build_export_bundle(profile, passport, core_plan, benchmark_sessions=[], feedback_by_week={})
integrity = build_review_pack_integrity(bundle["files"])
```

Review Pack integrity checks packaging only: file hashes, byte sizes, duplicate
filenames, and internal/cache path leaks. It does not validate SportRx rules or
prove outcomes.

Load synthetic demo state:

```python
from sportrx.demo_seed import build_demo_state

demo = build_demo_state()
```

Demo seed data is for product review only. It is not validation data, athlete
norms, or benchmark percentiles.

Load a named demo scenario:

```python
from sportrx.demo_scenarios import build_demo_scenario_state, build_demo_scenarios

scenarios = build_demo_scenarios()
state = build_demo_scenario_state("benchmark_underway")
```

Demo scenarios are synthetic product-review states. They are useful for testing
workflow gates, but they are not evidence, norms, or validation data.

Build a public release package manifest or zip:

```python
from pathlib import Path

from sportrx.release_package import build_release_package_manifest, write_release_package

manifest = build_release_package_manifest(Path("."))
write_release_package(Path("."), Path("dist/SportRx_public.zip"))
```

The public release package intentionally excludes `docs/internal/`, Python
bytecode caches, local hidden tooling folders, and historical review archives.

Build a local export bundle:

```python
from sportrx.export_bundle import build_export_bundle

bundle = build_export_bundle(profile, passport, core_plan, benchmark_sessions=[], feedback_by_week={})
```

Build an artifact catalog for reviewer handoff:

```python
from sportrx.artifact_catalog import build_artifact_catalog

catalog = build_artifact_catalog(bundle["files"])
```

The Artifact Catalog explains what each local export file is for. It does not
add validation or scoring.

Build an input ledger:

```python
from sportrx.input_ledger import build_input_ledger, input_ledger_markdown

ledger = build_input_ledger(profile)
markdown = input_ledger_markdown(ledger)
```

The Input Ledger explains why each field is collected, missing, retained for
legacy compatibility, or ignored. It does not add scoring or validation.

Build a benchmark worksheet:

```python
from sportrx.benchmark_worksheet import build_benchmark_worksheet, benchmark_worksheet_markdown

worksheet = build_benchmark_worksheet(equipment_access=["row", "kettlebell"])
markdown = benchmark_worksheet_markdown(worksheet)
```

The Benchmark Worksheet is a test-day data-capture aid. It does not score
performance or replace the Benchmark Log.

Build a one-page reviewer handoff:

```python
from sportrx.artifact_catalog import build_artifact_catalog
from sportrx.demo_scenarios import build_demo_scenarios
from sportrx.reviewer_handoff import build_reviewer_handoff
from sportrx.runtime_doctor import build_runtime_doctor

catalog = build_artifact_catalog(bundle["files"])
runtime = build_runtime_doctor(".")
handoff = build_reviewer_handoff(runtime, build_demo_scenarios(), catalog, launch)
```

The Reviewer Handoff explains how to inspect a local SportRx build. It does not
create validation data, athlete norms, predictions, or medical clearance.

Build a review-pack ZIP from export artifacts:

```python
from sportrx.export_archive import build_review_pack_zip

payload = build_review_pack_zip(bundle)
```

The Review Pack ZIP contains only local Export Center artifacts. It does not
include internal review notes, generated caches, or scientific validation data.

Run a local runtime readiness check:

```python
from sportrx.runtime_doctor import build_runtime_doctor

runtime = build_runtime_doctor(".")
```

Runtime Doctor checks local app launch readiness only. It does not validate
SportRx rules or scientific claims.

Build a measurement-loop timeline:

```python
from sportrx.measurement_timeline import build_measurement_timeline
from sportrx.walkthrough import build_walkthrough

walkthrough = build_walkthrough(passport, benchmark_summary, dashboard)
timeline = build_measurement_timeline(walkthrough)
```

The timeline is a product navigation view. It does not add scoring or validation.

Build a measurement schema registry:

```python
from sportrx.schema_registry import build_measurement_schema_registry, measurement_schema_registry_markdown

registry = build_measurement_schema_registry()
markdown = measurement_schema_registry_markdown(registry)
```

The registry documents local SportRx data objects and export coverage. It is a
data-contract review artifact, not scientific validation.

Build a demo scenario matrix:

```python
from sportrx.demo_scenario_matrix import build_demo_scenario_matrix, demo_scenario_matrix_markdown

matrix = build_demo_scenario_matrix()
markdown = demo_scenario_matrix_markdown(matrix)
```

The matrix helps reviewers choose between Measure First, Benchmark Underway,
and Complete Loop without treating synthetic demo states as validation data.

Build a reviewer session plan:

```python
from sportrx.reviewer_session_plan import build_reviewer_session_plan, reviewer_session_plan_markdown

session_plan = build_reviewer_session_plan(first_run_guide, scenario_matrix, runbook)
markdown = reviewer_session_plan_markdown(session_plan)
```

The session plan gives external reviewers 3-minute, 8-minute, and 12-minute
review tracks. It is product-review guidance, not evidence that SportRx works.

Build evidence coverage:

```python
from sportrx.evidence_coverage import build_evidence_coverage, evidence_coverage_markdown

coverage = build_evidence_coverage(".")
markdown = evidence_coverage_markdown(coverage)
```

Evidence Coverage summarizes local rule-evidence mapping and claim boundaries.
It does not validate SportRx or prove outcomes.

Build open-source integration notes:

```python
from sportrx.open_source_integration import (
    build_open_source_integration_console,
    open_source_integration_markdown,
)

console = build_open_source_integration_console()
markdown = open_source_integration_markdown(console)
```

Open-source integration notes are product-positioning artifacts. They explain
what SportRx borrowed from adjacent GitHub projects, what it deferred, and what
it refuses to claim. They now separate measurement/logging lessons from AI
coach, wearable, race-prediction, and platform-sync ideas, and they treat clean
pilot-data capture as the next realistic bridge to practice evidence. They do
not create scientific evidence.

Build a first-run guide for reviewers:

```python
from sportrx.first_run_guide import build_first_run_guide, first_run_guide_markdown

guide = build_first_run_guide(passport, benchmark_sessions=[], feedback_by_week={})
markdown = first_run_guide_markdown(guide)
```

The first-run guide is navigation only. It does not score users or change
prescription logic.

Build a lab readiness console:

```python
from sportrx.benchmark_log import summarize_benchmark_sessions
from sportrx.lab_readiness import build_lab_readiness_console, lab_readiness_markdown

console = build_lab_readiness_console(profile, passport, summarize_benchmark_sessions([]))
markdown = lab_readiness_markdown(console)
```

The Lab Readiness Console summarizes measurement workflow state only. It does
not create a performance score, risk estimate, or medical clearance.

Build a test-session operator:

```python
from sportrx.test_session_operator import (
    build_test_day_command_board,
    build_test_session_operator,
    test_day_command_board_markdown,
    test_session_operator_markdown,
)

operator = build_test_session_operator(
    equipment_access=["row", "kettlebell", "track"],
    safety_gate_status="GREEN",
)
board = build_test_day_command_board(operator)
markdown = test_session_operator_markdown(operator)
board_markdown = test_day_command_board_markdown(board)
```

The Test Session Operator is for running a repeatable local benchmark session.
It shows safety preflight, protocol lock, warm-up, component order, record-now
fields, stop rules, and Benchmark Log handoff. It does not score performance.
The Test-Day Command Board is the first-screen operator summary for reviewers
and local test sessions.

Build a test-day brief:

```python
from sportrx.test_day_brief import build_test_day_brief, test_day_brief_markdown

brief = build_test_day_brief(equipment_access=["row", "kettlebell", "track"])
markdown = test_day_brief_markdown(brief)
```

The Test-Day Brief is an operational checklist for running a repeatable local
benchmark session. It does not interpret performance.

Run local release QA checks:

```python
from sportrx.release_qa import build_release_qa

qa = build_release_qa(profile, passport, core_plan, benchmark_sessions=[], feedback_by_week={})
```

Release QA checks product completeness and claim boundaries. It is not
scientific validation.

Inspect Quick Match intake quality:

```python
from sportrx.quick_match import build_quick_match_intake_quality, build_quick_match_lab_intake_sheet

quality = build_quick_match_intake_quality(profile)
sheet = build_quick_match_lab_intake_sheet(profile)
```

The intake gate checks whether self-reported recent-behavior data are usable for
rough routing. It does not create a measured performance profile.
The Lab Intake Sheet is the user-facing record: it separates direct-number
self-report from measured performance and keeps missing tests as `Not tested`.
It is also exported as `sportrx_quick_match_lab_intake_sheet.md` for reviewer
handoff.

Build a public-beta gate from existing release and pilot-review checks:

```python
from sportrx.public_beta_readiness import build_public_beta_readiness

readiness = build_public_beta_readiness(
    qa,
    launch,
    runtime,
    package_manifest,
    runbook,
    evidence_files_present,
    pilot_review,
)
```

Public Beta Readiness is a product-release gate. It does not validate SportRx,
create athlete norms, provide medical clearance, or prove training outcomes.

## Out Of Scope

- Native mobile app
- Social feed
- Payment or subscriptions
- Wearable integrations
- Nutrition
- Disease-specific prescriptions
- Machine learning
- Injury prediction
- Medical risk prediction
- Fake benchmark data, percentiles, or validation claims
