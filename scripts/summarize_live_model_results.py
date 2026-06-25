from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = Path(__file__).resolve().parent


if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from experiment_utils import RAW_RESULTS_DIR, RESULTS_DIR, ensure_directories, markdown_table, relative_display  # noqa: E402
import run_constraint_experiment  # noqa: E402
import run_memory_drift_experiment  # noqa: E402
import run_security_guard_experiment  # noqa: E402
import run_trigger_experiment  # noqa: E402
import run_ablation_experiment  # noqa: E402


SUMMARY_CSV_PATH = RESULTS_DIR / "live_model_summary.csv"
SUMMARY_MD_PATH = RESULTS_DIR / "live_model_summary.md"

EXPERIMENT_METRIC_FUNCTIONS: dict[str, Callable[[list[dict[str, Any]]], list[dict[str, Any]]]] = {
    "trigger_routing_accuracy": run_trigger_experiment.compute_metric_rows,
    "constraint_compliance_rate": run_constraint_experiment.compute_metric_rows,
    "security_guard_detection_rate": run_security_guard_experiment.compute_metric_rows,
    "memory_drift_detection": run_memory_drift_experiment.compute_metric_rows,
    "ablation_study": run_ablation_experiment.compute_all_metrics,
}

EXPERIMENT_LABELS = {
    "trigger_routing_accuracy": "Trigger routing",
    "constraint_compliance_rate": "Constraint compliance",
    "security_guard_detection_rate": "Security guard",
    "memory_drift_detection": "Memory drift",
    "ablation_study": "Ablation study",
}

SUMMARY_FIELDNAMES = [
    "experiment",
    "provider",
    "model",
    "dimension_type",
    "dimension_value",
    "metric",
    "value",
    "numerator",
    "denominator",
    "notes",
    "raw_output_file",
]


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def _first_run_metadata(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        return {}
    metadata = records[0].get("run_metadata", {})
    if isinstance(metadata, dict) and metadata:
        return metadata
    raw_output = records[0].get("raw_output", {})
    return raw_output if isinstance(raw_output, dict) else {}


def _metric_dimension(row: dict[str, Any]) -> tuple[str, str]:
    if "prompt_variant" in row:
        return "prompt_variant", str(row["prompt_variant"])
    if "condition" in row:
        return "condition", str(row["condition"])
    if "group" in row and "value" in row:
        return str(row["group"]), str(row["value"])
    if "variant" in row:
        experiment_type = str(row.get("experiment_type", "")).strip()
        if experiment_type:
            return f"{experiment_type}_variant", str(row["variant"])
        return "variant", str(row["variant"])
    return "overall", "all"


def _metric_value(row: dict[str, Any]) -> str:
    if "rate" in row:
        value = row.get("rate", "")
    else:
        value = row.get("value", "")
    return str(value)


def summarize_raw_file(path: Path) -> list[dict[str, Any]]:
    records = _read_jsonl(path)
    metadata = _first_run_metadata(records)
    experiment = str(metadata.get("experiment", "")).strip()
    provider = str(metadata.get("provider", "")).strip()
    model = str(metadata.get("model", "")).strip()

    if not provider or provider == "None" or provider == "null":
        return []
    if experiment not in EXPERIMENT_METRIC_FUNCTIONS:
        return []

    metric_rows = EXPERIMENT_METRIC_FUNCTIONS[experiment](records)
    summary_rows: list[dict[str, Any]] = []
    for row in metric_rows:
        dimension_type, dimension_value = _metric_dimension(row)
        summary_rows.append(
            {
                "experiment": experiment,
                "provider": provider,
                "model": model,
                "dimension_type": dimension_type,
                "dimension_value": dimension_value,
                "metric": str(row.get("metric", "")),
                "value": _metric_value(row),
                "numerator": str(row.get("numerator", "")),
                "denominator": str(row.get("denominator", "")),
                "notes": str(row.get("notes", "")),
                "raw_output_file": relative_display(path),
            }
        )
    return summary_rows


def _write_markdown(rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Live Model Experiment Summary",
        "",
        "These metrics are recomputed from raw JSONL outputs produced during live model calls.",
        "They are single-run metrics on manually constructed internal cases and do not establish statistical significance, broad generality, or model ranking.",
        "",
    ]

    for experiment in sorted({row["experiment"] for row in rows}):
        experiment_rows = [row for row in rows if row["experiment"] == experiment]
        lines.extend([f"## {EXPERIMENT_LABELS.get(experiment, experiment)}", ""])
        for provider_model in sorted({(row["provider"], row["model"]) for row in experiment_rows}):
            provider, model = provider_model
            model_rows = [row for row in experiment_rows if row["provider"] == provider and row["model"] == model]
            table_rows = [
                [
                    row["dimension_type"],
                    row["dimension_value"],
                    row["metric"],
                    row["value"],
                    f"{row['numerator']}/{row['denominator']}",
                ]
                for row in model_rows
            ]
            lines.extend(
                [
                    f"### {provider} / {model}",
                    "",
                    markdown_table(["Dimension", "Value", "Metric", "Rate", "Count"], table_rows),
                    "",
                    f"Raw output: `{model_rows[0]['raw_output_file']}`",
                    "",
                ]
            )

    SUMMARY_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_directories([RESULTS_DIR])
    rows: list[dict[str, Any]] = []
    for path in sorted(RAW_RESULTS_DIR.glob("*.jsonl")):
        rows.extend(summarize_raw_file(path))

    with SUMMARY_CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    _write_markdown(rows)
    print(f"Wrote {relative_display(SUMMARY_CSV_PATH)}")
    print(f"Wrote {relative_display(SUMMARY_MD_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
