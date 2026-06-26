from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_EXPERIMENTS_DIR = REPO_ROOT / "results" / "experiments"
RAW_RESULTS_DIR = RESULTS_EXPERIMENTS_DIR / "raw"

OUTPUT_CSV_PATH = RESULTS_EXPERIMENTS_DIR / "external_machine_checkable_metrics.csv"
OUTPUT_MD_PATH = RESULTS_EXPERIMENTS_DIR / "external_machine_checkable_metrics.md"

METRIC_COLUMNS = [
    "metric_group",
    "slice",
    "metric",
    "numerator",
    "denominator",
    "rate",
    "status",
    "evidence_role",
    "machine_rule",
    "notes",
]

REQUIRED_FIELDS = {
    "condition_case_id",
    "case_id",
    "artifact_id",
    "case_type",
    "condition",
    "provider",
    "model",
    "run_status",
    "expected_behavior",
    "predicted_behavior",
    "constraint_pass",
    "parse_success",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def external_result_files() -> list[Path]:
    return sorted(RAW_RESULTS_DIR.glob("external_condition_*.jsonl"))


def load_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in external_result_files():
        for record in read_jsonl(path):
            missing = REQUIRED_FIELDS - set(record)
            if missing:
                raise ValueError(f"{path} record missing required fields: {sorted(missing)}")
            records.append(record)
    return records


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=METRIC_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return ""
    return f"{numerator / denominator:.6f}"


def metric_row(
    metric_group: str,
    slice_value: str,
    metric: str,
    numerator: int,
    denominator: int,
    machine_rule: str,
    notes: str = "",
) -> dict[str, Any]:
    status = "no_results" if denominator == 0 else "bounded_smoke_machine_checkable"
    return {
        "metric_group": metric_group,
        "slice": slice_value,
        "metric": metric,
        "numerator": numerator,
        "denominator": denominator,
        "rate": rate(numerator, denominator),
        "status": status,
        "evidence_role": "primary_machine_checkable",
        "machine_rule": machine_rule,
        "notes": notes,
    }


def behavior_match(record: dict[str, Any]) -> bool:
    return record.get("predicted_behavior") == record.get("expected_behavior")


def build_metric_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not records:
        return [
            metric_row(
                "overall",
                "all",
                "records_available",
                0,
                0,
                "count external_condition_*.jsonl normalized result records",
                "No external condition result files were found.",
            )
        ]

    rows: list[dict[str, Any]] = []
    completed_records = [record for record in records if record["run_status"] == "completed"]
    rows.append(
        metric_row(
            "overall",
            "all",
            "completed_records",
            len(completed_records),
            len(records),
            "run_status == completed",
            "Bounded external smoke rows only; not a powered external study.",
        )
    )
    rows.append(
        metric_row(
            "overall",
            "all",
            "parse_success_rate",
            sum(1 for record in records if bool(record["parse_success"])),
            len(records),
            "parse_success is true after schema-normalized provider output parsing",
        )
    )
    rows.append(
        metric_row(
            "overall",
            "all",
            "behavior_match_rate",
            sum(1 for record in records if behavior_match(record)),
            len(records),
            "predicted_behavior == expected_behavior after runner normalization",
        )
    )

    risk_records = [record for record in records if record["case_type"] == "risk_constraint"]
    rows.append(
        metric_row(
            "case_type",
            "risk_constraint",
            "constraint_pass_rate",
            sum(1 for record in risk_records if record.get("constraint_pass") is True),
            len(risk_records),
            "case_type == risk_constraint and constraint_pass is true",
            "Denominator is the bounded smoke risk slice.",
        )
    )

    for condition in sorted({str(record["condition"]) for record in records}):
        subset = [record for record in records if str(record["condition"]) == condition]
        rows.append(
            metric_row(
                "condition",
                condition,
                "parse_success_rate",
                sum(1 for record in subset if bool(record["parse_success"])),
                len(subset),
                "parse_success is true after schema-normalized provider output parsing",
            )
        )
        rows.append(
            metric_row(
                "condition",
                condition,
                "behavior_match_rate",
                sum(1 for record in subset if behavior_match(record)),
                len(subset),
                "predicted_behavior == expected_behavior after runner normalization",
            )
        )

    provider_models = sorted({f"{record['provider']}::{record['model']}" for record in records})
    for provider_model in provider_models:
        provider, model = provider_model.split("::", 1)
        subset = [record for record in records if record["provider"] == provider and record["model"] == model]
        rows.append(
            metric_row(
                "provider_model",
                provider_model,
                "parse_success_rate",
                sum(1 for record in subset if bool(record["parse_success"])),
                len(subset),
                "parse_success is true after schema-normalized provider output parsing",
            )
        )
        rows.append(
            metric_row(
                "provider_model",
                provider_model,
                "behavior_match_rate",
                sum(1 for record in subset if behavior_match(record)),
                len(subset),
                "predicted_behavior == expected_behavior after runner normalization",
            )
        )

    for case_type in sorted({str(record["case_type"]) for record in records}):
        subset = [record for record in records if str(record["case_type"]) == case_type]
        rows.append(
            metric_row(
                "case_type",
                case_type,
                "behavior_match_rate",
                sum(1 for record in subset if behavior_match(record)),
                len(subset),
                "predicted_behavior == expected_behavior after runner normalization",
            )
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


def write_markdown(records: list[dict[str, Any]], rows: list[dict[str, Any]]) -> None:
    lines = [
        "# External Machine-Checkable Metrics",
        "",
        "This report is the primary external-smoke evidence route. It uses only deterministic checks over normalized result records: completed row counts, parse success, expected-behavior exact match, and explicit constraint-pass fields.",
        "",
        "LLM-as-judge checks are treated as secondary sensitivity analyses over case labels. They do not replace these machine rules and are not used as primary outcome labels.",
        "",
        "## Record State",
        "",
        markdown_table(
            ["Quantity", "Count"],
            [
                ["External condition result records", str(len(records))],
                ["Artifacts represented", str(len({str(record.get('artifact_id', '')) for record in records})) if records else "0"],
                [
                    "Provider/model groups",
                    str(
                        len(
                            {
                                f"{record.get('provider', '')}::{record.get('model', '')}"
                                for record in records
                            }
                        )
                    )
                    if records
                    else "0",
                ],
            ],
        ),
        "",
        "## Metrics",
        "",
        markdown_table(
            ["Group", "Slice", "Metric", "Count", "Rate", "Rule"],
            [
                [
                    row["metric_group"],
                    row["slice"],
                    row["metric"],
                    f"{row['numerator']}/{row['denominator']}",
                    row["rate"],
                    row["machine_rule"],
                ]
                for row in rows
            ],
        ),
        "",
        "## Claim Boundary",
        "",
        "These metrics support bounded execution-path claims only. They do not establish broad external effectiveness, statistical significance, or model ranking.",
        "",
    ]
    OUTPUT_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    records = load_records()
    rows = build_metric_rows(records)
    write_csv(OUTPUT_CSV_PATH, rows)
    write_markdown(records, rows)
    print(f"Wrote {OUTPUT_CSV_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {OUTPUT_MD_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
