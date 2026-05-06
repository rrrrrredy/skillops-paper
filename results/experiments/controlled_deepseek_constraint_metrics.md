# Controlled DeepSeek Constraint Compliance Metrics

- Provider: `deepseek`
- Model: `deepseek-chat`
- Repeats: `3`
- Raw output: `results\experiments\raw\controlled_deepseek_constraint_20260506T024254Z.jsonl`
- Status: `complete`

## condition

| condition | Metric | Mean | Std | R1 | R2 | R3 | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| skillops | constraint_compliance_rate | 0.5694 | 0.0196 | 0.5833 | 0.5833 | 0.5417 |  |
| skillops | safe_handling_rate | 0.5694 | 0.0196 | 0.5833 | 0.5833 | 0.5417 |  |
| skillops | unsupported_success_claim_rate | 0.0417 | 0.0000 | 0.0417 | 0.0417 | 0.0417 |  |
| skillops | violation_rate | 0.4306 | 0.0196 | 0.4167 | 0.4167 | 0.4583 |  |
| vague | constraint_compliance_rate | 0.0972 | 0.0196 | 0.0833 | 0.1250 | 0.0833 |  |
| vague | safe_handling_rate | 0.1389 | 0.0196 | 0.1250 | 0.1667 | 0.1250 |  |
| vague | unsupported_success_claim_rate | 0.3472 | 0.0196 | 0.3333 | 0.3333 | 0.3750 |  |
| vague | violation_rate | 0.9028 | 0.0196 | 0.9167 | 0.8750 | 0.9167 |  |
