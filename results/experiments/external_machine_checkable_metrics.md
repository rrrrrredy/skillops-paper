# External Machine-Checkable Metrics

This report is the primary external-smoke evidence route. It uses only deterministic checks over normalized result records: completed row counts, parse success, expected-behavior exact match, and explicit constraint-pass fields.

LLM-as-judge checks are treated as secondary sensitivity analyses over case labels. They do not replace these machine rules and are not used as primary outcome labels.

## Record State

| Quantity | Count |
| --- | --- |
| External condition result records | 16 |
| Artifacts represented | 1 |
| Provider/model groups | 2 |

## Metrics

| Group | Slice | Metric | Count | Rate | Rule |
| --- | --- | --- | --- | --- | --- |
| overall | all | completed_records | 16/16 | 1.000000 | run_status == completed |
| overall | all | parse_success_rate | 16/16 | 1.000000 | parse_success is true after schema-normalized provider output parsing |
| overall | all | behavior_match_rate | 5/16 | 0.312500 | predicted_behavior == expected_behavior after runner normalization |
| case_type | risk_constraint | constraint_pass_rate | 0/3 | 0.000000 | case_type == risk_constraint and constraint_pass is true |
| condition | original_freeform | parse_success_rate | 6/6 | 1.000000 | parse_success is true after schema-normalized provider output parsing |
| condition | original_freeform | behavior_match_rate | 2/6 | 0.333333 | predicted_behavior == expected_behavior after runner normalization |
| condition | skillops_ablation | parse_success_rate | 5/5 | 1.000000 | parse_success is true after schema-normalized provider output parsing |
| condition | skillops_ablation | behavior_match_rate | 1/5 | 0.200000 | predicted_behavior == expected_behavior after runner normalization |
| condition | skillops_normalized | parse_success_rate | 5/5 | 1.000000 | parse_success is true after schema-normalized provider output parsing |
| condition | skillops_normalized | behavior_match_rate | 2/5 | 0.400000 | predicted_behavior == expected_behavior after runner normalization |
| provider_model | deepseek::deepseek-v4-flash | parse_success_rate | 12/12 | 1.000000 | parse_success is true after schema-normalized provider output parsing |
| provider_model | deepseek::deepseek-v4-flash | behavior_match_rate | 3/12 | 0.250000 | predicted_behavior == expected_behavior after runner normalization |
| provider_model | kimi::kimi-k2.7-code | parse_success_rate | 4/4 | 1.000000 | parse_success is true after schema-normalized provider output parsing |
| provider_model | kimi::kimi-k2.7-code | behavior_match_rate | 2/4 | 0.500000 | predicted_behavior == expected_behavior after runner normalization |
| case_type | boundary_clarification | behavior_match_rate | 0/3 | 0.000000 | predicted_behavior == expected_behavior after runner normalization |
| case_type | negative_trigger | behavior_match_rate | 0/4 | 0.000000 | predicted_behavior == expected_behavior after runner normalization |
| case_type | positive_trigger | behavior_match_rate | 2/6 | 0.333333 | predicted_behavior == expected_behavior after runner normalization |
| case_type | risk_constraint | behavior_match_rate | 3/3 | 1.000000 | predicted_behavior == expected_behavior after runner normalization |

## Claim Boundary

These metrics support bounded execution-path claims only. They do not establish broad external effectiveness, statistical significance, or model ranking.
