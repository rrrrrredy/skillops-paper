# Controlled DeepSeek Memory Drift Metrics

- Provider: `deepseek`
- Model: `deepseek-chat`
- Repeats: `3`
- Raw output: `results\experiments\raw\controlled_deepseek_memory_20260506T025754Z.jsonl`
- Status: `complete`

## condition

| condition | Metric | Mean | Std | R1 | R2 | R3 | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| current_context_only | conflict_resolution_success_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |
| current_context_only | correct_forgetting_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |
| current_context_only | current_instruction_adherence_rate | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| current_context_only | stale_info_usage_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |
| current_context_only | unsupported_memory_claim_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |
| full_skillops_memory_policy | conflict_resolution_success_rate | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| full_skillops_memory_policy | correct_forgetting_rate | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| full_skillops_memory_policy | current_instruction_adherence_rate | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| full_skillops_memory_policy | stale_info_usage_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |
| full_skillops_memory_policy | unsupported_memory_claim_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |
| no_forgetting_policy | conflict_resolution_success_rate | 0.0606 | 0.0214 | 0.0455 | 0.0909 | 0.0455 |  |
| no_forgetting_policy | correct_forgetting_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |
| no_forgetting_policy | current_instruction_adherence_rate | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| no_forgetting_policy | stale_info_usage_rate | 0.0455 | 0.0000 | 0.0455 | 0.0455 | 0.0455 |  |
| no_forgetting_policy | unsupported_memory_claim_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |
