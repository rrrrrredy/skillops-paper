# Benchmark Design Log

Date: 2026-04-28

## Repositories inspected

Primary paper workspace:

- `README.md`
- `research-log/2026-04-27-paper-spec.md`
- `research-log/2026-04-28-paper-consistency-patch.md`

Public artifact repositories inspected:

- `skill-design-guide`
  - `README.md`
  - `SKILL.md`
  - `scripts/skill_lint.py`
- `skill-security-guard`
  - `README.md`
  - `SKILL.md`
  - `references/detection-rules.md`
  - `scripts/scan.sh`
- `persistent-memory`
  - `README.md`
  - `SKILL.md`
  - `scripts/memory_manager.py`
- `agent-self-audit`
  - `README.md`
  - `SKILL.md`
  - `references/audit-criteria.md`
  - `scripts/health_check.sh`
- `lobster-guard`
  - `README.md`
  - `SKILL.md`
  - `references/identity-verification.md`

All five public source repositories were accessible during this inspection pass.

## Benchmark design rationale

The paper needs a reproducible artifact layer before it can add results,
tables, or figures. The benchmark therefore starts from public repository
inspection rather than from executed model runs.

The design uses three layers:

1. Artifact profiles in `benchmark/skill_samples.csv`
2. Trigger-routing cases in `benchmark/trigger_cases.csv`
3. Risk-detection cases in `benchmark/risk_cases.csv`

This structure keeps the benchmark modest. It connects paper claims to real
repositories, but it does not imply that the benchmark has already been run.

## Annotation categories

### Artifact profiles

Each artifact row records:

- purpose
- metadata
- trigger contract
- instruction style
- context boundary
- execution constraints
- memory interface
- tests
- security checks
- failure modes
- notes

### Trigger labels

The trigger benchmark uses three labels:

- `should_trigger`
- `should_not_trigger`
- `ambiguous`

These cases are manually constructed from the repositories' stated trigger
contracts and exclusion boundaries.

### Risk labels

The risk benchmark uses eight categories:

- `prompt_injection`
- `over_broad_trigger`
- `unsafe_file_access`
- `missing_constraints`
- `stale_memory`
- `missing_tests`
- `identity_confusion`
- `privacy_leakage`

These cases are also manually constructed and are intended as small,
inspectable stress cases rather than production incident reports.

## Case counts by category

Trigger cases:

- `should_trigger`: 15
- `should_not_trigger`: 12
- `ambiguous`: 9
- total: 36

Risk cases:

- `prompt_injection`: 3
- `over_broad_trigger`: 3
- `unsafe_file_access`: 3
- `missing_constraints`: 3
- `stale_memory`: 3
- `missing_tests`: 3
- `identity_confusion`: 3
- `privacy_leakage`: 3
- total: 24

Artifact profiles:

- total repositories profiled: 5

## What this benchmark can support

- Traceability from paper claims to concrete public repositories
- Small-scale inspection of trigger contracts and operational failure modes
- Future scripted evaluation work under `scripts/`
- Future generated outputs under `results/`
- Modest discussion of how the five artifacts map to RQ1, RQ2, and RQ3

## What this benchmark cannot support

- Broad empirical validation of modular-skill quality or safety
- General claims about all personal AI agents
- Statistical claims about model performance
- Comparative results across agent platforms
- Any results table or figure until the benchmark is actually executed

## Unresolved issues

- No inter-annotator agreement or external review of the manual labels yet
- No executed benchmark scripts yet
- No result tables or figures yet
- The artifact set is concentrated in one author's OpenClaw-oriented ecosystem
- Some repositories are documentation-heavy, so evidence is stronger for design
  intent than for measured runtime behavior
