You are an AI assistant with access only to the current valid context.
No historical or stale memory is available.

## Current Instruction

{{CURRENT_INSTRUCTION}}

## Current Context

{{CURRENT_MEMORY}}

---

Given the above context, respond to the following scenario:

**Scenario (Case ID: {{CASE_ID}}):** {{SCENARIO}}

Return exactly one JSON object with these keys:

- `case_id`: string — echo the case ID
- `condition`: string — must be `current_context_only`
- `response_action`: string — what action you recommend (1–2 sentences)
- `used_stale_info`: boolean — must be false (no stale memory available)
- `followed_current_instruction`: boolean — true if your response adheres to the current instruction
- `applied_forgetting`: boolean — must be false (no stale memory to forget)
- `conflict_resolution_applied`: boolean — must be false (no conflicting sources)
- `rationale`: string — brief explanation (1–2 sentences)
