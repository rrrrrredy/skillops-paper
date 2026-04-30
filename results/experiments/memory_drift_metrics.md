# Memory Drift Detection Metrics

These metrics were recomputed from preserved raw outputs after metadata normalization.

- Provider: `longcat`
- Model: `LongCat-Flash-Chat`
- Raw output: `results/experiments/raw/memory_drift_20260430T070521Z.jsonl`

## full_skillops_memory_policy

| Metric | Value | Count |
| --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |
| current_instruction_adherence_rate | 1.0000 | 22/22 |
| correct_forgetting_rate | 1.0000 | 22/22 |
| conflict_resolution_success_rate | 1.0000 | 22/22 |
| unsupported_memory_claim_rate | 0.0000 | 0/22 |

## no_forgetting_policy

| Metric | Value | Count |
| --- | --- | --- |
| stale_info_usage_rate | 0.2273 | 5/22 |
| current_instruction_adherence_rate | 1.0000 | 22/22 |
| correct_forgetting_rate | 0.0000 | 0/22 |
| conflict_resolution_success_rate | 0.0455 | 1/22 |
| unsupported_memory_claim_rate | 0.0000 | 0/22 |

## current_context_only

| Metric | Value | Count |
| --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |
| current_instruction_adherence_rate | 1.0000 | 22/22 |
| correct_forgetting_rate | 0.0000 | 0/22 |
| conflict_resolution_success_rate | 0.0000 | 0/22 |
| unsupported_memory_claim_rate | 0.0000 | 0/22 |
