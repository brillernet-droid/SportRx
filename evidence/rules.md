# SportRx Rules

## Safety Gate

SportRx uses GREEN/YELLOW/RED safety states:

- `GREEN`: no major automated stop flag identified
- `YELLOW`: professional assessment or clarification is recommended before
  high-intensity participation
- `RED`: stop automated training handoff and recommend appropriate professional
  assessment

Safety is independent from performance. RED blocks automated training.

The workflow is original to SportRx and informed by public exercise
preparticipation screening principles. It does not reproduce a proprietary
questionnaire.

## Quick Match

Quick Match uses internal numerical ranking, but user-facing output is
categorical:

- Strong current fit
- Good current fit
- Some preparation needed
- More preparation needed

Each result includes why it fits and what evidence is missing. It is a current
training fit, not innate potential.

## Hybrid Race Check

The check reports five key areas:

- Running
- Aerobic fitness
- Strength endurance
- Station experience
- Work capacity

Untested areas return `Not tested`.

Tests completed is data completeness only:

```text
3 of 5 key areas assessed
```

It is not predictive confidence.

## Tie Handling

If measured dimensions are effectively equal, SportRx reports a balanced profile
and does not force a single main gap.

If several lowest dimensions are tied, SportRx lists them together as main
development areas.

## Starter Path

Starter paths are based on the main area to improve, unless safety blocks
training. Week language should be direct:

```text
Week 1
Build repeatable aerobic volume

Tuesday
30 min easy run
RPE 3-4
```

## Preserved SportRx Core

The original aerobic FITT-VP engine remains available for simple 4-week aerobic
prescription and weekly progression from completion and RPE.
