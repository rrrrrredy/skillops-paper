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
8. `python scripts/run_trigger_experiment.py --run-live --provider deepseek --model deepseek-v4-flash`
9. `python scripts/run_constraint_experiment.py --run-live --provider deepseek --model deepseek-v4-flash`
10. `python scripts/run_security_guard_experiment.py --run-live --guard model --provider deepseek --model deepseek-v4-flash`
11. `python scripts/run_memory_drift_experiment.py --run-live --provider deepseek --model deepseek-v4-flash`
12. `python scripts/run_trigger_experiment.py --run-live --provider kimi --model kimi-k2.7-code`
13. `python scripts/run_constraint_experiment.py --run-live --provider kimi --model kimi-k2.7-code`
14. `python scripts/run_security_guard_experiment.py --run-live --guard model --provider kimi --model kimi-k2.7-code`
15. `python scripts/run_memory_drift_experiment.py --run-live --provider kimi --model kimi-k2.7-code`
16. `python scripts/sanitize_raw_results.py`
17. `python scripts/summarize_live_model_results.py`
18. `python scripts/analyze_external_corpus.py`
19. `python scripts/generate_external_case_plan.py`
20. `python scripts/select_external_artifacts.py`
21. `python scripts/build_external_sampling_manifest.py`
22. `python scripts/generate_external_annotation_packet.py`
23. `python scripts/run_external_condition_dry_run.py --shards 12`
24. `python scripts/build_external_representations.py`
25. `python scripts/run_external_payload_experiment.py --dry-run`
26. `python scripts/prepare_external_smoke_test_plan.py`
27. `python scripts/run_external_payload_experiment.py --run-live --provider deepseek --model deepseek-v4-flash --sample-limit 12 --max-live-rows 12`
28. `python scripts/run_external_payload_experiment.py --run-live --provider kimi --model kimi-k2.7-code --sample-limit 4 --max-live-rows 4`
29. `python scripts/summarize_external_results.py`
30. `python scripts/run_external_statistical_analysis.py`
31. `python scripts/prepare_external_pilot_plan.py`
32. `python scripts/run_external_pilot_experiment.py --dry-run`
33. `python scripts/generate_external_pilot_annotation_calibration.py`
34. `tectonic -o release paper/main.tex`
35. `python scripts/package_release.py`

## Outputs Generated

- `results/experiments/security_guard_metrics.csv`
- `results/experiments/security_guard_metrics.md`
- `results/experiments/raw/security_guard_20260625T070833Z.jsonl`
- `results/experiments/raw/trigger_20260625T051034Z.jsonl`
- `results/experiments/raw/constraint_20260625T051633Z.jsonl`
- `results/experiments/raw/security_guard_20260625T051917Z.jsonl`
- `results/experiments/raw/memory_drift_20260625T054747Z.jsonl`
- `results/experiments/raw/trigger_20260625T055723Z.jsonl`
- `results/experiments/raw/constraint_20260625T060926Z.jsonl`
- `results/experiments/raw/security_guard_20260625T061851Z.jsonl`
- `results/experiments/raw/memory_drift_20260625T063033Z.jsonl`
- `results/experiments/live_model_summary.csv`
- `results/experiments/live_model_summary.md`
- `results/tables/external_corpus_static_analysis.csv`
- `results/tables/external_corpus_summary.csv`
- `results/tables/external_corpus_summary.md`
- `results/tables/external_case_allocation.csv`
- `results/tables/external_case_plan.csv`
- `results/tables/external_condition_plan.csv`
- `results/tables/external_case_plan.md`
- `results/tables/external_artifact_selection.csv`
- `results/tables/external_artifact_selection_summary.csv`
- `results/tables/external_artifact_selection.md`
- `results/tables/external_sampling_manifest.csv`
- `results/tables/external_sampling_manifest.md`
- `results/tables/external_eligibility_manifest.csv`
- `results/tables/external_replacement_manifest.csv`
- `results/tables/external_case_construction.csv`
- `results/tables/external_annotation_packet.csv`
- `results/tables/external_condition_packet.csv`
- `results/tables/external_annotation_packet.md`
- `results/experiments/external_condition_manifest.csv`
- `results/experiments/external_condition_shards.csv`
- `results/experiments/external_statistical_analysis_plan.csv`
- `results/experiments/external_condition_dry_run.md`
- `results/experiments/external_statistical_analysis_plan.md`
- `results/experiments/external_representation_payloads.jsonl`
- `results/experiments/external_representation_payload_index.csv`
- `results/experiments/external_representation_payloads.md`
- `results/experiments/external_payload_run_plan.csv`
- `results/experiments/external_payload_run_plan.md`
- `results/experiments/external_pilot_artifacts.csv`
- `results/experiments/external_pilot_condition_plan.csv`
- `results/experiments/external_pilot_model_plan.csv`
- `results/experiments/external_pilot_plan.md`
- `results/experiments/external_pilot_run_plan.csv`
- `results/experiments/external_pilot_run_plan.md`
- `results/experiments/external_pilot_provider_readiness.csv`
- `results/experiments/external_pilot_provider_readiness.md`
- `results/tables/external_pilot_annotation_worklist.csv`
- `results/tables/external_pilot_annotation_calibration.csv`
- `results/tables/external_pilot_annotation_calibration.md`
- `results/experiments/external_smoke_test_plan.csv`
- `results/experiments/external_smoke_test_plan.md`
- `results/experiments/raw/external_condition_20260625T084916Z.jsonl`
- `results/experiments/raw/external_condition_20260625T085750Z.jsonl`
- `results/experiments/external_result_summary.csv`
- `results/experiments/external_result_summary.md`
- `results/experiments/external_statistical_summary.csv`
- `results/experiments/external_statistical_summary.md`
- `results/experiments/external_primary_effects.csv`
- `results/experiments/external_f1_bootstrap.csv`
- `results/experiments/external_mcnemar.csv`
- `results/experiments/external_annotation_reliability.csv`
- `results/experiments/external_exclusions.csv`
- `results/experiments/external_statistical_analysis.md`
- `release/skillops-paper.pdf`
- `release/skillops-paper-source.zip`

