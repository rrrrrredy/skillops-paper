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
- Archived public release v1.0.0:
  [GitHub](https://github.com/rrrrrredy/skillops-paper/releases/tag/v1.0.0),
  [Zenodo 10.5281/zenodo.20838908](https://doi.org/10.5281/zenodo.20838908)
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
python scripts/run_empirical_experiments.py --run-live --provider deepseek --model deepseek-v4-flash --security-guard model
python scripts/run_empirical_experiments.py --run-live --provider kimi --model kimi-k2.7-code --security-guard model
python scripts/summarize_live_model_results.py
python scripts/analyze_external_corpus.py
python scripts/generate_external_case_plan.py
python scripts/select_external_artifacts.py
python scripts/generate_external_annotation_packet.py
python scripts/run_external_condition_dry_run.py --shards 12
python scripts/build_external_representations.py
python scripts/run_external_payload_experiment.py --dry-run
python scripts/prepare_external_smoke_test_plan.py
python scripts/summarize_external_results.py
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
external study allocation: 240 target artifacts, 960 base cases, and 2880
condition-level evaluations. The corresponding annotation and pre-analysis
rules are in `docs/annotation_guide.md` and
`docs/preregistration_template.md`.

`python scripts/select_external_artifacts.py` derives a metadata-only candidate
inventory for the 240 external artifact references. It records source versions,
repository paths or upstream links, and selection bases without copying
third-party prose or code.

`python scripts/generate_external_annotation_packet.py` expands those 240
candidate references into 960 planned base cases, 960 pending review rows, and
2880 condition rows. These files define review and execution work; they do not
report collected annotations or behavior measurements.

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

`python scripts/prepare_external_smoke_test_plan.py` writes a no-secret,
bounded smoke-test plan for DeepSeek and Kimi. It records whether the required
environment variables are available, selected payload ids, and the exact
bounded command shape. This version also includes bounded live smoke outputs
for DeepSeek and Kimi under `results/experiments/raw/external_condition_*.jsonl`;
those files contain normalized result records, not model prose.

`python scripts/summarize_external_results.py` aggregates external condition
result JSONL files when present. In this version it summarizes 16 bounded smoke
records and marks the planned statistical metrics as requiring a separate
statistical model run.

The provider-backed commands require the corresponding provider credentials in
environment variables. Raw outputs are written under `results/experiments/raw/`;
`python scripts/summarize_live_model_results.py` recomputes the cross-model
summary from those raw files.

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
- External corpus validation and human review are specified in
  `benchmark/external_artifact_corpus_sources.csv` and
  `experiments/external_validation_protocol.md`, with executable allocation
  files, metadata-only candidate files, and pending review packets under
  `results/tables/`. A bounded external live smoke is included, but broad
  external validation is not claimed.

## Citation

For an immutable citation, use the Zenodo version DOI attached to the release
tag you use. For the archived `v1.0.0` record, use
[10.5281/zenodo.20838908](https://doi.org/10.5281/zenodo.20838908).

For a moving reference to the latest archived public artifact release, use
[10.5281/zenodo.20061198](https://doi.org/10.5281/zenodo.20061198).
