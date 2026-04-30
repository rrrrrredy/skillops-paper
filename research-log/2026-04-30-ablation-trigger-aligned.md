# Aligned Ablation Trigger-Routing Run Log

Date: 2026-04-30T09:24:24Z
Provider: deepseek
Model: deepseek-chat
Repeats: 1
Total records: 216
Elapsed: 627.1s
Scope: single-run pilot; descriptive only; no statistical significance or broad empirical validation.

## Results Summary

| Variant | Precision | Recall | F1 | Skill Routing Acc |
| --- | --- | --- | --- | --- |
| full_skillops | 0.6667 | 0.9333 | 0.7778 | 1.0000 |
| no_trigger_boundary | 0.5769 | 1.0000 | 0.7317 | 0.9333 |
| freeform_only | 0.6000 | 1.0000 | 0.7500 | 1.0000 |
| no_execution_constraints | 0.5833 | 0.9333 | 0.7179 | 1.0000 |
| no_security_checks | 0.6087 | 0.9333 | 0.7368 | 1.0000 |
| no_memory_interface | 0.6087 | 0.9333 | 0.7368 | 1.0000 |

## Errors

Parse failures: 0
Execution failures: 0

## Files Generated

- Raw: `results/experiments/raw/ablation_trigger_aligned_20260430T092424Z.jsonl`
- Metrics CSV: `results/experiments/ablation_trigger_aligned_metrics.csv`
- Metrics MD: `results/experiments/ablation_trigger_aligned_metrics.md`
- Research log: `research-log/2026-04-30-ablation-trigger-aligned.md`
