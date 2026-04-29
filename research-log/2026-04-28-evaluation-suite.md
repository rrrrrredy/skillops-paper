# Evaluation Suite Update

- Date recorded: `2026-04-29`
- Branch: `codex/evaluation-suite`
- Command run: `C:\Users\luosong03\AppData\Local\Programs\Python\Python311\python.exe scripts\run_tests.py`
- Pass/fail summary: `22/22 tests passed`

## Tests Added

- `tests/test_benchmark_schema.py`
- `tests/test_results_reproducibility.py`
- `tests/test_paper_claims.py`
- `tests/test_public_presentation.py`
- `tests/test_svg_figures.py`
- `tests/test_evidence_matrix.py`
- `scripts/run_tests.py`

## What They Verify

- Stable benchmark schemas and fixed case-count expectations for the repository benchmark inputs.
- Deterministic regeneration of descriptive tables and SVG figures from versioned repository inputs.
- Alignment between benchmark counts, generated result tables, and the counts reported in `paper/main.tex`.
- Limited use of unsupported claim terms so the paper does not overstate what the repository actually executes.
- Required public-facing identity fields and avoidance of prohibited draft/process wording.
- XML-valid SVG figures with the expected repository diagram labels.
- Explicit evidence-matrix language separating passed checks from items that were not run or not measured.

## What They Do Not Verify

- External artifact execution on the benchmark cases.
- Model performance or routed behavior under repeated execution.
- Scanner accuracy or labeled detector metrics.
- User-study outcomes or production validation.
- Statistical significance or generalizability beyond this repository state.

## Limitations

- The suite is a repository-level consistency layer, not an execution benchmark over the five source repositories.
- It depends on the benchmark CSVs and paper text remaining the authoritative source for descriptive counts.
- It does not replace future executable studies that run models, scanners, or self-audit workflows on labeled cases.
