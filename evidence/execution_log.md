# Executable Evidence Audit Log

- Task: Executable Evidence Audit for SkillOps
- Audit date: 2026-04-29
- Working directory: `D:\Codex\skillops-paper-artifact-benchmark`
- Branch at audit start: `main`
- Audit branch: `codex/executable-evidence-audit`
- Git identity: `Song Luo <luosongred@gmail.com>`
- Python interpreter requested for all Python commands: `C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe`
- Python version: direct version probes failed in this shell session with `Access denied`; the executed interpreter path targets Python 3.11, but the exact version string was not retrievable here

## Timestamps

- `2026-04-29T12:24:25.8592689+08:00`: reproducibility run started
- `2026-04-29T12:29:19.0780834+08:00`: post-run verification snapshot

## Commands Actually Run

Status `passed` unless noted otherwise.

1. `git status -sb`
2. `Get-Content "paper/main.tex"`
3. `Get-Content "scripts/run_all.py"`
4. `Get-ChildItem -Recurse -File scripts, benchmark, results\tables, figures, artifacts, research-log | ForEach-Object { $_.FullName }`
5. `Get-Content "scripts/analyze_structure.py"`
6. `Get-Content "scripts/analyze_trigger_cases.py"`
7. `Get-Content "scripts/analyze_risk_cases.py"`
8. `Get-Content "scripts/generate_figures.py"`
9. `Get-Content "benchmark/skill_samples.csv"`
10. `Get-Content "benchmark/trigger_cases.csv"`
11. `Get-Content "benchmark/risk_cases.csv"`
12. `Get-Content "artifacts/artifact_inventory.md"`
13. `Get-Content "research-log/2026-04-28-analysis-run.md"`
14. `Get-Content "research-log/2026-04-28-final-preprint-audit.md"`
15. `Get-Date -Format o`
16. `& 'C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe' --version`
    Status: `failed`
17. `& 'C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe' scripts\run_all.py`
18. `& 'C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe' -c "import sys; print(sys.version)"`
    Status: `failed`
19. `git status -sb`
20. `$paths = 'results/tables/artifact_coverage.md','results/tables/trigger_summary.md','results/tables/risk_summary.md','results/tables/artifact_coverage.csv','results/tables/trigger_summary.csv','results/tables/risk_summary.csv'; foreach ($p in $paths) { $item = Get-Item $p; "$($item.FullName)`t$($item.Length)" }`
21. `$paths = 'figures/skillops_lifecycle.svg','figures/skill_anatomy.svg','figures/evaluation_pipeline.svg'; foreach ($p in $paths) { try { $xml = [xml](Get-Content $p -Raw); if ($xml.DocumentElement.LocalName -eq 'svg') { "$p`treadable-svg" } else { "$p`tnot-svg-root" } } catch { "$p`tparse-failed: $($_.Exception.Message)" } }`
22. `$skills = Import-Csv 'benchmark/skill_samples.csv'; $triggers = Import-Csv 'benchmark/trigger_cases.csv'; $risks = Import-Csv 'benchmark/risk_cases.csv'; "skill_samples_total`t$($skills.Count)"; $triggers | Group-Object expected_label | ForEach-Object { "trigger_$($_.Name)`t$($_.Count)" }; "trigger_total`t$($triggers.Count)"; $risks | Group-Object risk_type | ForEach-Object { "risk_$($_.Name)`t$($_.Count)" }; "risk_type_total`t$(($risks | Group-Object risk_type).Count)"; "risk_total`t$($risks.Count)"`
23. `Select-String -Path 'paper/main.tex' -Pattern 'proven|validated|significant improvement|accuracy|precision|recall|F1|model execution|user study|production validation' -CaseSensitive:$false | ForEach-Object { "${($_.LineNumber)}`t$($_.Line.Trim())" }`
24. `Get-Content 'results/tables/artifact_coverage.md'`
25. `Get-Content 'results/tables/trigger_summary.md'`
26. `Get-Content 'results/tables/risk_summary.md'`
27. `Select-String -Path 'paper/main.tex' -Pattern 'five artifacts|36 trigger|15 labeled|12 labeled|9 labeled|24 manually written cases|three cases each|artifact coverage|descriptive coding of nine|statistically significant|broad empirical validation|user study|precision|recall|accuracy|validated empirical result|multi-model execution' -CaseSensitive:$false | ForEach-Object { Write-Output (('{0}`t{1}' -f $_.LineNumber, $_.Line.Trim())) }`
28. `Get-Content 'paper/main.tex' | Select-Object -Skip 430 -First 170`
29. `Get-Content 'paper/main.tex' | Select-Object -Skip 600 -First 180`
30. `Get-Content 'results/tables/artifact_coverage.csv'`
31. `Get-Content 'results/tables/trigger_summary.csv'`
32. `Get-Content 'results/tables/risk_summary.csv'`
33. `Get-Content 'research-log/2026-04-27-paper-spec.md'`
34. `Get-Content 'research-log/2026-04-27-related-work-notes.md'`
35. `Get-Content 'research-log/2026-04-28-benchmark-design.md'`
36. `Get-Content 'research-log/2026-04-28-paper-consistency-patch.md'`
37. `Get-Content 'research-log/2026-04-28-paper-integration-build.md'`
38. `Get-Content 'figures/skillops_lifecycle.svg' | Select-Object -First 12`
39. `Get-Content 'figures/skill_anatomy.svg' | Select-Object -First 12`
40. `Get-Content 'figures/evaluation_pipeline.svg' | Select-Object -First 12`
41. `git branch --list "codex/executable-evidence-audit"`
42. `git config user.name`
43. `git config user.email`
44. `git checkout -b codex/executable-evidence-audit`
    Status: `failed`
