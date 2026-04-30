# SkillOps Ablation Study Metrics

These metrics were generated from an actual live run.

- Provider: `longcat`
- Model: `deepseek-chat`
- Raw output: `results/experiments/raw/ablation_20260430T080511Z.jsonl`

## full_skillops

### trigger

| Metric | Value | Count |
| --- | --- | --- |
| precision | 0.0000 | 0/1 |
| recall | 0.0000 | 0/15 |
| f1 | 0.0000 | 0/36 |
| false_trigger_rate | 0.0833 | 1/12 |
| ambiguity_handling_rate | 0.0000 | 0/9 |

### constraint

| Metric | Value | Count |
| --- | --- | --- |
| violation_rate | 0.0833 | 2/24 |
| safe_handling_rate | 0.9583 | 23/24 |
| unsupported_success_claim_rate | 0.0000 | 0/24 |

### memory

| Metric | Value | Count |
| --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |
| correct_forgetting_rate | 1.0000 | 22/22 |
| current_instruction_adherence_rate | 1.0000 | 22/22 |

## no_trigger_boundary

### trigger

| Metric | Value | Count |
| --- | --- | --- |
| precision | 0.0000 | 0/1 |
| recall | 0.0000 | 0/15 |
| f1 | 0.0000 | 0/36 |
| false_trigger_rate | 0.0833 | 1/12 |
| ambiguity_handling_rate | 0.0000 | 0/9 |

### constraint

| Metric | Value | Count |
| --- | --- | --- |
| violation_rate | 0.0417 | 1/24 |
| safe_handling_rate | 1.0000 | 24/24 |
| unsupported_success_claim_rate | 0.0000 | 0/24 |

### memory

| Metric | Value | Count |
| --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |
| correct_forgetting_rate | 1.0000 | 22/22 |
| current_instruction_adherence_rate | 1.0000 | 22/22 |

## no_execution_constraints

### trigger

| Metric | Value | Count |
| --- | --- | --- |
| precision | 0.0000 | 0/1 |
| recall | 0.0000 | 0/15 |
| f1 | 0.0000 | 0/36 |
| false_trigger_rate | 0.0833 | 1/12 |
| ambiguity_handling_rate | 0.0000 | 0/9 |

### constraint

| Metric | Value | Count |
| --- | --- | --- |
| violation_rate | 0.0833 | 2/24 |
| safe_handling_rate | 0.9583 | 23/24 |
| unsupported_success_claim_rate | 0.0000 | 0/24 |

### memory

| Metric | Value | Count |
| --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |
| correct_forgetting_rate | 1.0000 | 22/22 |
| current_instruction_adherence_rate | 1.0000 | 22/22 |

## no_security_checks

### trigger

| Metric | Value | Count |
| --- | --- | --- |
| precision | 0.0000 | 0/1 |
| recall | 0.0000 | 0/15 |
| f1 | 0.0000 | 0/36 |
| false_trigger_rate | 0.0833 | 1/12 |
| ambiguity_handling_rate | 0.0000 | 0/9 |

### constraint

| Metric | Value | Count |
| --- | --- | --- |
| violation_rate | 0.0833 | 2/24 |
| safe_handling_rate | 0.7500 | 18/24 |
| unsupported_success_claim_rate | 0.0000 | 0/24 |

### memory

| Metric | Value | Count |
| --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |
| correct_forgetting_rate | 1.0000 | 22/22 |
| current_instruction_adherence_rate | 1.0000 | 22/22 |

## no_memory_interface

### trigger

| Metric | Value | Count |
| --- | --- | --- |
| precision | 0.0000 | 0/1 |
| recall | 0.0000 | 0/15 |
| f1 | 0.0000 | 0/36 |
| false_trigger_rate | 0.0833 | 1/12 |
| ambiguity_handling_rate | 0.0000 | 0/9 |

### constraint

| Metric | Value | Count |
| --- | --- | --- |
| violation_rate | 0.0833 | 2/24 |
| safe_handling_rate | 1.0000 | 24/24 |
| unsupported_success_claim_rate | 0.0000 | 0/24 |

### memory

| Metric | Value | Count |
| --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |
| correct_forgetting_rate | 1.0000 | 22/22 |
| current_instruction_adherence_rate | 1.0000 | 22/22 |

## freeform_only

### trigger

| Metric | Value | Count |
| --- | --- | --- |
| precision | 0.0000 | 0/1 |
| recall | 0.0000 | 0/15 |
| f1 | 0.0000 | 0/36 |
| false_trigger_rate | 0.0833 | 1/12 |
| ambiguity_handling_rate | 0.0000 | 0/9 |

### constraint

| Metric | Value | Count |
| --- | --- | --- |
| violation_rate | 0.0417 | 1/24 |
| safe_handling_rate | 0.9583 | 23/24 |
| unsupported_success_claim_rate | 0.0000 | 0/24 |

### memory

| Metric | Value | Count |
| --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |
| correct_forgetting_rate | 1.0000 | 22/22 |
| current_instruction_adherence_rate | 1.0000 | 22/22 |
