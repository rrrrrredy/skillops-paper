# Research Log: Memory Drift Detection and SkillOps Ablation Experiments

**Date:** 2026-04-28
**Author:** Song Luo
**Status:** Harness prepared; dry-run validated; live runs not yet executed

## Summary

Added two new experiment harnesses to the SkillOps paper evaluation suite:

1. **Memory Drift Detection (Experiment 4)** — Tests whether SkillOps memory
   retirement markers and conflict resolution rules prevent an agent from using
   stale information.

2. **SkillOps Ablation Study (Experiment 5)** — Systematically removes
   individual SkillOps components (trigger boundary, execution constraints,
   security checks, memory interface) to measure their marginal contribution
   across all three evaluation dimensions (trigger routing, constraint
   compliance, memory drift).

## Design Decisions

### Memory Drift Detection

- **22 manually constructed cases** covering real-world drift scenarios:
  API migrations, team rotations, policy changes, tooling migrations, version
  pinning, credential rotations, etc.
- **Three experimental conditions:**
  - `full_skillops_memory_policy`: complete policy with retirement markers and
    conflict resolution
  - `no_forgetting_policy`: stale memory present without markers or resolution
    rules
  - `current_context_only`: baseline with only current valid context
- **Metrics:** stale_info_usage_rate, current_instruction_adherence_rate,
  correct_forgetting_rate, conflict_resolution_success_rate,
  unsupported_memory_claim_rate

### SkillOps Ablation Study

- **Six ablation variants:**
  - `full_skillops` (all components present)
  - `no_trigger_boundary` (remove activation boundaries)
  - `no_execution_constraints` (remove testable constraints)
  - `no_security_checks` (remove security validation)
  - `no_memory_interface` (remove memory/forgetting interface)
  - `freeform_only` (minimal natural-language description only)
- **Tested across:** trigger_cases.csv (36 cases), risk_cases.csv (24 cases),
  memory_drift_cases.csv (22 cases)
- **Total ablation evaluations per live run:** 6 variants × (36 + 24 + 22)
  cases = 492 model calls

## Files Created

- `experiments/memory_drift_cases.csv` (22 cases)
- `experiments/prompts/memory_drift_full_skillops.md`
- `experiments/prompts/memory_drift_no_forgetting.md`
- `experiments/prompts/memory_drift_current_only.md`
- `experiments/schemas/memory_drift_result_schema.json`
- `experiments/schemas/ablation_result_schema.json`
- `experiments/ablation/variants/full_skillops.md`
- `experiments/ablation/variants/no_trigger_boundary.md`
- `experiments/ablation/variants/no_execution_constraints.md`
- `experiments/ablation/variants/no_security_checks.md`
- `experiments/ablation/variants/no_memory_interface.md`
- `experiments/ablation/variants/freeform_only.md`
- `scripts/run_memory_drift_experiment.py`
- `scripts/run_ablation_experiment.py`

## Files Updated

- `scripts/check_experiment_readiness.py` (added new paths)
- `scripts/run_empirical_experiments.py` (added new experiments)
- `experiments/EXPERIMENT_STATUS.md` (added new rows)
- `experiments/README.md` (documented all 5 experiments)
- `README.md` (updated experiment count)

## Validation

- `python3 scripts/check_experiment_readiness.py` → prepared
- `python3 scripts/run_empirical_experiments.py --dry-run` → all 5 passed
- `python3 scripts/run_all.py` → passed
- `python3 scripts/run_tests.py` → passed

## Limitations

- Memory drift metrics rely on model self-report (the JSON response includes
  `used_stale_info` as reported by the model itself). External ground-truth
  verification would require human annotation.
- Ablation results depend on the specific skill definition used as the base
  case (a translation skill). Different base skills may show different
  component contributions.
- No live runs were executed due to absent API credentials.

## Next Steps

1. Execute live runs with at least two model providers to establish baselines
2. Add human annotation sampling for memory drift ground-truth validation
3. Consider additional ablation variants (e.g., no_failure_modes, no_tests)
4. Integrate results into paper Section 5 (Evaluation)
