# Full-Text Access

The public corpus stores metadata and human-curated summaries, not article
full text. The following reviewed records have a PubMed Central identifier and
can be downloaded as structured JATS XML from Europe PMC by running:

```bash
python3 scripts/fetch_open_access_training_science_reviews.py
```

| Source ID | PMCID | Topic |
|---|---|---|
| `TS-RT-UMBRELLA-2024` | `PMC10818109` | Resistance prescription umbrella review |
| `TS-RT-REST-2024` | `PMC11349676` | Inter-set rest |
| `TS-RT-VL-2023` | `PMC9807551` | Velocity loss |
| `TS-RT-AUTOREG-2022` | `PMC8762534` | Autoregulation |
| `TS-END-TID-2024` | `PMC11329428` | Endurance intensity distribution |
| `TS-END-TAPER-2023` | `PMC10171681` | Tapering |
| `TS-FLEX-CHRONIC-2024` | `PMC10980866` | Stretch training |

JATS XML preserves the article structure while avoiding the very large image-
heavy PDF packages served by some publishers. Downloaded files and their
checksum manifest remain under
`evidence/private/fulltext/training_science/`, which is ignored by Git and
excluded from release packages and Knowledge RAG model context.
