# SkillOps Paper and Artifacts

SkillOps paper and reproducible artifacts for designing, testing, and
operating modular skills in personal AI agents.

This repository contains the paper source, manually constructed benchmark
inputs, reproducible analysis scripts, generated descriptive tables, and figure
assets for:

**SkillOps: A Practical Framework for Designing, Testing, and Operating
Modular Skills in Personal AI Agents**

Author: **Song Luo**  
Email: **luosongred@gmail.com**  
GitHub: **https://github.com/rrrrrredy**

## Repository Structure

```text
paper/          LaTeX source files and bibliography
benchmark/      Manually constructed benchmark cases and evaluation inputs
scripts/        Reproducible analysis and figure-generation scripts
results/        Generated tables and intermediate outputs
figures/        Generated diagrams and figure assets
research-log/   Design notes, literature notes, and audit logs
artifacts/      Artifact inventory and links to source repositories
```

## Linked Artifact Base

The paper is grounded in the following open-source artifacts maintained by the
author:

- [skill-design-guide](https://github.com/rrrrrredy/skill-design-guide)
- [skill-security-guard](https://github.com/rrrrrredy/skill-security-guard)
- [persistent-memory](https://github.com/rrrrrredy/persistent-memory)
- [agent-self-audit](https://github.com/rrrrrredy/agent-self-audit)
- [lobster-guard](https://github.com/rrrrrredy/lobster-guard)

These repositories are treated as exploratory engineering evidence and case
material. They are not presented as proof of broad empirical validation.

## Benchmark Inputs

The benchmark files live in:

- `artifacts/artifact_inventory.md`
- `benchmark/README.md`
- `benchmark/skill_samples.csv`
- `benchmark/trigger_cases.csv`
- `benchmark/risk_cases.csv`

These files are manually constructed from public repository inspection. They
document the benchmark inputs used by the paper and the descriptive analysis
pipeline.

The benchmark profiles five public repositories and includes:

- 5 artifact profiles in `benchmark/skill_samples.csv`
- 36 trigger-routing cases in `benchmark/trigger_cases.csv`
- 24 operational-risk cases in `benchmark/risk_cases.csv`

## Generated Outputs

The repository includes reproducible scripts for converting the benchmark
inputs into descriptive tables and publication-friendly figures:

- `scripts/analyze_structure.py`
- `scripts/analyze_trigger_cases.py`
- `scripts/analyze_risk_cases.py`
- `scripts/generate_figures.py`
- `scripts/run_all.py`

Generated outputs include:

- `results/tables/artifact_coverage.md`
- `results/tables/artifact_coverage.csv`
- `results/tables/trigger_summary.md`
- `results/tables/trigger_summary.csv`
- `results/tables/risk_summary.md`
- `results/tables/risk_summary.csv`
- `figures/skillops_lifecycle.svg` or `figures/skillops_lifecycle.png`
- `figures/skill_anatomy.svg` or `figures/skill_anatomy.png`
- `figures/evaluation_pipeline.svg` or `figures/evaluation_pipeline.png`

The generated tables and figures are descriptive summaries of manually
constructed benchmark files. They do not claim statistical significance or
broad empirical validation.

`paper/main.tex` integrates the generated summary tables from
`results/tables/`. The repository also includes the generated SVG figure assets
in `figures/`. The LaTeX source keeps boxed placeholders for those figures so
the document remains compatible with a pdflatex-oriented workflow.

## Dependencies

- Python 3.11 or newer
- Python standard library only for the analysis scripts
- `matplotlib` is optional; when unavailable, `scripts/generate_figures.py`
  writes SVG files instead of PNG files

## Reproducing the Analysis

From the repository root:

```bash
python scripts/run_all.py
```

This command:

- reads `artifacts/artifact_inventory.md` and the CSV files under
  `benchmark/`
- regenerates the descriptive tables under `results/tables/`
- regenerates the figures under `figures/`
- prints the output paths it created

## Limitations

- The evaluation is exploratory.
- The benchmark is manually constructed.
- The reported outputs are descriptive.
- The artifact base is limited to five public repositories.
- No broad empirical validation is claimed.
- No statistical significance is claimed.
