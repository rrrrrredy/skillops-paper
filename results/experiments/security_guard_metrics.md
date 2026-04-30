# Security Guard Detection Rate Metrics

These metrics were generated from an actual live run.

- Guard mode: `local-rules`
- Raw output: `results/experiments/raw/security_guard_20260430T065944Z.jsonl`

## Overall

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| detection_rate | 1.0000 | 24/24 |  |
| false_positive_rate | n/a | 0/0 | not applicable: no control cases supplied |

## Category Recall by risk_type

| risk_type | Recall | Count |
| --- | --- | --- |
| identity_confusion | 1.0000 | 3/3 |
| missing_constraints | 1.0000 | 3/3 |
| missing_tests | 1.0000 | 3/3 |
| over_broad_trigger | 1.0000 | 3/3 |
| privacy_leakage | 1.0000 | 3/3 |
| prompt_injection | 1.0000 | 3/3 |
| stale_memory | 1.0000 | 3/3 |
| unsafe_file_access | 1.0000 | 3/3 |

## Coverage by relevant_artifact

| relevant_artifact | Coverage | Count |
| --- | --- | --- |
| agent-self-audit | 1.0000 | 4/4 |
| lobster-guard | 1.0000 | 5/5 |
| persistent-memory | 1.0000 | 6/6 |
| skill-design-guide | 1.0000 | 4/4 |
| skill-security-guard | 1.0000 | 5/5 |
