# External Annotation Interface Spec

This spec defines the minimum participant-facing interface for the external pilot annotation workflow. It is designed for a spreadsheet, form tool, or lightweight internal review page.

## Reviewer Inputs

Show one row at a time with these fields:

| Field | Editable | Notes |
| --- | --- | --- |
| `case_id` | No | Stable row identifier. |
| `artifact_id` | No | Stable artifact identifier. |
| `study_family` | No | One of the four study-family strata. |
| `source_id` | No | Source repository or corpus identifier. |
| `source_version` | No | Commit, tag, DOI, or archived snapshot. |
| `artifact_reference` | No | Metadata-only locator. |
| `case_type` | No | Positive trigger, negative trigger, boundary clarification, or risk constraint. |
| `protocol_seed_request` | No | Starting point only. |
| `artifact_specific_user_request` | Yes | Reviewer-refined request grounded in the pinned source. |
| `required_evidence_refs` | Yes | URL, path, section, or commit reference used for the label. |
| `expected_behavior` | Yes | `trigger`, `no_trigger`, `clarify_scope`, or `apply_constraint_or_refuse`. |
| `risk_label` | Yes | `none` or a concrete risk class such as privacy, permission boundary, license, stale context, or irreversible action. |
| `review_rationale` | Yes | Short reason, metadata-only unless license allows quotation. |
| `exclusion_reason` | Conditional | Required if the row cannot be reviewed. |

## Hidden Fields

The interface must not show another reviewer response during independent review. It must not show contact details, payment details, credentials, private repository content, or raw provider outputs.

## Validation Rules

- `artifact_specific_user_request` is required unless `exclusion_reason` is set.
- `required_evidence_refs` is required for every included row.
- `expected_behavior` must use the four allowed labels.
- `risk_label` must be `none` for ordinary positive-trigger rows unless the pinned source justifies a risk label.
- `review_rationale` must not copy long third-party text or code into the released table.
- Adjudication fields remain locked until both independent reviewer slots are complete.

## Export Contract

For reviewer A, export to the `annotator_a_*` columns in `results/tables/external_pilot_annotation_worklist.csv`. For reviewer B, export to the `annotator_b_*` columns. After adjudication, export final labels to `adjudicated_expected_behavior`, `adjudicated_risk_label`, and `adjudication_reason`.

After each export, run:

```bash
python scripts/prepare_external_annotation_execution.py
python scripts/compute_external_annotation_reliability.py
python scripts/run_tests.py
```
