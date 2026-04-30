# Experiment Status

This status snapshot records the local harness preparation and dry-run results
observed in this repository state.

## Experiment States

| Experiment | Prepared | Dry-run | Live run status |
| --- | --- | --- | --- |
| Trigger Routing Accuracy | yes | passed | live run skipped |
| Constraint Compliance Rate | yes | passed | live run skipped |
| Security Guard Detection Rate | yes | passed | live run skipped |
| Memory Drift Detection | yes | passed | live run skipped |
| SkillOps Ablation Study | yes | passed | live run skipped |

## Credential Status

- `OPENAI_API_KEY`: absent
- `ANTHROPIC_API_KEY`: absent
- `LONGCAT_API_KEY`: absent

## Result Files

- `results/experiments/raw/trigger_*.jsonl`: absent
- `results/experiments/trigger_metrics.csv`: absent
- `results/experiments/trigger_metrics.md`: absent
- `results/experiments/raw/constraint_*.jsonl`: absent
- `results/experiments/constraint_metrics.csv`: absent
- `results/experiments/constraint_metrics.md`: absent
- `results/experiments/raw/security_guard_*.jsonl`: absent
- `results/experiments/security_guard_metrics.csv`: absent
- `results/experiments/security_guard_metrics.md`: absent
- `results/experiments/raw/memory_drift_*.jsonl`: absent
- `results/experiments/memory_drift_metrics.csv`: absent
- `results/experiments/memory_drift_metrics.md`: absent
- `results/experiments/raw/ablation_*.jsonl`: absent
- `results/experiments/ablation_metrics.csv`: absent
- `results/experiments/ablation_metrics.md`: absent

## Commands Run

- `python3 scripts/check_experiment_readiness.py`
  Result: prepared
- `python3 scripts/run_empirical_experiments.py --dry-run`
  Result: all five dry-runs passed; live runs skipped

## Limitations

- No live trigger-routing model run was executed.
- No live constraint-compliance model run was executed.
- No live security-guard run was executed.
- No live memory-drift model run was executed.
- No live ablation-study model run was executed.
- No empirical metrics are available until a live run produces result files.
