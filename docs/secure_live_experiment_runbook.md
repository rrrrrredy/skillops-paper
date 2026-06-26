# Secure Live Experiment Runbook

Audit date: 2026-06-25

## Purpose

This runbook describes how to run bounded provider-backed experiments without
placing API keys in repository files, command history, release packages, or
shared logs.

## Secret Boundary

- Never commit API keys, provider tokens, `.env.local`, `.env.*`,
  `*.local.env`, `*.secret`, `*.secrets`, `secrets/`, or `local-secrets/`.
- Store provider keys only in the local process environment or an operating
  system secret manager.
- Do not paste key values into commands that will be copied into issue trackers,
  paper artifacts, or shared terminal logs.
- Repository outputs may record credential variable names and boolean
  availability, but never credential values.

## Required Variables

| Provider | Required variable | Default model |
| --- | --- | --- |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-v4-flash` |
| Kimi/Moonshot | `MOONSHOT_API_KEY` | `kimi-k2.7-code` |

Optional overrides:

- `DEEPSEEK_MODEL`
- `DEEPSEEK_BASE_URL`
- `MOONSHOT_MODEL`
- `KIMI_MODEL`
- `MOONSHOT_BASE_URL`
- `KIMI_BASE_URL`

## Readiness Check

Run the readiness check before live execution:

```powershell
python scripts/check_experiment_readiness.py
python scripts/run_external_pilot_experiment.py --dry-run
```

Expected no-secret outputs:

- `results/experiments/external_pilot_provider_readiness.csv`
- `results/experiments/external_pilot_provider_readiness.md`
- `results/experiments/external_pilot_run_plan.csv`
- `results/experiments/external_pilot_run_plan.md`

These files may show `credential_available` as `true` or `false`, but should not
contain key values.

## Bounded Live Pilot Slice

After setting provider keys through a local secret mechanism, run only bounded
slices first:

```powershell
python scripts/run_external_pilot_experiment.py --run-live --provider deepseek --model deepseek-v4-flash --sample-limit 4 --max-live-rows 4
python scripts/run_external_pilot_experiment.py --run-live --provider kimi --model kimi-k2.7-code --sample-limit 4 --max-live-rows 4
```

The runner refuses unbounded live execution: `--sample-limit` is required and
the selected rows must not exceed `--max-live-rows`.

## Output Review

Before committing results:

```powershell
python scripts/sanitize_raw_results.py
python scripts/summarize_external_results.py
python scripts/run_machine_checkable_external_analysis.py
python scripts/run_external_statistical_analysis.py
python scripts/run_llm_judge_sensitivity.py --dry-run
python scripts/run_tests.py
rg -n "sk-[A-Za-z0-9]{24,}" README.md paper evidence docs benchmark experiments results scripts tests release\skillops-paper-source -S
```

Commit only sanitized summaries, manifests, and raw outputs that pass the secret
scan and evidence-boundary tests. Do not report external effect estimates until
eligibility review, machine-checkable scoring rules, model execution,
judge-sensitivity boundaries, and the preregistered statistical analysis are
complete.
