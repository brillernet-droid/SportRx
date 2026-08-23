# SportRx Evidence Base

This directory is the structured knowledge base for SportRx.

It is designed to answer four questions before a rule appears in the product:

1. What claim are we making?
2. What input data support that claim?
3. What evidence tier supports the rule?
4. What are we not allowed to imply?

## Directory Map

| File or folder | Purpose |
| --- | --- |
| `knowledge_base.md` | Evidence operating system and RAG boundary |
| `literature_matrix.md` | Source registry and source IDs |
| `library/` | Saved citation library grouped by topic |
| `evidence_appraisal.md` | Strength-of-evidence judgement by product area |
| `evidence_questions.md` | Open evidence questions to answer before stronger claims |
| `rule_evidence_map.md` | Product rules linked to evidence IDs |
| `validation_plan.md` | Self-use, alpha, and pilot evidence collection plan |
| `claim_policy.md` | What SportRx can and cannot say |
| `glossary.md` | Controlled vocabulary for product and evidence language |
| `source_notes/` | Human-readable notes for source clusters |
| `templates/` | Templates for adding new sources and claims |
| `validation.md` | Current validation status and claims not yet supported |
| `rules.md` | Product rule summaries |
| `references.md` | Public reference list |

## Update Rule

No new user-facing rule should be added without updating:

- `literature_matrix.md`,
- `rule_evidence_map.md`,
- and, when needed, one source note in `source_notes/`.

## Evidence First

This is intentionally not a vector database or RAG system yet. The current job
is evidence hygiene: stable IDs, conservative claims, traceable rules, and clear
limits.

The most important current evidence documents are:

1. `evidence_appraisal.md`
2. `rule_evidence_map.md`
3. `validation_plan.md`
4. `claim_policy.md`

The source collection itself is stored in `library/`.
