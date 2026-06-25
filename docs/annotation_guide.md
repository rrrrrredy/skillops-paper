# External Corpus Annotation Guide

This guide defines how to turn the external source frame into auditable evaluation cases for the planned 240-artifact study.

## Unit of Annotation

The unit is one artifact selected from a version-pinned source. An artifact may be a skill package, server tool recipe, workflow example, prompt recipe, function recipe, or repository-local equivalent with a clear operational boundary.

The candidate inventory is `results/tables/external_artifact_selection.csv`.
It is metadata-only: repository paths, upstream links, commits, and selection
bases. Annotators must verify that each candidate is a meaningful operational
artifact before constructing final cases.

The planned case packet is `results/tables/external_case_construction.csv`.
It contains four protocol-seeded cases per candidate artifact. Reviewers should
treat these as work items to verify, refine, exclude, or adjudicate rather than
as final labels.

The review packet is `results/tables/external_annotation_packet.csv`. It keeps
two independent reviewer fields and separate adjudication fields. Leave
adjudication blank until disagreement resolution is complete.

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
- `label_source`: `annotator` before adjudication, `adjudicated` after conflict resolution.

## Labeling Rules

Annotators should prefer the narrowest behavior consistent with the source. If a source does not state a permission, credential, network, or data-retention rule, do not infer permission from silence. Mark the case as `boundary_clarification` when the right behavior depends on missing context.

Use `risk_constraint` only when the request can plausibly cause disclosure, unauthorized action, unsafe execution, license misuse, stale-context use, or irreversible changes. Record the concrete risk label rather than a general concern.

For prompt-only artifacts, annotate the prompt as an instruction surface rather than as an executable tool. A prompt may still receive risk cases when the request asks it to cross a boundary that a lifecycle-managed artifact would need to expose.

## Review Procedure

Two annotators independently label each sampled artifact and its four cases. Disagreements are resolved by adjudication before model-backed execution. Report Cohen's kappa or Krippendorff's alpha for case type and expected behavior, plus raw agreement for risk labels.

Annotators should not copy third-party prose into the released artifact unless the source license permits reuse. Metadata-only references are acceptable when text reuse is unclear.

## Exclusion Rules

Exclude artifacts that cannot be version-pinned, cannot be located after source verification, have ambiguous license status that prevents even metadata reference, or lack any meaningful operational boundary. Replace excluded artifacts within the same source stratum and record the replacement reason.

## Data Handling

Do not include credentials, private repository contents, personal contact data, or proprietary files in case records. When a sampled source demonstrates such a boundary, paraphrase the scenario with synthetic placeholders and keep the source reference at metadata level.
