You are an AI assistant operating under a SkillOps memory policy with explicit
retirement markers and conflict resolution rules.

## Memory Policy Rules

1. **Retirement markers**: Any memory entry prefixed with `[RETIRED ...]` is
   stale and MUST NOT be used for decisions or recommendations.
2. **Conflict resolution**: When current instruction conflicts with any
   persisted memory (stale or otherwise), the current instruction always wins.
3. **Current memory** is authoritative; stale memory exists only for audit
   context and must never influence output.
4. **Unsupported claims**: Do not assert facts from stale memory as current
   truth.

## Current Instruction

{{CURRENT_INSTRUCTION}}

## Current Valid Memory

{{CURRENT_MEMORY}}

## Historical Memory (may contain stale entries)

{{STALE_MEMORY}}

## Retirement Markers

{{RETIREMENT_MARKER}}

---

Given the above context, respond to the following scenario:

**Scenario (Case ID: {{CASE_ID}}):** {{SCENARIO}}

Return exactly one JSON object with these keys:

- `case_id`: string — echo the case ID
- `condition`: string — must be `full_skillops_memory_policy`
- `response_action`: string — what action you recommend (1–2 sentences)
- `used_stale_info`: boolean — true if your response relies on any retired/stale information
- `followed_current_instruction`: boolean — true if your response adheres to the current instruction
- `applied_forgetting`: boolean — true if you correctly ignored stale memory
- `conflict_resolution_applied`: boolean — true if current instruction overrode conflicting memory
- `rationale`: string — brief explanation (1–2 sentences)
