from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_TABLES_DIR = REPO_ROOT / "results" / "tables"
RESULTS_EXPERIMENTS_DIR = REPO_ROOT / "results" / "experiments"
SCHEMAS_DIR = REPO_ROOT / "experiments" / "schemas"

CONDITION_PACKET_PATH = RESULTS_TABLES_DIR / "external_condition_packet.csv"
RESULT_SCHEMA_PATH = SCHEMAS_DIR / "external_condition_result_schema.json"
MANIFEST_PATH = RESULTS_EXPERIMENTS_DIR / "external_condition_manifest.csv"
SHARD_SUMMARY_PATH = RESULTS_EXPERIMENTS_DIR / "external_condition_shards.csv"
STAT_PLAN_CSV_PATH = RESULTS_EXPERIMENTS_DIR / "external_statistical_analysis_plan.csv"
STAT_PLAN_MD_PATH = RESULTS_EXPERIMENTS_DIR / "external_statistical_analysis_plan.md"
SUMMARY_MD_PATH = RESULTS_EXPERIMENTS_DIR / "external_condition_dry_run.md"

REQUIRED_INPUT_COLUMNS = [
    "condition_case_id",
    "case_id",
    "artifact_id",
    "source_id",
    "artifact_family_group",
    "case_type",
    "condition",
    "expected_behavior",
    "risk_label",
    "representation_status",
    "execution_status",
]

MANIFEST_COLUMNS = [
    "condition_case_id",
    "case_id",
    "artifact_id",
    "source_id",
    "artifact_family_group",
    "case_type",
    "condition",
    "expected_behavior",
    "risk_label",
    "shard_id",
    "run_status",
    "result_schema",
    "representation_status",
    "execution_status",
    "notes",
]

SHARD_COLUMNS = [
    "shard_id",
    "row_count",
    "first_condition_case_id",
    "last_condition_case_id",
    "status",
]

STAT_PLAN_COLUMNS = [
    "metric",
    "unit_of_analysis",
    "applicable_case_types",
    "outcome_type",
    "primary_analysis",
    "robustness_check",
    "multiple_testing",
    "status",
]

EXPECTED_CASE_TYPES = {
    "positive_trigger",
    "negative_trigger",
    "boundary_clarification",
    "risk_constraint",
}

EXPECTED_CONDITIONS = {
    "original_freeform",
    "skillops_normalized",
    "skillops_ablation",
}

