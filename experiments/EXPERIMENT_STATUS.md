# Experiment Status

This status snapshot records the harness preparation, dry-run validation,
local security-guard live run, and reported provider-backed runs observed in
this repository state.

## Experiment States

| Experiment | Prepared | Dry-run | Live run status |
| --- | --- | --- | --- |
| Trigger Routing | yes | passed | DeepSeek and Kimi model-backed runs reported |
| Constraint Compliance | yes | passed | DeepSeek and Kimi model-backed runs reported |
| Security Guard | yes | passed | local-rules run plus DeepSeek and Kimi model-backed runs reported |
| Memory Drift | yes | passed | DeepSeek and Kimi model-backed runs reported |
| SkillOps Ablation | yes | passed | live ablation prepared but not reported |

## Credential Status

- Provider credentials are not stored in repository files or release artifacts.
- Credential availability is recorded only as boolean readiness in provider
  readiness outputs.

## Reported Result Files

- `results/experiments/raw/security_guard_20260625T025048Z.jsonl`: present
- `results/experiments/live_model_summary.csv`: present
- `results/experiments/live_model_summary.md`: present
- `results/experiments/external_result_summary.csv`: present
- `results/experiments/external_result_summary.md`: present
- `results/experiments/security_guard_metrics.csv`: present
- `results/experiments/security_guard_metrics.md`: present

## Commands Run

- `python scripts/check_experiment_readiness.py`
  Result: prepared
- `python scripts/run_empirical_experiments.py --dry-run`
  Result: all five dry-runs passed; live ablation not reported
- `python scripts/run_security_guard_experiment.py --run-live --guard local-rules`
  Result: local security-guard live run completed
- `python scripts/run_trigger_experiment.py --run-live --provider deepseek --model deepseek-v4-flash`
  Result: model-backed trigger run completed
- `python scripts/run_constraint_experiment.py --run-live --provider deepseek --model deepseek-v4-flash`
  Result: model-backed constraint run completed
- `python scripts/run_security_guard_experiment.py --run-live --guard model --provider deepseek --model deepseek-v4-flash`
  Result: model-backed guard run completed
- `python scripts/run_memory_drift_experiment.py --run-live --provider deepseek --model deepseek-v4-flash`
  Result: model-backed memory run completed
- `python scripts/run_trigger_experiment.py --run-live --provider kimi --model kimi-k2.7-code`
  Result: model-backed trigger run completed
- `python scripts/run_constraint_experiment.py --run-live --provider kimi --model kimi-k2.7-code`
  Result: model-backed constraint run completed
- `python scripts/run_security_guard_experiment.py --run-live --guard model --provider kimi --model kimi-k2.7-code`
  Result: model-backed guard run completed
- `python scripts/run_memory_drift_experiment.py --run-live --provider kimi --model kimi-k2.7-code`
  Result: model-backed memory run completed
- `python scripts/run_tests.py`
  Result: repository-level checks passed

## Limitations

- Model-backed trigger, constraint, security-guard, and memory runs are
  reported for DeepSeek and Kimi as single-run benchmark evidence.
- No model-backed ablation-study run is reported in this repository state.
- The reported live pilot is a deterministic local-rule guard over manually
  constructed risk and benign-control cases.
- The bounded external smoke is not a powered external evaluation.
