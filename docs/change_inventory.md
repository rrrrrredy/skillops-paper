# Change Inventory

This inventory summarizes the major changes in the current working copy.

## Paper and Public Package

- Updated `paper/main.tex` with current model-backed evidence, external corpus framing, artifact lifecycle distinction, and stronger evidence boundaries.
- Updated `paper/references.bib` with current agent-skill, agent SDK, provider, artifact archive, and protocol citations.
- Rebuilt `release/skillops-paper.pdf`.
- Refreshed `release/skillops-paper-source.zip`.

## Provider and Experiment Harness

- Added DeepSeek and Kimi/Moonshot provider support to the experiment utilities and runners.
- Added current provider configuration tests.
- Added live model summary generation and raw-output sanitization.
- Preserved model names as experiment subjects while keeping public prose free of tool-process traces.

## Completed Live Evidence

- DeepSeek and Kimi trigger routing runs.
- DeepSeek and Kimi constraint compliance runs.
- DeepSeek and Kimi model-backed security guard runs.
- DeepSeek and Kimi memory drift runs.
- Local security guard run over risk and benign-control cases.

## External Corpus Scaffold

- Added `benchmark/external_artifact_corpus_sources.csv`.
- Added `scripts/analyze_external_corpus.py`.
- Added metadata-only external corpus result tables.
- Added `experiments/external_validation_protocol.md`.
- Added annotation and preregistration documents.

## External Case and Execution Preparation

- Added external case schema and seed cases.
- Added source allocation, case-plan, and condition-plan generation.
- Added metadata-only artifact selection for 240 candidate references.
- Added 960-case construction packet.
- Added pending review and condition packets.
- Added dry-run external condition manifest and shard summaries.
- Added metadata-only representation payloads for 2880 condition rows.
- Added live-ready external payload runner with bounded execution safeguards.
- Added seeded 24-artifact external pilot execution plan with 96 base cases,
  288 condition rows, and 576 provider-condition rows across DeepSeek and Kimi.
- Added resumable bounded pilot runner readiness over the 576
  provider-condition rows.
- Added 96-case pilot annotation worklist and balanced 32-case calibration
  subset for two-annotator review and adjudication.
- Added no-secret smoke-test plan.
- Added bounded external live smoke results for 16 metadata-only condition rows.
- Added external result and statistical summary files that separate smoke
  metrics from inferential statistical claims.

## Tests

- Expanded repository tests to cover provider configuration, live result hygiene, external corpus structure, external case scaffolding, artifact selection, annotation packets, dry-run manifests, representation payloads, pilot execution planning, pilot runner readiness, pilot annotation calibration, smoke-test planning, and external result summaries.
- Final status: 90 tests discovered, 90 passed.

## Remaining Work

- Conduct external human annotation and adjudication.
- Use the 24-artifact pilot execution plan to estimate annotation disagreement,
  parser/provider failure rates, and operational cost before a larger run.
- Provide provider credentials in the process environment before running a
  bounded pilot live slice.
- Execute the full external model study only after annotation and adjudication.
- Run inferential statistical analysis only after the full external result set exists.
- Perform one final commit and one final push for the public update.
- Update Zenodo/GitHub release metadata when publishing a new public version.
