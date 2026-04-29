# Executable Evidence Audit

Date recorded: 2026-04-29

Target filename requested by task: `research-log/2026-04-28-executable-evidence-audit.md`

## Commands Run

- `git status -sb`
- `Get-Content "paper/main.tex"`
- `Get-Content "scripts/run_all.py"`
- `Get-ChildItem -Recurse -File scripts, benchmark, results\tables, figures, artifacts, research-log | ForEach-Object { $_.FullName }`
- `Get-Content "scripts/analyze_structure.py"`
- `Get-Content "scripts/analyze_trigger_cases.py"`
- `Get-Content "scripts/analyze_risk_cases.py"`
- `Get-Content "scripts/generate_figures.py"`
- `Get-Content "benchmark/skill_samples.csv"`
- `Get-Content "benchmark/trigger_cases.csv"`
- `Get-Content "benchmark/risk_cases.csv"`
- `Get-Content "artifacts/artifact_inventory.md"`
- `Get-Content "research-log/2026-04-27-paper-spec.md"`
- `Get-Content "research-log/2026-04-27-related-work-notes.md"`
- `Get-Content "research-log/2026-04-28-analysis-run.md"`
- `Get-Content "research-log/2026-04-28-benchmark-design.md"`
- `Get-Content "research-log/2026-04-28-final-preprint-audit.md"`
- `Get-Content "research-log/2026-04-28-paper-consistency-patch.md"`
- `Get-Content "research-log/2026-04-28-paper-integration-build.md"`
- `Get-Date -Format o`
- `C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe scripts\run_all.py`
- `Import-Csv` verification of all three benchmark CSV inputs
- file-size checks for all six generated result tables
- XML parse checks for all three generated SVG files
- `Select-String` scan of `paper/main.tex` for unsupported claim language

## Files Verified

- `paper/main.tex`
- `scripts/run_all.py`
- `scripts/analyze_structure.py`
- `scripts/analyze_trigger_cases.py`
- `scripts/analyze_risk_cases.py`
- `scripts/generate_figures.py`
- `benchmark/skill_samples.csv`
- `benchmark/trigger_cases.csv`
- `benchmark/risk_cases.csv`
- `results/tables/artifact_coverage.md`
- `results/tables/trigger_summary.md`
- `results/tables/risk_summary.md`
- `results/tables/artifact_coverage.csv`
- `results/tables/trigger_summary.csv`
- `results/tables/risk_summary.csv`
- `figures/skillops_lifecycle.svg`
- `figures/skill_anatomy.svg`
- `figures/evaluation_pipeline.svg`
- `artifacts/artifact_inventory.md`
- `research-log/*.md`
- `evidence/execution_matrix.md`
- `evidence/execution_log.md`

## Counts Verified

- Skill samples: `5` artifacts
- Trigger cases: `36` total
- `should_trigger`: `15`
- `should_not_trigger`: `12`
- `ambiguous`: `9`
- Risk cases: `24` total
- Risk categories: `8`
- Cases per risk category: `3`

## Claims Allowed

- The repository contains a manually constructed benchmark with `5` artifact profiles, `36` trigger cases, and `24` risk cases.
- `scripts/run_all.py` successfully regenerates six descriptive summary tables and three SVG figures from versioned inputs.
- The generated tables are non-empty.
- The generated figures are readable SVG files.
- The evaluation layer is descriptive, exploratory, artifact-based, and script-generated.
- The paper may report counts from the generated summary files and the input CSVs.

## Claims Removed Or Weakened

- RQ3 wording was changed so it no longer implies that lint rules, security checks, or self-audit prompts were actually evaluated in this repository.
- The RQ mapping table now describes RQ2 and RQ3 as manually constructed benchmark cases and later executable checks, not completed behavioral evaluation.
- The methodology section now says the benchmark cases are intended for later evaluation rather than already evaluating trigger, lint, scanning, or self-audit behavior.
- The benchmark-description and evaluation-introduction paragraphs now state explicitly that `scripts/run_all.py` regenerates descriptive tables and SVG artwork only, without executing the five source repositories or scoring model, scanner, or self-audit behavior.

## Remaining Non-Executable Limitations

- No execution of `skill-design-guide`, `skill-security-guard`, `persistent-memory`, `agent-self-audit`, or `lobster-guard` against the benchmark cases was run in this repository.
- No model routing study was run.
- No scanner accuracy, precision, recall, or F1 metrics were measured.
- No user study was run.
- No production validation or multi-model comparison was run.
- The paper still uses LaTeX placeholders for the three figures; this audit verified the SVG assets only.
