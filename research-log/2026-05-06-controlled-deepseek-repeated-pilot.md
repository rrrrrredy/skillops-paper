# Controlled DeepSeek Repeated Pilot Run Log

Date: 2026-05-06T03:39:00Z
Provider: deepseek
Model: deepseek-chat
Repeats: 3
DEEPSEEK_API_KEY: present
Live run performed: yes

## Topline Metrics

- Trigger skillops mean F1: 0.800000
- Trigger freeform mean F1: 0.812500
- Constraint skillops compliance mean: 0.569444
- Constraint vague compliance mean: 0.097222
- Security detection mean: 0.888889
- Security false-positive mean: 0.000000
- Memory full policy stale-info mean: 0.000000
- Memory no-forgetting stale-info mean: 0.045455
- Ablation full_skillops mean F1: 0.750119

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
