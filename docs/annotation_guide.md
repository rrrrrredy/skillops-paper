# External Corpus Case-Label Guide

This guide defines how to turn the external source frame into auditable evaluation cases for the planned 240-artifact study.

The current evidence route is machine-first: provider outputs are scored by
deterministic parse, expected-behavior match, and constraint-pass rules.
LLM-as-judge sensitivity checks audit case-label stability only. External
human review is an optional future validity study and is not required for the
bounded claims in the current paper.

## Unit of Labeling

The unit is one artifact selected from a version-pinned source. An artifact may be a skill package, server tool recipe, workflow example, prompt recipe, function recipe, or repository-local equivalent with a clear operational boundary.

The candidate inventory is `results/tables/external_artifact_selection.csv`.
It is metadata-only: repository paths, upstream links, commits, and selection
bases. Eligibility checks must verify that each candidate is a meaningful operational
artifact before constructing final cases.

The planned case packet is `results/tables/external_case_construction.csv`.
It contains four protocol-seeded cases per candidate artifact. Treat these as
work items to verify, refine, exclude, or reserve for sensitivity review rather than
as final labels.

The review packet is `results/tables/external_annotation_packet.csv`. It keeps
legacy reviewer and adjudication columns for compatibility, but those fields
remain empty in the current machine-first route.

The eligibility packet is `results/tables/external_eligibility_manifest.csv`.
Eligibility checks must verify locator, version pin, license, and operational-boundary
status before cases can move from protocol seed to artifact-specific execution.
Rows marked as requiring replacement are listed in
`results/tables/external_replacement_manifest.csv`; they should be replaced
within the same or nearest feasible stratum before broad external-validity
claims are made.

Each artifact receives four base cases:

| Case type | Decision target | Required evidence |
| --- | --- | --- |
| `positive_trigger` | The artifact should be used. | The request matches the stated purpose, accepted inputs, and operating context. |
| `negative_trigger` | The artifact should not be used. | The request is adjacent in vocabulary but outside the stated boundary. |
| `boundary_clarification` | More information is required. | The request is missing a required parameter, permission, credential, environment, or stop condition. |
| `risk_constraint` | The artifact should apply a constraint or refuse. | The request touches privacy, safety, permission, license, stale-context, or execution-risk boundaries. |

## Required Fields

Each base case must satisfy `experiments/schemas/external_case_schema.json`.

- `source_id`: one row from `benchmark/external_artifact_corpus_sources.csv`.
- `source_version`: immutable commit, release tag, DOI, or archived snapshot.
- `artifact_reference`: path, URL fragment, package name, or metadata reference that locates the artifact.
- `artifact_family_group`: one of the four preregistered study families.
- `case_type`: one of the four base case types.
- `user_request`: the task request shown to the evaluated representation.
- `expected_behavior`: trigger, no trigger, clarify scope, or apply constraint/refuse.
- `risk_label`: `none` unless the case intentionally probes a risk class.
- `label_source`: protocol label, LLM-as-judge sensitivity label, or a future
  external-review label if a separate user study is run.

## Labeling Rules

Labels should prefer the narrowest behavior consistent with the source. If a source does not state a permission, credential, network, or data-retention rule, do not infer permission from silence. Mark the case as `boundary_clarification` when the right behavior depends on missing context.

Use `risk_constraint` only when the request can plausibly cause disclosure, unauthorized action, unsafe execution, license misuse, stale-context use, or irreversible changes. Record the concrete risk label rather than a general concern.

For prompt-only artifacts, treat the prompt as an instruction surface rather than as an executable tool. A prompt may still receive risk cases when the request asks it to cross a boundary that a lifecycle-managed artifact would need to expose.

## Machine And Judge-Sensitivity Procedure

First validate the case packet and representation payloads with the repository
dry-run scripts. Then run bounded provider slices and compute machine-checkable
metrics from normalized result records. Finally, run
`python scripts/run_llm_judge_sensitivity.py --dry-run` to prepare the
case-label sensitivity plan, and optionally run bounded provider-backed judge
slices when credentials are locally available.

The LLM-as-judge route should not score model outputs. It only checks whether
the authored expected-behavior and risk labels are stable from the
metadata-only case definition. Cases with unstable labels should be revised,
excluded, or reserved for a separate external validity study before powered
execution.

## Pilot Calibration

The 24-artifact pilot worklist is
`results/tables/external_pilot_annotation_worklist.csv`. It contains 96
case-label rows drawn from the seeded pilot execution plan.

The calibration subset is
`results/tables/external_pilot_annotation_calibration.csv`. It contains 32
cases: two artifacts per study family, crossed with the four case types. Use
this subset to estimate label instability, parsing risk, and provider
logistics before executing the pilot model run. Do not treat calibration rows
as model outcomes or broad external validation.

Do not copy third-party prose into the released artifact unless the source license permits reuse. Metadata-only references are acceptable when text reuse is unclear.

## Exclusion Rules

Exclude artifacts that cannot be version-pinned, cannot be located after source verification, have ambiguous license status that prevents even metadata reference, or lack any meaningful operational boundary. Replace excluded artifacts within the same source stratum and record the replacement reason.

## Data Handling

Do not include credentials, private repository contents, personal contact data, or proprietary files in case records. When a sampled source demonstrates such a boundary, paraphrase the scenario with synthetic placeholders and keep the source reference at metadata level.
