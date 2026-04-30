# SkillOps Live Pilot Report - Mixed-Provider Execution

> **Date**: 2026-04-30
> **Branch**: `empirical-live-longcat-pilot`
> **Status**: All 5 experiment tracks completed as a mixed-provider pilot artifact

---

## Interpretation Warning

This is a mixed-provider pilot. It verifies the execution pipeline and preserves descriptive results,
but it is not a controlled single-model comparison. These results should not be interpreted as
statistical significance or broad empirical validation.

---

## Provider Split

| Field | Value |
| --- | --- |
| LongCat model | LongCat-Flash-Chat |
| DeepSeek model | deepseek-chat |
| LongCat records attempted | 186 |
| LongCat records succeeded | 186 |
| LongCat records failed | 0 |
| DeepSeek records attempted | 492 |
| DeepSeek records succeeded | 492 |
| DeepSeek records failed | 0 |
| local-rules records | 24 |
| Experiments fully covered by LongCat | Trigger Routing, Constraint Compliance, Memory Drift |
| Experiments fully covered by DeepSeek | Ablation |
| Experiments fully covered by local-rules | Security Guard |
| Experiments split across providers | None |

Security Guard used local-rules and is not folded into LongCat counts.

### Provider Assignment by Experiment

| Experiment | Provider | Model | Records | Cases |
| --- | --- | --- | --- | --- |
| Trigger Routing Accuracy | longcat | LongCat-Flash-Chat | 72 | 36 cases x 2 prompt variants |
| Constraint Compliance Rate | longcat | LongCat-Flash-Chat | 48 | 24 cases x 2 prompt variants |
| Security Guard | local-rules | local-rules | 24 | 24 risk cases |
| Memory Drift Detection | longcat | LongCat-Flash-Chat | 66 | 22 cases x 3 conditions |
| SkillOps Ablation Study | deepseek | deepseek-chat | 492 | 82 cases x 6 variants |

---

## Metrics by Provider

### LongCat-only pilot results

#### Trigger Routing Accuracy

| Prompt Variant | Precision | Recall | F1 | False Trigger Rate | Ambiguity Handling |
| --- | --- | --- | --- | --- | --- |
| skillops | 0.6818 (15/22) | 1.0000 (15/15) | 0.8108 | 0.0000 (0/12) | 0.2222 (2/9) |
| freeform | 0.7143 (15/21) | 1.0000 (15/15) | 0.8333 | 0.0000 (0/12) | 0.3333 (3/9) |

Interpretation: These trigger numbers are LongCat-only pilot results. Recall was perfect and false-trigger rate was zero,
while ambiguity handling limited precision.

#### Constraint Compliance Rate

| Prompt Variant | Violation Rate | Safe Handling | Unsupported Claim | Compliance |
| --- | --- | --- | --- | --- |
| skillops | 1.0000 (24/24) | 0.0000 (0/24) | 0.2083 (5/24) | 0.0000 |
| vague | 0.4167 (10/24) | 0.5833 (14/24) | 0.0417 (1/24) | 0.5833 |

Interpretation: These constraint numbers are LongCat-only pilot results. In this pilot, the SkillOps condition performed worse
than the vague prompt on safe handling and compliance, so this slice should not be framed as a positive SkillOps effect.

#### Security Guard

| Metric | Value |
| --- | --- |
| Detection rate | 1.0000 (24/24) |
| False-positive rate | unmeasured (no benign controls) |
| Category recall | 8/8 risk categories reached 100% recall |
| Artifact coverage | 5/5 benchmark artifacts reached 100% coverage |

Interpretation: local-rules reached 24/24 detection on the supplied risk cases, but false positives remain unmeasured because no benign controls were included.

#### Memory Drift Detection

| Condition | Stale Usage | Current Adherence | Correct Forgetting | Conflict Resolution | Unsupported Claims |
| --- | --- | --- | --- | --- | --- |
| full_skillops_memory_policy | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| no_forgetting_policy | 0.2273 | 1.0000 | 0.0000 | 0.0455 | 0.0000 |
| current_context_only | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |

