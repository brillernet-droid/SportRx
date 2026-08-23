# SportRx Evidence Appraisal

This file answers the practical question:

> How strong is the evidence behind each SportRx product decision?

It is intentionally stricter than a reference list. A source only matters if it
supports, limits, or blocks a product claim.

## Summary

SportRx currently has strong evidence for general adult physical activity
guidance and basic aerobic prescription structure. It has moderate evidence for
RPE and standardized field testing principles. It has early, emerging evidence
for HYROX / Hybrid Race performance domains. It does not yet have validation for
SportRx-specific scores, percentiles, prediction, or benchmark cutoffs.

## Evidence Appraisal By Product Area

| Product area | Evidence strength | Current decision | Evidence IDs | Product boundary |
| --- | --- | --- | --- | --- |
| General adult activity target | Strong | Can reference 150-300 min/week moderate aerobic activity and 2+ days/week strengthening as public-health context | `PA-WHO-2020`, `PA-CDC-ADULT`, `PA-ACSM-CDC`, `PA-AHA` | Do not present as HYROX readiness |
| FITT-VP aerobic prescription | Strong | Keep SportRx Core aerobic prescription engine | `PA-ACSM-GETP12` | Keep scope to apparently healthy adults and conservative progression |
| Safety Gate | Moderate to strong conceptually | Keep Safety Gate separate from performance scoring | `SAFE-EIM`, `SAFE-EIM-SCREEN`, `SAFE-PARQ`, `SAFE-ACSM-ALGO` | Not medical clearance or diagnosis |
| RPE and session feedback | Moderate | Use RPE as subjective intensity/training-load feedback | `MON-RPE-ACSM`, `MON-SRPE-FOSTER`, `MON-SRPE-REVIEW` | Do not use RPE alone to infer fitness or injury risk |
| Field testing principle | Moderate but limited for adults | Use repeatable raw tests; record protocol and retest conditions | `TEST-6MWT-ATS`, `TEST-FIELD-ADULT`, `TEST-FIELD-SAFETY`, `TEST-FIELD-RELIABILITY` | Do not claim validated SportRx norms |
| HYROX / Hybrid Race domains | Emerging | Use five-domain Training Profile: running, aerobic base, strength endurance, station experience, work capacity | `HYROX-PHYS-2025`, `HIFT-HYBRID-REVIEW`, `HIFT-DEFINITION`, `HIFT-FITNESS` | Do not predict finish time, completion probability, or percentile |
| Starter Path routing | Weak / expert-informed | Allow only conservative 4-week starter focus when measured gap is available | `HYB-001`, `PATH-001`, `PATH-002`, `PATH-003` | Must be framed as a starting focus, not a proven outcome plan |
| Readiness / aggregate score | Weak / internal only | Hide from normal user experience | `PRED-001` | Do not show as validated score |
| Injury prediction | Not supported | Block | `INJ-CROSSFIT-SR`, `INJ-HIFT-SR` | No injury-risk percentages |

## What SportRx Can Say Now

SportRx can say:

- "This is your current measured training profile."
- "Some areas are not tested yet."
- "General adult guidelines support regular aerobic and strengthening activity."
- "RPE can help monitor how hard a session felt."
- "HYROX / Hybrid Race preparation likely requires both running and station
  capacity."
- "This Starter Path is a conservative starting focus based on measured gaps."

## What SportRx Cannot Say Yet

SportRx cannot say:

- "You are ready for HYROX."
- "Your finish probability is..."
- "Your injury risk is..."
- "Your percentile is..."
- "This benchmark is validated."
- "This plan is proven to improve your HYROX performance."

## Key Evidence Tensions

### 1. Guidelines Are Strong, But Not Event-Specific

WHO, CDC, ACSM, and AHA are strong for general activity targets. They are not
enough to claim race readiness. In the product, these should provide health and
baseline context only.

### 2. Field Tests Are Useful, But Must Be Standardized

Field tests are practical for recreational athletes, but adult evidence is mixed
and feasibility/safety reporting is limited. SportRx should store raw results,
protocol conditions, RPE, and retest changes before building norms.

### 3. HYROX Evidence Is Emerging

HYROX-specific research is new. It supports the idea that running and station
capacity matter, but not yet precise prediction or validated readiness scoring.

### 4. Practical Evidence Must Come From SportRx Users

The most important next evidence layer is not another paper. It is SportRx's own
repeatable benchmark and retest dataset.

## Product Decision

The next product milestone should be:

**SportRx 2.3 - Benchmark Protocol**

Priority:

1. Make SportRx Hybrid Benchmark v1 executable.
2. Record raw test results and protocol conditions.
3. Collect self-use and pilot retest data.
4. Keep recommendations conservative until SportRx has validation data.
