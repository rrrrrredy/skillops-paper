from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent


if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from experiment_utils import (  # noqa: E402
    EXPERIMENTS_DIR,
    PROMPTS_DIR,
    RAW_RESULTS_DIR,
    RESULTS_DIR,
    SCHEMAS_DIR,
    call_model,
    coerce_bool,
    detect_provider_env_vars,
    ensure_directories,
    filename_timestamp,
    format_metric,
    load_csv_rows,
    load_json,
    markdown_table,
    parse_json_object,
    read_text,
    relative_display,
    render_prompt_template,
    resolve_provider_config,
    safe_divide,
    utc_timestamp,
    write_csv_rows,
    write_jsonl,
)


MEMORY_DRIFT_COLUMNS = [
    "case_id",
    "scenario",
    "current_instruction",
    "current_memory",
    "stale_memory",
    "retirement_marker",
    "expected_behavior",
    "stale_info_trap",
    "relevant_artifact",
    "notes",
]

PROMPT_PATHS = {
    "full_skillops_memory_policy": PROMPTS_DIR / "memory_drift_full_skillops.md",
    "no_forgetting_policy": PROMPTS_DIR / "memory_drift_no_forgetting.md",
    "current_context_only": PROMPTS_DIR / "memory_drift_current_only.md",
}
SCHEMA_PATH = SCHEMAS_DIR / "memory_drift_result_schema.json"
MEMORY_DRIFT_CASES_PATH = EXPERIMENTS_DIR / "memory_drift_cases.csv"
METRICS_CSV_PATH = RESULTS_DIR / "memory_drift_metrics.csv"
METRICS_MD_PATH = RESULTS_DIR / "memory_drift_metrics.md"


def validate_setup() -> tuple[list[dict[str, str]], dict[str, str]]:
    """Validate all input files and prompt templates. Return cases and templates."""
    drift_rows = load_csv_rows(MEMORY_DRIFT_CASES_PATH, MEMORY_DRIFT_COLUMNS)
    load_json(SCHEMA_PATH)

    templates: dict[str, str] = {}
    for condition, path in PROMPT_PATHS.items():
        template = read_text(path)
        # Check required placeholders per condition
        if condition == "full_skillops_memory_policy":
            required = ("{{CURRENT_INSTRUCTION}}", "{{CURRENT_MEMORY}}", "{{STALE_MEMORY}}",
                        "{{RETIREMENT_MARKER}}", "{{CASE_ID}}", "{{SCENARIO}}")
        elif condition == "no_forgetting_policy":
            required = ("{{CURRENT_INSTRUCTION}}", "{{CURRENT_MEMORY}}", "{{STALE_MEMORY}}",
                        "{{CASE_ID}}", "{{SCENARIO}}")
        else:  # current_context_only
            required = ("{{CURRENT_INSTRUCTION}}", "{{CURRENT_MEMORY}}",
                        "{{CASE_ID}}", "{{SCENARIO}}")
        for placeholder in required:
            if placeholder not in template:
                raise ValueError(f"Missing placeholder {placeholder} in {path}")
        templates[condition] = template

    # Render a test prompt to verify template completeness
    first_row = drift_rows[0]
    for condition, template in templates.items():
        replacements = _build_replacements(condition, first_row)
        render_prompt_template(template, replacements)

    return drift_rows, templates


def _build_replacements(condition: str, case_row: dict[str, str]) -> dict[str, str]:
    """Build replacement dict for a given condition and case row."""
    replacements: dict[str, str] = {
        "CURRENT_INSTRUCTION": case_row["current_instruction"],
        "CURRENT_MEMORY": case_row["current_memory"],
        "CASE_ID": case_row["case_id"],
        "SCENARIO": case_row["scenario"],
    }
    if condition == "full_skillops_memory_policy":
        replacements["STALE_MEMORY"] = case_row["stale_memory"]
        replacements["RETIREMENT_MARKER"] = case_row["retirement_marker"]
    elif condition == "no_forgetting_policy":
        replacements["STALE_MEMORY"] = case_row["stale_memory"]
    # current_context_only has no stale memory or retirement marker
    return replacements


