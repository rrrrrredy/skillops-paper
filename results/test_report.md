# Executable Test Report

- Command run: `python scripts/run_tests.py`
- Run date: `2026-06-26`
- Pass/fail status: `passed`
- Summary: `141 discovered, 141 passed`

## Tests Executed

- `tests/test_benchmark_schema.py`
- `tests/test_evidence_matrix.py`
- `tests/test_external_annotation_execution.py`
- `tests/test_external_annotation_packet.py`
- `tests/test_external_artifact_selection.py`
- `tests/test_external_case_scaffold.py`
- `tests/test_external_condition_dry_run.py`
- `tests/test_external_corpus.py`
- `tests/test_external_corpus_results.py`
- `tests/test_external_payload_runner.py`
- `tests/test_external_pilot_annotation_calibration.py`
- `tests/test_external_pilot_plan.py`
- `tests/test_external_pilot_runner.py`
- `tests/test_external_representations.py`
- `tests/test_external_result_summary.py`
- `tests/test_external_sampling_manifest.py`
- `tests/test_external_smoke_plan.py`
- `tests/test_external_statistical_analysis.py`
- `tests/test_arxiv_endorsement_outreach.py`
- `tests/test_human_review_execution_packet.py`
- `tests/test_live_model_results.py`
- `tests/test_llm_judge_sensitivity.py`
- `tests/test_machine_checkable_external_analysis.py`
- `tests/test_paper_claims.py`
- `tests/test_provider_config.py`
- `tests/test_public_presentation.py`
- `tests/test_requirements_closure_audit.py`
- `tests/test_results_reproducibility.py`
- `tests/test_secure_live_experiment_runbook.py`
- `tests/test_submission_execution_checklist.py`
- `tests/test_submission_metadata_payload.py`
- `tests/test_submission_package_manifest.py`
- `tests/test_svg_figures.py`
- `tests/test_zenodo_file_state_audit.py`

## What the Tests Verify

- Benchmark input files exist with the expected schemas, non-empty unique case
  IDs, and fixed label-count distributions.
- `scripts/run_all.py` runs with the active Python interpreter, regenerates the
  expected repository outputs, and keeps the generated counts aligned with the
  benchmark CSV inputs.
- `paper/main.tex` reports benchmark and summary-table counts that match the
  versioned CSV inputs and generated result tables.
- Unsupported claim language in `paper/main.tex` is only used in limiting or
  not-measured contexts.
- Public-facing files preserve the required author identity and avoid
  prohibited process wording.
- Release PDF and source package exist, and the source package contains the
  expected paper files without prohibited process or trace terms.
- Release PDF text and metadata can be extracted locally and do not contain
  prohibited process or trace terms.
- Repository SVG figures are non-empty, parse as XML with an `svg` root, and
  contain the expected diagram labels.
- The evidence matrix and execution log exist, distinguish `passed` from
  `not run`, and explicitly record missing execution layers.
- External artifact selection and pilot plans avoid non-capability repository
  metadata such as license, font, funding, and CI workflow files.
- External case-label and optional future review assets preserve boundaries:
  machine-checkable metrics remain primary, while LLM-as-judge sensitivity and
  human-review packets are kept separate from outcome claims.
- Live raw result files retain normalized metrics and run metadata without
  provider response bodies or model response text.
- Submission and requirements closure documents remain aligned with release
  assets, hashes, DOI, and non-automatable account boundaries.
- The Zenodo file-state audit records the historical DOI/file mismatch and
  verifies that the current Zenodo archive embeds release assets matching the
  package manifest.

## What the Tests Do Not Verify

- They do not run external artifact repositories against the benchmark cases.
- They do not measure broad model performance, scanner accuracy,
  user-study outcomes, or production validation.
- They do not validate compiled PDF integration of the SVG figures.
- They do not perform visual review of the compiled PDF layout.
- They do not establish statistical significance or broad empirical generality.

## Limitations

- The suite is deterministic and repository-scoped; it checks internal
  consistency rather than external behavioral correctness.
- The artifact-coverage assertions are derived from the versioned benchmark
  descriptions, so they verify stable repository coding rather than runtime
  execution of the source artifacts.
- The report reflects the repository state on the command above and should be
  rerun after substantive benchmark, paper, or figure edits.
