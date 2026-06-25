# Live Model Experiment Summary

These metrics are recomputed from raw JSONL outputs produced during live model calls.

## Constraint compliance

### deepseek / deepseek-v4-flash

| Dimension | Value | Metric | Rate | Count |
| --- | --- | --- | --- | --- |
| prompt_variant | skillops | violation_rate | 0.708333 | 17/24 |
| prompt_variant | skillops | safe_handling_rate | 0.291667 | 7/24 |
| prompt_variant | skillops | unsupported_success_claim_rate | 0.041667 | 1/24 |
| prompt_variant | skillops | constraint_compliance_rate | 0.291667 | 7/24 |
| prompt_variant | vague | violation_rate | 0.875000 | 21/24 |
| prompt_variant | vague | safe_handling_rate | 0.166667 | 4/24 |
| prompt_variant | vague | unsupported_success_claim_rate | 0.166667 | 4/24 |
| prompt_variant | vague | constraint_compliance_rate | 0.125000 | 3/24 |

Raw output: `results\experiments\raw\constraint_20260625T051633Z.jsonl`

### kimi / kimi-k2.7-code

| Dimension | Value | Metric | Rate | Count |
| --- | --- | --- | --- | --- |
| prompt_variant | skillops | violation_rate | 0.541667 | 13/24 |
| prompt_variant | skillops | safe_handling_rate | 0.500000 | 12/24 |
| prompt_variant | skillops | unsupported_success_claim_rate | 0.041667 | 1/24 |
| prompt_variant | skillops | constraint_compliance_rate | 0.458333 | 11/24 |
| prompt_variant | vague | violation_rate | 0.500000 | 12/24 |
| prompt_variant | vague | safe_handling_rate | 0.583333 | 14/24 |
| prompt_variant | vague | unsupported_success_claim_rate | 0.125000 | 3/24 |
| prompt_variant | vague | constraint_compliance_rate | 0.500000 | 12/24 |

Raw output: `results\experiments\raw\constraint_20260625T060926Z.jsonl`

## Memory drift

### deepseek / deepseek-v4-flash

| Dimension | Value | Metric | Rate | Count |
| --- | --- | --- | --- | --- |
| condition | full_skillops_memory_policy | stale_info_usage_rate | 0.000000 | 0/22 |
| condition | full_skillops_memory_policy | current_instruction_adherence_rate | 1.000000 | 22/22 |
| condition | full_skillops_memory_policy | correct_forgetting_rate | 1.000000 | 22/22 |
| condition | full_skillops_memory_policy | conflict_resolution_success_rate | 0.954545 | 21/22 |
| condition | full_skillops_memory_policy | unsupported_memory_claim_rate | 0.000000 | 0/22 |
| condition | no_forgetting_policy | stale_info_usage_rate | 0.000000 | 0/22 |
| condition | no_forgetting_policy | current_instruction_adherence_rate | 1.000000 | 22/22 |
| condition | no_forgetting_policy | correct_forgetting_rate | 0.000000 | 0/22 |
| condition | no_forgetting_policy | conflict_resolution_success_rate | 0.090909 | 2/22 |
| condition | no_forgetting_policy | unsupported_memory_claim_rate | 0.000000 | 0/22 |
| condition | current_context_only | stale_info_usage_rate | 0.000000 | 0/22 |
| condition | current_context_only | current_instruction_adherence_rate | 0.954545 | 21/22 |
| condition | current_context_only | correct_forgetting_rate | 0.000000 | 0/22 |
| condition | current_context_only | conflict_resolution_success_rate | 0.000000 | 0/22 |
| condition | current_context_only | unsupported_memory_claim_rate | 0.000000 | 0/22 |

Raw output: `results\experiments\raw\memory_drift_20260625T054747Z.jsonl`

### kimi / kimi-k2.7-code

| Dimension | Value | Metric | Rate | Count |
| --- | --- | --- | --- | --- |
| condition | full_skillops_memory_policy | stale_info_usage_rate | 0.000000 | 0/22 |
| condition | full_skillops_memory_policy | current_instruction_adherence_rate | 1.000000 | 22/22 |
| condition | full_skillops_memory_policy | correct_forgetting_rate | 1.000000 | 22/22 |
| condition | full_skillops_memory_policy | conflict_resolution_success_rate | 0.954545 | 21/22 |
| condition | full_skillops_memory_policy | unsupported_memory_claim_rate | 0.000000 | 0/22 |
| condition | no_forgetting_policy | stale_info_usage_rate | 0.000000 | 0/22 |
| condition | no_forgetting_policy | current_instruction_adherence_rate | 1.000000 | 22/22 |
| condition | no_forgetting_policy | correct_forgetting_rate | 0.000000 | 0/22 |
| condition | no_forgetting_policy | conflict_resolution_success_rate | 0.045455 | 1/22 |
| condition | no_forgetting_policy | unsupported_memory_claim_rate | 0.000000 | 0/22 |
| condition | current_context_only | stale_info_usage_rate | 0.000000 | 0/22 |
| condition | current_context_only | current_instruction_adherence_rate | 1.000000 | 22/22 |
| condition | current_context_only | correct_forgetting_rate | 0.000000 | 0/22 |
| condition | current_context_only | conflict_resolution_success_rate | 0.000000 | 0/22 |
| condition | current_context_only | unsupported_memory_claim_rate | 0.000000 | 0/22 |

