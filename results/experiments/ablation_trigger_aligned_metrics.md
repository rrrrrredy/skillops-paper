# Aligned Ablation Trigger-Routing Metrics

- Provider: `deepseek`
- Model: `deepseek-chat`
- Raw output: `results/experiments/raw/ablation_trigger_aligned_20260430T092424Z.jsonl`
- Experiment: `ablation_trigger_aligned`
- Scope: single-run pilot on 36 trigger cases per variant; descriptive only; no statistical significance or broad empirical validation.

| Variant | Precision | Recall | F1 | False Trigger Rate | Ambiguity Handling | Skill Routing Acc | Cases | Parse Fail | Exec Fail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full_skillops | 0.6667 | 0.9333 | 0.7778 | 0.0833 | 0.3333 | 1.0000 | 36 | 0 | 0 |
| no_trigger_boundary | 0.5769 | 1.0000 | 0.7317 | 0.2500 | 0.0000 | 0.9333 | 36 | 0 | 0 |
| freeform_only | 0.6000 | 1.0000 | 0.7500 | 0.1667 | 0.0000 | 1.0000 | 36 | 0 | 0 |
| no_execution_constraints | 0.5833 | 0.9333 | 0.7179 | 0.1667 | 0.1111 | 1.0000 | 36 | 0 | 0 |
| no_security_checks | 0.6087 | 0.9333 | 0.7368 | 0.1667 | 0.2222 | 1.0000 | 36 | 0 | 0 |
| no_memory_interface | 0.6087 | 0.9333 | 0.7368 | 0.1667 | 0.2222 | 1.0000 | 36 | 0 | 0 |
