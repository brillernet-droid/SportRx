# SportRx Roadmap

## v0.1.0 - Core

- Safety screening
- Activity classification
- Aerobic intensity guidance
- Weekly volume rules
- 4-week FITT-VP prescription
- Weekly progression from completion and RPE

## v2.0.0 - SportRx Labs

- Quick Match
- Hybrid Race Performance Lab
- GREEN/YELLOW/RED safety gate
- Shareable result cards
- 4-week Starter Path
- External community routing only

## v2.1.0 - Humanize And Validate

- User-facing fit categories instead of precise prototype rankings
- Missing data remains `Not tested`
- Performance profile separated from training context
- Training Profile replaces identity-style athlete labels in the UI
- Strongest area and main gap include tie handling
- Hybrid Race Check result page
- Prototype Hybrid Benchmark v1
- Clear what we know, what we do not know, and what to measure next

## v2.2.0 - Measurement Loop

- Store benchmark results locally
- Compare retests against the user's own prior result
- Add consent-first beta feedback capture
- Move 5K/10K Running from registry-ready to enabled only if demand is clear

## v2.3.0 - Benchmark Log

- Add guided SportRx Hybrid Benchmark v1 protocol for standard and low-equipment paths
- Define safety stop rules, setup, execution, recording fields, and retest notes before logging
- Define SportRx Benchmark Log as a local JSON record
- Record benchmark protocol version, equipment, substitutions, raw results, RPE, and notes
- Add JSON export first, CSV export second
- Keep logs user-owned and inspectable
- Review WODIS compatibility after the SportRx schema stabilizes
- Import unit-compatible benchmark measurements into HYROX Check without creating artificial scores

## v2.4.0 - Pilot Reports

- Gym/member assessment report
- Race preparation check for event participants
- Exportable PDF or shareable report
- Aggregate anonymous reporting for pilot partners

## v2.5.0 - Open Source Lessons

- Add metric source labels across user-facing outputs
- Add output-prerequisite labels so users can see which gates affect decisions
- Add rule-coded plan-versus-actual reasons for training-block adjustment
- Add launch-readiness review package for public demo preparation
- Add demo runbook for first-time reviewer walkthroughs
- Add launch command-center cards for first-screen reviewer confidence
- Review WODIS mapping only after SportRx Benchmark Log stabilizes
- Keep external platform integrations deferred until local exports are stable

## Product Rules

1. Hybrid Race is the only fully enabled sport pack.
2. 5K/10K Running is registry-ready, not fully implemented.
3. Do not build a native mobile app.
4. Do not build a social network.
5. Do not add wearables, nutrition, payment, or subscriptions yet.
6. Do not call current fit innate ability or genetic suitability.
7. Do not invent validation, benchmark data, percentiles, or risk predictions.
8. Learn from open-source projects, but do not import code or datasets without explicit license review.
9. Export clean local records before building external integrations.
10. Treat GitHub competitor scans as product research, not scientific evidence.
