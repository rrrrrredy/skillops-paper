# External Annotation Execution Plan

This optional future plan converts the external pilot review packet into a concrete human-review workflow. It is not part of the current machine-first evidence route and is not evidence of completed external review.

## Inputs

| Asset | Role |
| --- | --- |
| `results/tables/external_pilot_annotation_calibration.csv` | 32-case calibration subset. |
| `results/tables/external_pilot_annotation_worklist.csv` | 96-case 24-artifact pilot worklist. |
| `results/tables/external_annotation_assignment_manifest.csv` | Two independent reviewer assignments per case. |
| `results/tables/external_annotation_adjudication_log.csv` | Disagreement and final-label log template. |
| `docs/annotation_guide.md` | Label definitions, exclusion rules, and evidence boundary. |
| `docs/external_annotation_interface_spec.md` | Participant-facing field and validation contract. |

## Execution Order

1. Lock reviewer instructions, consent text, compensation terms, and data-retention rules before sharing task rows.
2. Recruit reviewers with agent, tool-building, developer-workflow, evaluation, or technical documentation experience.
3. Assign the 32 calibration cases to two independent reviewers using `rater_001` and `rater_002` study-local IDs.
4. Hide peer responses until both reviewers complete each row.
5. Compute raw agreement and Cohen kappa with `python scripts/compute_external_annotation_reliability.py`.
6. Revise the guide only if calibration reveals systematic ambiguity; record any instruction change before the pilot cases open.
7. Run the remaining 64 pilot cases after calibration instructions are locked.
8. Adjudicate disagreements with a third study-local ID such as `adjudicator_001`.
9. Run reliability computation again and freeze the adjudicated worklist before outcome-bearing model execution.

## Completion Rules

| Step | Completion criterion |
| --- | --- |
| Calibration | 32 cases have two independent labels, adjudication for disagreements, and reliability rows. |
| Pilot review | 96 cases have two independent labels or documented exclusion reasons. |
| Adjudication | Every disagreement has a final expected behavior, final risk label, and rationale. |
| Model execution gate | Only adjudicated rows with evidence references and eligibility approval enter the provider pilot. |
| Release gate | Public claims mention human-review outcomes only after labels, adjudication, and reliability outputs are present. |

## Non-Automatable Boundary

Repository automation can prepare assignments, validate schemas, compute agreement, and summarize completed labels. It cannot truthfully serve as an external human annotator or adjudicator. Consent records, participant contact details, payment details, and private source-access notes must stay outside the public repository.
