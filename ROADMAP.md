# SportRX Roadmap

## Product Direction

SportRX is an **AI-assisted Population Prescription OS**. An AI Prescription
Planner creates and adapts the training plan inside an independently versioned
`Program Pack`; deterministic Safety and Constraint Gates decide whether that
candidate may be shown. AI makes the prescription choices, while hard product
boundaries remain outside the model.

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

1. Define the structured AI prescription contract: context, candidate plan,
   assumptions, evidence IDs, uncertainty and decision log.
2. Convert existing dose and progression rules into a Constraint Gate that
   accepts, rejects or returns machine-readable repair reasons.
3. Add a provider-neutral model adapter, starting with DeepSeek for internal
   evaluation and keeping model keys server-side.
4. Implement the prescription-first mobile layout: `今天`、`我的计划`、
   `调整计划`、`进展`、`我的资料`.
5. Build simulated acceptance cases for unsafe, unsupported, missing-data,
   model-timeout and repeated-repair failures before enabling user-facing AI.

## 5–12 Weeks

1. Compare AI-generated plans against the deterministic baseline with blinded
   sport-science review before a limited user release.
2. Validate whether the low-activity adult Pack produces acceptable, useful and
   understandable AI prescriptions in self-use and small pilot cohorts.
3. Add versioned prompt, model, evidence-retrieval and constraint logs so every
   approved plan can be reproduced and audited.

## 3–12 Months

1. Add professional collaboration workspaces, protocol locking and audit logs.
2. Evaluate optional HealthKit, Health Connect, Garmin and venue-equipment
   imports as source-labelled records only.
3. Use consented, de-identified pilot data to assess constraint-pass rate,
   completion, adaptation quality and usability before expanding AI authority.

## Product Rules

1. The AI Prescription Planner may determine dose and progression only inside
   the active Pack's declared candidate space.
2. Every AI plan must pass deterministic Safety and Constraint Gates before it
   is stored or shown; AI cannot override a failed gate.
3. Special populations remain professional-collaboration pathways until an
   independently reviewed and validated Pack is released.
4. Do not build medical clearance, diagnosis, injury-risk percentages, race
   prediction, fake percentiles, nutrition, social features or an open-ended AI
   coach as the primary product experience.
5. A missing measurement remains `Not tested`; never infer it from a midpoint,
   average, model, or another Pack.
