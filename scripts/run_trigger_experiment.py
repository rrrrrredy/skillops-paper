from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent


if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from experiment_utils import (  # noqa: E402
    ALLOWED_TRIGGER_LABELS,
    BENCHMARK_DIR,
    PROMPTS_DIR,
    RAW_RESULTS_DIR,
    RESULTS_DIR,
    SCHEMAS_DIR,
    SKILL_SAMPLE_COLUMNS,
    TRIGGER_CASE_COLUMNS,
    call_model,
    detect_provider_env_vars,
    ensure_directories,
    filename_timestamp,
    format_metric,
    load_csv_rows,
    load_json,
    markdown_table,
    parse_json_object,
    precision_recall_f1,
    read_text,
    relative_display,
    render_prompt_template,
    resolve_provider_config,
    safe_divide,
    utc_timestamp,
    write_csv_rows,
    write_jsonl,
)


PROMPT_PATHS = {
    "skillops": PROMPTS_DIR / "trigger_routing_skillops.md",
    "freeform": PROMPTS_DIR / "trigger_routing_freeform.md",
}
SCHEMA_PATH = SCHEMAS_DIR / "trigger_result_schema.json"
TRIGGER_CASES_PATH = BENCHMARK_DIR / "trigger_cases.csv"
SKILL_SAMPLES_PATH = BENCHMARK_DIR / "skill_samples.csv"
METRICS_CSV_PATH = RESULTS_DIR / "trigger_metrics.csv"
METRICS_MD_PATH = RESULTS_DIR / "trigger_metrics.md"


def build_skillops_catalog(skill_rows: list[dict[str, str]]) -> str:
    blocks: list[str] = []
    for row in skill_rows:
        blocks.append(f"Skill: {row['artifact_name']}")
        blocks.append(f"Purpose: {row['purpose']}")
        blocks.append(f"Activation boundary: {row['trigger_contract']}")
        blocks.append(f"Execution constraints: {row['execution_constraints']}")
        blocks.append(f"Security checks: {row['security_checks']}")
        blocks.append("")
    return "\n".join(blocks).strip()


def build_freeform_catalog(skill_rows: list[dict[str, str]]) -> str:
    blocks: list[str] = []
    for row in skill_rows:
        blocks.append(
            f"{row['artifact_name']}: {row['purpose']} {row['trigger_contract']} "
            f"{row['execution_constraints']}"
        )
    return "\n".join(blocks)


def validate_setup() -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, str]]:
    trigger_rows = load_csv_rows(TRIGGER_CASES_PATH, TRIGGER_CASE_COLUMNS)
    skill_rows = load_csv_rows(SKILL_SAMPLES_PATH, SKILL_SAMPLE_COLUMNS)
    load_json(SCHEMA_PATH)

    templates: dict[str, str] = {}
    for variant, path in PROMPT_PATHS.items():
        template = read_text(path)
        for placeholder in ("{{SKILL_CATALOG}}", "{{CASE_ID}}", "{{USER_REQUEST}}"):
            if placeholder not in template:
                raise ValueError(f"Missing placeholder {placeholder} in {path}")
        templates[variant] = template

    catalog_variants = {
        "skillops": build_skillops_catalog(skill_rows),
        "freeform": build_freeform_catalog(skill_rows),
    }
    for variant, template in templates.items():
        render_prompt_template(
            template,
            {
                "SKILL_CATALOG": catalog_variants[variant],
                "CASE_ID": trigger_rows[0]["case_id"],
                "USER_REQUEST": trigger_rows[0]["user_request"],
            },
        )

    return trigger_rows, skill_rows, templates


def normalize_result(case_row: dict[str, str], prompt_variant: str, parsed_json: Any) -> dict[str, Any]:
    parsed_ok = isinstance(parsed_json, dict)
    predicted_label = ""
    predicted_skill = "none"
    confidence = "unknown"
    ambiguity_reason = ""
    rationale = ""

    if parsed_ok:
        predicted_label = str(parsed_json.get("predicted_label", "")).strip()
        predicted_skill = str(parsed_json.get("predicted_skill", "none")).strip() or "none"
        confidence = str(parsed_json.get("confidence", "unknown")).strip() or "unknown"
        ambiguity_reason = str(parsed_json.get("ambiguity_reason", "")).strip()
        rationale = str(parsed_json.get("rationale", "")).strip()

    if predicted_label not in ALLOWED_TRIGGER_LABELS:
        predicted_label = "invalid"

    return {
        "case_id": case_row["case_id"],
        "prompt_variant": prompt_variant,
        "expected_label": case_row["expected_label"],
        "expected_skill": case_row["relevant_skill"],
        "predicted_label": predicted_label,
        "predicted_skill": predicted_skill,
        "confidence": confidence,
        "ambiguity_reason": ambiguity_reason,
        "rationale": rationale,
        "parsed_ok": parsed_ok,
    }


