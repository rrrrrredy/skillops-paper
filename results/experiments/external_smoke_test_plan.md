# External Smoke Test Plan

This no-secret plan selects a two-payload bounded smoke test for each provider. It does not report external model results.

## Providers

| Provider | Model | Credential env | Credential available | Status |
| --- | --- | --- | --- | --- |
| deepseek | deepseek-v4-flash | DEEPSEEK_API_KEY | false | not_run_missing_credentials |
| kimi | kimi-k2.7-code | MOONSHOT_API_KEY | false | not_run_missing_credentials |

## Payload Rows

| Provider | Payload | Condition case | Shard | Status |
| --- | --- | --- | --- | --- |
| deepseek | payload-ext-art-001-pos-original-freeform | ext-art-001-pos::original_freeform | external-shard-001 | not_run_missing_credentials |
| deepseek | payload-ext-art-001-pos-skillops-normalized | ext-art-001-pos::skillops_normalized | external-shard-001 | not_run_missing_credentials |
| kimi | payload-ext-art-001-pos-original-freeform | ext-art-001-pos::original_freeform | external-shard-001 | not_run_missing_credentials |
| kimi | payload-ext-art-001-pos-skillops-normalized | ext-art-001-pos::skillops_normalized | external-shard-001 | not_run_missing_credentials |
