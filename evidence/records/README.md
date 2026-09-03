# SportRX Structured Evidence Records

These JSON files are the machine-readable layer behind the human-reviewed
Markdown evidence base. They are for internal audit and retrieval only; they
are not a RAG chat corpus and never decide Safety Gate status or training dose.

## Record Chain

```text
SourceRecord -> ClaimRecord -> RuleRecord / ProtocolRecord -> product explanation
```

- `sources.json`: citation metadata, public link, access state, population and limits.
- `claims.json`: the smallest approved product conclusion, its source links and
  allowed/disallowed user-facing language.
- `rules.json`: a product rule linked to reviewed claims and explicit failure modes.
- `protocols.json`: the execution and retest boundary for a measurement workflow.
- `packs/`: reviewed domain additions merged with the base files by the loader.
  Each pack is append-only evidence content, not a separate source of truth.

Public records are metadata and structured notes only. Put licensed PDFs,
institutional documents, or other non-public material in `evidence/private/`;
that directory is ignored by Git and never enters the retrieval corpus.

## Review Workflow

1. Add a candidate to `evidence/intake_queue.md`.
2. Screen whether it changes a SportRX rule or claim boundary.
3. Add or update the source, claim, rule, and/or protocol record.
4. Update the corresponding Markdown note and rule map.
5. Run the record validator and retrieval evaluation before using it in the UI.

```bash
python3 - <<'PY'
from sportrx.evidence_store import (
    evaluate_retrieval_set,
    evaluate_unsafe_query_set,
    validate_evidence_records,
)

print(validate_evidence_records())
print(evaluate_retrieval_set())
print(evaluate_unsafe_query_set())
PY
```

The local SQLite FTS5 file is generated under `.cache/` and is intentionally not
committed.

Optional DOI, PMID, and PMCID values live in a source record's `identifiers`
object. The validator rejects repeated identifiers across merged source packs.
