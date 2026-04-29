# SkillOps Benchmark Inputs

This directory contains the manually constructed benchmark inputs for the
SkillOps paper. The purpose of this layer is to make the paper's artifact base
inspectable and reproducible without presenting the benchmark as an executed
performance study.

These files are exploratory inputs only. They are not model outputs, result
tables, or figures.

## Files

- `skill_samples.csv`: structured artifact summaries derived from the five
  inspected public repositories
- `trigger_cases.csv`: manually constructed routing cases for skill triggering
- `risk_cases.csv`: manually constructed risk-detection cases for operational
  failure modes

## Manual construction process

1. Inspect the five public GitHub repositories named in the paper.
2. Record each artifact's purpose, files inspected, supported SkillOps
   components, and limitations in `artifacts/artifact_inventory.md`.
3. Convert the inspected evidence into one row per artifact in
   `skill_samples.csv`.
4. Write realistic but synthetic user requests for trigger analysis and label
   them as `should_trigger`, `should_not_trigger`, or `ambiguous`.
5. Write realistic but synthetic risk examples for prompt injection,
   over-triggering, unsafe file access, missing constraints, stale memory,
   missing tests, identity confusion, and privacy leakage.

All benchmark cases are manually constructed. To make that explicit, every case
identifier in `trigger_cases.csv` and `risk_cases.csv` begins with `manual-`.

## Categories

### Artifact-level samples

`skill_samples.csv` captures repository-level features that map the paper's
framework claims back to inspected artifact evidence. The columns are:

- artifact name and repository URL
- purpose and metadata
- trigger contract and instruction style
- context boundary and execution constraints
- memory interface
- tests, security checks, and failure modes
- notes about manual profiling and limitations

### Trigger cases

`trigger_cases.csv` is a small routing dataset for deciding when a modular
skill should be activated.

Labels:

- `should_trigger`: the request clearly matches one inspected skill
- `should_not_trigger`: the request should be handled without triggering one of
  the inspected skills
- `ambiguous`: the request plausibly touches a skill but needs more context or
  policy clarification

Count: 36 cases total.

- `should_trigger`: 15
- `should_not_trigger`: 12
- `ambiguous`: 9

### Risk cases

`risk_cases.csv` is a small operational risk set aimed at static review,
policy checks, and benchmark scripting.

Risk types currently included:

- `prompt_injection`
- `over_broad_trigger`
- `unsafe_file_access`
- `missing_constraints`
- `stale_memory`
- `missing_tests`
- `identity_confusion`
- `privacy_leakage`

Count: 24 cases total, with 3 cases for each risk type.

## Limitations

- The benchmark is manually constructed from public repository inspection, not
  from executed experiments.
- The artifact base comes from one author's public repositories in one agent
  ecosystem.
- No inter-annotator agreement or external label validation is provided.
- The cases are designed to be realistic, but they are still synthetic.
- The descriptive scripts and generated outputs do not measure actual
  model behavior; that would require a later execution layer under `scripts/`
  and `results/`.

## Why this benchmark is exploratory

This benchmark is intended to support artifact inspection, benchmark design,
and reproducible evaluation extensions. It is not broad validation of modular
skills, agent safety, or long-term memory systems in general.

The benchmark should therefore be read as a modest bridge between the paper's
framework claims and concrete public repositories:

- it supports traceability from paper claims to inspected artifacts
- it supports scripted evaluation design
- it does not support general performance claims on its own
