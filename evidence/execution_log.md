# Executable Evidence Log

- Task: SkillOps evidence refresh
- Audit date: 2026-06-25
- Working directory: local project workspace
- Branch: local working copy

## Commands Actually Run

Status `passed` unless noted otherwise.

1. `git status --short --branch`
2. `rg --files`
3. `python --version`
4. `python scripts/run_tests.py`
5. `python scripts/check_experiment_readiness.py`
6. `python scripts/run_empirical_experiments.py --dry-run`
7. `python scripts/run_security_guard_experiment.py --run-live --guard local-rules`

## Outputs Generated

- `results/experiments/security_guard_metrics.csv`
- `results/experiments/security_guard_metrics.md`
- `results/experiments/raw/security_guard_20260625T025048Z.jsonl`

## Counts Verified

- `benchmark/skill_samples.csv`: `5` rows
- `benchmark/trigger_cases.csv`: `36` total cases
- `benchmark/trigger_cases.csv`: `15` `should_trigger`
- `benchmark/trigger_cases.csv`: `12` `should_not_trigger`
- `benchmark/trigger_cases.csv`: `9` `ambiguous`
- `benchmark/risk_cases.csv`: `24` total cases
- `benchmark/risk_cases.csv`: `8` risk categories
- `experiments/security_benign_cases.csv`: `24` benign controls

## Local Security-Guard Pilot

- Command: `python scripts/run_security_guard_experiment.py --run-live --guard local-rules`
- Status: passed
- Risk detection rate: `24/24`
- Benign false-positive rate: `1/24`
- Benign specificity: `23/24`

## Limitations

- Model-backed live runs were not reported in this repository state.
- External source repositories were not executed against the benchmark cases.
- The local security-guard pilot uses deterministic rules over manually
  constructed cases and controls.
