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
| `records/` | Machine-readable source, claim, rule, and protocol records for internal audit and retrieval |
| `evaluation/` | Curated retrieval and unsafe-query checks; not user data |
| `evidence_appraisal.md` | Strength-of-evidence judgement by product area |
| `evidence_questions.md` | Open evidence questions to answer before stronger claims |
| `rule_evidence_map.md` | Product rules linked to evidence IDs |
| `validation_plan.md` | Self-use, alpha, and pilot evidence collection plan |
| `data_governance.md` | Phase 0 / Alpha data-minimization, consent, retention, deletion, and de-identification rules |
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

This is a structured evidence layer with local internal SQLite FTS5 retrieval.
It is not an LLM RAG system or a user-facing chat product. The job remains
evidence hygiene: stable IDs, conservative claims, traceable rules, and clear
limits.

The generated local search index lives under `.cache/`; copyrighted source PDFs
and institutional documents belong in ignored `evidence/private/`, never in the
public repository or retrieval corpus.

The most important current evidence documents are:

1. `evidence_appraisal.md`
2. `rule_evidence_map.md`
3. `validation_plan.md`
4. `claim_policy.md`

`source_notes/006_benchmark_component_evidence.md` is the component evidence
ledger. It labels each real Benchmark component as `partial_evidence` or
`experimental`; it does not make any component a normed SportRX test.

The source collection itself is stored in `library/`.
