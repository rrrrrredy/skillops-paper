# Controlled DeepSeek Repeated Pilot Run Log

Date: 2026-05-06T03:39:00Z
Provider: deepseek
Model: deepseek-chat
Repeats: 3
Credential handling: DEEPSEEK_API_KEY was provided via local environment variable for the live run; the value was not printed or committed.
Live run performed: yes

## Topline Metrics

### Trigger

- skillops mean F1: 0.800000
- freeform mean F1: 0.812500
- skillops false-trigger rate: 0.000000
- freeform false-trigger rate: 0.000000

### Constraint

- skillops compliance mean: 0.569444
- vague compliance mean: 0.097222
- skillops violation rate mean: 0.430556
- vague violation rate mean: 0.902778

### Security

- detection rate mean: 0.888889
- false-positive rate mean: 0.000000
- specificity mean: 1.000000

### Memory

- full policy stale-info usage mean: 0.000000
- no-forgetting stale-info usage mean: 0.045455
- current-context-only stale-info usage mean: 0.000000
- full policy current-instruction adherence mean: 1.000000
- no-forgetting current-instruction adherence mean: 1.000000
- current-context-only current-instruction adherence mean: 1.000000
- full policy correct-forgetting mean: 1.000000
- no-forgetting correct-forgetting mean: 0.000000

### Aligned ablation

- full_skillops mean F1: 0.750119
- no_trigger_boundary mean F1: 0.731707
- freeform_only mean F1: 0.750000
- full_skillops false-trigger rate: 0.111111
- no_trigger_boundary false-trigger rate: 0.250000
- freeform_only false-trigger rate: 0.166667

## Trigger

- completed: yes
- partial: no
- rows: 216/216
- parse_failures: 0
- execution_failures: 0
- raw_output: `results\experiments\raw\controlled_deepseek_trigger_20260506T023135Z.jsonl`
- metrics_csv: `results\experiments\controlled_deepseek_trigger_metrics.csv`
- metrics_md: `results\experiments\controlled_deepseek_trigger_metrics.md`

## Constraint

- completed: yes
- partial: no
- rows: 144/144
- parse_failures: 0
- execution_failures: 0
- raw_output: `results\experiments\raw\controlled_deepseek_constraint_20260506T024254Z.jsonl`
- metrics_csv: `results\experiments\controlled_deepseek_constraint_metrics.csv`
- metrics_md: `results\experiments\controlled_deepseek_constraint_metrics.md`

## Security

- completed: yes
- partial: no
- rows: 144/144
- parse_failures: 0
- execution_failures: 0
- raw_output: `results\experiments\raw\controlled_deepseek_security_20260506T025114Z.jsonl`
- metrics_csv: `results\experiments\controlled_deepseek_security_metrics.csv`
- metrics_md: `results\experiments\controlled_deepseek_security_metrics.md`

## Memory

- completed: yes
- partial: no
- rows: 198/198
- parse_failures: 0
- execution_failures: 0
- raw_output: `results\experiments\raw\controlled_deepseek_memory_20260506T025754Z.jsonl`
- metrics_csv: `results\experiments\controlled_deepseek_memory_metrics.csv`
- metrics_md: `results\experiments\controlled_deepseek_memory_metrics.md`

## Aligned ablation

- completed: yes
- partial: no
- rows: 648/648
- parse_failures: 0
- execution_failures: 0
- raw_output: `results\experiments\raw\controlled_deepseek_ablation_trigger_20260506T030834Z.jsonl`
- metrics_csv: `results\experiments\controlled_deepseek_ablation_trigger_metrics.csv`
- metrics_md: `results\experiments\controlled_deepseek_ablation_trigger_metrics.md`
