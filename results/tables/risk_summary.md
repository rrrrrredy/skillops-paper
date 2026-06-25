# Risk Case Summary

This summary is generated from `benchmark/risk_cases.csv`, which is a
manually constructed operational risk benchmark input.

The counts below describe the benchmark inventory only. They are not model
detection scores, significance claims, or broad empirical validation.

## Input Summary

- Total cases: 24
- Case IDs with the `manual-` prefix: 24
- Distinct risk types: 8
- Distinct relevant artifact values: 5

## Counts by Risk Type

| Risk Type | Count |
| --- | --- |
| prompt_injection | 3 |
| over_broad_trigger | 3 |
| unsafe_file_access | 3 |
| missing_constraints | 3 |
| stale_memory | 3 |
| missing_tests | 3 |
| identity_confusion | 3 |
| privacy_leakage | 3 |

## Counts by Relevant Artifact

| Relevant Artifact | Count |
| --- | --- |
| skill-security-guard | 5 |
| lobster-guard | 5 |
| skill-design-guide | 4 |
| persistent-memory | 6 |
| agent-self-audit | 4 |

## Limitations

- Every case is manually written from repository inspection rather than observed incidents.
- The summary does not estimate real-world prevalence or detector performance.
- The table should be read as a benchmark-design inventory for later evaluation.