def compute_metric_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for prompt_variant in ("skillops", "freeform"):
        normalized = [
            record["normalized_result"]
            for record in records
            if record["normalized_result"]["prompt_variant"] == prompt_variant
        ]
        true_positive = sum(
            1
            for row in normalized
            if row["expected_label"] == "should_trigger" and row["predicted_label"] == "should_trigger"
        )
        false_positive = sum(
            1
            for row in normalized
            if row["expected_label"] != "should_trigger" and row["predicted_label"] == "should_trigger"
        )
        false_negative = sum(
            1
            for row in normalized
            if row["expected_label"] == "should_trigger" and row["predicted_label"] != "should_trigger"
        )
        metrics = precision_recall_f1(true_positive, false_positive, false_negative)

        should_not_trigger_cases = [row for row in normalized if row["expected_label"] == "should_not_trigger"]
        false_trigger_hits = sum(1 for row in should_not_trigger_cases if row["predicted_label"] == "should_trigger")
        ambiguity_cases = [row for row in normalized if row["expected_label"] == "ambiguous"]
        ambiguity_hits = sum(1 for row in ambiguity_cases if row["predicted_label"] == "ambiguous")

        metric_specs = [
            ("precision", metrics["precision"], true_positive, true_positive + false_positive),
            ("recall", metrics["recall"], true_positive, true_positive + false_negative),
            ("f1", metrics["f1"], true_positive, true_positive + false_positive + false_negative),
            (
                "false_trigger_rate_on_should_not_trigger",
                safe_divide(false_trigger_hits, len(should_not_trigger_cases)),
                false_trigger_hits,
                len(should_not_trigger_cases),
            ),
            (
                "ambiguity_handling_rate",
                safe_divide(ambiguity_hits, len(ambiguity_cases)),
                ambiguity_hits,
                len(ambiguity_cases),
            ),
        ]

        for metric_name, metric_value, numerator, denominator in metric_specs:
            rows.append(
                {
                    "prompt_variant": prompt_variant,
                    "metric": metric_name,
                    "value": "" if metric_value is None else f"{metric_value:.6f}",
                    "numerator": numerator,
                    "denominator": denominator,
                    "notes": "",
                }
            )
    return rows


def write_metrics_markdown(metric_rows: list[dict[str, Any]], config_provider: str, config_model: str, raw_output_path: Path) -> None:
    lines = [
        "# Trigger Routing Accuracy Metrics",
        "",
        "These metrics were generated from an actual live run.",
        "",
        f"- Provider: `{config_provider}`",
        f"- Model: `{config_model}`",
        f"- Raw output: `{relative_display(raw_output_path)}`",
        "",
    ]
    for prompt_variant in ("skillops", "freeform"):
        variant_rows = [row for row in metric_rows if row["prompt_variant"] == prompt_variant]
        table_rows = [
            [
                row["metric"],
                format_metric(float(row["value"])) if row["value"] else "n/a",
                f"{row['numerator']}/{row['denominator']}",
            ]
            for row in variant_rows
        ]
        lines.extend(
            [
                f"## {prompt_variant}",
                "",
                markdown_table(["Metric", "Value", "Count"], table_rows),
                "",
            ]
        )
    METRICS_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def run_experiment(
    *,
    dry_run: bool = False,
    run_live: bool = False,
    provider: str | None = None,
    model: str | None = None,
    emit_status: bool = True,
) -> dict[str, Any]:
    ensure_directories([RESULTS_DIR, RAW_RESULTS_DIR])
    trigger_rows, skill_rows, templates = validate_setup()
    del skill_rows

    status = {
        "experiment": "Trigger Routing Accuracy",
        "prepared": True,
        "dry_run_passed": False,
        "live_status": "live run skipped",
        "metrics_files": [],
        "raw_output_files": [],
        "credentials": detect_provider_env_vars(),
    }

    if emit_status:
        print("Trigger Routing Accuracy: prepared")

    if dry_run:
        status["dry_run_passed"] = True
        if emit_status:
            print("Trigger Routing Accuracy: dry-run passed")

    if not run_live:
        if emit_status:
            print("Trigger Routing Accuracy: live run skipped")
        return status

    config, error = resolve_provider_config(provider=provider, model=model)
    if error is not None:
        status["live_status"] = error
        if emit_status:
            print(f"Trigger Routing Accuracy: {error}")
        return status

    catalogs = {
        "skillops": build_skillops_catalog(load_csv_rows(SKILL_SAMPLES_PATH, SKILL_SAMPLE_COLUMNS)),
        "freeform": build_freeform_catalog(load_csv_rows(SKILL_SAMPLES_PATH, SKILL_SAMPLE_COLUMNS)),
    }
    records: list[dict[str, Any]] = []

    for prompt_variant, prompt_path in PROMPT_PATHS.items():
        template = templates[prompt_variant]
        for case_row in trigger_rows:
            prompt = render_prompt_template(
                template,
                {
                    "SKILL_CATALOG": catalogs[prompt_variant],
                    "CASE_ID": case_row["case_id"],
                    "USER_REQUEST": case_row["user_request"],
                },
            )
            started_at = utc_timestamp()
            response_text, provider_response_json = call_model(prompt, config)
            completed_at = utc_timestamp()
            parsed_json = parse_json_object(response_text)
            normalized_result = normalize_result(case_row, prompt_variant, parsed_json)
            records.append(
                {
                    "raw_output": {
                        "experiment": "trigger_routing_accuracy",
                        "case_id": case_row["case_id"],
                        "prompt_variant": prompt_variant,
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
                }
            )

    raw_output_path = RAW_RESULTS_DIR / f"trigger_{filename_timestamp()}.jsonl"
    write_jsonl(raw_output_path, records)

    metric_rows = compute_metric_rows(records)
    write_csv_rows(
        METRICS_CSV_PATH,
        ["prompt_variant", "metric", "value", "numerator", "denominator", "notes"],
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
        print("Trigger Routing Accuracy: live run completed")

    return status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Trigger Routing Accuracy experiment.")
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
