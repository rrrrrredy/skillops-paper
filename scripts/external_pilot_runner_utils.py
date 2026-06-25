from __future__ import annotations

import csv
import os
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from experiment_utils import (  # noqa: E402
    RAW_RESULTS_DIR,
    RESULTS_DIR,
    call_model,
    filename_timestamp,
    resolve_provider_config,
    write_csv_rows,
    write_jsonl,
)
from run_external_payload_experiment import (  # noqa: E402
    normalize_live_result,
    read_jsonl,
    render_payload_prompt,
    sha256_text,
)

PILOT_MODEL_PLAN_PATH = RESULTS_DIR / "external_pilot_model_plan.csv"
PAYLOAD_JSONL_PATH = RESULTS_DIR / "external_representation_payloads.jsonl"
RUN_PLAN_CSV_PATH = RESULTS_DIR / "external_pilot_run_plan.csv"
RUN_PLAN_MD_PATH = RESULTS_DIR / "external_pilot_run_plan.md"
READINESS_CSV_PATH = RESULTS_DIR / "external_pilot_provider_readiness.csv"
READINESS_MD_PATH = RESULTS_DIR / "external_pilot_provider_readiness.md"
LIVE_MANIFEST_CSV_PATH = RESULTS_DIR / "external_pilot_live_run_manifest.csv"
LIVE_MANIFEST_MD_PATH = RESULTS_DIR / "external_pilot_live_run_manifest.md"
RAW_PREFIX = "external_pilot_condition_"
EVIDENCE_BOUNDARY = "pilot_logistics_not_external_effect_estimate"
MAX_DEFAULT_LIVE_ROWS = 12

PROVIDER_SPECS = {
    "deepseek": ("deepseek-v4-flash", "DEEPSEEK_API_KEY"),
    "kimi": ("kimi-k2.7-code", "MOONSHOT_API_KEY"),
}

PLAN_COLUMNS = [
    "provider",
    "model",
    "condition_case_id",
    "case_id",
    "artifact_id",
    "study_family",
    "source_id",
    "source_owner",
    "ecosystem",
    "case_type",
    "condition",
    "expected_behavior",
    "pilot_status",
    "run_status",
    "resume_status",
    "credential_env",
    "credential_available",
    "content_boundary",
    "raw_output_path",
    "evidence_boundary",
]

READINESS_COLUMNS = [
    "provider",
    "model",
    "credential_env",
    "credential_available",
    "planned_rows",
    "completed_rows",
    "pending_rows",
    "bounded_command",
    "status",
    "evidence_boundary",
]

def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

def credential_available(provider: str) -> bool:
    return bool(os.getenv(PROVIDER_SPECS[provider][1], "").strip())

def completed_keys() -> set[tuple[str, str, str]]:
    keys: set[tuple[str, str, str]] = set()
    for path in sorted(RAW_RESULTS_DIR.glob(f"{RAW_PREFIX}*.jsonl")):
        for record in read_jsonl(path):
            if record.get("run_status") == "completed":
                keys.add((str(record.get("provider", "")), str(record.get("model", "")), str(record.get("condition_case_id", ""))))
    return keys

def load_payload_lookup() -> dict[str, dict[str, Any]]:
    return {row["condition_case_id"]: row for row in read_jsonl(PAYLOAD_JSONL_PATH)}


def select_rows(
    rows: list[dict[str, str]],
    provider: str | None,
    model: str | None,
    sample_limit: int | None,
    completed: set[tuple[str, str, str]],
    *,
    resume: bool,
) -> list[dict[str, str]]:
    selected = [
        row
        for row in rows
        if (provider is None or row["provider"] == provider)
        and (model is None or row["model"] == model)
        and (not resume or (row["provider"], row["model"], row["condition_case_id"]) not in completed)
    ]
    if sample_limit is not None:
        if sample_limit < 1:
            raise ValueError("sample-limit must be positive")
        selected = selected[:sample_limit]
    return selected


