# External Corpus Study Preregistration Template

## Study Identity

- Title: SkillOps external corpus evaluation
- Protocol version:
- Registration date:
- Repository release:
- Artifact archive DOI:
- Principal investigator:

## Research Questions

1. Does lifecycle-normalized representation improve routing, clarification, constraint handling, and output-contract behavior relative to native freeform artifact representation?
2. Which lifecycle components account for the largest behavioral differences when ablated?
3. Do effects vary by artifact family: Agent Skills, MCP/tool recipes, workflow templates, and prompt/function recipes?

## Sampling Plan

- Source frame: `benchmark/external_artifact_corpus_sources.csv`
- Allocation files:
  - `results/tables/external_case_allocation.csv`
  - `results/tables/external_case_plan.csv`
  - `results/tables/external_condition_plan.csv`
- Candidate inventory:
  - `results/tables/external_artifact_selection.csv`
- Planned review packets:
  - `results/tables/external_case_construction.csv`
  - `results/tables/external_annotation_packet.csv`
  - `results/tables/external_condition_packet.csv`
- Execution preparation:
  - `results/experiments/external_condition_manifest.csv`
  - `results/experiments/external_condition_shards.csv`
  - `results/experiments/external_statistical_analysis_plan.csv`
- Target artifacts: 240
- Base cases per artifact: 4
- Total base cases: 960
- Representation conditions: native/freeform, SkillOps-normalized, SkillOps-ablation
- Total condition evaluations: 2880

Sampling must use version-pinned sources. Any replacement must remain inside the same study family and source stratum unless no eligible artifact remains.

## Conditions

| Condition | Definition |
| --- | --- |
| `original_freeform` | Native artifact representation or metadata-preserving paraphrase allowed by license. |
| `skillops_normalized` | Same operational content represented through SkillOps lifecycle fields. |
| `skillops_ablation` | One preregistered lifecycle component removed or weakened while task content is preserved. |

## Outcomes

Primary outcomes:

- Routing F1
- False trigger rate
- Clarification appropriateness
- Constraint compliance
- Unsafe action refusal
- Output contract pass rate
- Stale-context use
- Structured parse success

Secondary outcomes:

- Token use
- Latency
- Reviewable failure rationale category
- LLM-as-judge case-label stability as a secondary sensitivity check

## Analysis Plan

Use paired, stratified mixed-effects logistic models with random effects for model, artifact, and case. Use McNemar tests as robustness checks for paired binary outcomes. Use bootstrap confidence intervals for F1. Control multiple comparisons with Holm-Bonferroni correction.

Report per-family estimates and pooled estimates. Do not present model ranking unless model identity, version, sampling date, and run parameters are fully reported.

## Exclusions

Exclude cases only for one of the following reasons:

- Source cannot be version-pinned.
- Artifact cannot be located.
- License prevents required inspection or representation.
- Case violates data-handling restrictions.
- Execution failure is caused by provider outage or infrastructure failure unrelated to the artifact or condition.

All exclusions must be reported with source id, artifact family, case type, condition, and reason.

## LLM-as-Judge Sensitivity Layer

The judge-sensitivity layer checks case-label stability only. It does not score
model outputs and does not replace machine-checkable parse, behavior-match, or
constraint-pass metrics. Run it with bounded provider rows and report it
separately from primary outcomes.

External human review may be added later as a separate validity study for audit
usefulness and user experience, but it is outside the current machine-only
evidence route.

## Reporting Boundary

Clearly separate completed evidence from protocol artifacts. Static source indicators, allocation files, seed cases, and schemas are study preparation artifacts; they are not behavioral outcomes.
