You are evaluating whether a user request should activate one of a fixed set of
skills.

Use the structured SkillOps-style catalog below. Each entry describes a skill's
purpose, activation boundary, and operational constraints.

Return exactly one JSON object with these keys:

- `case_id`
- `prompt_variant`
- `predicted_label`
- `predicted_skill`
- `confidence`
- `ambiguity_reason`
- `rationale`

Rules:

- `prompt_variant` must be `skillops`.
- `predicted_label` must be one of `should_trigger`, `should_not_trigger`, or
  `ambiguous`.
- `predicted_skill` must be one of the catalog skill names or `none`.
- Use `should_trigger` only when one catalog entry is clearly the best match.
- Use `should_not_trigger` when none of the catalog entries should activate.
- Use `ambiguous` when the request lacks enough information, straddles multiple
  skills, or needs clarification before routing.
- Prefer caution over over-triggering.
- Keep `rationale` to at most two sentences.
- Keep `ambiguity_reason` empty unless `predicted_label` is `ambiguous`.

Structured skill catalog:

{{SKILL_CATALOG}}

Case ID: {{CASE_ID}}
User request: {{USER_REQUEST}}
