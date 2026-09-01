# SportRX AI Handoff

## What this repository is

SportRX is a Chinese-first Streamlit prototype for an explainable, adaptive
aerobic exercise prescription loop for apparently healthy adults. It is not an
AI fitness coach. Deterministic Python rules determine screening routes,
training dose, and weekly progression; evidence and knowledge components are
kept separate from those decisions.

Current release: **v0.1.3**.

## Read this first

The repository contains earlier research and measurement experiments in
addition to the active v0.1 product. Treat the following as the active product
path unless a task explicitly asks to revive a different module:

```text
Onboarding (two short steps)
  -> screening route
  -> Today's current-week FITT-VP session
  -> one-session completion + RPE record
  -> week-level feedback
  -> next-week hold / small increase / reduce / pause decision
```

The active navigation is implemented in `app/streamlit_app.py`:

- `首页`: today's prescribed aerobic session.
- `设置`: two-step setup and prescription generation.
- `记录`: one session at a time; captures completion, RPE, difficulty, and
  adverse-event signal.
- `计划`: current committed week plus an explicitly conditional four-week
  adaptive route.
- `动作`: optional catalogue instructions that support execution but do not
  decide dose.

## Best reading order

1. `README.md` for product scope, user flow, limits, and local run commands.
2. `docs/zh-CN/quickstart.md` for an end-to-end local experience.
3. `app/streamlit_app.py` for the active UI and state transitions.
4. `sportrx/prescription.py` for the four-week plan format and current-week
   commitment rule.
5. `sportrx/session_feedback.py` and `sportrx/progression.py` for adaptive
   feedback logic.
6. `sportrx/screening.py`, `sportrx/intensity.py`, and `sportrx/volume.py` for
   screening, intensity, and volume decisions.
7. `tests/test_session_feedback.py` and `tests/test_prescription.py` for
   behavioural expectations.

## Active product constraints

- v0.1 auto-prescribes **aerobic exercise only**.
- Scope is apparently healthy adults; signals requiring further professional
  assessment stop automation.
- A future week is not a guaranteed prescription. It remains awaiting feedback
  until the preceding week has been recorded.
- RPE and completion inform weekly adjustment. Optional exercise-catalogue
  movements never alter frequency, duration, or intensity.
- Do not add medical clearance, diagnosis, injury-risk percentages, race
  predictions, fake percentiles, nutrition features, wearable integrations, or
  an AI chat coach to the active flow.

## Evidence and RAG boundaries

- `evidence/records/` is the structured, rule-linked evidence store.
- `evidence/knowledge/` is an internal research corpus and retrieval layer.
- Knowledge RAG may summarize approved research but must never change Safety
  Gate, prescription dose, or progression outputs.
- The user-facing product currently does not expose free-form AI answers.

Read `evidence/README.md` and `evidence/knowledge/README.md` before changing
rules or evidence-related outputs.

## Repository map

```text
app/                 Streamlit interface
sportrx/             deterministic engine and supporting modules
data/exercises/      local third-party movement catalogue and license notices
evidence/            public metadata, rule evidence, knowledge cards, evaluation
docs/zh-CN/          Chinese public product documentation
examples/            example inputs and outputs
tests/               executable behaviour and boundary checks
scripts/             local run, smoke check, and data utilities
```

## Historical / experimental modules

The repository retains benchmark, venue-entry, readiness, quick-match, hybrid,
and internal review modules from prior explorations. They are not the default
v0.1 user journey. Do not delete or silently re-enable them; changes to them
need a deliberate product decision and their existing tests must continue to
pass.

## Local verification

```bash
python3 -m pip install -e ".[dev,app]"
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider
bash scripts/run_local.sh
```

## How to give useful advice about this project

Prefer advice that makes the active loop more usable, measurable, testable, or
evidence-traceable. Name assumptions clearly. Separate:

1. a product recommendation,
2. a scientific/evidence recommendation, and
3. an implementation recommendation.

Do not describe unreleased research, legacy modules, or future AI capabilities
as if they are already public SportRX functionality.
