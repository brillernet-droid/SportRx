# SportRX

> **A practical, explainable, adjustable 4-week aerobic exercise prescription.**

SportRX is an aerobic exercise-prescription prototype for apparently healthy
adults. It is not an AI fitness coach: deterministic rules set the initial
FITT-VP dose and weekly progression.

The active v0.1 core loop is:

```text
basic inputs → screening boundary → 4-week FITT-VP plan → session execution → RPE / completion → next-week adjustment
```

The first interface is Chinese and mobile-first: Set-up, Plan, Today, and
Progress. It asks only for inputs that affect the plan: recent activity, time
availability, preferred aerobic modality, optional resting heart rate, and a
minimal stop boundary.

## Current status

This is an aerobic-prescription prototype. Current work focuses on self-use
and small-sample usability testing. SportRX does not claim
medical clearance, injury-risk percentages, race predictions, population
percentiles, validated readiness scores, or official event certification.

AI does not decide safety, exercise dose, weekly volume, or progression.

## Scope boundary

v0.1 covers aerobic exercise only, for adults aged 18-64. It blocks automated
prescription when a warning symptom, a relevant condition, or uncertainty is
reported. It does not provide medical clearance, diagnosis, emergency advice,
injury-risk estimates, race prediction, nutrition advice, or athlete percentiles.

## Internal Knowledge RAG

The repository also contains an internal, Chinese-answer research layer under
[`evidence/knowledge/`](evidence/knowledge/README.md). It indexes only
human-reviewed bilingual knowledge cards and stays separate from the
deterministic rule-evidence store. The optional DeepSeek synthesis path remains
disabled until the corpus and citation, boundary, and answer-quality gates pass.

## Run locally

```bash
python3 -m pip install -e ".[dev,app]"
python3 scripts/smoke_check.py
bash scripts/run_local.sh
```

The primary early-testing interface is Chinese. The default runtime launches
the v0.1 aerobic prescription flow. Set `SPORT_RX_PRODUCT_MODE=labs` only to
open the retained internal measurement-lab prototype.

## Chinese documentation

- [Quick start](docs/zh-CN/quickstart.md)
- [Product guide](docs/zh-CN/product-guide.md)
- [Claim boundaries](docs/zh-CN/claim-boundaries.md)
- [Terminology](docs/zh-CN/terminology.md)
- [Venue Entry (Chinese)](docs/zh-CN/venue-entry.md)

Technical evidence, rule IDs, schemas, and source documents remain in English
under [`evidence/`](evidence/).
