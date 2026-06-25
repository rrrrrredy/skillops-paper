# Artifact Coverage Summary

This table summarizes manually constructed artifact profiles derived from
`benchmark/skill_samples.csv` and cross-checked against
`artifacts/artifact_inventory.md`.

The counts below are descriptive summaries of inspected artifacts, not
executed model results, statistical tests, or broad empirical validation.

## Input Summary

- Inventory date: 2026-04-28
- Artifact rows in `skill_samples.csv`: 5
- Artifact sections in `artifact_inventory.md`: 5
- Artifact names aligned across the two inputs: yes

## Classification Rule

- `documented`: the CSV field contains a concrete description of the component.
- `limited`: the field explicitly says the artifact lacks a standalone
  implementation or executable harness for that component.
- `absent`: the field is blank.

## Component-Level Coverage

| Component | Documented | Limited | Absent | Documented Artifacts | Limited Artifacts |
| --- | --- | --- | --- | --- | --- |
| Metadata | 5 | 0 | 0 | skill-design-guide, skill-security-guard, persistent-memory, agent-self-audit, lobster-guard | - |
| Trigger Contract | 5 | 0 | 0 | skill-design-guide, skill-security-guard, persistent-memory, agent-self-audit, lobster-guard | - |
| Instructions | 5 | 0 | 0 | skill-design-guide, skill-security-guard, persistent-memory, agent-self-audit, lobster-guard | - |
| Context Boundary | 5 | 0 | 0 | skill-design-guide, skill-security-guard, persistent-memory, agent-self-audit, lobster-guard | - |
| Execution Constraints | 5 | 0 | 0 | skill-design-guide, skill-security-guard, persistent-memory, agent-self-audit, lobster-guard | - |
| Memory Interface | 1 | 4 | 0 | persistent-memory | skill-design-guide, skill-security-guard, agent-self-audit, lobster-guard |
| Tests | 3 | 2 | 0 | skill-design-guide, persistent-memory, agent-self-audit | skill-security-guard, lobster-guard |
| Security Checks | 5 | 0 | 0 | skill-design-guide, skill-security-guard, persistent-memory, agent-self-audit, lobster-guard | - |
| Failure Modes | 5 | 0 | 0 | skill-design-guide, skill-security-guard, persistent-memory, agent-self-audit, lobster-guard | - |

## Artifact-Level Coverage Matrix

| Artifact | Metadata | Trigger Contract | Instructions | Context Boundary | Execution Constraints | Memory Interface | Tests | Security Checks | Failure Modes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| skill-design-guide | documented | documented | documented | documented | documented | limited | documented | documented | documented |
| skill-security-guard | documented | documented | documented | documented | documented | limited | limited | documented | documented |
| persistent-memory | documented | documented | documented | documented | documented | documented | documented | documented | documented |
| agent-self-audit | documented | documented | documented | documented | documented | limited | documented | documented | documented |
| lobster-guard | documented | documented | documented | documented | documented | limited | limited | documented | documented |

## Limitations

- These summaries come from manually constructed benchmark inputs.
- The component labels reflect descriptive coding of repository summaries,
  not direct execution evidence.
- The table should be read as traceability support for the paper, not as
  statistical validation.

