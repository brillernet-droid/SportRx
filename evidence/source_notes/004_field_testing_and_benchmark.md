# Source Note 004: Field Testing And Benchmark Design

## Source Cluster

- Evidence IDs: `TEST-6MWT-ATS`, `TEST-FIELD-ADULT`,
  `TEST-FIELD-SAFETY`, `TEST-FIELD-RELIABILITY`
- Topic: standardized field testing and repeatable benchmark design
- Evidence tier: B
- Product area: SportRx Hybrid Benchmark v1

## What The Evidence Supports

Field tests can be useful when they are:

- standardized,
- repeatable,
- documented with protocol details,
- interpreted within known limits,
- and retested under similar conditions.

Recent systematic review evidence also warns that, when criterion validity,
reliability, feasibility, and safety are considered together, adult field-test
evidence can be limited. That makes SportRx's own pilot retest dataset necessary
before claiming norms or validated cutoffs.

The six-minute walk test literature is useful less because SportRx is building
a clinical 6MWT product, and more because it demonstrates protocol discipline:
same route, same instructions, safety stopping rules, and repeatable recording.

## What It Does Not Support

The current evidence does not validate:

- SportRx Hybrid Benchmark v1 cutoffs.
- SportRx station circuit scores.
- Population norms.
- HYROX outcome prediction.

## SportRx Rules Affected

| Rule ID | Effect |
| --- | --- |
| `MEAS-001` | Supports keeping untested areas as `Not tested` |
| `MEAS-002` | Supports requiring measurement before comparison, but the two-dimension threshold is still SportRx's own conservative rule |
| `HYB-002` | Supports treating the benchmark as raw measurement and retest layer |
| `PROTOCOL-001` | Supports documenting setup, order, stop rules, recording fields, and retest notes before interpreting logs |
| `PATH-001` | Supports routing insufficient-data users to benchmark first |

## User-Facing Language Allowed

- "Use the same route, equipment, and setup when you retest."
- "This benchmark stores raw measurements first. It is not a validated score."
- "If there is not enough measured data, SportRx will not generate a tailored
  Starter Path."

## User-Facing Language Not Allowed

- "This benchmark is validated."
- "Your score is above average."
- "This station score predicts your HYROX finish time."

## Review Notes

- Reviewed by: SportRx
- Date: 2026-08-15
- Open question: collect SportRx test-retest data for 1 km run, station circuit,
  RowErg/SkiErg, and compromised-run components.
