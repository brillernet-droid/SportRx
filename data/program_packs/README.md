# SportRX Program Pack Registry

Each JSON file is a versioned product configuration, not a content template.
The registry controls which user context may reach a deterministic rule set.

`self_service` Packs may generate a dose only when Safety Gate and the Pack's
scope both allow it. `assessment_only` Packs may collect or display structured
context, but they must not generate an automatic prescription.

Before changing a Pack, update its tests, evidence mapping, user-facing
limitations, and release status together. Do not add a rule ID unless it exists
in `evidence/records/rules.json` and is reviewed for the Pack's scope.
