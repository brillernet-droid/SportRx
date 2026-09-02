# SportRX Roadmap

## Product Direction

SportRX is a **Population Prescription OS**: a common exercise-prescription
core plus independently versioned and reviewable `Program Pack` configurations.
The platform may serve many contexts, but automatic dose generation opens only
when a specific Pack has rules, evidence mapping, QA, and a published boundary.

## Current Foundation

- Common core: safety routing, FITT-VP interface, RPE/completion feedback,
  plan-versus-actual records, explanations, exports and retest-ready records.
- Program Pack registry: scope, inputs, rule IDs, measurement protocol,
  content mapping, evidence version, limitations, QA status and withdrawal
  switch.
- Published Pack: low-activity adults, aerobic start and weekly RPE/completion
  adjustment.
- Limited Pack: general-fitness foundation, with aerobic automation only;
  strength remains content and recording, not automatic dose generation.
- Assessment-only paths: metabolic-health activity support and performance-entry
  measurement preparation.

## Next 0–4 Weeks

1. Make the mobile information architecture consistently reflect: `今天`、
   `我的计划`、`评估`、`进展`、`我的资料`.
2. Attach Pack ID, Pack version, rule IDs and source labels to all local plan,
   measurement and completed-session exports.
3. Add simulated acceptance cases for every Pack: eligible, assessment-only,
   professional-collaboration, missing-data, stop and withdrawal paths.
4. Publish Pack review checklist and release / rollback process.

## 5–12 Weeks

1. Improve the Athlete App MVP around the current Pack route, Today loop,
   source labels, export and deletion controls.
2. Validate the low-activity and general-fitness Pack with small self-use /
   pilot cohorts before expanding their dose rules.
3. Build independent evidence, rule and test requirements for strength, running,
   Hybrid and cycling Packs; do not reuse a Pack's dose rules by analogy.

## 3–12 Months

1. Add professional collaboration workspaces, protocol locking and audit logs.
2. Evaluate optional HealthKit, Health Connect, Garmin and venue-equipment
   imports as source-labelled records only.
3. Use consented, de-identified pilot data to assess completion, protocol
   consistency, test-retest error and usability before any model influences a
   Pack.

## Product Rules

1. Only Pack-linked deterministic rules may determine current-week dose or
   progression.
2. Evidence, movement catalogues, device data and AI may support review,
   execution or explanation; none can bypass a Pack or Safety Gate.
3. Special populations remain professional-collaboration pathways until an
   independently reviewed and validated Pack is released.
4. Do not build medical clearance, diagnosis, injury-risk percentages, race
   prediction, fake percentiles, nutrition, social features or an AI coach.
5. A missing measurement remains `Not tested`; never infer it from a midpoint,
   average, model, or another Pack.
