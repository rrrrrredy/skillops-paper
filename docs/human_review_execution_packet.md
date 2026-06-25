# External Human Review Execution Packet

Audit date: 2026-06-25

## Purpose

This packet operationalizes the human-review layer for the external corpus
study. It is a protocol artifact, not collected evidence. Do not report human
outcomes until recruitment, consent, annotation, adjudication, and analysis are
complete.

## Study Boundary

- Target release: `v1.1.0`
- Artifact DOI: `10.5281/zenodo.20844038`
- Candidate packet: `results/tables/external_pilot_annotation_worklist.csv`
- Calibration packet: `results/tables/external_pilot_annotation_calibration.csv`
- Main annotation packet: `results/tables/external_annotation_packet.csv`
- Study population: participants with agent, tool-building, developer-workflow,
  evaluation, or technical documentation experience.
- Planned sample: 48-72 participants for the broader study; at least two
  independent annotators plus adjudication for each pilot case before
  outcome-bearing model execution.

## Consent and Data Handling

Before participation, provide a plain-language consent page that states:

- the task asks participants to judge whether artifact-backed agent behavior is
  appropriate for sampled requests;
- participation is voluntary and can stop at any time;
- compensation, expected time, and payment conditions are stated before work
  starts;
- no credentials, private repositories, real customer data, or personal contact
  data should be entered into the study interface;
- responses may be analyzed in aggregate and released only after de-identifying
  participant metadata.

Store reviewer IDs as study-local pseudonyms such as `rater_001`. Do not store
direct contact details in released tables.

## Session Flow

1. Eligibility screen: confirm relevant experience and absence of conflicts
   with sampled repositories when applicable.
2. Consent screen: record agreement before showing any task rows.
3. Calibration block: assign rows from
   `results/tables/external_pilot_annotation_calibration.csv`.
4. Instruction check: require reviewers to identify the four case types and the
   expected behavior labels before proceeding.
5. Annotation block: assign balanced rows by artifact family and case type.
6. Confidence and workload block: collect optional confidence and workload
   ratings after each block, not after every row.
7. Exit screen: allow reviewers to flag confusing, unsafe, or unreviewable
   cases.

## Review Fields

The study interface should expose only the fields needed for judgment:

- source id, source version, artifact reference, artifact family, and case type;
- protocol-seeded request and required evidence references;
- empty reviewer fields for final user request, expected behavior, risk label,
  and rationale;
- exclusion reason when the artifact cannot be reviewed.

Do not show another reviewer response before independent annotation is
complete.

## Quality Controls

- Balance rows by artifact family and case type.
- Use the 32-case calibration subset before the 96-case pilot worklist.
- Measure raw agreement, Cohen's kappa or Krippendorff's alpha, and
  disagreement category counts before adjudication.
- Require adjudication notes when independent labels disagree.
- Exclude rows only under the exclusion rules in `docs/annotation_guide.md`.
- Keep all released rows metadata-only unless the source license permits
  quoting or redistribution.

## Stop Conditions

Pause the study and revise instructions if any of the following occur:

- more than 20 percent of calibration rows are marked unreviewable;
- reviewers repeatedly infer permissions that are not present in source
  evidence;
- a sampled artifact requires private credentials or private repository access;
- the task interface exposes personal data, secrets, or copied third-party
  content beyond the allowed metadata boundary;
- adjudication cannot resolve a case without changing the study definition.

## Reporting Boundary

Report this packet as readiness evidence only. Outcome-bearing claims require:

1. completed consent and recruitment records;
2. populated independent annotation fields;
3. adjudication for disagreements;
4. reliability statistics;
5. model execution over adjudicated cases; and
6. statistical analysis using the preregistered plan.
