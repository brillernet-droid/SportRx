# Source Note 002: Safety And Preparticipation Screening

## Source Cluster

- Evidence IDs: `SAFE-EIM`, `SAFE-EIM-SCREEN`, `SAFE-PARQ`,
  `SAFE-ACSM-ALGO`
- Topic: exercise preparticipation screening and referral boundary
- Evidence tier: A/B
- Product area: Safety Gate

## What The Evidence Supports

The sources support a conservative preparticipation boundary:

- Screen for major symptoms, known disease history, and relevant warning signs.
- Consider current activity level and intended exercise intensity.
- Route uncertain or higher-risk cases to professional assessment rather than
  automated training handoff.
- Avoid turning a performance assessment into medical clearance.

## What It Does Not Support

These sources do not support:

- SportRx diagnosing disease.
- SportRx clearing someone for competition.
- A numeric medical risk score.
- Adjusting performance scores upward or downward based on safety status.

## SportRx Rules Affected

| Rule ID | Effect |
| --- | --- |
| `SAFE-001` | Supports keeping Safety Gate separate from performance scoring |
| `PRED-001` | Supports blocking medical-risk percentages |

## User-Facing Language Allowed

- "SportRx detected information that should be clarified before automated
  training handoff."
- "Safety Gate is separate from performance scoring."
- "This is not medical clearance."

## User-Facing Language Not Allowed

- "You are medically cleared."
- "You are safe to compete."
- "Your medical risk is X percent."

## Review Notes

- Reviewed by: SportRx
- Date: 2026-08-15
- Open question: decide whether SportRx should link users directly to PAR-Q+
  or only describe the referral boundary.