def normalize_result(case_row: dict[str, str], condition: str, parsed_json: Any) -> dict[str, Any]:
    """Normalize the parsed JSON response into a structured result dict."""
    parsed_ok = isinstance(parsed_json, dict)
    normalized: dict[str, Any] = {
        "case_id": case_row["case_id"],
        "condition": condition,
        "expected_behavior": case_row["expected_behavior"],
        "stale_info_trap": case_row["stale_info_trap"],
        "used_stale_info": False,
        "followed_current_instruction": False,
        "applied_forgetting": False,
        "conflict_resolution_applied": False,
        "response_action": "",
        "rationale": "",
        "parsed_ok": parsed_ok,
    }
    if parsed_ok:
        normalized["used_stale_info"] = coerce_bool(parsed_json.get("used_stale_info"))
        normalized["followed_current_instruction"] = coerce_bool(
            parsed_json.get("followed_current_instruction")
        )
        normalized["applied_forgetting"] = coerce_bool(parsed_json.get("applied_forgetting"))
        normalized["conflict_resolution_applied"] = coerce_bool(
            parsed_json.get("conflict_resolution_applied")
        )
        normalized["response_action"] = str(parsed_json.get("response_action", "")).strip()
        normalized["rationale"] = str(parsed_json.get("rationale", "")).strip()
    return normalized


