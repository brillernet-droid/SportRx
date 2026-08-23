# SportRx Methodology

SportRx is a rules-first sport assessment prototype. The engine uses explicit
rules for safety gate status, current fit, training profile, missing data, and
starter-path generation.

The normal product screen should stay plain. Evidence status belongs under
`Why this result?` or in these methodology files.

## SportRx 2.1 Principle

Measure what we know.
Show what we do not know.
Explain what matters.
Recommend the next useful action.

## Data Handling

Missing tests stay missing.

SportRx should not assign midpoint, average, or neutral values to untested
capacities. Unknown station ability is not `50/100`; it is `Not tested`.

## Performance vs Training Context

Performance profile:

- Running
- Aerobic fitness
- Strength endurance
- Station experience
- Work capacity

Training context:

- Days available per week
- Minutes available per session
- Equipment access
- Recent training consistency
- Training history

Available time can change the plan, but it is not a sport performance
capability.

## Evidence Ledger

- Safety gate: `evidence_backed`
- FITT-VP aerobic prescription rules: `evidence_backed`
- Hybrid Race dimension rules: `expert_informed`
- Current fit categories: `experimental`
- Internal aggregate score: `experimental`
- Hybrid Benchmark v1 cutoffs: `not_validated`

The active evidence knowledge base is maintained in:

- `evidence/literature_matrix.md`
- `evidence/rule_evidence_map.md`

Product rules should not be promoted unless they have a rule ID, an evidence
tier, and a documented user-facing claim.

## Benchmark Status

SportRx Hybrid Benchmark v1 is a prototype benchmark. It is designed to collect
repeatable measurements, not to provide validated cutoffs or population
percentiles.
