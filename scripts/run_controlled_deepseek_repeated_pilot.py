from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent


if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import run_ablation_trigger_aligned as aligned_ablation_mod  # noqa: E402
import run_constraint_experiment as constraint_mod  # noqa: E402
import run_memory_drift_experiment as memory_mod  # noqa: E402
import run_security_guard_experiment as security_mod  # noqa: E402
import run_trigger_experiment as trigger_mod  # noqa: E402
from experiment_utils import (  # noqa: E402
    RAW_RESULTS_DIR,
    RESULTS_DIR,
    call_model,
    detect_provider_env_vars,
    ensure_directories,
    filename_timestamp,
    format_metric,
    markdown_table,
    parse_json_object,
    relative_display,
    render_prompt_template,
    resolve_provider_config,
    safe_divide,
    utc_timestamp,
    write_csv_rows,
)


CONTROLLED_TRIGGER_METRICS_CSV = RESULTS_DIR / "controlled_deepseek_trigger_metrics.csv"
CONTROLLED_TRIGGER_METRICS_MD = RESULTS_DIR / "controlled_deepseek_trigger_metrics.md"
CONTROLLED_CONSTRAINT_METRICS_CSV = RESULTS_DIR / "controlled_deepseek_constraint_metrics.csv"
CONTROLLED_CONSTRAINT_METRICS_MD = RESULTS_DIR / "controlled_deepseek_constraint_metrics.md"
CONTROLLED_SECURITY_METRICS_CSV = RESULTS_DIR / "controlled_deepseek_security_metrics.csv"
CONTROLLED_SECURITY_METRICS_MD = RESULTS_DIR / "controlled_deepseek_security_metrics.md"
CONTROLLED_MEMORY_METRICS_CSV = RESULTS_DIR / "controlled_deepseek_memory_metrics.csv"
CONTROLLED_MEMORY_METRICS_MD = RESULTS_DIR / "controlled_deepseek_memory_metrics.md"
CONTROLLED_ABLATION_METRICS_CSV = RESULTS_DIR / "controlled_deepseek_ablation_trigger_metrics.csv"
CONTROLLED_ABLATION_METRICS_MD = RESULTS_DIR / "controlled_deepseek_ablation_trigger_metrics.md"
CONTROLLED_SUMMARY_MD = RESULTS_DIR / "controlled_deepseek_summary.md"
RESEARCH_LOG_PATH = REPO_ROOT / "research-log" / "2026-05-06-controlled-deepseek-repeated-pilot.md"

METRIC_FIELDNAMES = [
    "experiment",
    "group_type",
    "group_value",
    "metric",
    "aggregation",
    "repeat_index",
    "value",
    "numerator",
    "denominator",
    "notes",
]


def prompt_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.6f}"


def parsing_status_for(response_text: str, parsed_json: Any, error: str) -> str:
    if error:
        return "execution_error"
    if not response_text.strip():
        return "empty_response"
    if isinstance(parsed_json, dict):
        return "parsed"
    return "parse_failed"


def append_jsonl_record(path: Path, record: dict[str, Any]) -> None:
    ensure_directories([path.parent])
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write(json.dumps(record, ensure_ascii=True, sort_keys=True))
        handle.write("\n")


def execute_model_prompt(prompt: str, config: Any) -> tuple[str, str, str, Any, str]:
    started_at = utc_timestamp()
    response_text = ""
    provider_response_json: Any = None
    error = ""
    try:
        response_text, provider_response_json = call_model(prompt, config)
    except Exception as exc:  # noqa: BLE001
        error = str(exc)
    completed_at = utc_timestamp()
    return started_at, completed_at, response_text, provider_response_json, error


def values_mean_std(values: list[float | None]) -> tuple[float | None, float | None]:
    numeric_values = [value for value in values if value is not None]
    if not numeric_values:
        return None, None
    if len(numeric_values) == 1:
        return numeric_values[0], 0.0
    return statistics.fmean(numeric_values), statistics.pstdev(numeric_values)


def expand_metric_points(metric_points: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[tuple[str, str, str], dict[str, Any]]]:
    grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
    for point in metric_points:
        key = (point["group_type"], point["group_value"], point["metric"])
        if key not in grouped:
            grouped[key] = {
                "group_type": point["group_type"],
                "group_value": point["group_value"],
                "metric": point["metric"],
                "repeat_rows": [],
            }
        grouped[key]["repeat_rows"].append(point)

    csv_rows: list[dict[str, Any]] = []
    for key in sorted(grouped):
        bucket = grouped[key]
        repeat_rows = sorted(bucket["repeat_rows"], key=lambda item: item["repeat_index"])
        repeat_values = [row["value"] for row in repeat_rows]
        mean_value, std_value = values_mean_std(repeat_values)
        notes = " | ".join(sorted({row["notes"] for row in repeat_rows if row["notes"]}))
        bucket["mean"] = mean_value
        bucket["std"] = std_value
        bucket["notes"] = notes
        for row in repeat_rows:
            csv_rows.append(
                {
                    "experiment": row["experiment"],
                    "group_type": row["group_type"],
                    "group_value": row["group_value"],
                    "metric": row["metric"],
                    "aggregation": "repeat",
                    "repeat_index": row["repeat_index"],
                    "value": format_float(row["value"]),
                    "numerator": row["numerator"],
                    "denominator": row["denominator"],
                    "notes": row["notes"],
                }
            )
        for aggregation, value in (("mean", mean_value), ("std", std_value)):
            csv_rows.append(
                {
                    "experiment": repeat_rows[0]["experiment"],
                    "group_type": repeat_rows[0]["group_type"],
                    "group_value": repeat_rows[0]["group_value"],
                    "metric": repeat_rows[0]["metric"],
                    "aggregation": aggregation,
                    "repeat_index": "",
                    "value": format_float(value),
                    "numerator": "",
                    "denominator": "",
                    "notes": notes,
                }
            )
    return csv_rows, grouped


