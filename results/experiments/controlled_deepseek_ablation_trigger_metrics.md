# Controlled DeepSeek Aligned Ablation Trigger Metrics

- Provider: `deepseek`
- Model: `deepseek-chat`
- Repeats: `3`
- Raw output: `results\experiments\raw\controlled_deepseek_ablation_trigger_20260506T030834Z.jsonl`
- Status: `complete`

## variant

| variant | Metric | Mean | Std | R1 | R2 | R3 | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| freeform_only | ambiguity_handling_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |
| freeform_only | f1 | 0.7500 | 0.0000 | 0.7500 | 0.7500 | 0.7500 |  |
| freeform_only | false_trigger_rate | 0.1667 | 0.0000 | 0.1667 | 0.1667 | 0.1667 |  |
| freeform_only | precision | 0.6000 | 0.0000 | 0.6000 | 0.6000 | 0.6000 |  |
| freeform_only | recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| freeform_only | skill_routing_accuracy | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| full_skillops | ambiguity_handling_rate | 0.2222 | 0.0000 | 0.2222 | 0.2222 | 0.2222 |  |
| full_skillops | f1 | 0.7501 | 0.0094 | 0.7568 | 0.7368 | 0.7568 |  |
| full_skillops | false_trigger_rate | 0.1111 | 0.0393 | 0.0833 | 0.1667 | 0.0833 |  |
| full_skillops | precision | 0.6271 | 0.0130 | 0.6364 | 0.6087 | 0.6364 |  |
| full_skillops | recall | 0.9333 | 0.0000 | 0.9333 | 0.9333 | 0.9333 |  |
| full_skillops | skill_routing_accuracy | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| no_execution_constraints | ambiguity_handling_rate | 0.0741 | 0.1048 | 0.0000 | 0.2222 | 0.0000 |  |
| no_execution_constraints | f1 | 0.7123 | 0.0174 | 0.7000 | 0.7368 | 0.7000 |  |
| no_execution_constraints | false_trigger_rate | 0.1667 | 0.0000 | 0.1667 | 0.1667 | 0.1667 |  |
| no_execution_constraints | precision | 0.5762 | 0.0230 | 0.5600 | 0.6087 | 0.5600 |  |
| no_execution_constraints | recall | 0.9333 | 0.0000 | 0.9333 | 0.9333 | 0.9333 |  |
| no_execution_constraints | skill_routing_accuracy | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| no_memory_interface | ambiguity_handling_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |
| no_memory_interface | f1 | 0.7000 | 0.0000 | 0.7000 | 0.7000 | 0.7000 |  |
| no_memory_interface | false_trigger_rate | 0.1667 | 0.0000 | 0.1667 | 0.1667 | 0.1667 |  |
| no_memory_interface | precision | 0.5600 | 0.0000 | 0.5600 | 0.5600 | 0.5600 |  |
| no_memory_interface | recall | 0.9333 | 0.0000 | 0.9333 | 0.9333 | 0.9333 |  |
| no_memory_interface | skill_routing_accuracy | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| no_security_checks | ambiguity_handling_rate | 0.1481 | 0.0524 | 0.1111 | 0.2222 | 0.1111 |  |
| no_security_checks | f1 | 0.7242 | 0.0089 | 0.7179 | 0.7368 | 0.7179 |  |
| no_security_checks | false_trigger_rate | 0.1667 | 0.0000 | 0.1667 | 0.1667 | 0.1667 |  |
| no_security_checks | precision | 0.5918 | 0.0120 | 0.5833 | 0.6087 | 0.5833 |  |
| no_security_checks | recall | 0.9333 | 0.0000 | 0.9333 | 0.9333 | 0.9333 |  |
| no_security_checks | skill_routing_accuracy | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| no_trigger_boundary | ambiguity_handling_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |
| no_trigger_boundary | f1 | 0.7317 | 0.0000 | 0.7317 | 0.7317 | 0.7317 |  |
| no_trigger_boundary | false_trigger_rate | 0.2500 | 0.0000 | 0.2500 | 0.2500 | 0.2500 |  |
| no_trigger_boundary | precision | 0.5769 | 0.0000 | 0.5769 | 0.5769 | 0.5769 |  |
| no_trigger_boundary | recall | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |  |
| no_trigger_boundary | skill_routing_accuracy | 0.9333 | 0.0000 | 0.9333 | 0.9333 | 0.9333 |  |
