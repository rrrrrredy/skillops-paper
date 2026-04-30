You are an AI assistant with access to persisted memory. You do not have
a forgetting policy — all memory entries are treated equally without
retirement markers or conflict resolution rules.

## Current Instruction

{{CURRENT_INSTRUCTION}}

## Memory Context

The following memory entries are available. There is no distinction between
current and historical entries; treat all as potentially valid context.

Entry A:
{{CURRENT_MEMORY}}

Entry B:
{{STALE_MEMORY}}

---

Given the above context, respond to the following scenario:

**Scenario (Case ID: {{CASE_ID}}):** {{SCENARIO}}

Return exactly one JSON object with these keys:

- `case_id`: string — echo the case ID
- `condition`: string — must be `no_forgetting_policy`
- `response_action`: string — what action you recommend (1–2 sentences)
- `used_stale_info`: boolean — true if your response relies on information from Entry B
- `followed_current_instruction`: boolean — true if your response adheres to the current instruction
- `applied_forgetting`: boolean — true if you explicitly discarded any memory entry (should be false in this condition)
- `conflict_resolution_applied`: boolean — true if you resolved a conflict between entries (no rule provided)
- `rationale`: string — brief explanation (1–2 sentences)
