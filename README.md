# SkillOps Paper

This repository contains the working paper draft, research logs, benchmark
design notes, bibliography, figures directory, and reproducibility scaffolding
for:

**SkillOps: A Practical Framework for Designing, Testing, and Operating
Modular Skills in Personal AI Agents**

Author: **Song Luo**  
Affiliation: **Independent Researcher**

## Status

This repository is an active first-preprint workspace.

The current draft is internally consistent enough for review as a preprint
draft, but it is still incomplete in two important ways:

- The paper now includes framework tables, integrated descriptive benchmark
  summary tables, figure placeholders linked to generated SVG artwork, and a
  cleaned bibliography.
- The benchmark remains manually constructed and exploratory rather than a
  broad empirical evaluation.

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

## Current Stage

The project is currently at the following stage:

- Paper framing, research questions, and methodology draft are in place.
- Related-work coverage is now substantially expanded and tied to the paper's
  claims.
- Conceptual framework tables are present in the LaTeX draft.
- Benchmark inputs, reproducible analysis scripts, generated summary tables,
  and publication-friendly concept figures are now versioned in the repository.
- `paper/main.tex` now integrates the generated descriptive result summaries
  from `results/tables/`.
- SVG figure files remain separate from the LaTeX source because this
  workspace does not currently have a local SVG-to-PDF/PNG conversion toolchain
  or LaTeX build toolchain.

## Research Questions

**RQ1:** What structural components should a skill include as an agent
capability unit?

**RQ2:** How do trigger descriptions, context injection, execution constraints,
and forgetting affect agent stability?

**RQ3:** Can automated linting, security scanning, and self-auditing reduce
operational risk?

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

## Benchmark Files

The first benchmark-design layer now lives in:

- `artifacts/artifact_inventory.md`
- `benchmark/README.md`
- `benchmark/skill_samples.csv`
- `benchmark/trigger_cases.csv`
- `benchmark/risk_cases.csv`

These files are manually constructed from public repository inspection. They
document the benchmark inputs, but they do not contain generated results,
evaluation tables, or figures.

## Analysis Scripts and Generated Outputs

The repository now includes reproducible scripts for converting the benchmark
inputs into descriptive tables and publication-friendly figures:

- `scripts/analyze_structure.py`
- `scripts/analyze_trigger_cases.py`
- `scripts/analyze_risk_cases.py`
- `scripts/generate_figures.py`
- `scripts/run_all.py`

Generated outputs currently include:

- `results/tables/artifact_coverage.md`
- `results/tables/artifact_coverage.csv`
- `results/tables/trigger_summary.md`
- `results/tables/trigger_summary.csv`
- `results/tables/risk_summary.md`
- `results/tables/risk_summary.csv`
- `figures/skillops_lifecycle.svg` or `figures/skillops_lifecycle.png`
- `figures/skill_anatomy.svg` or `figures/skill_anatomy.png`
- `figures/evaluation_pipeline.svg` or `figures/evaluation_pipeline.png`

These generated results are descriptive summaries of manually constructed
benchmark files. They should not be read as statistical significance claims or
broad empirical validation.

The current LaTeX draft now integrates the generated summary tables from
`results/tables/`. The generated SVG figures are referenced indirectly through
boxed placeholders until a PDF/PNG conversion path is available.

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

- reads only `artifacts/artifact_inventory.md` and the CSV files under
  `benchmark/`
- regenerates the descriptive tables under `results/tables/`
- regenerates the figures under `figures/`
- prints the output paths it created

## Target Venue Strategy

The current publication strategy is staged rather than single-shot:

1. Maintain the GitHub repository as the canonical artifact base.
2. Prepare an OSF or TechRxiv-style preprint release once the benchmark
   implementation is less skeletal.
3. Seek workshop feedback on the framework and evaluation design.
4. Submit a later revision to arXiv after the paper and artifact package are
   more mature.

If the paper keeps its current operational framing, `cs.SE` remains a plausible
primary category with `cs.AI` as a cross-list. If later revisions foreground
agent design more strongly than engineering lifecycle, that balance may shift.

## Reproducibility

The repository is intended to make the paper inspectable and incrementally
reproducible.

Current reproducibility status:

- The paper source and bibliography are versioned in this repository.
- The benchmark design is documented in the paper and research logs.
- The benchmark input files are versioned under `benchmark/` and
  `artifacts/`.
- Reproducible scripts for descriptive summaries and figure generation are
  versioned under `scripts/`.
- Generated summary tables and figures are versioned under `results/` and
  `figures/`.

Future revisions should add benchmark inputs, scripts, generated tables,
figure-generation steps, and any annotation guidance needed for manual review.

## Limitations

This project remains intentionally modest:

- It is based on a single independent researcher's open-source practice.
- It reports only descriptive summaries of manually constructed benchmark
  files.
- It should not be read as evidence of broad empirical validation.
- The benchmark is expected to be small-scale and partially manual even after it
  is implemented.

## Current Next Steps

- Decide which generated tables and figures should be cited directly in the
  next paper revision.
- Review whether additional benchmark cases are needed before claiming any
  stronger evaluation scope.
- Add an SVG-to-PDF/PNG conversion path so the generated figures can replace
  the current LaTeX placeholders.
- Run a full LaTeX compilation pass once a compiler is available.
- Prepare an external review pass focused on claim strength and evaluation
  scope.