def compute_metric_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Compute per-condition metrics from normalized results."""
    rows: list[dict[str, Any]] = []
    for condition in ("full_skillops_memory_policy", "no_forgetting_policy", "current_context_only"):
        normalized = [
            record["normalized_result"]
            for record in records
            if record["normalized_result"]["condition"] == condition
        ]
        total = len(normalized)
        if total == 0:
            continue

        stale_usage_hits = sum(1 for row in normalized if row["used_stale_info"])
        current_adherence_hits = sum(1 for row in normalized if row["followed_current_instruction"])
        forgetting_hits = sum(1 for row in normalized if row["applied_forgetting"])
        conflict_hits = sum(1 for row in normalized if row["conflict_resolution_applied"])
        # unsupported_memory_claim: used stale info AND did not follow current instruction
        unsupported_claim_hits = sum(
            1 for row in normalized
            if row["used_stale_info"] and not row["followed_current_instruction"]
        )

        metric_specs = [
            ("stale_info_usage_rate", safe_divide(stale_usage_hits, total), stale_usage_hits, total),
            ("current_instruction_adherence_rate", safe_divide(current_adherence_hits, total), current_adherence_hits, total),
            ("correct_forgetting_rate", safe_divide(forgetting_hits, total), forgetting_hits, total),
            ("conflict_resolution_success_rate", safe_divide(conflict_hits, total), conflict_hits, total),
            ("unsupported_memory_claim_rate", safe_divide(unsupported_claim_hits, total), unsupported_claim_hits, total),
        ]
        for metric_name, metric_value, numerator, denominator in metric_specs:
            rows.append({
                "condition": condition,
                "metric": metric_name,
                "value": "" if metric_value is None else f"{metric_value:.6f}",
                "numerator": numerator,
                "denominator": denominator,
                "notes": "",
            })
    return rows


def write_metrics_markdown(
    metric_rows: list[dict[str, Any]],
    config_provider: str,
    config_model: str,
    raw_output_path: Path,
) -> None:
    """Write a markdown summary of the metrics."""
    lines = [
        "# Memory Drift Detection Metrics",
        "",
        "These metrics were generated from an actual live run.",
        "",
        f"- Provider: `{config_provider}`",
        f"- Model: `{config_model}`",
        f"- Raw output: `{relative_display(raw_output_path)}`",
        "",
    ]
    for condition in ("full_skillops_memory_policy", "no_forgetting_policy", "current_context_only"):
        condition_rows = [row for row in metric_rows if row["condition"] == condition]
        if not condition_rows:
            continue
        table_rows = [
            [
                row["metric"],
                format_metric(float(row["value"])) if row["value"] else "n/a",
                f"{row['numerator']}/{row['denominator']}",
            ]
            for row in condition_rows
        ]
        lines.extend([
            f"## {condition}",
            "",
            markdown_table(["Metric", "Value", "Count"], table_rows),
            "",
        ])
    METRICS_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def run_experiment(
    *,
    dry_run: bool = False,
    run_live: bool = False,
    provider: str | None = None,
    model: str | None = None,
    emit_status: bool = True,
) -> dict[str, Any]:
    """Run the Memory Drift Detection experiment."""
    ensure_directories([RESULTS_DIR, RAW_RESULTS_DIR])
    drift_rows, templates = validate_setup()

    status: dict[str, Any] = {
        "experiment": "Memory Drift Detection",
        "prepared": True,
        "dry_run_passed": False,
        "live_status": "live run skipped",
        "metrics_files": [],
        "raw_output_files": [],
        "credentials": detect_provider_env_vars(),
    }

    if emit_status:
        print("Memory Drift Detection: prepared")

    if dry_run:
        status["dry_run_passed"] = True
        if emit_status:
            print("Memory Drift Detection: dry-run passed")

    if not run_live:
        if emit_status:
            print("Memory Drift Detection: live run skipped")
        return status

    config, error = resolve_provider_config(provider=provider, model=model)
    if error is not None:
        status["live_status"] = error
        if emit_status:
            print(f"Memory Drift Detection: {error}")
        return status

    records: list[dict[str, Any]] = []
    for condition, prompt_path in PROMPT_PATHS.items():
        template = templates[condition]
        for case_row in drift_rows:
            replacements = _build_replacements(condition, case_row)
            prompt = render_prompt_template(template, replacements)
            started_at = utc_timestamp()
            response_text, provider_response_json = call_model(prompt, config)
            completed_at = utc_timestamp()
            parsed_json = parse_json_object(response_text)
            normalized_result = normalize_result(case_row, condition, parsed_json)
            records.append({
                "raw_output": {
                    "experiment": "memory_drift_detection",
                    "case_id": case_row["case_id"],
                    "condition": condition,
                    "provider": config.provider,
                    "model": config.model,
                    "prompt_path": relative_display(prompt_path),
                    "case_input": case_row,
                    "response_text": response_text,
                    "response_json": provider_response_json,
                    "started_at_utc": started_at,
                    "completed_at_utc": completed_at,
                },
                "normalized_result": normalized_result,
            })

    raw_output_path = RAW_RESULTS_DIR / f"memory_drift_{filename_timestamp()}.jsonl"
    write_jsonl(raw_output_path, records)

    metric_rows = compute_metric_rows(records)
    write_csv_rows(
        METRICS_CSV_PATH,
        ["condition", "metric", "value", "numerator", "denominator", "notes"],
        metric_rows,
    )
    write_metrics_markdown(metric_rows, config.provider, config.model, raw_output_path)

    status["live_status"] = "live run completed"
    status["metrics_files"] = [
        relative_display(METRICS_CSV_PATH),
        relative_display(METRICS_MD_PATH),
    ]
    status["raw_output_files"] = [relative_display(raw_output_path)]

    if emit_status:
        print("Memory Drift Detection: live run completed")

    return status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Memory Drift Detection experiment.")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and prompts without model calls.")
    parser.add_argument("--run-live", action="store_true", help="Execute live model calls.")
    parser.add_argument("--provider", choices=["openai", "anthropic", "longcat"], help="Preferred model provider.")
    parser.add_argument("--model", help="Model name for live execution.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.dry_run and not args.run_live:
        args.dry_run = True

    result = run_experiment(
        dry_run=args.dry_run,
        run_live=args.run_live,
        provider=args.provider,
        model=args.model,
        emit_status=True,
    )
    return 0 if result["prepared"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