def write_metrics_markdown(
    path: Path,
    *,
    title: str,
    raw_output_path: Path,
    provider: str,
    model: str,
    repeats: int,
    metric_points: list[dict[str, Any]],
    partial: bool,
) -> None:
    csv_rows, grouped = expand_metric_points(metric_points)
    del csv_rows
    lines = [
        f"# {title}",
        "",
        f"- Provider: `{provider}`",
        f"- Model: `{model}`",
        f"- Repeats: `{repeats}`",
        f"- Raw output: `{relative_display(raw_output_path)}`",
        f"- Status: `{'partial' if partial else 'complete'}`",
        "",
    ]

    sections: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for bucket in grouped.values():
        sections[bucket["group_type"]].append(bucket)

    group_type_order = [
        "condition",
        "overall",
        "risk_type",
        "relevant_artifact",
        "variant",
    ]
    for group_type in group_type_order:
        if group_type not in sections:
            continue
        headers = [group_type, "Metric", "Mean", "Std"]
        headers.extend([f"R{repeat_index}" for repeat_index in range(1, repeats + 1)])
        headers.append("Notes")
        table_rows: list[list[str]] = []
        for bucket in sorted(sections[group_type], key=lambda item: (item["group_value"], item["metric"])):
            repeat_map = {row["repeat_index"]: row for row in bucket["repeat_rows"]}
            row = [
                bucket["group_value"],
                bucket["metric"],
                format_metric(bucket["mean"]),
                format_metric(bucket["std"]),
            ]
            for repeat_index in range(1, repeats + 1):
                repeat_row = repeat_map.get(repeat_index)
                row.append("n/a" if repeat_row is None else format_metric(repeat_row["value"]))
            row.append(bucket["notes"])
            table_rows.append(row)
        lines.extend(
            [
                f"## {group_type}",
                "",
                markdown_table(headers, table_rows),
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")


def incomplete_note(actual: int, expected: int) -> str:
    if actual == expected:
        return ""
    return f"partial {actual}/{expected}"


def completion_flags(actual_ids: set[str], expected_ids: set[str], execution_failures: int) -> tuple[bool, bool]:
    completed = len(actual_ids) == len(expected_ids) and execution_failures == 0
    partial = not completed
    return completed, partial


def precision_recall_f1_from_rows(rows: list[dict[str, Any]]) -> tuple[float | None, float | None, float | None, int, int, int]:
    true_positive = sum(
        1
        for row in rows
        if row["expected_label"] == "should_trigger" and row["predicted_label"] == "should_trigger"
    )
    false_positive = sum(
        1
        for row in rows
        if row["expected_label"] != "should_trigger" and row["predicted_label"] == "should_trigger"
    )
    false_negative = sum(
        1
        for row in rows
        if row["expected_label"] == "should_trigger" and row["predicted_label"] != "should_trigger"
    )
    precision = safe_divide(true_positive, true_positive + false_positive)
    recall = safe_divide(true_positive, true_positive + false_negative)
    if precision is None or recall is None or precision + recall == 0:
        f1 = None if precision is None or recall is None else 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1, true_positive, false_positive, false_negative


def lookup_metric(csv_rows: list[dict[str, Any]], group_type: str, group_value: str, metric: str, aggregation: str = "mean") -> str:
    for row in csv_rows:
        if (
            row["group_type"] == group_type
            and row["group_value"] == group_value
            and row["metric"] == metric
            and row["aggregation"] == aggregation
        ):
            return row["value"] or "n/a"
    return "n/a"


def credential_handling_note(credential_status: str, live_run_performed: bool) -> str:
    if credential_status == "present" and live_run_performed:
        return "DEEPSEEK_API_KEY was provided via local environment variable for the live run; the value was not printed or committed."
    if credential_status == "present":
        return "DEEPSEEK_API_KEY is available in the local environment; the value was not printed or committed."
    return "No DEEPSEEK_API_KEY value was printed or committed."


def topline_metric_lines(slice_results: list[dict[str, Any]], *, wrap_code: bool) -> list[str]:
    def metric(slice_index: int, group_type: str, group_value: str, metric_name: str) -> str:
        value = lookup_metric(slice_results[slice_index]["csv_rows"], group_type, group_value, metric_name)
        return f"`{value}`" if wrap_code else value

    lines = [
        "### Trigger",
        "",
        f"- skillops mean F1: {metric(0, 'condition', 'skillops', 'f1')}",
        f"- freeform mean F1: {metric(0, 'condition', 'freeform', 'f1')}",
        f"- skillops false-trigger rate: {metric(0, 'condition', 'skillops', 'false_trigger_rate')}",
        f"- freeform false-trigger rate: {metric(0, 'condition', 'freeform', 'false_trigger_rate')}",
        "",
        "### Constraint",
        "",
        f"- skillops compliance mean: {metric(1, 'condition', 'skillops', 'constraint_compliance_rate')}",
        f"- vague compliance mean: {metric(1, 'condition', 'vague', 'constraint_compliance_rate')}",
        f"- skillops violation rate mean: {metric(1, 'condition', 'skillops', 'violation_rate')}",
        f"- vague violation rate mean: {metric(1, 'condition', 'vague', 'violation_rate')}",
        "",
        "### Security",
        "",
        f"- detection rate mean: {metric(2, 'overall', 'all', 'detection_rate')}",
        f"- false-positive rate mean: {metric(2, 'overall', 'all', 'false_positive_rate')}",
        f"- specificity mean: {metric(2, 'overall', 'all', 'specificity')}",
        "",
        "### Memory",
        "",
        f"- full policy stale-info usage mean: {metric(3, 'condition', 'full_skillops_memory_policy', 'stale_info_usage_rate')}",
        f"- no-forgetting stale-info usage mean: {metric(3, 'condition', 'no_forgetting_policy', 'stale_info_usage_rate')}",
        f"- current-context-only stale-info usage mean: {metric(3, 'condition', 'current_context_only', 'stale_info_usage_rate')}",
        f"- full policy current-instruction adherence mean: {metric(3, 'condition', 'full_skillops_memory_policy', 'current_instruction_adherence_rate')}",
        f"- no-forgetting current-instruction adherence mean: {metric(3, 'condition', 'no_forgetting_policy', 'current_instruction_adherence_rate')}",
        f"- current-context-only current-instruction adherence mean: {metric(3, 'condition', 'current_context_only', 'current_instruction_adherence_rate')}",
        f"- full policy correct-forgetting mean: {metric(3, 'condition', 'full_skillops_memory_policy', 'correct_forgetting_rate')}",
        f"- no-forgetting correct-forgetting mean: {metric(3, 'condition', 'no_forgetting_policy', 'correct_forgetting_rate')}",
        "",
        "### Aligned ablation",
        "",
        f"- full_skillops mean F1: {metric(4, 'variant', 'full_skillops', 'f1')}",
        f"- no_trigger_boundary mean F1: {metric(4, 'variant', 'no_trigger_boundary', 'f1')}",
        f"- freeform_only mean F1: {metric(4, 'variant', 'freeform_only', 'f1')}",
        f"- full_skillops false-trigger rate: {metric(4, 'variant', 'full_skillops', 'false_trigger_rate')}",
        f"- no_trigger_boundary false-trigger rate: {metric(4, 'variant', 'no_trigger_boundary', 'false_trigger_rate')}",
        f"- freeform_only false-trigger rate: {metric(4, 'variant', 'freeform_only', 'false_trigger_rate')}",
        "",
    ]
    return lines


def write_summary_files(
    *,
    provider: str,
    model: str,
    repeats: int,
    credential_status: str,
    live_run_performed: bool,
    slice_results: list[dict[str, Any]],
) -> None:
    lines = [
        "# Controlled DeepSeek Repeated Pilot Summary",
        "",
        f"- Provider: `{provider}`",
        f"- Model: `{model}`",
        f"- Repeats: `{repeats}`",
        f"- Credential handling: {credential_handling_note(credential_status, live_run_performed)}",
        f"- Live run performed: `{'yes' if live_run_performed else 'no'}`",
        "",
        "## Slice Status",
        "",
    ]

    table_rows = []
    for result in slice_results:
        table_rows.append(
            [
                result["experiment"],
                "yes" if result["completed"] else "no",
                "yes" if result["partial"] else "no",
                str(result["actual_rows"]),
                str(result["expected_rows"]),
                str(result["parse_failures"]),
                str(result["execution_failures"]),
            ]
        )
    lines.append(
        markdown_table(
            ["Experiment", "Completed", "Partial", "Rows", "Expected", "Parse Failures", "Execution Failures"],
            table_rows,
        )
    )
    lines.append("")
    lines.extend(["## Topline Metrics", "", *topline_metric_lines(slice_results, wrap_code=True)])

    for result in slice_results:
        if result["missing_ids"]:
            lines.extend(
                [
                    f"## Missing IDs: {result['experiment']}",
                    "",
                    "\n".join(f"- `{item}`" for item in result["missing_ids"]),
                    "",
                ]
            )

    CONTROLLED_SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")

    log_lines = [
        "# Controlled DeepSeek Repeated Pilot Run Log",
        "",
        f"Date: {utc_timestamp()}",
        f"Provider: {provider}",
        f"Model: {model}",
        f"Repeats: {repeats}",
        f"Credential handling: {credential_handling_note(credential_status, live_run_performed)}",
        f"Live run performed: {'yes' if live_run_performed else 'no'}",
        "",
        "## Topline Metrics",
        "",
        *topline_metric_lines(slice_results, wrap_code=False),
    ]
    for result in slice_results:
        log_lines.extend(
            [
                f"## {result['experiment']}",
                "",
                f"- completed: {'yes' if result['completed'] else 'no'}",
                f"- partial: {'yes' if result['partial'] else 'no'}",
                f"- rows: {result['actual_rows']}/{result['expected_rows']}",
                f"- parse_failures: {result['parse_failures']}",
                f"- execution_failures: {result['execution_failures']}",
                f"- raw_output: `{result['raw_output']}`" if result["raw_output"] else "- raw_output: n/a",
                f"- metrics_csv: `{result['metrics_csv']}`" if result["metrics_csv"] else "- metrics_csv: n/a",
                f"- metrics_md: `{result['metrics_md']}`" if result["metrics_md"] else "- metrics_md: n/a",
                "",
            ]
        )
        if result["missing_ids"]:
            log_lines.append("Missing IDs:")
            log_lines.extend(f"- {item}" for item in result["missing_ids"])
            log_lines.append("")
    RESEARCH_LOG_PATH.write_text("\n".join(log_lines), encoding="utf-8")


def record_common_fields(
    *,
    provider: str,
    model: str,
    experiment: str,
    case_id: str,
    repeat_index: int,
    prompt_file: str | None,
    prompt_text: str,
    raw_response: str,
    parsing_status: str,
    error: str,
    started_at: str,
    completed_at: str,
) -> dict[str, Any]:
    return {
        "provider": provider,
        "model": model,
        "experiment": experiment,
        "case_id": case_id,
        "repeat_index": repeat_index,
        "prompt_file": prompt_file,
        "prompt_hash": prompt_hash(prompt_text),
        "raw_response": raw_response,
        "parsing_status": parsing_status,
        "error": error,
        "started_at_utc": started_at,
        "completed_at_utc": completed_at,
    }


def run_trigger_experiment(config: Any, repeats: int) -> dict[str, Any]:
    trigger_rows, skill_rows, templates = trigger_mod.validate_setup()
    raw_output_path = RAW_RESULTS_DIR / f"controlled_deepseek_trigger_{filename_timestamp()}.jsonl"
    raw_output_path.write_text("", encoding="utf-8")

    catalogs = {
        "skillops": trigger_mod.build_skillops_catalog(skill_rows),
        "freeform": trigger_mod.build_freeform_catalog(skill_rows),
    }
    records: list[dict[str, Any]] = []
    for condition, prompt_path in trigger_mod.PROMPT_PATHS.items():
        template = templates[condition]
        for repeat_index in range(1, repeats + 1):
            for case_row in trigger_rows:
                prompt = render_prompt_template(
                    template,
                    {
                        "SKILL_CATALOG": catalogs[condition],
                        "CASE_ID": case_row["case_id"],
                        "USER_REQUEST": case_row["user_request"],
                    },
                )
                started_at, completed_at, response_text, _, error = execute_model_prompt(prompt, config)
                parsed_json = parse_json_object(response_text) if not error else None
                normalized = trigger_mod.normalize_result(case_row, condition, parsed_json)
                record = {
                    **record_common_fields(
                        provider=config.provider,
                        model=config.model,
                        experiment="trigger_routing_accuracy",
                        case_id=case_row["case_id"],
                        repeat_index=repeat_index,
                        prompt_file=relative_display(prompt_path),
                        prompt_text=prompt,
                        raw_response=response_text,
                        parsing_status=parsing_status_for(response_text, parsed_json, error),
                        error=error,
                        started_at=started_at,
                        completed_at=completed_at,
                    ),
                    "condition": condition,
                    "expected_label": case_row["expected_label"],
                    "expected_skill": case_row["relevant_skill"],
                    "predicted_label": normalized["predicted_label"],
                    "predicted_skill": normalized["predicted_skill"],
                    "normalized_prediction": normalized,
                }
                append_jsonl_record(raw_output_path, record)
                records.append(record)

    metric_points: list[dict[str, Any]] = []
    expected_per_repeat = len(trigger_rows)
    for condition in ("skillops", "freeform"):
        for repeat_index in range(1, repeats + 1):
            members = [
                row
                for row in records
                if row["condition"] == condition and row["repeat_index"] == repeat_index
            ]
            note = incomplete_note(len(members), expected_per_repeat)
            precision, recall, f1, tp, fp, fn = precision_recall_f1_from_rows(members)
            should_not_rows = [row for row in members if row["expected_label"] == "should_not_trigger"]
            false_trigger_hits = sum(1 for row in should_not_rows if row["predicted_label"] == "should_trigger")
            ambiguous_rows = [row for row in members if row["expected_label"] == "ambiguous"]
            ambiguity_hits = sum(1 for row in ambiguous_rows if row["predicted_label"] == "ambiguous")
            metric_points.extend(
                [
                    {
                        "experiment": "trigger",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "precision",
                        "repeat_index": repeat_index,
                        "value": precision,
                        "numerator": tp,
                        "denominator": tp + fp,
                        "notes": note,
                    },
                    {
                        "experiment": "trigger",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "recall",
                        "repeat_index": repeat_index,
                        "value": recall,
                        "numerator": tp,
                        "denominator": tp + fn,
                        "notes": note,
                    },
                    {
                        "experiment": "trigger",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "f1",
                        "repeat_index": repeat_index,
                        "value": f1,
                        "numerator": tp,
                        "denominator": len(members),
                        "notes": note,
                    },
                    {
                        "experiment": "trigger",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "false_trigger_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(false_trigger_hits, len(should_not_rows)),
                        "numerator": false_trigger_hits,
                        "denominator": len(should_not_rows),
                        "notes": note,
                    },
                    {
                        "experiment": "trigger",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "ambiguity_handling_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(ambiguity_hits, len(ambiguous_rows)),
                        "numerator": ambiguity_hits,
                        "denominator": len(ambiguous_rows),
                        "notes": note,
                    },
                ]
            )

    csv_rows, _ = expand_metric_points(metric_points)
    write_csv_rows(CONTROLLED_TRIGGER_METRICS_CSV, METRIC_FIELDNAMES, csv_rows)
    write_metrics_markdown(
        CONTROLLED_TRIGGER_METRICS_MD,
        title="Controlled DeepSeek Trigger Routing Metrics",
        raw_output_path=raw_output_path,
        provider=config.provider,
        model=config.model,
        repeats=repeats,
        metric_points=metric_points,
        partial=len(records) != len(trigger_rows) * 2 * repeats,
    )
    expected_ids = {
        f"{condition}:r{repeat_index}:{row['case_id']}"
        for condition in ("skillops", "freeform")
        for repeat_index in range(1, repeats + 1)
        for row in trigger_rows
    }
    actual_ids = {f"{row['condition']}:r{row['repeat_index']}:{row['case_id']}" for row in records}
    execution_failures = sum(1 for row in records if row["parsing_status"] == "execution_error")
    completed, partial = completion_flags(actual_ids, expected_ids, execution_failures)
    return {
        "experiment": "Trigger",
        "completed": completed,
        "partial": partial,
        "expected_rows": len(expected_ids),
        "actual_rows": len(records),
        "parse_failures": sum(1 for row in records if row["parsing_status"] in {"parse_failed", "empty_response"}),
        "execution_failures": execution_failures,
        "missing_ids": sorted(expected_ids - actual_ids),
        "raw_output": relative_display(raw_output_path),
        "metrics_csv": relative_display(CONTROLLED_TRIGGER_METRICS_CSV),
        "metrics_md": relative_display(CONTROLLED_TRIGGER_METRICS_MD),
        "csv_rows": csv_rows,
    }


def run_constraint_experiment(config: Any, repeats: int) -> dict[str, Any]:
    risk_rows, templates = constraint_mod.validate_setup()
    raw_output_path = RAW_RESULTS_DIR / f"controlled_deepseek_constraint_{filename_timestamp()}.jsonl"
    raw_output_path.write_text("", encoding="utf-8")

    records: list[dict[str, Any]] = []
    for condition, prompt_path in constraint_mod.PROMPT_PATHS.items():
        template = templates[condition]
        for repeat_index in range(1, repeats + 1):
            for case_row in risk_rows:
                prompt = render_prompt_template(
                    template,
                    {
                        "CASE_ID": case_row["case_id"],
                        "SCENARIO": case_row["example"],
                    },
                )
                started_at, completed_at, response_text, _, error = execute_model_prompt(prompt, config)
                parsed_json = parse_json_object(response_text) if not error else None
                normalized = constraint_mod.normalize_result(case_row, condition, parsed_json)
                record = {
                    **record_common_fields(
                        provider=config.provider,
                        model=config.model,
                        experiment="constraint_compliance_rate",
                        case_id=case_row["case_id"],
                        repeat_index=repeat_index,
                        prompt_file=relative_display(prompt_path),
                        prompt_text=prompt,
                        raw_response=response_text,
                        parsing_status=parsing_status_for(response_text, parsed_json, error),
                        error=error,
                        started_at=started_at,
                        completed_at=completed_at,
                    ),
                    "condition": condition,
                    "expected_label": "risk",
                    "expected_skill": "",
                    "predicted_label": "risk" if normalized["risk_detected"] else "benign",
                    "predicted_skill": "",
                    "normalized_prediction": normalized,
                }
                append_jsonl_record(raw_output_path, record)
                records.append(record)

    metric_points: list[dict[str, Any]] = []
    expected_per_repeat = len(risk_rows)
    for condition in ("skillops", "vague"):
        for repeat_index in range(1, repeats + 1):
            members = [
                row
                for row in records
                if row["condition"] == condition and row["repeat_index"] == repeat_index
            ]
            note = incomplete_note(len(members), expected_per_repeat)
            violation_hits = sum(1 for row in members if row["normalized_prediction"]["scored_violations"])
            safe_handling_hits = sum(
                1
                for row in members
                if row["normalized_prediction"]["risk_detected"]
                and row["normalized_prediction"]["safe_response"]
                and not any(
                    item.startswith("missing_action_tag:")
                    for item in row["normalized_prediction"]["scored_violations"]
                )
            )
            unsupported_hits = sum(1 for row in members if row["normalized_prediction"]["unsupported_success_claim"])
            compliant_hits = sum(1 for row in members if row["normalized_prediction"]["constraint_compliant"])
            metric_points.extend(
                [
                    {
                        "experiment": "constraint",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "violation_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(violation_hits, len(members)),
                        "numerator": violation_hits,
                        "denominator": len(members),
                        "notes": note,
                    },
                    {
                        "experiment": "constraint",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "safe_handling_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(safe_handling_hits, len(members)),
                        "numerator": safe_handling_hits,
                        "denominator": len(members),
                        "notes": note,
                    },
                    {
                        "experiment": "constraint",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "unsupported_success_claim_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(unsupported_hits, len(members)),
                        "numerator": unsupported_hits,
                        "denominator": len(members),
                        "notes": note,
                    },
                    {
                        "experiment": "constraint",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "constraint_compliance_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(compliant_hits, len(members)),
                        "numerator": compliant_hits,
                        "denominator": len(members),
                        "notes": note,
                    },
                ]
            )

    csv_rows, _ = expand_metric_points(metric_points)
    write_csv_rows(CONTROLLED_CONSTRAINT_METRICS_CSV, METRIC_FIELDNAMES, csv_rows)
    write_metrics_markdown(
        CONTROLLED_CONSTRAINT_METRICS_MD,
        title="Controlled DeepSeek Constraint Compliance Metrics",
        raw_output_path=raw_output_path,
        provider=config.provider,
        model=config.model,
        repeats=repeats,
        metric_points=metric_points,
        partial=len(records) != len(risk_rows) * 2 * repeats,
    )
    expected_ids = {
        f"{condition}:r{repeat_index}:{row['case_id']}"
        for condition in ("skillops", "vague")
        for repeat_index in range(1, repeats + 1)
        for row in risk_rows
    }
    actual_ids = {f"{row['condition']}:r{row['repeat_index']}:{row['case_id']}" for row in records}
    execution_failures = sum(1 for row in records if row["parsing_status"] == "execution_error")
    completed, partial = completion_flags(actual_ids, expected_ids, execution_failures)
    return {
        "experiment": "Constraint",
        "completed": completed,
        "partial": partial,
        "expected_rows": len(expected_ids),
        "actual_rows": len(records),
        "parse_failures": sum(1 for row in records if row["parsing_status"] in {"parse_failed", "empty_response"}),
        "execution_failures": execution_failures,
        "missing_ids": sorted(expected_ids - actual_ids),
        "raw_output": relative_display(raw_output_path),
        "metrics_csv": relative_display(CONTROLLED_CONSTRAINT_METRICS_CSV),
        "metrics_md": relative_display(CONTROLLED_CONSTRAINT_METRICS_MD),
        "csv_rows": csv_rows,
    }


def run_security_experiment(config: Any, repeats: int) -> dict[str, Any]:
    risk_rows, benign_rows, prompt_template = security_mod.validate_setup()
    raw_output_path = RAW_RESULTS_DIR / f"controlled_deepseek_security_{filename_timestamp()}.jsonl"
    raw_output_path.write_text("", encoding="utf-8")

    records: list[dict[str, Any]] = []
    for repeat_index in range(1, repeats + 1):
        for case_row in risk_rows:
            prompt = render_prompt_template(
                prompt_template,
                {
                    "CASE_ID": case_row["case_id"],
                    "SCENARIO": case_row["example"],
                },
            )
            started_at, completed_at, response_text, _, error = execute_model_prompt(prompt, config)
            parsed_json = parse_json_object(response_text) if not error else None
            normalized = security_mod.normalize_model_result(case_row, parsed_json)
            record = {
                **record_common_fields(
                    provider=config.provider,
                    model=config.model,
                    experiment="security_guard_detection_rate",
                    case_id=case_row["case_id"],
                    repeat_index=repeat_index,
                    prompt_file=relative_display(security_mod.PROMPT_PATH),
                    prompt_text=prompt,
                    raw_response=response_text,
                    parsing_status=parsing_status_for(response_text, parsed_json, error),
                    error=error,
                    started_at=started_at,
                    completed_at=completed_at,
                ),
                "condition": "risk",
                "expected_label": "risk",
                "expected_skill": "",
                "predicted_label": normalized["predicted_risk_label"],
                "predicted_skill": "",
                "expected_risk_label": normalized["expected_risk_label"],
                "predicted_risk_label": normalized["predicted_risk_label"],
                "is_false_positive": normalized["is_false_positive"],
                "risk_type": case_row["risk_type"],
                "relevant_artifact": case_row["relevant_artifact"],
                "normalized_prediction": normalized,
            }
            append_jsonl_record(raw_output_path, record)
            records.append(record)
        for case_row in benign_rows:
            prompt = render_prompt_template(
                prompt_template,
                {
                    "CASE_ID": case_row["case_id"],
                    "SCENARIO": case_row["user_request"],
                },
            )
            started_at, completed_at, response_text, _, error = execute_model_prompt(prompt, config)
            parsed_json = parse_json_object(response_text) if not error else None
            normalized = security_mod.normalize_model_control_result(case_row, parsed_json)
            record = {
                **record_common_fields(
                    provider=config.provider,
                    model=config.model,
                    experiment="security_guard_detection_rate",
                    case_id=case_row["case_id"],
                    repeat_index=repeat_index,
                    prompt_file=relative_display(security_mod.PROMPT_PATH),
                    prompt_text=prompt,
                    raw_response=response_text,
                    parsing_status=parsing_status_for(response_text, parsed_json, error),
                    error=error,
                    started_at=started_at,
                    completed_at=completed_at,
                ),
                "condition": "benign_control",
                "expected_label": "benign",
                "expected_skill": "",
                "predicted_label": normalized["predicted_risk_label"],
                "predicted_skill": "",
                "expected_risk_label": normalized["expected_risk_label"],
                "predicted_risk_label": normalized["predicted_risk_label"],
                "is_false_positive": normalized["is_false_positive"],
                "risk_type": case_row["benign_type"],
                "relevant_artifact": case_row["relevant_artifact"],
                "normalized_prediction": normalized,
            }
            append_jsonl_record(raw_output_path, record)
            records.append(record)

    metric_points: list[dict[str, Any]] = []
    expected_risk_per_repeat = len(risk_rows)
    expected_benign_per_repeat = len(benign_rows)
    risk_types = sorted({row["risk_type"] for row in risk_rows})
    artifacts = sorted({row["relevant_artifact"] for row in risk_rows})
    for repeat_index in range(1, repeats + 1):
        risk_members = [
            row
            for row in records
            if row["condition"] == "risk" and row["repeat_index"] == repeat_index
        ]
        benign_members = [
            row
            for row in records
            if row["condition"] == "benign_control" and row["repeat_index"] == repeat_index
        ]
        note = " | ".join(
            item
            for item in [
                incomplete_note(len(risk_members), expected_risk_per_repeat),
                incomplete_note(len(benign_members), expected_benign_per_repeat),
            ]
            if item
        )
        detection_hits = sum(1 for row in risk_members if row["normalized_prediction"]["risk_type_detected"])
        false_positive_hits = sum(1 for row in benign_members if row["is_false_positive"])
        true_negative_hits = len(benign_members) - false_positive_hits
        metric_points.extend(
            [
                {
                    "experiment": "security",
                    "group_type": "overall",
                    "group_value": "all",
                    "metric": "detection_rate",
                    "repeat_index": repeat_index,
                    "value": safe_divide(detection_hits, len(risk_members)),
                    "numerator": detection_hits,
                    "denominator": len(risk_members),
                    "notes": note,
                },
                {
                    "experiment": "security",
                    "group_type": "overall",
                    "group_value": "all",
                    "metric": "false_positive_rate",
                    "repeat_index": repeat_index,
                    "value": safe_divide(false_positive_hits, len(benign_members)),
                    "numerator": false_positive_hits,
                    "denominator": len(benign_members),
                    "notes": note,
                },
                {
                    "experiment": "security",
                    "group_type": "overall",
                    "group_value": "all",
                    "metric": "specificity",
                    "repeat_index": repeat_index,
                    "value": safe_divide(true_negative_hits, len(benign_members)),
                    "numerator": true_negative_hits,
                    "denominator": len(benign_members),
                    "notes": note,
                },
            ]
        )
        for risk_type in risk_types:
            members = [row for row in risk_members if row["risk_type"] == risk_type]
            hits = sum(1 for row in members if row["normalized_prediction"]["risk_type_detected"])
            metric_points.append(
                {
                    "experiment": "security",
                    "group_type": "risk_type",
                    "group_value": risk_type,
                    "metric": "category_recall",
                    "repeat_index": repeat_index,
                    "value": safe_divide(hits, len(members)),
                    "numerator": hits,
                    "denominator": len(members),
                    "notes": note,
                }
            )
        for artifact in artifacts:
            members = [row for row in risk_members if row["relevant_artifact"] == artifact]
            hits = sum(1 for row in members if row["normalized_prediction"]["risk_type_detected"])
            metric_points.append(
                {
                    "experiment": "security",
                    "group_type": "relevant_artifact",
                    "group_value": artifact,
                    "metric": "artifact_coverage",
                    "repeat_index": repeat_index,
                    "value": safe_divide(hits, len(members)),
                    "numerator": hits,
                    "denominator": len(members),
                    "notes": note,
                }
            )

    csv_rows, _ = expand_metric_points(metric_points)
    write_csv_rows(CONTROLLED_SECURITY_METRICS_CSV, METRIC_FIELDNAMES, csv_rows)
    write_metrics_markdown(
        CONTROLLED_SECURITY_METRICS_MD,
        title="Controlled DeepSeek Security Guard Metrics",
        raw_output_path=raw_output_path,
        provider=config.provider,
        model=config.model,
        repeats=repeats,
        metric_points=metric_points,
        partial=len(records) != (len(risk_rows) + len(benign_rows)) * repeats,
    )
    expected_ids = {
        f"risk:r{repeat_index}:{row['case_id']}"
        for repeat_index in range(1, repeats + 1)
        for row in risk_rows
    } | {
        f"benign_control:r{repeat_index}:{row['case_id']}"
        for repeat_index in range(1, repeats + 1)
        for row in benign_rows
    }
    actual_ids = {f"{row['condition']}:r{row['repeat_index']}:{row['case_id']}" for row in records}
    execution_failures = sum(1 for row in records if row["parsing_status"] == "execution_error")
    completed, partial = completion_flags(actual_ids, expected_ids, execution_failures)
    return {
        "experiment": "Security",
        "completed": completed,
        "partial": partial,
        "expected_rows": len(expected_ids),
        "actual_rows": len(records),
        "parse_failures": sum(1 for row in records if row["parsing_status"] in {"parse_failed", "empty_response"}),
        "execution_failures": execution_failures,
        "missing_ids": sorted(expected_ids - actual_ids),
        "raw_output": relative_display(raw_output_path),
        "metrics_csv": relative_display(CONTROLLED_SECURITY_METRICS_CSV),
        "metrics_md": relative_display(CONTROLLED_SECURITY_METRICS_MD),
        "csv_rows": csv_rows,
    }


def run_memory_experiment(config: Any, repeats: int) -> dict[str, Any]:
    drift_rows, templates = memory_mod.validate_setup()
    raw_output_path = RAW_RESULTS_DIR / f"controlled_deepseek_memory_{filename_timestamp()}.jsonl"
    raw_output_path.write_text("", encoding="utf-8")

    records: list[dict[str, Any]] = []
    for condition, prompt_path in memory_mod.PROMPT_PATHS.items():
        template = templates[condition]
        for repeat_index in range(1, repeats + 1):
            for case_row in drift_rows:
                replacements = memory_mod._build_replacements(condition, case_row)
                prompt = render_prompt_template(template, replacements)
                started_at, completed_at, response_text, _, error = execute_model_prompt(prompt, config)
                parsed_json = parse_json_object(response_text) if not error else None
                normalized = memory_mod.normalize_result(case_row, condition, parsed_json)
                record = {
                    **record_common_fields(
                        provider=config.provider,
                        model=config.model,
                        experiment="memory_drift_detection",
                        case_id=case_row["case_id"],
                        repeat_index=repeat_index,
                        prompt_file=relative_display(prompt_path),
                        prompt_text=prompt,
                        raw_response=response_text,
                        parsing_status=parsing_status_for(response_text, parsed_json, error),
                        error=error,
                        started_at=started_at,
                        completed_at=completed_at,
                    ),
                    "condition": condition,
                    "expected_label": case_row["expected_behavior"],
                    "expected_skill": "",
                    "predicted_label": normalized["response_action"] or "unparsed",
                    "predicted_skill": "",
                    "stale_info_used": normalized["used_stale_info"],
                    "current_instruction_followed": normalized["followed_current_instruction"],
                    "correct_forgetting": normalized["applied_forgetting"],
                    "conflict_resolution_success": normalized["conflict_resolution_applied"],
                    "unsupported_memory_claim": normalized["used_stale_info"] and not normalized["followed_current_instruction"],
                    "normalized_prediction": {
                        **normalized,
                        "stale_info_used": normalized["used_stale_info"],
                        "current_instruction_followed": normalized["followed_current_instruction"],
                        "correct_forgetting": normalized["applied_forgetting"],
                        "conflict_resolution_success": normalized["conflict_resolution_applied"],
                        "unsupported_memory_claim": normalized["used_stale_info"] and not normalized["followed_current_instruction"],
                    },
                }
                append_jsonl_record(raw_output_path, record)
                records.append(record)

    metric_points: list[dict[str, Any]] = []
    expected_per_repeat = len(drift_rows)
    for condition in ("full_skillops_memory_policy", "no_forgetting_policy", "current_context_only"):
        for repeat_index in range(1, repeats + 1):
            members = [
                row
                for row in records
                if row["condition"] == condition and row["repeat_index"] == repeat_index
            ]
            note = incomplete_note(len(members), expected_per_repeat)
            stale_hits = sum(1 for row in members if row["stale_info_used"])
            current_hits = sum(1 for row in members if row["current_instruction_followed"])
            forgetting_hits = sum(1 for row in members if row["correct_forgetting"])
            conflict_hits = sum(1 for row in members if row["conflict_resolution_success"])
            unsupported_hits = sum(1 for row in members if row["unsupported_memory_claim"])
            metric_points.extend(
                [
                    {
                        "experiment": "memory",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "stale_info_usage_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(stale_hits, len(members)),
                        "numerator": stale_hits,
                        "denominator": len(members),
                        "notes": note,
                    },
                    {
                        "experiment": "memory",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "current_instruction_adherence_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(current_hits, len(members)),
                        "numerator": current_hits,
                        "denominator": len(members),
                        "notes": note,
                    },
                    {
                        "experiment": "memory",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "correct_forgetting_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(forgetting_hits, len(members)),
                        "numerator": forgetting_hits,
                        "denominator": len(members),
                        "notes": note,
                    },
                    {
                        "experiment": "memory",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "conflict_resolution_success_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(conflict_hits, len(members)),
                        "numerator": conflict_hits,
                        "denominator": len(members),
                        "notes": note,
                    },
                    {
                        "experiment": "memory",
                        "group_type": "condition",
                        "group_value": condition,
                        "metric": "unsupported_memory_claim_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(unsupported_hits, len(members)),
                        "numerator": unsupported_hits,
                        "denominator": len(members),
                        "notes": note,
                    },
                ]
            )

    csv_rows, _ = expand_metric_points(metric_points)
    write_csv_rows(CONTROLLED_MEMORY_METRICS_CSV, METRIC_FIELDNAMES, csv_rows)
    write_metrics_markdown(
        CONTROLLED_MEMORY_METRICS_MD,
        title="Controlled DeepSeek Memory Drift Metrics",
        raw_output_path=raw_output_path,
        provider=config.provider,
        model=config.model,
        repeats=repeats,
        metric_points=metric_points,
        partial=len(records) != len(drift_rows) * 3 * repeats,
    )
    expected_ids = {
        f"{condition}:r{repeat_index}:{row['case_id']}"
        for condition in ("full_skillops_memory_policy", "no_forgetting_policy", "current_context_only")
        for repeat_index in range(1, repeats + 1)
        for row in drift_rows
    }
    actual_ids = {f"{row['condition']}:r{row['repeat_index']}:{row['case_id']}" for row in records}
    execution_failures = sum(1 for row in records if row["parsing_status"] == "execution_error")
    completed, partial = completion_flags(actual_ids, expected_ids, execution_failures)
    return {
        "experiment": "Memory",
        "completed": completed,
        "partial": partial,
        "expected_rows": len(expected_ids),
        "actual_rows": len(records),
        "parse_failures": sum(1 for row in records if row["parsing_status"] in {"parse_failed", "empty_response"}),
        "execution_failures": execution_failures,
        "missing_ids": sorted(expected_ids - actual_ids),
        "raw_output": relative_display(raw_output_path),
        "metrics_csv": relative_display(CONTROLLED_MEMORY_METRICS_CSV),
        "metrics_md": relative_display(CONTROLLED_MEMORY_METRICS_MD),
        "csv_rows": csv_rows,
    }


def build_aligned_ablation_prompt(variant_text: str, case_row: dict[str, str]) -> str:
    return (
        f"{variant_text}\n\n"
        "## User Request\n\n"
        f"case_id: {case_row['case_id']}\n"
        f"Request: {case_row['user_request']}"
    )


def run_ablation_trigger_experiment(config: Any, repeats: int) -> dict[str, Any]:
    with aligned_ablation_mod.TRIGGER_CASES_PATH.open("r", encoding="utf-8", newline="") as handle:
        import csv as _csv

        trigger_rows = list(_csv.DictReader(handle))
    variant_texts = {
        variant_name: aligned_ablation_mod.read_text(aligned_ablation_mod.VARIANTS_DIR / f"{variant_name}.md")
        for variant_name in aligned_ablation_mod.VARIANT_NAMES
    }
    raw_output_path = RAW_RESULTS_DIR / f"controlled_deepseek_ablation_trigger_{filename_timestamp()}.jsonl"
    raw_output_path.write_text("", encoding="utf-8")

    records: list[dict[str, Any]] = []
    for variant_name in aligned_ablation_mod.VARIANT_NAMES:
        variant_path = aligned_ablation_mod.VARIANTS_DIR / f"{variant_name}.md"
        variant_text = variant_texts[variant_name]
        for repeat_index in range(1, repeats + 1):
            for case_row in trigger_rows:
                prompt = build_aligned_ablation_prompt(variant_text, case_row)
                started_at, completed_at, response_text, _, error = execute_model_prompt(prompt, config)
                parsed_json = parse_json_object(response_text) if not error else None
                predicted_label = ""
                predicted_skill = "none"
                confidence = "unknown"
                rationale = ""
                if isinstance(parsed_json, dict):
                    predicted_label = str(parsed_json.get("predicted_label", "")).strip()
                    predicted_skill = str(parsed_json.get("predicted_skill", "none")).strip() or "none"
                    confidence = str(parsed_json.get("confidence", "unknown")).strip() or "unknown"
                    rationale = str(parsed_json.get("rationale", "")).strip()
                if predicted_label not in trigger_mod.ALLOWED_TRIGGER_LABELS:
                    predicted_label = "invalid"
                normalized = {
                    "case_id": case_row["case_id"],
                    "variant": variant_name,
                    "predicted_label": predicted_label,
                    "predicted_skill": predicted_skill,
                    "confidence": confidence,
                    "rationale": rationale,
                    "parsed_ok": isinstance(parsed_json, dict),
                }
                record = {
                    **record_common_fields(
                        provider=config.provider,
                        model=config.model,
                        experiment="ablation_trigger_aligned",
                        case_id=case_row["case_id"],
                        repeat_index=repeat_index,
                        prompt_file=relative_display(variant_path),
                        prompt_text=prompt,
                        raw_response=response_text,
                        parsing_status=parsing_status_for(response_text, parsed_json, error),
                        error=error,
                        started_at=started_at,
                        completed_at=completed_at,
                    ),
                    "variant": variant_name,
                    "expected_label": case_row["expected_label"],
                    "expected_skill": case_row["relevant_skill"],
                    "predicted_label": predicted_label,
                    "predicted_skill": predicted_skill,
                    "normalized_prediction": normalized,
                }
                append_jsonl_record(raw_output_path, record)
                records.append(record)

    metric_points: list[dict[str, Any]] = []
    expected_per_repeat = len(trigger_rows)
    for variant_name in aligned_ablation_mod.VARIANT_NAMES:
        for repeat_index in range(1, repeats + 1):
            members = [
                row
                for row in records
                if row["variant"] == variant_name and row["repeat_index"] == repeat_index
            ]
            note = incomplete_note(len(members), expected_per_repeat)
            precision, recall, f1, tp, fp, fn = precision_recall_f1_from_rows(members)
            should_not_rows = [row for row in members if row["expected_label"] == "should_not_trigger"]
            false_trigger_hits = sum(1 for row in should_not_rows if row["predicted_label"] == "should_trigger")
            ambiguous_rows = [row for row in members if row["expected_label"] == "ambiguous"]
            ambiguity_hits = sum(1 for row in ambiguous_rows if row["predicted_label"] == "ambiguous")
            correct_skill_hits = sum(
                1
                for row in members
                if row["expected_label"] == "should_trigger"
                and row["predicted_label"] == "should_trigger"
                and row["predicted_skill"] == row["expected_skill"]
            )
            skill_routing_accuracy = safe_divide(correct_skill_hits, tp)
            metric_points.extend(
                [
                    {
                        "experiment": "ablation_trigger",
                        "group_type": "variant",
                        "group_value": variant_name,
                        "metric": "precision",
                        "repeat_index": repeat_index,
                        "value": precision,
                        "numerator": tp,
                        "denominator": tp + fp,
                        "notes": note,
                    },
                    {
                        "experiment": "ablation_trigger",
                        "group_type": "variant",
                        "group_value": variant_name,
                        "metric": "recall",
                        "repeat_index": repeat_index,
                        "value": recall,
                        "numerator": tp,
                        "denominator": tp + fn,
                        "notes": note,
                    },
                    {
                        "experiment": "ablation_trigger",
                        "group_type": "variant",
                        "group_value": variant_name,
                        "metric": "f1",
                        "repeat_index": repeat_index,
                        "value": f1,
                        "numerator": tp,
                        "denominator": len(members),
                        "notes": note,
                    },
                    {
                        "experiment": "ablation_trigger",
                        "group_type": "variant",
                        "group_value": variant_name,
                        "metric": "false_trigger_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(false_trigger_hits, len(should_not_rows)),
                        "numerator": false_trigger_hits,
                        "denominator": len(should_not_rows),
                        "notes": note,
                    },
                    {
                        "experiment": "ablation_trigger",
                        "group_type": "variant",
                        "group_value": variant_name,
                        "metric": "ambiguity_handling_rate",
                        "repeat_index": repeat_index,
                        "value": safe_divide(ambiguity_hits, len(ambiguous_rows)),
                        "numerator": ambiguity_hits,
                        "denominator": len(ambiguous_rows),
                        "notes": note,
                    },
                    {
                        "experiment": "ablation_trigger",
                        "group_type": "variant",
                        "group_value": variant_name,
                        "metric": "skill_routing_accuracy",
                        "repeat_index": repeat_index,
                        "value": skill_routing_accuracy,
                        "numerator": correct_skill_hits,
                        "denominator": tp,
                        "notes": note,
                    },
                ]
            )

    csv_rows, _ = expand_metric_points(metric_points)
    write_csv_rows(CONTROLLED_ABLATION_METRICS_CSV, METRIC_FIELDNAMES, csv_rows)
    write_metrics_markdown(
        CONTROLLED_ABLATION_METRICS_MD,
        title="Controlled DeepSeek Aligned Ablation Trigger Metrics",
        raw_output_path=raw_output_path,
        provider=config.provider,
        model=config.model,
        repeats=repeats,
        metric_points=metric_points,
        partial=len(records) != len(trigger_rows) * len(aligned_ablation_mod.VARIANT_NAMES) * repeats,
    )
    expected_ids = {
        f"{variant_name}:r{repeat_index}:{row['case_id']}"
        for variant_name in aligned_ablation_mod.VARIANT_NAMES
        for repeat_index in range(1, repeats + 1)
        for row in trigger_rows
    }
    actual_ids = {f"{row['variant']}:r{row['repeat_index']}:{row['case_id']}" for row in records}
    execution_failures = sum(1 for row in records if row["parsing_status"] == "execution_error")
    completed, partial = completion_flags(actual_ids, expected_ids, execution_failures)
    return {
        "experiment": "Aligned ablation",
        "completed": completed,
        "partial": partial,
        "expected_rows": len(expected_ids),
        "actual_rows": len(records),
        "parse_failures": sum(1 for row in records if row["parsing_status"] in {"parse_failed", "empty_response"}),
        "execution_failures": execution_failures,
        "missing_ids": sorted(expected_ids - actual_ids),
        "raw_output": relative_display(raw_output_path),
        "metrics_csv": relative_display(CONTROLLED_ABLATION_METRICS_CSV),
        "metrics_md": relative_display(CONTROLLED_ABLATION_METRICS_MD),
        "csv_rows": csv_rows,
    }


def dry_run(repeats: int) -> int:
    trigger_rows, skill_rows, _ = trigger_mod.validate_setup()
    del skill_rows
    risk_rows, _ = constraint_mod.validate_setup()
    security_risk_rows, security_benign_rows, _ = security_mod.validate_setup()
    drift_rows, _ = memory_mod.validate_setup()
    aligned_ablation_mod.validate_inputs()

    print("Controlled DeepSeek Repeated Pilot: dry-run passed")
    print(f"- trigger planned rows: {len(trigger_rows) * 2 * repeats}")
    print(f"- constraint planned rows: {len(risk_rows) * 2 * repeats}")
    print(f"- security planned rows: {(len(security_risk_rows) + len(security_benign_rows)) * repeats}")
    print(f"- memory planned rows: {len(drift_rows) * 3 * repeats}")
    print(f"- aligned ablation planned rows: {len(trigger_rows) * len(aligned_ablation_mod.VARIANT_NAMES) * repeats}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the controlled DeepSeek repeated pilot experiments.")
    parser.add_argument("--dry-run", action="store_true", help="Validate setup only.")
    parser.add_argument("--run-live", action="store_true", help="Execute live DeepSeek calls.")
    parser.add_argument("--provider", choices=["deepseek"], default="deepseek", help="Provider for the controlled run.")
    parser.add_argument("--model", default="deepseek-chat", help="Model for the controlled run.")
    parser.add_argument("--repeats", type=int, default=3, help="Number of repeats per case.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.dry_run and not args.run_live:
        args.dry_run = True

    ensure_directories([RESULTS_DIR, RAW_RESULTS_DIR, RESEARCH_LOG_PATH.parent])

    if args.dry_run:
        dry_run(args.repeats)
        if not args.run_live:
            return 0

    credential_status = "present" if detect_provider_env_vars().get("DEEPSEEK_API_KEY") else "absent"
    if args.run_live and credential_status == "absent":
        print("live run not performed: missing DEEPSEEK_API_KEY")
        return 1

    config, error = resolve_provider_config(provider=args.provider, model=args.model)
    if error is not None or config is None:
        print(error or "not run: missing provider configuration")
        return 1

    slice_results = [
        run_trigger_experiment(config, args.repeats),
        run_constraint_experiment(config, args.repeats),
        run_security_experiment(config, args.repeats),
        run_memory_experiment(config, args.repeats),
        run_ablation_trigger_experiment(config, args.repeats),
    ]
    write_summary_files(
        provider=config.provider,
        model=config.model,
        repeats=args.repeats,
        credential_status=credential_status,
        live_run_performed=True,
        slice_results=slice_results,
    )

    total_attempted = sum(result["actual_rows"] for result in slice_results)
    total_parse_failures = sum(result["parse_failures"] for result in slice_results)
    total_execution_failures = sum(result["execution_failures"] for result in slice_results)
    print("Controlled DeepSeek Repeated Pilot: live run completed")
    print(f"- calls attempted: {total_attempted}")
    print(f"- parse failures: {total_parse_failures}")
    print(f"- execution failures: {total_execution_failures}")
    print(f"- summary: {relative_display(CONTROLLED_SUMMARY_MD)}")
    print(f"- research log: {relative_display(RESEARCH_LOG_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
