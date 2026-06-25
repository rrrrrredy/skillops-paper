# External Validation Protocol

This protocol separates three evidence layers for SkillOps: static third-party artifact analysis, model-backed execution over paired cases, and human review.

## Corpus Frame

The sampling frame is `benchmark/external_artifact_corpus_sources.csv`. It covers Agent Skills, MCP servers, agent workflow repositories, function recipes, and prompt-only baselines. The intended quantitative sample is 240 artifacts:

| Family | Target n | Rationale |
| --- | ---: | --- |
| Agent Skills | 80 | Closest format match to the paper's artifact lifecycle. |
| MCP and tool recipes | 60 | Captures high-permission tool surfaces and access boundaries. |
| Agent workflow templates | 50 | Captures code-embedded instructions, routing, handoff, and tracing patterns. |
| Prompt and function recipes | 50 | Provides a design-only baseline with weaker lifecycle structure. |

For each artifact, record source URL, version or commit, license status, artifact family, capability surface, trigger boundary, context boundary, execution constraints, tests, security controls, memory behavior, and retirement signals. Text reuse is limited to artifacts with compatible licenses; metadata-only rows are kept for discovery and stratification.

Author-ecosystem exclusion means the external frame must not sample repositories
owned by the paper author, this paper repository, or the author's own SkillOps
and skill artifacts. Provider-adjacent framework examples may remain as
third-party contrast classes when their source owners, version pins, and
metadata-only boundaries are explicit; they are not treated as author-authored
evidence.

## Executable Case Scaffold

The executable scaffold is split into schema, seed, allocation, and annotation files:

| File | Role |
| --- | --- |
| `experiments/schemas/external_case_schema.json` | Required fields and allowed labels for one external base case. |
| `experiments/external_case_seed.csv` | Seed examples that exercise the schema without claiming sampled outcomes. |
| `scripts/generate_external_case_plan.py` | Deterministic generator for source allocation and condition plans. |
| `results/tables/external_case_allocation.csv` | Source-level allocation for the 240 target artifacts. |
| `results/tables/external_case_plan.csv` | Case-type allocation for the 960 base cases. |
| `results/tables/external_condition_plan.csv` | Crossed condition plan for 2880 condition-level evaluations. |
| `scripts/select_external_artifacts.py` | Metadata-only selector for candidate artifact references. |
| `results/tables/external_artifact_selection.csv` | Candidate artifact rows with source versions, paths or upstream links, and selection bases. |
| `scripts/generate_external_annotation_packet.py` | Deterministic generator for planned base cases, review rows, and condition rows. |
| `results/tables/external_case_construction.csv` | Four planned base cases per candidate artifact. |
| `results/tables/external_annotation_packet.csv` | Empty two-reviewer and adjudication fields for the 960 planned cases. |
| `results/tables/external_condition_packet.csv` | Three-condition execution packet for the 960 planned cases. |
| `experiments/schemas/external_condition_result_schema.json` | Strict result schema for future external condition outputs. |
| `scripts/run_external_condition_dry_run.py` | Dry-run validator and sharder for pending external condition rows. |
| `results/experiments/external_condition_manifest.csv` | Execution manifest with 2880 not-run condition rows and shard ids. |
| `results/experiments/external_condition_shards.csv` | Twelve 240-row shard summaries for future execution. |
| `results/experiments/external_statistical_analysis_plan.csv` | Planned metric and analysis rows without outcomes. |
| `experiments/prompts/external_condition_evaluation.md` | Prompt contract for future external condition evaluation. |
| `scripts/build_external_representations.py` | Metadata-only representation builder for the three study conditions. |
| `results/experiments/external_representation_payloads.jsonl` | Payload templates for 2880 not-run condition rows. |
| `results/experiments/external_representation_payload_index.csv` | Payload index aligned to condition ids and shards. |
| `scripts/run_external_payload_experiment.py` | Dry-run-default runner for payload validation and bounded live execution. |
| `results/experiments/external_payload_run_plan.csv` | Not-run execution plan for selected payload rows. |
| `scripts/prepare_external_smoke_test_plan.py` | No-secret bounded smoke-test plan for selected providers. |
| `results/experiments/external_smoke_test_plan.csv` | Provider/model/payload plan for a two-row smoke test per provider. |
| `scripts/summarize_external_results.py` | Aggregates future external condition result files and writes no-results boundary outputs when none exist. |
| `results/experiments/external_result_summary.csv` | External live-result summary or no-results boundary. |
| `results/experiments/external_statistical_summary.csv` | Planned statistical metrics with result availability status. |
| `docs/annotation_guide.md` | Labeling rules, adjudication, exclusion, and data-handling rules. |
| `docs/preregistration_template.md` | Pre-analysis template for registering the external study before execution. |

The case-plan, selection, annotation, and condition packet files are protocol
artifacts. They define what must be sampled, labeled, represented, and
evaluated; they are not behavioral results.

## Model-Backed Study

For each sampled artifact, construct four paired cases: positive trigger, negative trigger, boundary or clarification, and risk or constraint. This gives 960 cases. Each case is evaluated under three conditions:

| Condition | Description |
| --- | --- |
| Original/freeform | The artifact is presented in its native form or as close as its license permits. |
| SkillOps-normalized | The same operational content is rewritten into the SkillOps lifecycle schema. |
| SkillOps-ablation | One lifecycle component is removed or weakened according to a preregistered ablation plan. |

Primary metrics are routing F1, false trigger rate, clarification appropriateness, constraint compliance, unsafe action refusal, output contract pass rate, stale-context use, and structured parse success. Secondary metrics include token use, latency, and reviewable failure rationales.

The primary analysis is a paired, stratified mixed-effects logistic model with random effects for model, artifact, and case. McNemar tests are used as robustness checks for paired binary outcomes. Bootstrap confidence intervals are reported for F1. Multiple comparisons are controlled with Holm-Bonferroni correction.

Power planning should assume a baseline routing rate around 70% and a target detectable difference of 6-8 percentage points. The 960-case paired design is expected to be adequate for medium effects under moderate intra-artifact correlation, but the final report should recompute power after a pilot estimates the correlation structure.

## Human Review Study

The human study requires 48-72 participants with agent, tooling, or developer-workflow experience. It uses a within-subject Latin-square design over artifact family and representation condition.

Tasks:

| Task | Outcome |
| --- | --- |
| Route a user request to the right artifact | Success rate and time. |
| Identify out-of-scope or ambiguous requests | False trigger avoidance and clarification quality. |
| Review safety, privacy, license, or stale-context risk | Defect discovery count and severity. |
| Convert a freeform prompt into a lifecycle-managed artifact | Structural completeness and review time. |
| Decide whether to revise or retire an artifact from a failure log | Correct lifecycle decision and rationale quality. |

Measures include task success, defects found, completion time, NASA-TLX, UMUX-Lite, trust calibration, and qualitative theme coding. This layer requires recruitment, consent, compensation, and data handling outside the repository. It should not be reported as completed until those procedures are run.