## Counts Verified

- `benchmark/skill_samples.csv`: `5` rows
- `benchmark/trigger_cases.csv`: `36` total cases
- `benchmark/trigger_cases.csv`: `15` `should_trigger`
- `benchmark/trigger_cases.csv`: `12` `should_not_trigger`
- `benchmark/trigger_cases.csv`: `9` `ambiguous`
- `benchmark/risk_cases.csv`: `24` total cases
- `benchmark/risk_cases.csv`: `8` risk categories
- `experiments/security_benign_cases.csv`: `24` benign controls
- `results/tables/external_case_allocation.csv`: `240` target artifacts
- `results/tables/external_case_plan.csv`: `960` target base cases
- `results/tables/external_condition_plan.csv`: `2880` target condition-level
  evaluations
- `results/tables/external_artifact_selection.csv`: `240` metadata-only
  candidate artifact rows
- `results/tables/external_sampling_manifest.csv`: `240` seeded sampling rows
- `results/tables/external_sampling_manifest.csv`: `100` rows exceeding current
  source/owner cap targets and requiring replacement or corpus expansion
- `results/tables/external_eligibility_manifest.csv`: `240` pending eligibility
  review rows
- `results/tables/external_replacement_manifest.csv`: `100` pending replacement
  or corpus-expansion rows
- `results/tables/external_case_construction.csv`: `960` planned base cases
- `results/tables/external_annotation_packet.csv`: `960` pending review rows
- `results/tables/external_condition_packet.csv`: `2880` pending condition rows
- `results/experiments/external_condition_manifest.csv`: `2880` not-run
  manifest rows
- `results/experiments/external_condition_shards.csv`: `12` shards with `240`
  rows each
- `results/experiments/external_statistical_analysis_plan.csv`: `6` planned
  metrics
- `results/experiments/external_representation_payloads.jsonl`: `2880`
  metadata-only payload templates
- `results/experiments/external_payload_run_plan.csv`: `2880` not-run plan rows
- `results/experiments/external_pilot_artifacts.csv`: `24` selected
  within-cap pilot artifacts
- `results/experiments/external_pilot_condition_plan.csv`: `288` selected
  pilot condition rows
- `results/experiments/external_pilot_model_plan.csv`: `576`
  provider-condition rows
- `results/experiments/external_pilot_run_plan.csv`: `576` not-run pilot
  provider-condition rows
- `results/experiments/external_pilot_provider_readiness.csv`: `2` provider
  readiness rows
- `results/tables/external_pilot_annotation_worklist.csv`: `96` pending
  pilot annotation cases
- `results/tables/external_pilot_annotation_calibration.csv`: `32` balanced
  calibration cases
- `results/experiments/external_smoke_test_plan.csv`: `4` no-secret smoke-plan
  rows
