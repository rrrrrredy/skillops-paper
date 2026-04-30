# Empirical Experiment Harness

- Repository: `D:\Codex\skillops-paper-artifact-benchmark`
- Branch: `empirical-experiment-harness`
- Git identity: `Song Luo <luosongred@gmail.com>`
- Python interpreter used for commands:
  `C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe`

## Files Created

- `experiments/README.md`
- `experiments/EXPERIMENT_STATUS.md`
- `experiments/prompts/trigger_routing_skillops.md`
- `experiments/prompts/trigger_routing_freeform.md`
- `experiments/prompts/constraint_skillops.md`
- `experiments/prompts/constraint_vague.md`
- `experiments/prompts/security_guard_detection.md`
- `experiments/schemas/trigger_result_schema.json`
- `experiments/schemas/constraint_result_schema.json`
- `experiments/schemas/security_guard_result_schema.json`
- `results/experiments/.gitkeep`
- `results/experiments/raw/.gitkeep`
- `scripts/experiment_utils.py`
- `scripts/check_experiment_readiness.py`
- `scripts/run_trigger_experiment.py`
- `scripts/run_constraint_experiment.py`
- `scripts/run_security_guard_experiment.py`
- `scripts/run_empirical_experiments.py`

## Files Updated

- `README.md`

## Readiness Result

Command:

`C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe scripts\check_experiment_readiness.py`

Observed result:

- readiness: prepared
- inputs: present
- prompts: present
- schemas: present
- result directories: present

Credential status:

- `OPENAI_API_KEY`: absent
- `ANTHROPIC_API_KEY`: absent
- `LONGCAT_API_KEY`: absent

## Dry-Run Result

Command:

`C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe scripts\run_empirical_experiments.py --dry-run`

Observed result:

- Trigger Routing Accuracy: prepared
- Trigger Routing Accuracy: dry-run passed
- Trigger Routing Accuracy: live run skipped
- Constraint Compliance Rate: prepared
- Constraint Compliance Rate: dry-run passed
- Constraint Compliance Rate: live run skipped
- Security Guard Detection Rate: prepared
- Security Guard Detection Rate: dry-run passed
- Security Guard Detection Rate: live run skipped

## Repository Checks

Commands:

- `C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe scripts\run_all.py`
- `C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe scripts\run_tests.py`

Observed result:

- reproducibility pipeline: passed
- repository tests discovered: 22
- repository tests passed: 22
- repository tests failed: 0
- repository tests errors: 0
- repository tests skipped: 0

## Live Execution Status

- Trigger routing live run: not run
- Constraint compliance live run: not run
- Security guard live run: not run
- Metrics files generated: no

## Limitations

- No provider credentials were available in this shell environment.
- No paid or live model execution was attempted.
- No empirical metrics were produced in this repository state.
