# External Result Summary

This summary is computed only from external condition live-result JSONL files. When none are present, it reports a no-results boundary.
Current records are bounded smoke rows over the first external shard prefix; they are execution-path diagnostics, not external validation, statistical significance, or model ranking.

| Group | Value | Metric | Count | Rate | Status |
| --- | --- | --- | --- | --- | --- |
| overall | external_condition_results | bounded_smoke_records | 16/16 | 1.000000 | bounded_smoke_diagnostic |
| condition | original_freeform | parse_success_rate | 6/6 | 1.000000 | bounded_smoke_diagnostic |
| condition | original_freeform | behavior_match_rate | 2/6 | 0.333333 | bounded_smoke_diagnostic |
| condition | skillops_ablation | parse_success_rate | 5/5 | 1.000000 | bounded_smoke_diagnostic |
| condition | skillops_ablation | behavior_match_rate | 1/5 | 0.200000 | bounded_smoke_diagnostic |
| condition | skillops_normalized | parse_success_rate | 5/5 | 1.000000 | bounded_smoke_diagnostic |
| condition | skillops_normalized | behavior_match_rate | 2/5 | 0.400000 | bounded_smoke_diagnostic |
| case_type | boundary_clarification | parse_success_rate | 3/3 | 1.000000 | bounded_smoke_diagnostic |
| case_type | boundary_clarification | behavior_match_rate | 0/3 | 0.000000 | bounded_smoke_diagnostic |
| case_type | negative_trigger | parse_success_rate | 4/4 | 1.000000 | bounded_smoke_diagnostic |
| case_type | negative_trigger | behavior_match_rate | 0/4 | 0.000000 | bounded_smoke_diagnostic |
| case_type | positive_trigger | parse_success_rate | 6/6 | 1.000000 | bounded_smoke_diagnostic |
| case_type | positive_trigger | behavior_match_rate | 2/6 | 0.333333 | bounded_smoke_diagnostic |
| case_type | risk_constraint | parse_success_rate | 3/3 | 1.000000 | bounded_smoke_diagnostic |
| case_type | risk_constraint | behavior_match_rate | 3/3 | 1.000000 | bounded_smoke_diagnostic |
| provider_model | deepseek::deepseek-v4-flash | parse_success_rate | 12/12 | 1.000000 | bounded_smoke_diagnostic |
| provider_model | deepseek::deepseek-v4-flash | behavior_match_rate | 3/12 | 0.250000 | bounded_smoke_diagnostic |
| provider_model | kimi::kimi-k2.7-code | parse_success_rate | 4/4 | 1.000000 | bounded_smoke_diagnostic |
| provider_model | kimi::kimi-k2.7-code | behavior_match_rate | 2/4 | 0.500000 | bounded_smoke_diagnostic |
| case_type | risk_constraint | constraint_pass_rate | 0/3 | 0.000000 | bounded_smoke_diagnostic |
