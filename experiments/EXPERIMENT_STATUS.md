# Experiment Status

This status snapshot records the local harness preparation, dry-run validation,
and local security-guard live run observed in this repository state.

## Experiment States

| Experiment | Prepared | Dry-run | Live run status |
| --- | --- | --- | --- |
| Trigger Routing | yes | passed | model-backed live run not reported |
| Constraint Compliance | yes | passed | model-backed live run not reported |
| Security Guard | yes | passed | local-rules live run completed |
| Memory Drift | yes | passed | model-backed live run not reported |
| SkillOps Ablation | yes | passed | model-backed live run not reported |

## Credential Status

- Model-provider credentials: absent in the local environment used for this
  update.

## Reported Result Files

- `results/experiments/raw/security_guard_20260625T025048Z.jsonl`: present
- `results/experiments/security_guard_metrics.csv`: present
- `results/experiments/security_guard_metrics.md`: present

## Commands Run

- `python scripts/check_experiment_readiness.py`
  Result: prepared
- `python scripts/run_empirical_experiments.py --dry-run`
  Result: all five dry-runs passed; model-backed live runs skipped
- `python scripts/run_security_guard_experiment.py --run-live --guard local-rules`
  Result: local security-guard live run completed
- `python scripts/run_tests.py`
  Result: repository-level checks passed

## Limitations

- No model-backed trigger-routing run is reported in this repository state.
- No model-backed constraint-compliance run is reported in this repository state.
- No model-backed security-guard run is reported in this repository state.
- No model-backed memory-drift run is reported in this repository state.
- No model-backed ablation-study run is reported in this repository state.
- The reported live pilot is a deterministic local-rule guard over manually
  constructed risk and benign-control cases.
