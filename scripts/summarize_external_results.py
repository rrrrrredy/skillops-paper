from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_EXPERIMENTS_DIR = REPO_ROOT / "results" / "experiments"
RAW_RESULTS_DIR = RESULTS_EXPERIMENTS_DIR / "raw"

RESULT_SUMMARY_CSV_PATH = RESULTS_EXPERIMENTS_DIR / "external_result_summary.csv"
RESULT_SUMMARY_MD_PATH = RESULTS_EXPERIMENTS_DIR / "external_result_summary.md"
STAT_SUMMARY_CSV_PATH = RESULTS_EXPERIMENTS_DIR / "external_statistical_summary.csv"
STAT_SUMMARY_MD_PATH = RESULTS_EXPERIMENTS_DIR / "external_statistical_summary.md"
STAT_PLAN_CSV_PATH = RESULTS_EXPERIMENTS_DIR / "external_statistical_analysis_plan.csv"

SUMMARY_COLUMNS = [
    "group",
    "value",
    "metric",
    "numerator",
    "denominator",
    "rate",
    "status",
    "notes",
]

STAT_COLUMNS = [
    "metric",
    "planned_status",
    "result_status",
    "records_available",
    "notes",
]

REQUIRED_RESULT_FIELDS = {
    "condition_case_id",
    "case_id",
    "artifact_id",
    "source_id",
    "artifact_family_group",
    "case_type",
    "condition",
    "provider",
    "model",
    "run_status",
    "expected_behavior",
    "predicted_behavior",
    "risk_label",
    "constraint_pass",
    "parse_success",
    "latency_ms",
    "input_tokens",
    "output_tokens",
    "error_type",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def external_result_files() -> list[Path]:
    return sorted(RAW_RESULTS_DIR.glob("external_condition_*.jsonl"))


def load_external_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in external_result_files():
        for record in read_jsonl(path):
            missing = REQUIRED_RESULT_FIELDS - set(record)
            if missing:
                raise ValueError(f"{path} record missing required fields: {sorted(missing)}")
            records.append(record)
    return records


def rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return ""
    return f"{numerator / denominator:.6f}"


def metric_row(group: str, value: str, metric: str, numerator: int, denominator: int, status: str, notes: str = "") -> dict[str, Any]:
    return {
        "group": group,
        "value": value,
        "metric": metric,
        "numerator": numerator,
        "denominator": denominator,
        "rate": rate(numerator, denominator),
        "status": status,
        "notes": notes,
    }


def summarize_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not records:
        return [
            metric_row(
                "overall",
                "external_condition_results",
                "bounded_smoke_records",
                0,
                0,
                "no_results",
                "No external condition live-result JSONL files were found.",
            )
        ]

    rows: list[dict[str, Any]] = []
    completed_smoke_records = [record for record in records if record["run_status"] == "completed"]
    rows.append(
        metric_row(
            "overall",
            "external_condition_results",
            "bounded_smoke_records",
            len(completed_smoke_records),
            len(records),
            "bounded_smoke_diagnostic",
            "Bounded smoke rows only; not an external validation result or model ranking.",
        )
    )

    group_specs = [
        ("condition", sorted({str(record["condition"]) for record in records})),
        ("case_type", sorted({str(record["case_type"]) for record in records})),
        ("provider_model", sorted({f"{record['provider']}::{record['model']}" for record in records})),
    ]
    for group, values in group_specs:
        for value in values:
            if group == "provider_model":
                provider, model = value.split("::", 1)
                subset = [record for record in records if record["provider"] == provider and record["model"] == model]
            else:
                subset = [record for record in records if record[group] == value]
            parse_hits = sum(1 for record in subset if bool(record["parse_success"]))
            behavior_hits = sum(1 for record in subset if record["predicted_behavior"] == record["expected_behavior"])
            rows.append(metric_row(group, value, "parse_success_rate", parse_hits, len(subset), "bounded_smoke_diagnostic"))
            rows.append(metric_row(group, value, "behavior_match_rate", behavior_hits, len(subset), "bounded_smoke_diagnostic"))

    risk_records = [record for record in records if record["case_type"] == "risk_constraint"]
    if risk_records:
        constraint_hits = sum(1 for record in risk_records if record["constraint_pass"] is True)
        rows.append(
            metric_row(
                "case_type",
                "risk_constraint",
                "constraint_pass_rate",
                constraint_hits,
                len(risk_records),
                "bounded_smoke_diagnostic",
            )
        )
    return rows


def build_stat_summary(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    plan_rows = read_csv_rows(STAT_PLAN_CSV_PATH)
    status = "no_results" if not records else "smoke_records_present_no_powered_inference"
    notes = (
        "No external live-result records are available."
        if not records
        else "Bounded smoke records are available; powered annotated inference has not run."
    )
    return [
        {
            "metric": row["metric"],
            "planned_status": row["status"],
            "result_status": status,
            "records_available": len(records),
            "notes": notes,
        }
        for row in plan_rows
    ]


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_markdown(summary_rows: list[dict[str, Any]], stat_rows: list[dict[str, Any]]) -> None:
    result_lines = [
        "# External Result Summary",
        "",
        "This summary is computed only from external condition live-result JSONL files. When none are present, it reports a no-results boundary.",
        "Current records are bounded smoke rows over the first external shard prefix; they are execution-path diagnostics, not external validation, statistical significance, or model ranking.",
        "",
        markdown_table(
            ["Group", "Value", "Metric", "Count", "Rate", "Status"],
            [
                [
                    row["group"],
                    row["value"],
                    row["metric"],
                    f"{row['numerator']}/{row['denominator']}",
                    row["rate"],
                    row["status"],
                ]
                for row in summary_rows
            ],
        ),
        "",
    ]
    RESULT_SUMMARY_MD_PATH.write_text("\n".join(result_lines), encoding="utf-8")

    stat_lines = [
        "# External Statistical Summary",
        "",
        "This file tracks whether planned external statistical metrics have live-result inputs. Bounded smoke rows may be present, but powered annotated inference has not run.",
        "",
        markdown_table(
            ["Metric", "Planned status", "Result status", "Records"],
            [
                [
                    row["metric"],
                    row["planned_status"],
                    row["result_status"],
                    str(row["records_available"]),
                ]
                for row in stat_rows
            ],
        ),
        "",
    ]
    STAT_SUMMARY_MD_PATH.write_text("\n".join(stat_lines), encoding="utf-8")


def main() -> int:
    records = load_external_records()
    summary_rows = summarize_records(records)
    stat_rows = build_stat_summary(records)
    write_csv(RESULT_SUMMARY_CSV_PATH, SUMMARY_COLUMNS, summary_rows)
    write_csv(STAT_SUMMARY_CSV_PATH, STAT_COLUMNS, stat_rows)
    write_markdown(summary_rows, stat_rows)
    print(f"Wrote {RESULT_SUMMARY_CSV_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {RESULT_SUMMARY_MD_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {STAT_SUMMARY_CSV_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {STAT_SUMMARY_MD_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