- `results/experiments/external_result_summary.csv`: `16` bounded external
  live-smoke records
- `results/experiments/external_primary_effects.csv`: descriptive paired
  contrasts only

## Local Security-Guard Pilot

- Command: `python scripts/run_security_guard_experiment.py --run-live --guard local-rules`
- Status: passed
- Risk detection rate: `24/24`
- Benign false-positive rate: `1/24`
- Benign specificity: `23/24`

## Live Model Runs

- DeepSeek model: `deepseek-v4-flash`
- Kimi model: `kimi-k2.7-code`
- Core protocols: trigger routing, constraint compliance, model-backed security
  guard, and memory drift
- DeepSeek trigger F1: SkillOps `0.857143`, freeform `0.833333`
- Kimi trigger F1: SkillOps `0.882353`, freeform `0.909091`
- DeepSeek model-backed security detection: `22/24`, false positives `0/24`
- Kimi model-backed security detection: `23/24`, false positives `0/24`
- Full memory policy conflict resolution: `21/22` for both models

## External Corpus Static Analysis

- Source frame: `11` third-party sources
- GitHub file-tree analysis: `10` successfully analyzed sources
- README indicators: `10/10`
- License-file indicators: `10/10`
- Test-file indicators: `9/10`
- Script/code indicators: `9/10`
- Security-related indicators: `7/10`
- `SKILL.md` indicators: `4/10`

## External Case-Plan Scaffold

- Command: `python scripts/generate_external_case_plan.py`
- Status: passed
- Target artifacts: `240`
- Base cases: `960`
- Condition-level evaluations: `2880`
- Supporting files:
  - `experiments/schemas/external_case_schema.json`
  - `experiments/external_case_seed.csv`
  - `docs/annotation_guide.md`
  - `docs/preregistration_template.md`

## External Artifact-Selection Scaffold

- Command: `python scripts/select_external_artifacts.py`
- Status: passed
- Candidate artifact rows: `240`
- Base cases implied by candidate rows: `960`
- Condition-level evaluations implied by candidate rows: `2880`
- Selection bases:
  - `skill_package_directory`: `49`
  - `index_upstream_link`: `20`
  - `manifest_directory`: `24`
  - `readme_directory`: `16`
  - `relevant_tree_path`: `128`
  - `textlike_tree_path`: `3`

## External Sampling Manifest

- Command: `python scripts/build_external_sampling_manifest.py`
- Status: passed
- Candidate artifact rows: `240`
- Seed: `20260625`
- Rows exceeding current source/owner cap targets: `100`
- Evidence boundary: sampling-frame and cap-pressure diagnostics only.

## External Annotation Packet

- Command: `python scripts/generate_external_annotation_packet.py`
- Status: passed
- Candidate artifacts: `240`
- Pending eligibility rows: `240`
- Pending replacement or corpus-expansion rows: `100`
- Planned base cases: `960`
- Pending review rows: `960`
- Pending condition rows: `2880`
- Case-type balance:
  - `positive_trigger`: `240`
  - `negative_trigger`: `240`
  - `boundary_clarification`: `240`
  - `risk_constraint`: `240`

## External Condition Dry Run

- Command: `python scripts/run_external_condition_dry_run.py --shards 12`
- Status: passed
- Manifest rows: `2880`
- Shards: `12`
- Rows per shard: `240`
- Planned metrics: `6`
- Execution status: `not_run`

## External Representation Payloads

- Command: `python scripts/build_external_representations.py`
- Status: passed
- Payload rows: `2880`
- Conditions:
  - `original_freeform`: `960`
  - `skillops_normalized`: `960`
  - `skillops_ablation`: `960`
- Content boundary: metadata-only; no third-party prose or code copied

## External Payload Runner Dry Run

- Command: `python scripts/run_external_payload_experiment.py --dry-run`
- Status: passed
- Selected payload rows: `2880`
- Run status: `not_run`
- Live execution: not run

## External Pilot Execution Plan

- Command: `python scripts/prepare_external_pilot_plan.py`
- Status: passed
- Selected pilot artifacts: `24`
- Base cases: `96`
- Condition rows per provider/model: `288`
- Provider-condition rows:
  - `deepseek` / `deepseek-v4-flash`: `288`
  - `kimi` / `kimi-k2.7-code`: `288`
- Family balance:
  - `agent_skills`: `6`
  - `agent_workflow_templates`: `6`
  - `mcp_and_tool_recipes`: `6`
  - `prompt_and_function_recipes`: `6`
