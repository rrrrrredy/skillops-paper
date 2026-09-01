# SkillOps Paper and Artifacts

[![DOI](https://zenodo.org/badge/1222288144.svg)](https://doi.org/10.5281/zenodo.20061198)

This repository contains the paper and supporting artifacts for:

**SkillOps: A Practical Framework for Designing, Testing, and Operating Modular Skills in Personal AI Agents**

Author: Song Luo
Contact: luosongred@gmail.com

## Paper and release

- Paper source: [paper/main.tex](paper/main.tex)
- Compiled PDF: [release/skillops-paper.pdf](release/skillops-paper.pdf)
- Source package: [release/skillops-paper-source.zip](release/skillops-paper-source.zip)
- Current release target v1.3.0:
  [GitHub](https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.3.0)
- Zenodo latest-version record:
  [10.5281/zenodo.20061198](https://doi.org/10.5281/zenodo.20061198)

## Repository contents

This repository includes the paper source, benchmark inputs, reproducibility
scripts, local and model-backed outputs, metrics, external corpus planning, and
supporting artifact documentation.

```text
paper/          LaTeX paper source and bibliography
release/        compiled PDF and source package
benchmark/      manually constructed benchmark cases
experiments/    experiment prompts, schemas, and runners
scripts/        reproducibility and validation scripts
results/        tables, pilot outputs, and metrics
figures/        diagram and figure assets
artifacts/      artifact inventory and source-repository links
evidence/       supporting evidence records
docs/           publication and submission planning
tests/          repository-level checks
```

## Reproducibility

Requirements:

- Python 3.11 or newer
- `matplotlib` is optional; without it, figure generation writes SVG assets

From the repository root:

```bash
python scripts/run_all.py
python scripts/run_security_guard_experiment.py --run-live --guard local-rules
python scripts/run_trigger_experiment.py --run-live --provider deepseek --model deepseek-v4-flash
python scripts/run_constraint_experiment.py --run-live --provider deepseek --model deepseek-v4-flash
python scripts/run_security_guard_experiment.py --run-live --guard model --provider deepseek --model deepseek-v4-flash
python scripts/run_memory_drift_experiment.py --run-live --provider deepseek --model deepseek-v4-flash
python scripts/run_trigger_experiment.py --run-live --provider kimi --model kimi-k2.7-code
python scripts/run_constraint_experiment.py --run-live --provider kimi --model kimi-k2.7-code
python scripts/run_security_guard_experiment.py --run-live --guard model --provider kimi --model kimi-k2.7-code
python scripts/run_memory_drift_experiment.py --run-live --provider kimi --model kimi-k2.7-code
python scripts/summarize_live_model_results.py
python scripts/analyze_external_corpus.py
python scripts/generate_external_case_plan.py
python scripts/select_external_artifacts.py
python scripts/build_external_sampling_manifest.py
python scripts/generate_external_annotation_packet.py
python scripts/run_external_condition_dry_run.py --shards 12
python scripts/build_external_representations.py
python scripts/run_external_payload_experiment.py --dry-run
python scripts/prepare_external_pilot_plan.py
python scripts/run_external_pilot_experiment.py --dry-run
python scripts/generate_external_pilot_annotation_calibration.py
python scripts/prepare_external_smoke_test_plan.py
python scripts/summarize_external_results.py
python scripts/run_machine_checkable_external_analysis.py
python scripts/run_external_statistical_analysis.py
python scripts/run_llm_judge_sensitivity.py --dry-run
python scripts/analyze_runtime_evolution_ledger.py --input <skill-impact-ledger.json> --output-dir <summary-directory>
python scripts/run_tests.py
```

`python scripts/run_all.py` rebuilds the descriptive tables under
`results/tables/` and figure assets under `figures/` from the benchmark and
artifact inventory files.

`python scripts/run_security_guard_experiment.py --run-live --guard local-rules`
runs the local security-guard pilot over risk and benign-control cases.

`python scripts/analyze_external_corpus.py` runs a metadata-only static pass
over the third-party source frame and writes external corpus tables under
`results/tables/`.

`python scripts/generate_external_case_plan.py` builds the deterministic
planned external-corpus allocation: 240 target artifact slots, 960 planned base
cases, and 2880 planned condition rows. The corresponding case-label and pre-analysis
rules are in `docs/annotation_guide.md` and
`docs/preregistration_template.md`.

`python scripts/select_external_artifacts.py` derives a metadata-only candidate
inventory for the 240 external target slots. In the current snapshot this is
232 concrete third-party references plus 8 pending replacement slots. It
records source versions, repository paths or upstream links, and selection
bases without copying third-party prose or code.

`python scripts/build_external_sampling_manifest.py` adds deterministic random
keys, owner/ecosystem strata, and cap-pressure indicators to the metadata-only
candidate set. It reports sampling pressure and eligibility status; it does not
report artifact eligibility, case outcomes, or model outcomes.

`python scripts/generate_external_annotation_packet.py` expands those 240
target slots into eligibility and replacement manifests, 960 planned base
cases, 960 pending review rows, and 2880 planned condition rows. These files
define artifact-specific request construction and execution planning; they do
not report behavior measurements.

`python scripts/run_external_condition_dry_run.py --shards 12` validates the
2880 pending condition rows, writes a not-run execution manifest, creates twelve
240-row shards, and emits a planned statistical analysis table without
outcomes.

`python scripts/build_external_representations.py` builds metadata-only payload
templates for the three representation conditions. It produces 2880 not-run
payload rows aligned to the dry-run manifest and avoids copying third-party
prose or code.

`python scripts/run_external_payload_experiment.py --dry-run` validates payload
selection and writes a not-run execution plan. Bounded live execution is
available only with explicit `--run-live --sample-limit N`; the command refuses
unbounded live execution.

`python scripts/prepare_external_pilot_plan.py` selects a seeded 24-artifact
pilot from within-cap external candidates and writes the 96 base-case, 288
condition-row, and 576 provider-condition-row execution plan for DeepSeek and
Kimi. The plan is for label stability checks, provider logistics, parsing, and
bounded machine scoring; it is not a final external effect estimate.

`python scripts/run_external_pilot_experiment.py --dry-run` consumes the pilot
model plan and writes a not-run provider-condition execution plan plus
no-secret provider readiness. Bounded live execution requires explicit
`--run-live --provider ... --sample-limit N --max-live-rows N` and uses resume
state from prior pilot raw outputs.

`python scripts/generate_external_pilot_annotation_calibration.py` writes the
96-case pilot case-label worklist and a balanced 32-case calibration subset.
Those rows feed bounded label-sensitivity checks; they do not report model
outcomes.

`python scripts/prepare_external_smoke_test_plan.py` writes a no-secret,
bounded smoke-test plan for DeepSeek and Kimi. It records whether the required
environment variables are available, selected payload ids, and the exact
bounded command shape. This version also includes bounded live smoke outputs
for DeepSeek and Kimi under `results/experiments/raw/external_condition_*.jsonl`;
those files contain normalized result records, not model prose.

`python scripts/summarize_external_results.py` aggregates external condition
result JSONL files when present. In this version it summarizes 16 bounded smoke
records and marks planned statistical metrics as smoke-present but not powered
inference.

`python scripts/run_machine_checkable_external_analysis.py` writes the primary
external-smoke metrics: completed-record counts, parse success,
expected-behavior exact match, and constraint-pass checks over normalized
JSONL records.

`python scripts/run_external_statistical_analysis.py` writes descriptive paired
contrast, cluster-bootstrap, McNemar, and exclusion tables. In the current
repository state these are diagnostics over bounded smoke records, not
statistical significance claims.

`python scripts/run_llm_judge_sensitivity.py --dry-run` prepares the
LLM-as-judge case-label sensitivity route. Live judging is secondary evidence
only and requires explicit bounded provider execution.

`python scripts/analyze_runtime_evolution_ledger.py` is the file-only boundary
to Runtime Evolution Workbench. It verifies every `digest_material`, the
forward hash chain, and the terminal digest before producing descriptive JSON,
CSV, and Markdown summaries for task quality, tool and token cost, rule length,
rollback events, and cross-model transfer. It never reads the workbench
database and grants no approval or publication authority.

The provider-backed commands require the corresponding provider credentials in
environment variables. Raw outputs are written under `results/experiments/raw/`;
`python scripts/summarize_live_model_results.py` recomputes the cross-model
summary from those raw files. Use `docs/secure_live_experiment_runbook.md`
before running bounded live provider slices.

For account-side upload and external-study execution steps, use
`docs/submission_execution_checklist.md` and
`docs/account_external_execution_readiness.md`.
For the Zenodo file-state audit, use `docs/zenodo_file_state_audit.md`.
For the full request-to-evidence closure audit, use
`docs/requirements_closure_audit.md`.
For copy-ready submission fields, use `docs/submission_metadata_payload.md`.

`python scripts/run_tests.py` runs repository-level checks for benchmark
schema, table reproduction, figure validity, evidence links, and public
artifact consistency.

## Scope and limitations

- The repository supports descriptive and reproducible analysis of the included
  benchmark, local pilot outputs, and model-backed live runs.
- Benchmark inputs are manually constructed from public repository inspection.
- Tables and figures summarize the included artifact set; they do not establish
  statistical significance or broad performance claims.
- Live model or API execution for experiment runners requires credentials.
- External corpus validation is specified in
  `benchmark/external_artifact_corpus_sources.csv` and
  `experiments/external_validation_protocol.md`, with executable allocation
  files, metadata-only candidate files, and case-construction packets under
  `results/tables/`. The current external selection contains 232 concrete
  metadata-only third-party references plus 8 pending replacement slots within
  a 240-slot study design. A seeded 24-artifact external pilot execution plan,
  case-label calibration worklist, provider-readiness plan, machine-checkable
  smoke metrics, and bounded external live smoke are included, but broad
  external validation is not claimed.

## Citation

For an immutable citation, use the Zenodo version DOI attached to the release
tag you use. For `v1.3.0`, use the DOI shown on the corresponding Zenodo
version record after publication.

For a moving reference to the latest archived public artifact release, use
[10.5281/zenodo.20061198](https://doi.org/10.5281/zenodo.20061198).