45. `Get-Item 'C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe' | Select-Object -ExpandProperty VersionInfo | Format-List ProductVersion, FileVersion`
46. `Get-Date -Format o`
47. `Select-String -Path 'paper/main.tex' -Pattern 'Can automated linting, security scanning, and self-auditing|expected output is an evaluation of lint rules|construct test cases that evaluate|RQ3 & Linting, security scanning, and self-audit & Seeded failure cases' | ForEach-Object { Write-Output (('{0}`t{1}' -f $_.LineNumber, $_.Line.Trim())) }`
48. `Get-Content 'paper/main.tex' | Select-Object -Skip 420 -First 60`
49. `Get-Content 'paper/main.tex' | Select-Object -Skip 540 -First 40`
50. `Get-Content 'C:\Users\luosong03\AppData\Local\Programs\Python\Python311\pyvenv.cfg'`
    Status: `failed`
51. `Get-ChildItem 'C:\Users\luosong03\AppData\Local\Programs\Python\Python311' | ForEach-Object { $_.Name }`
    Status: `failed`
52. `git checkout -b codex/executable-evidence-audit`
    Status: `passed`
    Note: this second branch-creation command was rerun outside the sandbox after the first attempt failed with a lock-file permission error

## Outputs Generated

These files were regenerated by `C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe scripts\run_all.py`.

- `results/tables/artifact_coverage.md`
- `results/tables/artifact_coverage.csv`
- `results/tables/trigger_summary.md`
- `results/tables/trigger_summary.csv`
- `results/tables/risk_summary.md`
- `results/tables/risk_summary.csv`
- `figures/skillops_lifecycle.svg`
- `figures/skill_anatomy.svg`
- `figures/evaluation_pipeline.svg`

## Output Verification

- `results/tables/artifact_coverage.md`: exists, non-empty, size `3399` bytes
- `results/tables/trigger_summary.md`: exists, non-empty, size `1128` bytes
- `results/tables/risk_summary.md`: exists, non-empty, size `1216` bytes
- `results/tables/artifact_coverage.csv`: exists, non-empty, size `1156` bytes
- `results/tables/trigger_summary.csv`: exists, non-empty, size `321` bytes
- `results/tables/risk_summary.csv`: exists, non-empty, size `454` bytes
- `figures/skillops_lifecycle.svg`: XML parsed successfully with SVG root
- `figures/skill_anatomy.svg`: XML parsed successfully with SVG root
- `figures/evaluation_pipeline.svg`: XML parsed successfully with SVG root

## Counts Verified

- `benchmark/skill_samples.csv`: `5` rows
- `benchmark/trigger_cases.csv`: `36` total cases
- `benchmark/trigger_cases.csv`: `15` `should_trigger`
- `benchmark/trigger_cases.csv`: `12` `should_not_trigger`
- `benchmark/trigger_cases.csv`: `9` `ambiguous`
- `benchmark/risk_cases.csv`: `24` total cases
- `benchmark/risk_cases.csv`: `8` risk categories
- `benchmark/risk_cases.csv`: `3` cases in each category

## Failures Observed

- Direct Python version probes failed:
  - `& 'C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe' --version`
  - `& 'C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe' -c "import sys; print(sys.version)"`
- Reading the Python installation directory and `pyvenv.cfg` path also failed in this sandboxed shell session.
- The first `git checkout -b codex/executable-evidence-audit` attempt failed because `.git\refs\heads\codex\executable-evidence-audit.lock` could not be created inside the sandbox. Re-running the same command outside the sandbox succeeded.

## Limitations

- `scripts/run_all.py` regenerates descriptive tables and schematic SVG figures only.
- This audit did not execute `skill-design-guide`, `skill-security-guard`, `persistent-memory`, `agent-self-audit`, or `lobster-guard` against the benchmark cases.
- This audit did not run a model over the benchmark prompts.
- No accuracy, precision, recall, F1, detector-performance, risk-reduction, user-study, multi-model, or production-validation result was executed in this repository state.
