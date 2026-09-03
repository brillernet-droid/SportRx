# SportRX Training Science Foundation v1

This layer expands the internal Knowledge Corpus from exercise anatomy and
movement selection toward program-level training science.

## Coverage

- resistance-training volume, frequency, periodization, rest, tempo,
  velocity loss, and autoregulation;
- endurance training-intensity distribution, HIIT versus continuous work,
  tapering, and temporary maintenance blocks;
- internal versus external load, recovery, and the diagnostic boundary around
  overtraining syndrome;
- flexibility training and lower-body plyometric training.

The structured chain is:

`SourceRecord -> ClaimRecord -> KnowledgeCard -> internal retrieval`

The pack adds 20 reviewed sources, 17 atomic claims, and 26 bilingual
KnowledgeCards. The complete corpus therefore contains 80 sources, 68 claims,
and 122 reviewed KnowledgeCards as of 2026-09-03.

## Authority Boundary

This is an educational and research-explanation layer. It does not change a
Safety Gate result, activate a Program Pack, prescribe an individual dose,
diagnose overtraining, or predict injury or performance. Conflicting evidence
is represented as a limitation instead of being resolved by model preference.

Public GitHub files contain citations, identifiers, links, curated summaries,
and limitations. Lawfully available open-access JATS XML may be downloaded by the
reviewer script into ignored `evidence/private/` storage. They are not part of
the public repository or model context.

## Files

- `topic_map.md`: covered questions, evidence state, and remaining gaps.
- `review_log.md`: search and review provenance.
- `fulltext_access.md`: lawful full-text storage rules and available records.
- `manifest.json`: machine-readable pack inventory and authority boundary.