EXPECTED_BEHAVIORS = {
    "trigger",
    "no_trigger",
    "clarify_scope",
    "apply_constraint_or_refuse",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and shard the external condition packet without model execution.")
    parser.add_argument("--shards", type=int, default=12, help="Number of execution shards to generate.")
    return parser.parse_args()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != REQUIRED_INPUT_COLUMNS:
            raise ValueError(f"Unexpected columns in {path}: {reader.fieldnames}")
        return list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def validate_rows(rows: list[dict[str, str]]) -> None:
    if len(rows) != 2880:
        raise ValueError(f"Expected 2880 condition rows, found {len(rows)}")
    ids = [row["condition_case_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate condition_case_id values")

    conditions_by_case: dict[str, set[str]] = {}
    for row in rows:
        if row["case_type"] not in EXPECTED_CASE_TYPES:
            raise ValueError(f"Unexpected case type: {row['case_type']}")
        if row["condition"] not in EXPECTED_CONDITIONS:
            raise ValueError(f"Unexpected condition: {row['condition']}")
        if row["expected_behavior"] not in EXPECTED_BEHAVIORS:
            raise ValueError(f"Unexpected expected behavior: {row['expected_behavior']}")
        if row["representation_status"] != "pending_construction":
            raise ValueError(f"Unexpected representation status: {row['representation_status']}")
        if row["execution_status"] != "not_run":
            raise ValueError(f"Unexpected execution status: {row['execution_status']}")
        conditions_by_case.setdefault(row["case_id"], set()).add(row["condition"])

    if len(conditions_by_case) != 960:
        raise ValueError(f"Expected 960 base cases, found {len(conditions_by_case)}")
    for case_id, conditions in conditions_by_case.items():
        if conditions != EXPECTED_CONDITIONS:
            raise ValueError(f"Case {case_id} does not have all conditions: {conditions}")


def assign_shards(rows: list[dict[str, str]], shard_count: int) -> list[dict[str, Any]]:
    if shard_count < 1:
        raise ValueError("Shard count must be positive")
    rows_per_shard = math.ceil(len(rows) / shard_count)
    manifest_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        shard_index = min(index // rows_per_shard, shard_count - 1) + 1
        manifest_rows.append(
            {
                "condition_case_id": row["condition_case_id"],
                "case_id": row["case_id"],
                "artifact_id": row["artifact_id"],
                "source_id": row["source_id"],
                "artifact_family_group": row["artifact_family_group"],
                "case_type": row["case_type"],
                "condition": row["condition"],
                "expected_behavior": row["expected_behavior"],
                "risk_label": row["risk_label"],
                "shard_id": f"external-shard-{shard_index:03d}",
                "run_status": "not_run",
                "result_schema": str(RESULT_SCHEMA_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
                "representation_status": row["representation_status"],
                "execution_status": row["execution_status"],
                "notes": "Dry-run manifest row; representation and model execution remain pending.",
            }
        )
    return manifest_rows


def build_shard_summary(manifest_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    shard_ids = sorted({str(row["shard_id"]) for row in manifest_rows})
    rows: list[dict[str, Any]] = []
    for shard_id in shard_ids:
        shard_rows = [row for row in manifest_rows if row["shard_id"] == shard_id]
        rows.append(
            {
                "shard_id": shard_id,
                "row_count": len(shard_rows),
                "first_condition_case_id": shard_rows[0]["condition_case_id"],
                "last_condition_case_id": shard_rows[-1]["condition_case_id"],
                "status": "not_run",
            }
        )
    return rows


def build_statistical_plan() -> list[dict[str, Any]]:
    pending = "planned_no_outcomes_yet"
    return [
        {
            "metric": "routing_correct",
            "unit_of_analysis": "condition_case_id",
            "applicable_case_types": "positive_trigger;negative_trigger",
            "outcome_type": "binary",
            "primary_analysis": "mixed_effects_logistic_with_random_effects_for_model_artifact_and_case",
            "robustness_check": "mcnemar_test_for_paired_conditions",
            "multiple_testing": "holm_bonferroni",
            "status": pending,
        },
        {
            "metric": "clarification_correct",
            "unit_of_analysis": "condition_case_id",
            "applicable_case_types": "boundary_clarification",
            "outcome_type": "binary",
            "primary_analysis": "mixed_effects_logistic_with_random_effects_for_model_artifact_and_case",
            "robustness_check": "paired_bootstrap_by_artifact",
            "multiple_testing": "holm_bonferroni",
            "status": pending,
        },
        {
            "metric": "constraint_compliance",
            "unit_of_analysis": "condition_case_id",
            "applicable_case_types": "risk_constraint",
            "outcome_type": "binary",
            "primary_analysis": "mixed_effects_logistic_with_random_effects_for_model_artifact_and_case",
            "robustness_check": "mcnemar_test_for_paired_conditions",
            "multiple_testing": "holm_bonferroni",
            "status": pending,
        },
        {
            "metric": "parse_success",
            "unit_of_analysis": "condition_case_id",
            "applicable_case_types": "all",
            "outcome_type": "binary",
            "primary_analysis": "mixed_effects_logistic_with_random_effects_for_model_artifact_and_case",
            "robustness_check": "paired_bootstrap_by_artifact",
            "multiple_testing": "holm_bonferroni",
            "status": pending,
        },
        {
            "metric": "latency_ms",
            "unit_of_analysis": "condition_case_id",
            "applicable_case_types": "all",
            "outcome_type": "continuous",
            "primary_analysis": "paired_log_scale_model_with_artifact_and_case_blocks",
            "robustness_check": "median_difference_bootstrap",
            "multiple_testing": "secondary_metric_reported_separately",
            "status": pending,
        },
        {
            "metric": "token_count",
            "unit_of_analysis": "condition_case_id",
            "applicable_case_types": "all",
            "outcome_type": "count",
            "primary_analysis": "paired_negative_binomial_or_log_scale_model",
            "robustness_check": "median_difference_bootstrap",
            "multiple_testing": "secondary_metric_reported_separately",
            "status": pending,
        },
    ]


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(row) + " |" for row in rows],
        ]
    )


def write_markdown(manifest_rows: list[dict[str, Any]], shard_rows: list[dict[str, Any]], stat_rows: list[dict[str, Any]]) -> None:
    case_type_counts = Counter(row["case_type"] for row in manifest_rows)
    condition_counts = Counter(row["condition"] for row in manifest_rows)
    family_counts = Counter(row["artifact_family_group"] for row in manifest_rows)

    dry_run_lines = [
        "# External Condition Dry Run",
        "",
        "This report validates and shards pending external condition rows. It does not report model execution or statistical outcomes.",
        "",
        "## Totals",
        "",
        markdown_table(
            ["Quantity", "Count"],
            [
                ["Manifest rows", str(len(manifest_rows))],
                ["Shards", str(len(shard_rows))],
                ["Statistical metrics planned", str(len(stat_rows))],
            ],
        ),
        "",
        "## Families",
        "",
        markdown_table(
            ["Family", "Rows"],
            [[family, str(count)] for family, count in sorted(family_counts.items())],
        ),
        "",
        "## Case Types",
        "",
        markdown_table(
            ["Case type", "Rows"],
            [[case_type, str(count)] for case_type, count in sorted(case_type_counts.items())],
        ),
        "",
        "## Conditions",
        "",
        markdown_table(
            ["Condition", "Rows"],
            [[condition, str(count)] for condition, count in sorted(condition_counts.items())],
        ),
        "",
    ]
    SUMMARY_MD_PATH.write_text("\n".join(dry_run_lines), encoding="utf-8")

    stat_lines = [
        "# External Statistical Analysis Plan",
        "",
        "This plan defines analysis rows for future external-condition results. All metrics remain planned until execution outputs are collected.",
        "",
        markdown_table(
            ["Metric", "Outcome", "Primary analysis", "Status"],
            [
                [
                    row["metric"],
                    row["outcome_type"],
                    row["primary_analysis"],
                    row["status"],
                ]
                for row in stat_rows
            ],
        ),
        "",
    ]
    STAT_PLAN_MD_PATH.write_text("\n".join(stat_lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    condition_rows = read_csv_rows(CONDITION_PACKET_PATH)
    validate_rows(condition_rows)
    manifest_rows = assign_shards(condition_rows, args.shards)
    shard_rows = build_shard_summary(manifest_rows)
    stat_rows = build_statistical_plan()

    write_csv(MANIFEST_PATH, MANIFEST_COLUMNS, manifest_rows)
    write_csv(SHARD_SUMMARY_PATH, SHARD_COLUMNS, shard_rows)
    write_csv(STAT_PLAN_CSV_PATH, STAT_PLAN_COLUMNS, stat_rows)
    write_markdown(manifest_rows, shard_rows, stat_rows)

    print(f"Wrote {MANIFEST_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SHARD_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {STAT_PLAN_CSV_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_MD_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {STAT_PLAN_MD_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