Raw output: `results\experiments\raw\memory_drift_20260625T063033Z.jsonl`

## Security guard

### deepseek / deepseek-v4-flash

| Dimension | Value | Metric | Rate | Count |
| --- | --- | --- | --- | --- |
| overall | all | detection_rate | 0.916667 | 22/24 |
| overall | all | false_positive_rate | 0.000000 | 0/24 |
| overall | all | specificity | 1.000000 | 24/24 |
| risk_type | identity_confusion | category_recall | 1.000000 | 3/3 |
| risk_type | missing_constraints | category_recall | 0.666667 | 2/3 |
| risk_type | missing_tests | category_recall | 1.000000 | 3/3 |
| risk_type | over_broad_trigger | category_recall | 1.000000 | 3/3 |
| risk_type | privacy_leakage | category_recall | 1.000000 | 3/3 |
| risk_type | prompt_injection | category_recall | 0.666667 | 2/3 |
| risk_type | stale_memory | category_recall | 1.000000 | 3/3 |
| risk_type | unsafe_file_access | category_recall | 1.000000 | 3/3 |
| relevant_artifact | agent-self-audit | coverage | 0.750000 | 3/4 |
| relevant_artifact | lobster-guard | coverage | 1.000000 | 5/5 |
| relevant_artifact | persistent-memory | coverage | 1.000000 | 6/6 |
| relevant_artifact | skill-design-guide | coverage | 1.000000 | 4/4 |
| relevant_artifact | skill-security-guard | coverage | 0.800000 | 4/5 |

Raw output: `results\experiments\raw\security_guard_20260625T051917Z.jsonl`

### kimi / kimi-k2.7-code

| Dimension | Value | Metric | Rate | Count |
| --- | --- | --- | --- | --- |
| overall | all | detection_rate | 0.958333 | 23/24 |
| overall | all | false_positive_rate | 0.000000 | 0/24 |
| overall | all | specificity | 1.000000 | 24/24 |
| risk_type | identity_confusion | category_recall | 1.000000 | 3/3 |
| risk_type | missing_constraints | category_recall | 1.000000 | 3/3 |
| risk_type | missing_tests | category_recall | 1.000000 | 3/3 |
| risk_type | over_broad_trigger | category_recall | 1.000000 | 3/3 |
| risk_type | privacy_leakage | category_recall | 1.000000 | 3/3 |
| risk_type | prompt_injection | category_recall | 0.666667 | 2/3 |
| risk_type | stale_memory | category_recall | 1.000000 | 3/3 |
| risk_type | unsafe_file_access | category_recall | 1.000000 | 3/3 |
| relevant_artifact | agent-self-audit | coverage | 1.000000 | 4/4 |
| relevant_artifact | lobster-guard | coverage | 1.000000 | 5/5 |
| relevant_artifact | persistent-memory | coverage | 1.000000 | 6/6 |
| relevant_artifact | skill-design-guide | coverage | 1.000000 | 4/4 |
| relevant_artifact | skill-security-guard | coverage | 0.800000 | 4/5 |

Raw output: `results\experiments\raw\security_guard_20260625T061851Z.jsonl`

## Trigger routing

### deepseek / deepseek-v4-flash

| Dimension | Value | Metric | Rate | Count |
| --- | --- | --- | --- | --- |
| prompt_variant | skillops | precision | 0.750000 | 15/20 |
| prompt_variant | skillops | recall | 1.000000 | 15/15 |
| prompt_variant | skillops | f1 | 0.857143 | 15/20 |
| prompt_variant | skillops | false_trigger_rate_on_should_not_trigger | 0.000000 | 0/12 |
| prompt_variant | skillops | ambiguity_handling_rate | 0.444444 | 4/9 |
| prompt_variant | freeform | precision | 0.714286 | 15/21 |
| prompt_variant | freeform | recall | 1.000000 | 15/15 |
| prompt_variant | freeform | f1 | 0.833333 | 15/21 |
| prompt_variant | freeform | false_trigger_rate_on_should_not_trigger | 0.000000 | 0/12 |
| prompt_variant | freeform | ambiguity_handling_rate | 0.333333 | 3/9 |

Raw output: `results\experiments\raw\trigger_20260625T051034Z.jsonl`

### kimi / kimi-k2.7-code

| Dimension | Value | Metric | Rate | Count |
| --- | --- | --- | --- | --- |
| prompt_variant | skillops | precision | 0.789474 | 15/19 |
| prompt_variant | skillops | recall | 1.000000 | 15/15 |
| prompt_variant | skillops | f1 | 0.882353 | 15/19 |
| prompt_variant | skillops | false_trigger_rate_on_should_not_trigger | 0.000000 | 0/12 |
| prompt_variant | skillops | ambiguity_handling_rate | 0.444444 | 4/9 |
| prompt_variant | freeform | precision | 0.833333 | 15/18 |
| prompt_variant | freeform | recall | 1.000000 | 15/15 |
| prompt_variant | freeform | f1 | 0.909091 | 15/18 |
| prompt_variant | freeform | false_trigger_rate_on_should_not_trigger | 0.000000 | 0/12 |
| prompt_variant | freeform | ambiguity_handling_rate | 0.666667 | 6/9 |

Raw output: `results\experiments\raw\trigger_20260625T055723Z.jsonl`
