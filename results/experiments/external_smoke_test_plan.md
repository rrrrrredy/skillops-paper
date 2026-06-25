# External Smoke Test Plan

This no-secret plan selects a two-payload bounded smoke test for each provider. It does not report external model results.

## Providers

| Provider | Model | Credential env | Credential available | Status |
| --- | --- | --- | --- | --- |
| deepseek | deepseek-v4-flash | DEEPSEEK_API_KEY | true | ready_for_bounded_live_smoke |
| kimi | kimi-k2.7-code | MOONSHOT_API_KEY | true | ready_for_bounded_live_smoke |

## Payload Rows

| Provider | Payload | Condition case | Shard | Status |
| --- | --- | --- | --- | --- |
| deepseek | payload-ext-art-001-pos-original-freeform | ext-art-001-pos::original_freeform | external-shard-001 | ready_for_bounded_live_smoke |
| deepseek | payload-ext-art-001-pos-skillops-normalized | ext-art-001-pos::skillops_normalized | external-shard-001 | ready_for_bounded_live_smoke |
| kimi | payload-ext-art-001-pos-original-freeform | ext-art-001-pos::original_freeform | external-shard-001 | ready_for_bounded_live_smoke |
| kimi | payload-ext-art-001-pos-skillops-normalized | ext-art-001-pos::skillops_normalized | external-shard-001 | ready_for_bounded_live_smoke |
