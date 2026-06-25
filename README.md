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
- Archived public release v0.1.1:
  [GitHub](https://github.com/rrrrrredy/skillops-paper/releases/tag/v0.1.1),
  [Zenodo 10.5281/zenodo.20061199](https://doi.org/10.5281/zenodo.20061199)
- Zenodo latest-version record:
  [10.5281/zenodo.20061198](https://doi.org/10.5281/zenodo.20061198)

## Repository contents

This repository includes the paper source, benchmark inputs, reproducibility
scripts, local pilot outputs, metrics, and supporting artifact documentation.

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
python scripts/run_tests.py
```

`python scripts/run_all.py` rebuilds the descriptive tables under
`results/tables/` and figure assets under `figures/` from the benchmark and
artifact inventory files.

`python scripts/run_security_guard_experiment.py --run-live --guard local-rules`
runs the local security-guard pilot over risk and benign-control cases.

`python scripts/run_tests.py` runs repository-level checks for benchmark
schema, table reproduction, figure validity, evidence links, and public
artifact consistency.

## Scope and limitations

- The repository supports descriptive and reproducible analysis of the included
  benchmark and local pilot outputs.
- Benchmark inputs are manually constructed from public repository inspection.
- Tables and figures summarize the included artifact set; they do not establish
  statistical significance or broad performance claims.
- Live model or API execution for experiment runners requires credentials and
  explicit run logging before any model-backed metric is cited.
- The artifact base is limited to the repositories and records included here.

## Citation

For an immutable citation, use the Zenodo version DOI attached to the release
tag you use. For the archived `v0.1.1` record, use
[10.5281/zenodo.20061199](https://doi.org/10.5281/zenodo.20061199).

For a moving reference to the latest archived public artifact release, use
[10.5281/zenodo.20061198](https://doi.org/10.5281/zenodo.20061198).