def build_plan_rows(
    plan_rows: list[dict[str, str]],
    payload_lookup: dict[str, dict[str, Any]],
    completed: set[tuple[str, str, str]],
    *,
    run_status: str,
    raw_output_path: str = "",
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in plan_rows:
        payload = payload_lookup.get(row["condition_case_id"])
        if payload is None:
            raise ValueError(f"Missing payload for {row['condition_case_id']}")
        key = (row["provider"], row["model"], row["condition_case_id"])
        resume_status = "already_completed" if key in completed else "pending"
        status = "completed" if resume_status == "already_completed" and run_status == "not_run" else run_status
        rows.append(
            {
                **{field: row[field] for field in PLAN_COLUMNS if field in row},
                "run_status": status,
                "resume_status": resume_status,
                "credential_env": PROVIDER_SPECS[row["provider"]][1],
                "credential_available": str(credential_available(row["provider"])).lower(),
                "content_boundary": payload["content_boundary"],
                "raw_output_path": raw_output_path,
                "evidence_boundary": EVIDENCE_BOUNDARY,
            }
        )
    return rows


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_plan_markdown(path: Path, title: str, description: str, rows: list[dict[str, Any]]) -> None:
    status_counts = Counter(row["run_status"] for row in rows)
    provider_counts = Counter(f"{row['provider']}::{row['model']}" for row in rows)
    condition_counts = Counter(row["condition"] for row in rows)
    lines = [
        f"# {title}",
        "",
        description,
        "",
        "## Totals",
        "",
        markdown_table(["Metric", "Count"], [["Rows", str(len(rows))], *[[key, str(value)] for key, value in sorted(status_counts.items())]]),
        "",
        "## Providers",
        "",
        markdown_table(["Provider/model", "Rows"], [[key, str(value)] for key, value in sorted(provider_counts.items())]),
        "",
        "## Conditions",
        "",
        markdown_table(["Condition", "Rows"], [[key, str(value)] for key, value in sorted(condition_counts.items())]),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_readiness(all_rows: list[dict[str, str]], completed: set[tuple[str, str, str]]) -> None:
    rows: list[dict[str, Any]] = []
    for provider, (model, env_name) in PROVIDER_SPECS.items():
        provider_rows = [row for row in all_rows if row["provider"] == provider and row["model"] == model]
        completed_count = sum(1 for row in provider_rows if (provider, model, row["condition_case_id"]) in completed)
        available = credential_available(provider)
        rows.append(
            {
                "provider": provider,
                "model": model,
                "credential_env": env_name,
                "credential_available": str(available).lower(),
                "planned_rows": len(provider_rows),
                "completed_rows": completed_count,
                "pending_rows": len(provider_rows) - completed_count,
                "bounded_command": f"python scripts/run_external_pilot_experiment.py --run-live --provider {provider} --model {model} --sample-limit 4 --max-live-rows 4",
                "status": "ready_for_bounded_pilot_slice" if available else "not_run_missing_credentials",
                "evidence_boundary": EVIDENCE_BOUNDARY,
            }
        )
    write_csv_rows(READINESS_CSV_PATH, READINESS_COLUMNS, rows)
    lines = [
        "# External Pilot Provider Readiness",
        "",
        "This no-secret readiness file records whether bounded pilot slices can run. It does not report external effect estimates.",
        "",
        markdown_table(
            ["Provider", "Model", "Credential env", "Credential available", "Pending rows", "Status"],
            [[row["provider"], row["model"], row["credential_env"], row["credential_available"], str(row["pending_rows"]), row["status"]] for row in rows],
        ),
        "",
    ]
    READINESS_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def failure_record(row: dict[str, Any], provider: str, model: str, elapsed_ms: float, error_type: str, run_id: str, batch_id: str) -> dict[str, Any]:
    return {
        "payload_id": row["payload_id"],
        "run_id": run_id,
        "batch_id": batch_id,
        "condition_case_id": row["condition_case_id"],
        "case_id": row["case_id"],
        "artifact_id": row["artifact_id"],
        "source_id": row["source_id"],
        "artifact_family_group": row["artifact_family_group"],
        "case_type": row["case_type"],
        "condition": row["condition"],
        "provider": provider,
        "model": model,
        "run_status": "failed",
        "expected_behavior": row["expected_behavior"],
        "predicted_behavior": "invalid",
        "risk_label": row["risk_label"],
        "constraint_pass": None,
        "parse_success": False,
        "latency_ms": round(elapsed_ms, 3),
        "input_tokens": None,
        "output_tokens": None,
        "error_type": error_type,
        "shard_id": row["shard_id"],
        "prompt_hash": "",
        "representation_hash": sha256_text(row["artifact_representation"]),
        "model_version": model,
        "temperature": 0 if provider == "deepseek" else None,
        "max_tokens": None,
        "finish_reason": "",
        "usage": None,
        "rationale": "",
        "retry_count": 0,
    }


def run_live(selected_rows: list[dict[str, str]], payload_lookup: dict[str, dict[str, Any]], provider: str, model: str) -> Path:
    config, skip_reason = resolve_provider_config(provider=provider, model=model)
    if config is None:
        raise RuntimeError(skip_reason or "not run: missing credentials")
    records: list[dict[str, Any]] = []
    run_id = f"external-pilot-{filename_timestamp()}"
    batch_id = f"{provider}-{model}-{len(selected_rows)}"
    for plan_row in selected_rows:
        payload = payload_lookup[plan_row["condition_case_id"]]
        started = time.perf_counter()
        try:
            prompt = render_payload_prompt(payload)
            response_text, response_json = call_model(prompt, config)
            elapsed_ms = (time.perf_counter() - started) * 1000
            records.append(
                normalize_live_result(
                    payload,
                    config.provider,
                    config.model,
                    response_text,
                    response_json,
                    elapsed_ms,
                    prompt_hash=sha256_text(prompt),
                    run_id=run_id,
                    batch_id=batch_id,
                )
            )
        except Exception as error:  # noqa: BLE001
            elapsed_ms = (time.perf_counter() - started) * 1000
            records.append(failure_record(payload, provider, model, elapsed_ms, type(error).__name__, run_id, batch_id))
    output_path = RAW_RESULTS_DIR / f"{RAW_PREFIX}{filename_timestamp()}.jsonl"
    write_jsonl(output_path, records)
    return output_path
