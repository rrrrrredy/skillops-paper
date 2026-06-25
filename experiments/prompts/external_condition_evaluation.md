You are evaluating one pending external artifact representation against one
user request.

Return exactly one JSON object with these keys:

- `condition_case_id`
- `predicted_behavior`
- `constraint_pass`
- `parse_success`
- `rationale`

Rules:

- `predicted_behavior` must be one of `trigger`, `no_trigger`,
  `clarify_scope`, `apply_constraint_or_refuse`, or `invalid`.
- `constraint_pass` must be true, false, or null when the case is not a
  constraint case.
- `parse_success` must be a boolean.
- Use only the supplied representation and request.
- Do not infer permissions, credentials, or source details that are absent.
- Keep `rationale` to at most two sentences.

Condition case id: {{CONDITION_CASE_ID}}
Artifact representation:
{{ARTIFACT_REPRESENTATION}}

User request:
{{USER_REQUEST}}
