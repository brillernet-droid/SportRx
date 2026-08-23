# GitHub Comparable Products Scan

Date: 2026-08-22

Purpose: identify open-source projects near SportRx and decide what to absorb
into the product architecture without turning SportRx into a generic AI coach,
wearable dashboard, or workout tracker.

This is product research, not scientific evidence. Scientific claims still need
to flow through `evidence/`.

## Short Answer

There are many adjacent projects, but few are doing exactly what SportRx is
trying to do.

Most projects start from:

```text
goal -> plan -> workout log -> progress chart
```

SportRx should keep starting from:

```text
safety boundary -> measured benchmark -> training profile -> starter path -> retest
```

The useful integration direction is not more AI. It is:

1. better measurement records,
2. clearer metric source labels,
3. stronger export formats,
4. plan-versus-actual feedback,
5. protocol documents and review checks,
6. explicit claim boundaries.

## Compared Projects

| Project | What it is | Useful lesson for SportRx | Boundary |
| --- | --- | --- | --- |
| FitOntology | Local-first decision workspace for personal trainers | Recommendation traceability is a product feature: source rows, thresholds, override history, and decision boundaries should be inspectable | Do not add wearables, coach accounts, AI assistant workflows, or recovery scoring now |
| exercise-prescription-recommendation | ACSM/FITT-VP exercise-prescription generator | Generic FITT-VP generation is already an obvious baseline; SportRx must differentiate through measured benchmark gates before FITT-VP handoff | Do not become a broad AI exercise-prescription generator |
| WODIS | JSON workout data specification | Portable records and unit-preserving exports can become a trust layer | Do not overbuild a full workout interchange standard before benchmark logs stabilize |
| Domestique | Adaptive cycling planner with structured workouts and post-ride adjustment | Dashboard signals feel real when they can change future prescription through explicit guardrails | Do not import cycling-specific load models, huge workout libraries, or opaque performance claims |
| OpenAthlete | Self-hosted endurance platform | Transparent algorithms, full export, and user-owned data are positioning features | Do not add Strava, Garmin, mobile apps, cloud accounts, or endurance-platform scope now |
| Fit Log Web App | Broad health and fitness assessment web app | Users understand assessment dashboards, progress history, and prescription summaries | Do not expand into blood metrics, clinical risk, VO2max estimates, or all-in-one health assessment |
| REGmon | Athlete monitoring and research data-management platform | Configurable forms, dashboards, analysis templates, and research workflows make sport-science products feel operational rather than decorative | Do not add team accounts, permission systems, GDPR workflows, or a full athlete-monitoring platform now |
| AthleteLoadMonitor | Team-sport load monitoring tool | RPE, questionnaire context, and sensor-derived data should stay visibly separated before training decisions use them | Do not add predictive risk models, team-sport sensors, ACWR dashboards, or injury-risk labels |
| Athlete Report Generator | Field-assessment report generator | Strict required columns and profile/report outputs are useful for future alpha review packs | Do not add youth-athlete profiling, FMS/Y-balance scoring, batch dashboards, or PDF automation now |
| Ballast | Privacy-first local fitness tracker PWA | Low-friction local tracking and data ownership increase trust | Do not add PWA/mobile packaging until measurement is stable |
| ShredTrack | HYROX/CrossFit tracker | HYROX users need station-level logging, scaling, and equipment detail | Do not add social features, community competition, or a training marketplace |
| Section 11 | Protocol-driven AI endurance guidance | Protocol files, dossier templates, and bad-response checks make AI-adjacent workflows less vague | Do not give an LLM exercise-dose authority or add an AI chat coach |
| Free Exercise DB | Public JSON exercise database | A controlled exercise/station taxonomy may help later | Do not import a large exercise catalog into the current prototype |
| Claude Coach | Local AI endurance plan generator | Editable exports and local files make generated plans tangible | Do not reposition SportRx as an endurance AI coach |
| Coach Paddy | Wearable-driven AI fitness coach | Plain-text local files and bilingual UX are useful ideas | Do not add Garmin, HRV, sleep, body battery, readiness, or daily AI coaching |
| URUJ Labs | Personal physiology lab and cycling-training brain | Source labels, methodology versions, and raw data ownership create trust | Do not add HRV, recovery scoring, live cycling HUDs, or wearable readiness claims |
| HYROX-Pace | HYROX race execution and pacing app | Race-specific tools make event structure concrete | Do not add finish-time prediction, live pacing, or fake event-readiness labels |
| hyrox-race-insights | HYROX race analytics tool | Real race splits may later calibrate benchmark relevance | Do not create fake race predictions or fake percentile benchmarks |
| Openweight | Strength-training data format | Vendor-neutral schemas can become valuable when real user data accumulates | Resistance training remains future scope |

