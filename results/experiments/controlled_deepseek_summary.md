# Controlled DeepSeek Repeated Pilot Summary

- Provider: `deepseek`
- Model: `deepseek-chat`
- Repeats: `3`
- Credential handling: DEEPSEEK_API_KEY was provided via local environment variable for the live run; the value was not printed or committed.
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

### Trigger

- skillops mean F1: `0.800000`
- freeform mean F1: `0.812500`
- skillops false-trigger rate: `0.000000`
- freeform false-trigger rate: `0.000000`

### Constraint

- skillops compliance mean: `0.569444`
- vague compliance mean: `0.097222`
- skillops violation rate mean: `0.430556`
- vague violation rate mean: `0.902778`

### Security

- detection rate mean: `0.888889`
- false-positive rate mean: `0.000000`
- specificity mean: `1.000000`

### Memory

- full policy stale-info usage mean: `0.000000`
- no-forgetting stale-info usage mean: `0.045455`
- current-context-only stale-info usage mean: `0.000000`
- full policy current-instruction adherence mean: `1.000000`
- no-forgetting current-instruction adherence mean: `1.000000`
- current-context-only current-instruction adherence mean: `1.000000`
- full policy correct-forgetting mean: `1.000000`
- no-forgetting correct-forgetting mean: `0.000000`

### Aligned ablation

- full_skillops mean F1: `0.750119`
- no_trigger_boundary mean F1: `0.731707`
- freeform_only mean F1: `0.750000`
- full_skillops false-trigger rate: `0.111111`
- no_trigger_boundary false-trigger rate: `0.250000`
- freeform_only false-trigger rate: `0.166667`
