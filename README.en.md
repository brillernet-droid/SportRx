# SportRX

> **A population prescription platform built from versioned, explainable Program Packs.**

SportRX is a population prescription platform prototype. A common core handles
safety routing, FITT-VP interfaces, feedback, records and explanation. A
versioned `Program Pack` defines which context may use which inputs, rules,
measurements and automation boundary. SportRX is not an AI fitness coach:
deterministic Pack-linked rules set dose and progression, while movement content
supplies instructions without deciding a dose.

The active v0.1 core loop is:

```text
current context → Program Pack route → screening boundary → current-week FITT-VP plan → session execution → RPE / completion → next-week adjustment
```

The first interface is Chinese and mobile-first: Today, My Plan, Assessment,
Progress and My Profile. It asks only for inputs that affect routing or dose:
goal, recent activity, time availability, preferred aerobic modality, optional
resting heart rate, and a minimal stop boundary.

## Current status

The released self-service capability remains aerobic prescription for
apparently healthy adults. The registry also includes a limited general-fitness
Pack (aerobic automation only), plus assessment-only metabolic-health and
performance-entry routes. Current work focuses on self-use and small-sample
usability testing. The local
catalogue contains 1,324 text-only records from the reviewed
[`hasaneyldrm/exercises-dataset`](https://github.com/hasaneyldrm/exercises-dataset)
source; third-party images and GIFs are excluded. SportRX does not claim
medical clearance, injury-risk percentages, race predictions, population
percentiles, validated readiness scores, or official event certification.

AI does not decide safety, exercise dose, weekly volume, or progression.

## Scope boundary

The published self-service Packs cover aerobic exercise only, for adults aged
18-64. They block automated prescription when a warning symptom, a relevant
condition, uncertainty, or a non-released Pack route is present. SportRX does
not provide medical clearance, diagnosis, emergency advice, injury-risk
estimates, race prediction, nutrition advice, or athlete percentiles.

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
- [Program Pack path](docs/zh-CN/program-packs.md)
- [Product guide](docs/zh-CN/product-guide.md)
- [Claim boundaries](docs/zh-CN/claim-boundaries.md)
- [Terminology](docs/zh-CN/terminology.md)
- [Venue Entry (Chinese)](docs/zh-CN/venue-entry.md)

Technical evidence, rule IDs, schemas, and source documents remain in English
under [`evidence/`](evidence/).
