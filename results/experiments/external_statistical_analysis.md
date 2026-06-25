# External Statistical Analysis

This report computes descriptive paired contrasts and robustness-ready tables from external live-result records. It does not claim statistical significance unless a full annotated external run is present.

## Record State

| Quantity | Count |
| --- | --- |
| External records | 16 |
| Provider/model groups | 2 |
| Artifacts | 1 |

## Primary Contrasts

| Contrast | Provider/model | Pairs | Risk difference | Status |
| --- | --- | --- | --- | --- |
| skillops_normalized_vs_original_freeform | deepseek::deepseek-v4-flash | 4 | 0.000000 | descriptive_only |
| skillops_normalized_vs_skillops_ablation | deepseek::deepseek-v4-flash | 4 | 0.000000 | descriptive_only |
| skillops_normalized_vs_original_freeform | kimi::kimi-k2.7-code | 1 | 0.000000 | descriptive_only |
| skillops_normalized_vs_skillops_ablation | kimi::kimi-k2.7-code | 1 | 1.000000 | descriptive_only |

## McNemar Diagnostics

| Contrast | Provider/model | Pairs | Statistic | Approx p | Status |
| --- | --- | --- | --- | --- | --- |
| skillops_normalized_vs_original_freeform | deepseek::deepseek-v4-flash | 4 |  |  | no_discordant_pairs |
| skillops_normalized_vs_skillops_ablation | deepseek::deepseek-v4-flash | 4 |  |  | no_discordant_pairs |
| skillops_normalized_vs_original_freeform | kimi::kimi-k2.7-code | 1 |  |  | no_discordant_pairs |
| skillops_normalized_vs_skillops_ablation | kimi::kimi-k2.7-code | 1 | 0.000000 | 1.000000 | descriptive_mcnemar |