## Product Mechanisms To Absorb

### 1. Metric Source Labels

Borrowed from decision-support and physiology-lab style projects.

Every user-facing metric should show:

- measured / estimated / self-reported / not tested,
- protocol version,
- equipment path,
- date of test,
- whether it can affect a recommendation.

This supports the SportRx principle:

```text
Do not guess what we can measure.
Do not hide what we do not know.
Do not collect data that does not affect an output.
```

### 2. Measurement Ledger

Borrowed from WODIS, Ballast, and local-data projects.

SportRx should treat each benchmark session as a durable record:

- raw result,
- unit,
- RPE,
- completion status,
- substitution,
- equipment,
- protocol version,
- conditions,
- notes.

This is more important than another score.

### 3. Protocol Documents

Borrowed from Section 11 as a product mechanism, not as a training model.

SportRx should keep first-class documents for:

- benchmark protocol,
- test-day brief,
- operator checklist,
- evidence map,
- blocked-language checks,
- Review Pack handoff.

The goal is to make the product inspectable before it becomes more automated.

### 4. Plan-Actual Feedback

Borrowed from adaptive training projects.

SportRx should show why a future training block changes:

- completed as planned,
- missed session,
- RPE too high,
- RPE too low,
- benchmark retest improved,
- benchmark retest not comparable,
- safety gate blocked handoff.

The decision should be rule-coded before it is explained in friendly language.

### 5. Export Before Integration

Borrowed from data-portability projects and self-hosted endurance tools.

SportRx should export clean local files before connecting external platforms:

- benchmark log JSON,
- benchmark log CSV,
- training profile Markdown,
- training block Markdown,
- feedback dashboard Markdown,
- release manifest.

External integrations can wait until the internal record format is boring and
stable.

### 6. Pilot Data Capture

Borrowed from REGmon, AthleteLoadMonitor, and field-assessment report tools.

SportRx should treat future alpha use as a small measurement dataset, not as
chat history:

- participant table,
- Safety Gate outcome,
- Quick Match self-report record,
- benchmark-session record,
- weekly RPE feedback,
- protocol-deviation review,
- retest comparison,
- export/report handoff.

This supports the next honest milestone: real self-use and small-group alpha
data before stronger claims.

## Integration Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Keep SportRx as measurement-first | Adopt | This is the clearest differentiation from AI coaching apps |
| Add decision traceability as a product layer | Adopt | GitHub decision-support products show that source rows, thresholds, and override boundaries create trust |
| Add metric source labels across UI | Adopt | Makes uncertainty visible and improves trust |
| Keep Benchmark Log as the core data object | Adopt | This creates reusable pilot data |
| Add pilot-data capture as an architecture lane | Adopt | Athlete-monitoring projects show that clean forms, RPE records, benchmark logs, and reports are the real bridge to practice evidence |
| Add protocol documents as product surfaces | Adopt | Protocols and bad-response checks make the system feel less like a vague AI assessment |
| Keep FITT-VP as handoff, not identity | Adopt | Generic ACSM/FITT-VP generators exist; SportRx's identity is measured gatekeeping before prescription |
| Review WODIS/openweight compatibility later | Later | Useful only after SportRx's own benchmark schema stabilizes |
| Add race-result import or split analysis | Later | Requires real data and careful claim boundaries |
| Add wearable import | Reject for now | Would pull the product toward recovery/readiness dashboards |
| Add full exercise database | Reject for now | Does not improve the current measurement loop |
| Add AI chat coach | Reject | Crowded category and weak differentiation |

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
