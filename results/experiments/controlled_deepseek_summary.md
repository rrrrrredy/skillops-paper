# Controlled DeepSeek Repeated Pilot Summary

- Provider: `deepseek`
- Model: `deepseek-chat`
- Repeats: `3`
- DEEPSEEK_API_KEY: `present`
- Live run performed: `yes`

## Slice Status

| Experiment | Completed | Partial | Rows | Expected | Parse Failures | Execution Failures |
| --- | --- | --- | --- | --- | --- | --- |
| Trigger | yes | no | 216 | 216 | 0 | 0 |
| Constraint | yes | no | 144 | 144 | 0 | 0 |
| Security | yes | no | 144 | 144 | 0 | 0 |
| Memory | yes | no | 198 | 198 | 0 | 0 |
| Aligned ablation | yes | no | 648 | 648 | 0 | 0 |

## Topline Metrics

- Trigger skillops mean F1: `0.800000`
- Trigger freeform mean F1: `0.812500`
- Constraint skillops compliance mean: `0.569444`
- Constraint vague compliance mean: `0.097222`
- Security detection mean: `0.888889`
- Security false-positive mean: `0.000000`
- Memory full policy stale-info mean: `0.000000`
- Memory no-forgetting stale-info mean: `0.045455`
- Ablation full_skillops mean F1: `0.750119`