Interpretation: This LongCat pilot supports the usefulness of explicit forgetting and retirement policy.
The full policy condition avoided stale-info use, while removing the forgetting policy increased stale-info usage.

### DeepSeek-only ablation pilot

| Variant | Trigger F1 | False Trigger | Constraint Violation | Safe Handling | Stale Info | Correct Forgetting |
| --- | --- | --- | --- | --- | --- | --- |
| full_skillops | 0.0000 | 0.0833 | 0.0833 | 0.9583 | 0.0000 | 1.0000 |
| no_trigger_boundary | 0.0000 | 0.0833 | 0.0417 | 1.0000 | 0.0000 | 1.0000 |
| no_execution_constraints | 0.0000 | 0.0833 | 0.0833 | 0.9583 | 0.0000 | 1.0000 |
| no_security_checks | 0.0000 | 0.0833 | 0.0833 | 0.7500 | 0.0000 | 1.0000 |
| no_memory_interface | 0.0000 | 0.0833 | 0.0833 | 1.0000 | 0.0000 | 1.0000 |
| freeform_only | 0.0000 | 0.0833 | 0.0417 | 0.9583 | 0.0000 | 1.0000 |

Interpretation: DeepSeek ablation raw outputs exist and the numeric summaries are retained for traceability,
but the trigger-routing slice is inconclusive. The ablation skill variants define a translation skill, while
the trigger benchmark expects routing across skill-design-guide, skill-security-guard, persistent-memory,
agent-self-audit, lobster-guard, and none. Do not use the ablation trigger-routing numbers as evidence of a
SkillOps effect without rerunning ablation with aligned skill definitions.

---

## Mixed-Provider Aggregate

| Metric | Value | Notes |
| --- | --- | --- |
| Total records | 702 | 186 LongCat + 492 DeepSeek + 24 local-rules |
| Experiments split across providers | None | Each track stayed on one provider or local-rules |
| Parse errors | 0 | All rows parsed successfully |
| Execution failures | 0 | No failed rows were recorded |

---

## Limitations

1. Mixed providers: LongCat handled Trigger, Constraint, and Memory Drift; DeepSeek handled Ablation; Security Guard used local-rules.
2. Repetitions: single-repeat pilot only (`repeat_index = 1` for all rows after normalization).
3. Security false positives are unmeasured because no benign control set was included.
4. The ablation trigger-routing slice is inconclusive because the benchmark and ablation skill definitions are misaligned.
5. This artifact is descriptive only and does not establish statistical significance or broad empirical validation.

---

## Raw Output Files

| File | Size | Experiment | Provider |
| --- | --- | --- | --- |
| `raw/trigger_20260430T065510Z.jsonl` | 191KB | Trigger Routing | LongCat |
| `raw/constraint_20260430T065944Z.jsonl` | 169KB | Constraint Compliance | LongCat |
| `raw/security_guard_20260430T065944Z.jsonl` | 29KB | Security Guard | local-rules |
| `raw/memory_drift_20260430T070521Z.jsonl` | 236KB | Memory Drift | LongCat |
| `raw/ablation_20260430T080511Z.jsonl` | 1362KB | Ablation Study | DeepSeek |

## Metrics Files

| File | Experiment | Provider |
| --- | --- | --- |
| `trigger_metrics.csv` / `.md` | Trigger | LongCat |
| `constraint_metrics.csv` / `.md` | Constraint | LongCat |
| `security_guard_metrics.csv` / `.md` | Security Guard | local-rules |
| `memory_drift_metrics.csv` / `.md` | Memory Drift | LongCat |
| `ablation_metrics.csv` / `.md` | Ablation | DeepSeek |

---

## Next Steps

1. Rerun ablation with skill definitions aligned to the trigger benchmark before using that slice in any paper-level argument.
2. Add repeated trials if variance estimation matters for later interpretation.
3. Add benign control cases for Security Guard before making any false-positive claim.
4. Keep `paper/main.tex` unchanged until human review decides which pilot slices, if any, are fit for integration.
