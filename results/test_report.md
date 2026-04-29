# Executable Test Report

- Command run: `C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe scripts\run_tests.py`
- Run date: `2026-04-29`
- Pass/fail status: `passed`
- Summary: `22/22 tests passed`

## Tests Executed

- `tests/test_benchmark_schema.py`
- `tests/test_results_reproducibility.py`
- `tests/test_paper_claims.py`
- `tests/test_public_presentation.py`
- `tests/test_svg_figures.py`
- `tests/test_evidence_matrix.py`

## What the Tests Verify

- Benchmark input files exist with the expected schemas, non-empty unique case IDs, and fixed label-count distributions.
- `scripts/run_all.py` runs with the active Python interpreter, regenerates the expected repository outputs, and keeps the generated counts aligned with the benchmark CSV inputs.
- `paper/main.tex` reports benchmark and summary-table counts that match the versioned CSV inputs and generated result tables.
- Unsupported claim language in `paper/main.tex` is only used in limiting or not-measured contexts.
- Public-facing files preserve the required author identity and avoid prohibited draft or process wording.
- Repository SVG figures are non-empty, parse as XML with an `svg` root, and contain the expected diagram labels.
- The evidence matrix and execution log exist, distinguish `passed` from `not run`, and explicitly record missing execution layers.

## What the Tests Do Not Verify

- They do not run external artifact repositories against the benchmark cases.
- They do not measure model performance, scanner accuracy, precision, recall, F1, user-study outcomes, or production validation.
- They do not validate compiled PDF integration of the SVG figures.
- They do not establish statistical significance or broad empirical generality.

## Limitations

- The suite is deterministic and repository-scoped; it checks internal consistency rather than external behavioral correctness.
- The artifact-coverage assertions are derived from the versioned benchmark descriptions, so they verify stable repository coding rather than runtime execution of the source artifacts.
- The report reflects the repository state on the command above and should be rerun after substantive benchmark, paper, or figure edits.
