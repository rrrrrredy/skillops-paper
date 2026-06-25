from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from experiment_utils import (  # noqa: E402
    RESULTS_DIR,
    RAW_RESULTS_DIR,
    call_model,
    ensure_directories,
    filename_timestamp,
    parse_json_object,
    read_text,
    render_prompt_template,
    resolve_provider_config,
    write_csv_rows,
    write_jsonl,
)


PAYLOAD_JSONL_PATH = RESULTS_DIR / "external_representation_payloads.jsonl"
RUN_PLAN_CSV_PATH = RESULTS_DIR / "external_payload_run_plan.csv"
RUN_PLAN_MD_PATH = RESULTS_DIR / "external_payload_run_plan.md"
MAX_DEFAULT_LIVE_ROWS = 25

PLAN_COLUMNS = [
    "payload_id",
    "condition_case_id",
    "artifact_id",
    "source_id",
    "case_type",
    "condition",
    "shard_id",
    "provider",
    "model",
    "prompt_path",
    "run_status",
    "content_boundary",
]

ALLOWED_PREDICTED_BEHAVIORS = {
    "trigger",
    "no_trigger",
    "clarify_scope",
    "apply_constraint_or_refuse",
    "invalid",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dry-run or bounded live execution for external representation payloads.")
    parser.add_argument("--dry-run", action="store_true", help="Validate payload selection and write a run plan.")
    parser.add_argument("--run-live", action="store_true", help="Run bounded live execution for selected payloads.")
    parser.add_argument("--provider", choices=["openai", "anthropic", "deepseek", "moonshot", "kimi"], help="Provider for live execution.")
    parser.add_argument("--model", help="Model name for live execution.")
    parser.add_argument("--shard", help="Optional shard id such as external-shard-001.")
    parser.add_argument("--sample-limit", type=int, help="Maximum selected rows to include.")
    parser.add_argument("--max-live-rows", type=int, default=MAX_DEFAULT_LIVE_ROWS, help="Safety cap for one live invocation.")
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def select_payloads(payloads: list[dict[str, Any]], shard: str | None, sample_limit: int | None) -> list[dict[str, Any]]:
    selected = [row for row in payloads if shard is None or row["shard_id"] == shard]
    if shard is not None and not selected:
        raise ValueError(f"No payload rows found for shard {shard}")
    if sample_limit is not None:
        if sample_limit < 1:
            raise ValueError("sample-limit must be positive")
        selected = selected[:sample_limit]
    return selected


def validate_payloads(payloads: list[dict[str, Any]]) -> None:
    if len(payloads) != 2880:
        raise ValueError(f"Expected 2880 payload rows, found {len(payloads)}")
    payload_ids = [row["payload_id"] for row in payloads]
    if len(payload_ids) != len(set(payload_ids)):
        raise ValueError("Duplicate payload_id values")
    condition_ids = [row["condition_case_id"] for row in payloads]
    if len(condition_ids) != len(set(condition_ids)):
        raise ValueError("Duplicate condition_case_id values")
    for row in payloads:
        if row["payload_status"] != "template_ready_not_run":
            raise ValueError(f"Unexpected payload status: {row['payload_status']}")
        if row["content_boundary"] != "metadata_only_no_third_party_prose_or_code_copied":
            raise ValueError(f"Unexpected content boundary: {row['content_boundary']}")


def build_plan_rows(payloads: list[dict[str, Any]], provider: str | None, model: str | None, status: str) -> list[dict[str, Any]]:
    return [
        {
            "payload_id": row["payload_id"],
            "condition_case_id": row["condition_case_id"],
            "artifact_id": row["artifact_id"],
            "source_id": row["source_id"],
            "case_type": row["case_type"],
            "condition": row["condition"],
            "shard_id": row["shard_id"],
            "provider": provider or "",
            "model": model or "",
            "prompt_path": row["prompt_path"],
            "run_status": status,
            "content_boundary": row["content_boundary"],
        }
        for row in payloads
    ]


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_plan_markdown(rows: list[dict[str, Any]], run_mode: str) -> None:
    condition_counts: dict[str, int] = {}
    shard_counts: dict[str, int] = {}
    for row in rows:
        condition_counts[row["condition"]] = condition_counts.get(row["condition"], 0) + 1
        shard_counts[row["shard_id"]] = shard_counts.get(row["shard_id"], 0) + 1
    lines = [
        "# External Payload Run Plan",
        "",
        "This report records selected external payload rows for execution planning. It does not report external model results.",
        "",
        "## Totals",
        "",
        markdown_table(
            ["Quantity", "Count"],
            [
                ["Selected payload rows", str(len(rows))],
                ["Run mode", run_mode],
            ],
        ),
        "",
        "## Conditions",
        "",
        markdown_table(
            ["Condition", "Rows"],
            [[condition, str(count)] for condition, count in sorted(condition_counts.items())],
        ),
        "",
        "## Shards",
        "",
        markdown_table(
            ["Shard", "Rows"],
            [[shard, str(count)] for shard, count in sorted(shard_counts.items())],
        ),
        "",
    ]
    RUN_PLAN_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def render_payload_prompt(row: dict[str, Any]) -> str:
    template = read_text(REPO_ROOT / row["prompt_path"])
    return render_prompt_template(
        template,
        {
            "CONDITION_CASE_ID": row["condition_case_id"],
            "ARTIFACT_REPRESENTATION": row["artifact_representation"],
            "USER_REQUEST": row["user_request"],
        },
    )


def normalize_live_result(row: dict[str, Any], provider: str, model: str, response_text: str, response_json: Any, elapsed_ms: float) -> dict[str, Any]:
    parsed = parse_json_object(response_text)
    parsed_ok = isinstance(parsed, dict)
    predicted_behavior = "invalid"
    constraint_pass: bool | None = None
    error_type = ""
    if parsed_ok:
        predicted_behavior = str(parsed.get("predicted_behavior", "invalid")).strip()
        if predicted_behavior not in ALLOWED_PREDICTED_BEHAVIORS:
            predicted_behavior = "invalid"
        raw_constraint = parsed.get("constraint_pass")
        if isinstance(raw_constraint, bool) or raw_constraint is None:
            constraint_pass = raw_constraint
        else:
            constraint_pass = None
    else:
        error_type = "parse_error"

    return {
        "condition_case_id": row["condition_case_id"],
        "case_id": row["case_id"],
        "artifact_id": row["artifact_id"],
        "source_id": row["source_id"],
        "artifact_family_group": row["artifact_family_group"],
        "case_type": row["case_type"],
        "condition": row["condition"],
        "provider": provider,
        "model": model,
        "run_status": "completed",
        "expected_behavior": row["expected_behavior"],
        "predicted_behavior": predicted_behavior,
        "risk_label": row["risk_label"],
        "constraint_pass": constraint_pass,
        "parse_success": parsed_ok,
        "latency_ms": round(elapsed_ms, 3),
        "input_tokens": None,
        "output_tokens": None,
        "error_type": error_type,
    }


def run_live(selected: list[dict[str, Any]], provider: str | None, model: str | None, max_live_rows: int) -> Path:
    if max_live_rows < 1:
        raise ValueError("max-live-rows must be positive")
    if len(selected) > max_live_rows:
        raise ValueError(f"Refusing to run {len(selected)} rows; max-live-rows is {max_live_rows}")
    config, skip_reason = resolve_provider_config(provider=provider, model=model)
    if config is None:
        raise RuntimeError(skip_reason or "provider configuration unavailable")

    records: list[dict[str, Any]] = []
    for row in selected:
        prompt = render_payload_prompt(row)
        started = time.perf_counter()
        response_text, response_json = call_model(prompt, config)
        elapsed_ms = (time.perf_counter() - started) * 1000
        records.append(normalize_live_result(row, config.provider, config.model, response_text, response_json, elapsed_ms))

    output_path = RAW_RESULTS_DIR / f"external_condition_{filename_timestamp()}.jsonl"
    write_jsonl(output_path, records)
    return output_path


def run_dry_plan(selected: list[dict[str, Any]], provider: str | None, model: str | None) -> None:
    plan_rows = build_plan_rows(selected, provider, model, "not_run")
    write_csv_rows(RUN_PLAN_CSV_PATH, PLAN_COLUMNS, plan_rows)
    write_plan_markdown(plan_rows, "dry_run")


def main() -> int:
    args = parse_args()
    if not args.dry_run and not args.run_live:
        args.dry_run = True

    payloads = read_jsonl(PAYLOAD_JSONL_PATH)
    validate_payloads(payloads)
    selected = select_payloads(payloads, args.shard, args.sample_limit)
    if not selected:
        raise ValueError("No payload rows selected")

    if args.dry_run:
        run_dry_plan(selected, args.provider, args.model)
        print(f"Wrote {RUN_PLAN_CSV_PATH.relative_to(REPO_ROOT)}")
        print(f"Wrote {RUN_PLAN_MD_PATH.relative_to(REPO_ROOT)}")
        return 0

    if args.sample_limit is None:
        raise ValueError("Live execution requires --sample-limit")
    output_path = run_live(selected, args.provider, args.model, args.max_live_rows)
    print(f"Wrote {output_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