- Evidence boundary: pilot logistics and annotation-readiness plan only.

## External Pilot Runner Dry Run

- Command: `python scripts/run_external_pilot_experiment.py --dry-run`
- Status: passed
- Pilot provider-condition rows: `576`
- Provider/model pairs:
  - `deepseek` / `deepseek-v4-flash`: `288`
  - `kimi` / `kimi-k2.7-code`: `288`
- Run status: `not_run`
- Provider readiness rows: `2`
- Environment availability in this run:
  - `DEEPSEEK_API_KEY`: `false`
  - `MOONSHOT_API_KEY`: `false`
- Evidence boundary: bounded runner and readiness evidence only.

## External Pilot Annotation Calibration

- Command: `python scripts/generate_external_pilot_annotation_calibration.py`
- Status: passed
- Pilot annotation worklist cases: `96`
- Calibration cases: `32`
- Calibration artifacts: `8`
- Calibration family balance:
  - `agent_skills`: `8`
  - `agent_workflow_templates`: `8`
  - `mcp_and_tool_recipes`: `8`
  - `prompt_and_function_recipes`: `8`
- Evidence boundary: pending review plan only.

## External Smoke-Test Plan

- Command: `python scripts/prepare_external_smoke_test_plan.py`
- Status: passed; bounded provider execution completed separately
- Provider/model pairs:
  - `deepseek` / `deepseek-v4-flash`
  - `kimi` / `kimi-k2.7-code`
- Selected payload rows: `4`
- Environment availability in this run:
  - `DEEPSEEK_API_KEY`: `true`
  - `MOONSHOT_API_KEY`: `true`

## External Bounded Live Smoke

- Command: `python scripts/run_external_payload_experiment.py --run-live --provider deepseek --model deepseek-v4-flash --sample-limit 12 --max-live-rows 12`
- Status: passed
- Output: `results/experiments/raw/external_condition_20260625T084916Z.jsonl`
- Records: `12`
- Command: `python scripts/run_external_payload_experiment.py --run-live --provider kimi --model kimi-k2.7-code --sample-limit 4 --max-live-rows 4`
- Status: passed
- Output: `results/experiments/raw/external_condition_20260625T085750Z.jsonl`
- Records: `4`

## External Result Summary

- Command: `python scripts/summarize_external_results.py`
- Status: passed; bounded external live-smoke records summarized
- External live-result records: `16`
- Parse success: `16/16`
- Expected-behavior match: `5/16`
- Statistical result status: `requires_statistical_model_run`

## External Statistical Diagnostics

- Command: `python scripts/run_external_statistical_analysis.py`
- Status: passed
- Outputs:
  - `results/experiments/external_primary_effects.csv`
  - `results/experiments/external_f1_bootstrap.csv`
  - `results/experiments/external_mcnemar.csv`
  - `results/experiments/external_annotation_reliability.csv`
  - `results/experiments/external_exclusions.csv`
  - `results/experiments/external_statistical_analysis.md`
- Evidence boundary: descriptive diagnostics over bounded smoke records only.

## Limitations

- External source repositories were not executed against the benchmark cases.
- The local security-guard pilot uses deterministic rules over manually
  constructed cases and controls.
- Live model-backed runs are single-run metrics over a manually constructed
  benchmark, not statistical evidence or broad model ranking.
- External case-plan files define a study protocol, not measured external
  outcomes.
- External artifact-selection files are metadata-only candidate references for
  case construction, not validated artifacts.
- External sampling manifest files expose source/owner cap pressure, but do not
  complete replacement, eligibility review, or corpus balancing.
- External case-construction packet files define pending eligibility,
  replacement, artifact-specific request construction, case-label rows, and
  not-run condition rows, not measured outcomes.
- External dry-run files validate execution readiness but do not include model
  outputs or statistical outcomes.
- External representation payloads are not-run templates and do not include
  third-party source content.
- External payload runner dry-run output is a run plan; the separate bounded
  live smoke covers only 16 condition rows.
- External pilot execution plan output selects a bounded 24-artifact subset,
  but does not complete powered external model execution.
- External pilot runner output is dry-run/readiness evidence; the current
  process did not contain provider credentials for a pilot live slice.
- External pilot case-label calibration output is a worklist and calibration
  subset for label-sensitivity checks, not model outcome evidence.
- External smoke-test outputs are normalized provider records, not a powered
  external evaluation.
- External result summaries record bounded smoke metrics, not measured
  statistical effects.
- External statistical diagnostic files are not powered inferential analyses.
