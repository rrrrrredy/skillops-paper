# SkillOps Ablation Study Metrics

These metrics were recomputed from preserved raw outputs after metadata normalization.

- Provider: `deepseek`
- Model: `deepseek-chat`
- Raw output: `results/experiments/raw/ablation_20260430T080511Z.jsonl`

Interpretation note: The trigger-routing slice is retained for traceability only.
The ablation skill variants define a translation skill, while the trigger benchmark routes across benchmark skills.
Treat the trigger-routing slice as inconclusive until it is rerun with aligned skill definitions.

## full_skillops

### trigger

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| precision | 0.0000 | 0/1 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| recall | 0.0000 | 0/15 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| f1 | 0.0000 | 0/36 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| false_trigger_rate | 0.0833 | 1/12 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| ambiguity_handling_rate | 0.0000 | 0/9 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |

### constraint

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| violation_rate | 0.0833 | 2/24 |  |
| safe_handling_rate | 0.9583 | 23/24 |  |
| unsupported_success_claim_rate | 0.0000 | 0/24 |  |

### memory

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |  |
| correct_forgetting_rate | 1.0000 | 22/22 |  |
| current_instruction_adherence_rate | 1.0000 | 22/22 |  |

## no_trigger_boundary

### trigger

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| precision | 0.0000 | 0/1 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| recall | 0.0000 | 0/15 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| f1 | 0.0000 | 0/36 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| false_trigger_rate | 0.0833 | 1/12 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| ambiguity_handling_rate | 0.0000 | 0/9 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |

### constraint

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| violation_rate | 0.0417 | 1/24 |  |
| safe_handling_rate | 1.0000 | 24/24 |  |
| unsupported_success_claim_rate | 0.0000 | 0/24 |  |

### memory

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |  |
| correct_forgetting_rate | 1.0000 | 22/22 |  |
| current_instruction_adherence_rate | 1.0000 | 22/22 |  |

## no_execution_constraints

### trigger

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| precision | 0.0000 | 0/1 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| recall | 0.0000 | 0/15 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| f1 | 0.0000 | 0/36 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| false_trigger_rate | 0.0833 | 1/12 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| ambiguity_handling_rate | 0.0000 | 0/9 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |

### constraint

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| violation_rate | 0.0833 | 2/24 |  |
| safe_handling_rate | 0.9583 | 23/24 |  |
| unsupported_success_claim_rate | 0.0000 | 0/24 |  |

### memory

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |  |
| correct_forgetting_rate | 1.0000 | 22/22 |  |
| current_instruction_adherence_rate | 1.0000 | 22/22 |  |

## no_security_checks

### trigger

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| precision | 0.0000 | 0/1 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| recall | 0.0000 | 0/15 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| f1 | 0.0000 | 0/36 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| false_trigger_rate | 0.0833 | 1/12 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| ambiguity_handling_rate | 0.0000 | 0/9 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |

### constraint

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| violation_rate | 0.0833 | 2/24 |  |
| safe_handling_rate | 0.7500 | 18/24 |  |
| unsupported_success_claim_rate | 0.0000 | 0/24 |  |

### memory

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |  |
| correct_forgetting_rate | 1.0000 | 22/22 |  |
| current_instruction_adherence_rate | 1.0000 | 22/22 |  |

## no_memory_interface

### trigger

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| precision | 0.0000 | 0/1 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| recall | 0.0000 | 0/15 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| f1 | 0.0000 | 0/36 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| false_trigger_rate | 0.0833 | 1/12 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| ambiguity_handling_rate | 0.0000 | 0/9 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |

### constraint

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| violation_rate | 0.0833 | 2/24 |  |
| safe_handling_rate | 1.0000 | 24/24 |  |
| unsupported_success_claim_rate | 0.0000 | 0/24 |  |

### memory

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |  |
| correct_forgetting_rate | 1.0000 | 22/22 |  |
| current_instruction_adherence_rate | 1.0000 | 22/22 |  |

## freeform_only

### trigger

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| precision | 0.0000 | 0/1 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| recall | 0.0000 | 0/15 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| f1 | 0.0000 | 0/36 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| false_trigger_rate | 0.0833 | 1/12 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |
| ambiguity_handling_rate | 0.0000 | 0/9 | retained for traceability; benchmark/variant mismatch makes this trigger slice inconclusive |

### constraint

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| violation_rate | 0.0417 | 1/24 |  |
| safe_handling_rate | 0.9583 | 23/24 |  |
| unsupported_success_claim_rate | 0.0000 | 0/24 |  |

### memory

| Metric | Value | Count | Notes |
| --- | --- | --- | --- |
| stale_info_usage_rate | 0.0000 | 0/22 |  |
| correct_forgetting_rate | 1.0000 | 22/22 |  |
| current_instruction_adherence_rate | 1.0000 | 22/22 |  |
