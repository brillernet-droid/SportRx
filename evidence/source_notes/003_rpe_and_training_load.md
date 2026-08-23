# Source Note 003: RPE And Training Load

## Source Cluster

- Evidence IDs: `MON-RPE-ACSM`, `MON-SRPE-FOSTER`, `MON-SRPE-REVIEW`
- Topic: perceived exertion and session-RPE training-load monitoring
- Evidence tier: B
- Product area: intensity explanation, weekly feedback, progression

## What The Evidence Supports

RPE and session-RPE can be useful in SportRx because they are:

- low-equipment,
- easy to collect,
- interpretable by recreational athletes,
- useful for intensity communication,
- and practical for monitoring training load over time.

This is especially useful when a user does not have a reliable HR device.

## What It Does Not Support

RPE does not provide:

- objective physiological measurement by itself,
- medical diagnosis,
- direct injury prediction,
- or automatic validation of a training plan.

RPE is subjective and should be interpreted with completion rate, symptoms,
training context, and retest results.

## SportRx Rules Affected

| Rule ID | Effect |
| --- | --- |
| `INT-001` | Supports using RPE when HR devices are unavailable |
| `CORE-002` | Supports intensity and progression feedback within FITT-VP |

## User-Facing Language Allowed

- "Use RPE to describe how hard the session felt."
- "RPE helps SportRx adjust conservatively when completion and perceived effort
  do not match the planned load."

## User-Facing Language Not Allowed

- "RPE proves your fitness improved."
- "Low RPE means low injury risk."
- "RPE alone determines your next training block."

## Review Notes

- Reviewed by: SportRx
- Date: 2026-08-15
- Open question: decide whether the UI should teach CR10 RPE or Borg 6-20. For
  v0.2, CR10 is simpler for recreational use.
