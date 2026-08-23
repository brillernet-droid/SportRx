# Open Source Landscape Scan

Date: 2026-08-22

Purpose: identify GitHub projects adjacent to SportRx and extract product,
architecture, and evidence-boundary lessons without turning SportRx into a
generic AI fitness coach.

For the detailed comparable-product table, see
`docs/research/github_comparable_products_2026.md`.

## Summary

The open-source landscape is crowded around:

- AI fitness coaches,
- workout trackers,
- wearable connectors,
- HYROX/CrossFit training apps,
- exercise databases,
- self-hosted endurance dashboards,
- and data-format projects.

SportRx should not compete head-on with those categories. Its clearer position
is:

> Measurement-first exercise assessment and prescription intelligence.

The most useful open-source lessons are data portability, structured logs,
station-specific result capture, plan-versus-actual adjustment, metric source
labels, protocol documents, and clear user-owned records.

## Differentiation

Most projects start from:

```text
user goal -> training plan -> tracking
```

SportRx should start from:

```text
user situation -> safety boundary -> measured benchmark -> training profile -> conservative starter path -> retest
```

That difference should stay visible in the product.

## Reference Groups

### Decision Support

FitOntology is the strongest current reference for a decision-support product
that is not trying to be a black-box AI coach. The useful pattern is that a
reviewer can inspect the rows, thresholds, rules, and overrides behind a
recommendation.

SportRx action:

- show whether an output came from measured data, self-report, safety screening,
  or a missing prerequisite,
- expose the gate that allowed or blocked a Starter Path,
- preserve enough raw benchmark context to challenge the output later.

### Measurement And Logs

WODIS, Ballast, ShredTrack, and Openweight reinforce the same product lesson:
portable, local, unit-preserving records matter. SportRx should create a
smaller benchmark-specific record before considering broader workout schemas.

SportRx action:

- `benchmark_session`,
- `test_component`,
- `raw_result`,
- `unit`,
- `rpe`,
- `equipment`,
- `substitution`,
- `protocol_version`,
- `conditions`,
- `notes`.

### Athlete Monitoring And Pilot Data

REGmon and AthleteLoadMonitor are closer to the "sport-science product" feeling
than most AI fitness repositories. They treat forms, dashboards, templates,
RPE, questionnaires, sensor context, and research/practice data capture as
operational workflow pieces.

SportRx action:

- keep Quick Match, Safety Gate, Benchmark Log, weekly RPE, protocol deviation,
  and retest comparison as separate records,
- design exports as future alpha-dataset tables,
- preserve the boundary between safety screening, self-report context, measured
  performance, and feedback,
- avoid predictive risk labels until real data and validation exist.

Athlete Report Generator adds one useful future pattern: strict column
requirements and report handoffs are easier to review than vague coach notes.
SportRx should keep this as a future alpha-review idea, not a current batch
dashboard.

### Adaptive Planning

Domestique shows that adaptive training feels credible when every change is
tied to a visible plan-versus-actual signal.

SportRx action:

- keep feedback decisions rule-coded,
- show why a plan is held, progressed, or reduced,
- keep safety blocks separate from performance scoring.

### Protocol Documents

Section 11 is useful as a protocol-product reference, not as a model for
turning SportRx into an AI coach. It shows that explicit protocols, dossier
templates, checks, and bad-response examples can make an AI-adjacent tool less
vague.

SportRx action:

- keep benchmark protocol, operator checklist, evidence map, and Review Pack
  artifacts first-class,
- keep the LLM in explanation only,
- block language that implies validation, medical clearance, or official race
  readiness.

### Event-Specific Tools

HYROX-Pace and hyrox-race-insights show that HYROX structure is easy for users
to understand when station-level data is concrete. They also show the boundary:
race prediction and pacing require assumptions and real event data.

SportRx action:

- use HYROX vocabulary when it clarifies the benchmark,
- log station-level details,
- defer finish-time prediction, race pacing, and event-readiness claims.

### Platform And Wearable Tools

OpenAthlete, Claude Coach, Coach Paddy, and URUJ Labs show demand for
self-hosting, exports, wearable context, and daily coaching. Those are tempting
but off-scope for SportRx 2.2.

SportRx action:

- keep local files and exports,
- defer cloud accounts, Garmin/Apple/Strava connectors, sleep/HRV recovery, and
  daily AI coaching.

## Ideas To Reject For Now

- Native mobile app.
- Garmin / Apple Watch / Strava / TrainingPeaks integration.
- AI chat coach.
- Social feed or leaderboard.
- Nutrition.
- Sleep/recovery dashboard.
- Medical risk percentage.
- Race completion prediction.
- Full exercise database import.
- Resistance engine.

These are either crowded, off-scope, or require validation/data that SportRx
does not yet have.

## Sources

- FitOntology: https://github.com/Conalh/fit-ontology
- exercise-prescription-recommendation: https://github.com/keanu77/exercise-prescription-recommendation
- WODIS: https://github.com/aassoiants/workout-open-data-spec
- Domestique: https://github.com/platypus45/domestique
- OpenAthlete: https://github.com/openathleteorg/openathlete
- Fit Log Web App: https://github.com/souzamonteiro/fitlogwebapp
- REGmon: https://github.com/REGmon-project/regmon
- AthleteLoadMonitor: https://github.com/SaxionAMI/AthleteLoadMonitor
- Athlete Report Generator: https://github.com/BartWil/athlete_report_generator
- Ballast: https://github.com/N-O-P-E/Ballast
- ShredTrack: https://github.com/shredstack/shred-track
- Section 11: https://github.com/CrankAddict/section-11
- Free Exercise DB: https://github.com/yuhonas/free-exercise-db
- Claude Coach: https://github.com/felixrieseberg/claude-coach
- Coach Paddy: https://github.com/BorisBW/claude-fitness-cn
- URUJ Labs: https://github.com/gazzycodes/uruj-labs
- HYROX-Pace: https://github.com/willckim/HYROX-Pace
- hyrox-race-insights: https://github.com/JamesIves/hyrox-race-insights
- Openweight: https://github.com/radupana/openweight
