# Evidence Intake Queue

This file tracks sources that should be reviewed before they enter the evidence
matrix.

## Review Status

| Status | Meaning |
| --- | --- |
| `candidate` | Found, not yet reviewed |
| `screened` | Looks relevant, needs source note |
| `included` | Added to literature matrix and source notes |
| `excluded` | Not useful or too weak for SportRx |

## Queue

| Source | Topic | Status | Next action |
| --- | --- | --- | --- |
| ACSM GETP 12th edition detailed chapters | FITT-VP, testing, progression | candidate | Review accessible excerpts or owned text; avoid copying proprietary content |
| HYROX race-result datasets | Event performance norms | candidate | Only use if source, sampling, and consent are clear |
| Recreational HYROX first-timer studies | First-event preparation | candidate | Search periodically; evidence is emerging |
| RowErg/SkiErg test reliability literature | Station-specific measurement | candidate | Add if field-test reliability is directly relevant |
| Chinese adult physical activity guideline sources | China-local context | candidate | Add Chinese guideline layer if SportRx targets Chinese users |
| Station circuit test-retest pilot data | SportRx-specific validation | not started | Collect internally before claiming cutoffs |

## Intake Checklist

Before adding a source to `literature_matrix.md`:

- Is it primary, guideline, systematic review, or a credible official source?
- Does it support a specific SportRx rule?
- Does it change a user-facing claim?
- What are its population, sample, and limits?
- Is the claim too strong for the evidence?
