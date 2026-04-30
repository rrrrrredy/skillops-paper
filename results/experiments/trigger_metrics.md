# Trigger Routing Accuracy Metrics

These metrics were recomputed from preserved raw outputs after metadata normalization.

- Provider: `longcat`
- Model: `LongCat-Flash-Chat`
- Raw output: `results/experiments/raw/trigger_20260430T065510Z.jsonl`

## skillops

| Metric | Value | Count |
| --- | --- | --- |
| precision | 0.6818 | 15/22 |
| recall | 1.0000 | 15/15 |
| f1 | 0.8108 | 15/22 |
| false_trigger_rate_on_should_not_trigger | 0.0000 | 0/12 |
| ambiguity_handling_rate | 0.2222 | 2/9 |

## freeform

| Metric | Value | Count |
| --- | --- | --- |
| precision | 0.7143 | 15/21 |
| recall | 1.0000 | 15/15 |
| f1 | 0.8333 | 15/21 |
| false_trigger_rate_on_should_not_trigger | 0.0000 | 0/12 |
| ambiguity_handling_rate | 0.3333 | 3/9 |
